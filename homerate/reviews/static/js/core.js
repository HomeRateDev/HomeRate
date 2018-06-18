/* Converts text rating values into visual stars using BarRating.js */
function createVisualStars() {
    const starFields = $('.createStars');
    starFields.each(function (i, field) {
        /* Wrap the star field in a jQuery object */
        field = $(field);

        /* Retrieve the number of stars the field contains
        *  and generate HTML for the select field needed to
        *  display visual stars */
        const value = parseInt(field.html()),
            select = $('<select/>').addClass('starRating');

        /* If the value couldn't be parsed, the field wasn't filled
         * out in the review, so don't display this review point. */
        if (isNaN(value)) {
            field.parent('.reviewPoint').remove();
            return;
        }

        if (value === 0) {
            select.append($("<option/>").html(""));
        }

        /* Append <option> tags with values 1-5 to the select field */
        for (let i = 1; i <= 5; i++) {
            const option = $("<option/>").html(i);

            /* Mark the option that matches the number of stars
             * we want to display as "selected" */
            if (i === value) {
                option.attr('selected', 'true');
            }

            select.append(option);
        }

        /* Insert the select tag and remove the original text field */
        select.insertAfter(field);
        field.remove();

        /* Initialise the bar rating plugin to display stars
         * for the select field */
        select.barrating({
            theme: 'fontawesome-stars',
            readonly: true,
            allowEmpty: true
        })
    })
}

(function ($) {

    /* Sets the HTML content of the homepage's error message field
       and makes it visible. */
    function renderErrorMessage(errorMessage) {
        $('.errorMessage').html(errorMessage).show();
    }

    /* Retrieves addresses for the queried postcode via our API and
       inserts them into the autocomplete DOM element. */
    function populateAddresses(query) {

        /* Strip trailing whitespace and remove (optional) space within postcode */
        const postcode = query.trim().replace(' ', '').toUpperCase();

        /* Make a GET request to our address API. */
        $.get({
            'url': '/address_api/postcode/' + postcode,
            success: function (data) {

                const addresses = data.addresses;

                /* Postcode is valid, but doesn't actually exist. */
                if (addresses === undefined) {
                    renderErrorMessage("We couldn't find that postcode...");
                    return;
                }

                const autocomplete = $('.autocomplete');

                /* Delete everything in the autocomplete box */
                autocomplete.empty();

                /* Generate list entries with URLs for each address
                 * and appends them to the autocomplete box */
                addresses.forEach(addr => generateAddressEntry(addr, postcode));

                toggleAutocomplete(false);
            }
        })
    }

    /* Creates HTML for an autocomplete address entry and inserts it into
       the DOM. */
    function generateAddressEntry(address, postcode) {
        const formattedAddr = formatAddress(address, postcode),
              entry = $('<li/>').addClass('entry'),
              url = '/reviews/check_address/' + encodeURIComponent(formattedAddr),
              link = $('<a/>').attr('href', url).html(formattedAddr);
        link.appendTo(entry);
        entry.appendTo('.autocomplete');
    }

    /* Takes a raw address string (e.g. "1 Stratford Avenue, , , , , Rochdale, Lancashire")
     * and a postcode. Strips empty components of the address and returns a string containing
     * each non-empty component (including the postcode) separated by ", " */
    function formatAddress(rawAddress, postcode) {

        /* Split the string into an array of components using the comma as a delimiter */
        let components = rawAddress.split(","),
            result = "";

        for (let i = 0; i < components.length; i++) {
            /* If component is non-empty */
            if (components[i].trim().length > 0) {
                result += components[i] + ", ";
            }
            /* Append the postcode if we're at the last component */
            if (i === components.length - 1) {
                result += postcode
            }
        }

        return result;
    }

    /* Takes a number and a range defined by a 2-element array: [lower, upper].
       Returns true if lower <= number <= upper. */
    function inRange(num, range) {
        const lower = range[0],
            upper = range[1];
        return num >= lower && num <= upper;
    }

    /* Returns true iff query is a valid UK postcode. */
    function validPostcode(query) {
        const postcode = new RegExp('^(GIR ?0AA|[A-PR-UWYZ]([0-9]{1,2}|([A-HK-Y][0-9]([0-9ABEHMNPRV-Y])?)|[0-9][A-HJKPS-UW]) ?[0-9][ABD-HJLNP-UW-Z]{2})$', 'i');
        return postcode.test(query);
    }

    /* Returns true if the key pressed in a keypress event would affect the
       postcode input field. */
    function relevantKey(event) {
        const key = event.which;

        /* Key codes that we're interested in. CMD and CTRL
           are included to allow copy + paste events to go through. */
        const codes = {
                  'alphanumeric': [48, 90],
                  'cmd_keys': [91, 92],
                  'numpad': [96, 105],
                  'backspace': 8,
                  'delete': 46,
                  'ctrl': 17
              };

        return inRange(key, codes['alphanumeric']) ||
               inRange(key, codes['numpad']) ||
               inRange(key, codes['cmd_keys']) ||
               key === codes['backspace'] ||
               key === codes['delete'] ||
               key === codes['ctrl']
    }

    /* After a key is typed in the search box */
    $('.searchBox').keyup(function (event) {

        /* If a key that doesn't affect our input was pressed,
           do nothing. */
        if (!relevantKey(event)) {
            return;
        }

        const query = $(this).val().replace(/ /g,''),
              postCode = new RegExp('^(GIR ?0AA|[A-PR-UWYZ]([0-9]{1,2}|([A-HK-Y][0-9]([0-9ABEHMNPRV-Y])?)|[0-9][A-HJKPS-UW]) ?[0-9][ABD-HJLNP-UW-Z]{2})$', 'i'),
              errorMsg = $('.errorMessage');

        /* Hide the previous error message if it's visible. */
        if (errorMsg.css('display') !== 'none') {
            errorMsg.hide()
        }

        if (validPostcode(query)) {
            /* If current input is a valid postcode, populate the autocomplete box */
            populateAddresses(query);
        } else {
            /* Invalid postcode typed, hide the autocomplete box */
            toggleAutocomplete(true);
        }
    })
        .focus(function () {
            if (validPostcode($(this).val())) {
                toggleAutocomplete(false);
            }
        })
        .blur(() => toggleAutocomplete(true));


    /* Mousedown event fires before blur() event on the searchbox,
       so we can use it to simulate "clicking" on an autocomplete
       link before the autocomplete box disappears due to blur()
     */
    $('.autocomplete .entry').mousedown(function() {
        window.location.href = $(this).attr('href');
    });

    /* If hide is true, the search autocomplete box fades out.
       If hide is false, the search autocomplete box fades in.
     */
    function toggleAutocomplete(hide) {
        const ac = $('.autocomplete');
        if (hide) {
            ac.stop().css('opacity', '0').delay(1000).queue(function(next) {
                $(this).css('visibility', 'hidden');
                next();
            });
        } else {
            ac.stop().css('visibility', 'visible').css('opacity', '1');
        }
    }

})(jQuery);