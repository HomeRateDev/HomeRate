(function ($) {
    function populateAddresses(query) {
        /* Strip trailing whitespace and remove (optional) space within postcode */
        const postcode = query.trim().replace(' ', '');
        $.get({
            'url': '/address_api/postcode/' + postcode,
            success: function (data) {
                /* Delete everything in the autocomplete box */
                $('.autocomplete').empty();

                const addresses = data.addresses;

                /* Generate list entries with URLs for each address
                 * and appends them to the autocomplete box */
                addresses.forEach(function (address) {
                    const formattedAddr = formatAddress(address, postcode),
                        entry = $('<li/>').addClass('entry'),
                        url = '/reviews/check_address/' + encodeURIComponent(formattedAddr),
                        link = $('<a/>').attr('href', url).html(formattedAddr);
                    link.appendTo(entry);
                    entry.appendTo('.autocomplete');
                });
            }
        })
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

    /* After a key is typed in the search box */
    $('.searchBox').keyup(function () {
        const query = $(this).val(),
              postCode = new RegExp('(GIR ?0AA|[A-PR-UWYZ]([0-9]{1,2}|([A-HK-Y][0-9]([0-9ABEHMNPRV-Y])?)|[0-9][A-HJKPS-UW]) ?[0-9][ABD-HJLNP-UW-Z]{2})', 'i');

        // If current input is a valid postcode, populate the autocomplete box
        if (postCode.test(query)) {
            populateAddresses(query);
        }
    })

})(jQuery);