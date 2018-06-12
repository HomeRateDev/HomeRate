(function ($) {

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
    $('.postcode').keyup(function (event) {

        /* If a key that doesn't affect our input was pressed,
           do nothing. */
        if (!relevantKey(event)) {
            return;
        }

        const inputCode = $('#id_postcode').val()
              postCodeRegex = new RegExp('^(GIR ?0AA|[A-PR-UWYZ]([0-9]{1,2}|([A-HK-Y][0-9]([0-9ABEHMNPRV-Y])?)|[0-9][A-HJKPS-UW]) ?[0-9][ABD-HJLNP-UW-Z]{2})$', 'i');

        /* Test if the current value matches the regex */
        if (postCodeRegex.test(inputCode)) {
            /* If current input is a valid postcode, enable the submission box and make full opacity. */
            $("#postcodeSubmit").removeAttr('disabled').css({"opacity": 1});
        } else {
            /* If the current input is invalid, disbale the submission box and reduce opacity. */
            $("#postcodeSubmit").attr('disabled', 'disabled').css({"opacity": 0.7});
        }
    })

})(jQuery);