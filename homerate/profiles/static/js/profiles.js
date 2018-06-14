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

    createVisualStars();
    $('#firstNameForm').hide()

})(jQuery);


$("#changeFirst").click(function() {
    $('#firstNameForm').slideDown(300)
    $('html, body').animate({scrollTop: $(document).height()}, 'slow');
})