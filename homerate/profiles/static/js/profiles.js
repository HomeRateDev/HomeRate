(function ($) {

    /* Set the mandatory bar ratings. */
    $('.weightingMandatory').barrating({
        theme: 'bars-square',
        showValues: true,
        showSelectedRating: false
    });

    /* Set the optional bar ratings. */
    $('.weighting').barrating({
        theme: 'bars-square',
        allowEmpty: true,
        initialRating: 0,
        deselectable: true,
        showValues: true,
        showSelectedRating: false
    });

    /* After a key is typed in the postcode box try and valdate */
    $('.postcode').keyup(function (event) {
        validatePostcode()
    });

    /* Signup Form Password Validation */
    $('#id_password1').keyup(function () {
        const passwordInput = $(this),
            password = passwordInput.val();

        const lengthReq = $('.requirement.length'),
            numericReq = $('.requirement.numeric');

        /* Check if the current password is entirely numeric */
        let entirelyNumeric = true;
        for (let i = 0; i < password.length; i++) {
            entirelyNumeric &= isDigit(password[i]);
        }

        requirementChange(lengthReq, password.length >= 8);
        requirementChange(numericReq, !entirelyNumeric);

    });

    /* Marks requirements as valid/invalid and hides/displays them, based on the
     * 'valid' flag */
    function requirementChange(req, valid) {
        if (valid) {
            req.removeClass('invalid').addClass('valid').slideUp(300);
            req.find('i').removeClass('fa-times-circle').addClass('fa-check-circle');
        } else {
            req.addClass('invalid').removeClass('valid').slideDown(300);
            req.find('i').addClass('fa-times-circle').removeClass('fa-check-circle');
        }
    }
})(jQuery);