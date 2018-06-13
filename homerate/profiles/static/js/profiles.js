(function ($) {

    /* After a key is typed in the search box */
    $('.postcode').keyup(function (event) {

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