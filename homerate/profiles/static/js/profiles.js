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
    $('#passwordForm').hide()
    $('.confirmDelete').hide()

})(jQuery);


$("#changeFirst").click(function() {
    $('#passwordForm').slideUp(300)
    $('#firstNameForm').slideDown(300)
    $('html, body').animate({scrollTop: $(document).height()}, 'slow');
});

$("#changePassword").click(function() {
    $('#firstNameForm').slideUp(300)
    $('#passwordForm').slideDown(300)
    $('html, body').animate({scrollTop: $(document).height()}, 'slow');
});

$('#deleteAccount').click(function() {
    $('.buttons').slideUp(300)
    $('#firstNameForm').slideUp(300)
    $('#passwordForm').slideUp(300)
    $('.confirmDelete').slideDown(300)
    $('html, body').animate({scrollTop: $(document).height()}, 'slow');
});

$('#noDeleteButton').click(function() {
    $('.confirmDelete').slideUp(300)
    $('.buttons').slideDown(300)
});

const is_reported = 0;

$('.reportReview').click(funtion() {
    $('.reportReview').toggle()
});