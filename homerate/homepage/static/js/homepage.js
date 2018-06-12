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

                autocomplete.css('opacity', '1');
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

        const query = $(this).val(),
              postCode = new RegExp('^(GIR ?0AA|[A-PR-UWYZ]([0-9]{1,2}|([A-HK-Y][0-9]([0-9ABEHMNPRV-Y])?)|[0-9][A-HJKPS-UW]) ?[0-9][ABD-HJLNP-UW-Z]{2})$', 'i'),
              errorMsg = $('.errorMessage');

        /* Hide the previous error message if it's visible. */
        if (errorMsg.css('display') !== 'none') {
            errorMsg.hide()
        }

        if (postCode.test(query)) {
            /* If current input is a valid postcode, populate the autocomplete box */
            populateAddresses(query);
        } else {
            /* Invalid postcode typed, hide the autocomplete box */
            $('.autocomplete').css('opacity', '0');
        }
    })

})(jQuery);