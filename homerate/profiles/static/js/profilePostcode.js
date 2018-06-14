/* Validate the postcode and set the save box accordingly. */
function validatePostcode() {
    const postcodeField = $('#id_postcode'),
        postcodeSubmit = $("#postcodeSubmit"),
        inputCode = postcodeField.val().replace(/ /g, ''),
        postCodeRegex = new RegExp('(^(GIR ?0AA|[A-PR-UWYZ]([0-9]{1,2}|([A-HK-Y][0-9]([0-9ABEHMNPRV-Y])?)|[0-9][A-HJKPS-UW]) ?[0-9][ABD-HJLNP-UW-Z]{2})$)|^$', 'i');

    /* Test if the current value matches the regex */
    if (postCodeRegex.test(inputCode)) {
        /* If current input is a valid postcode, enable the submission box and make full opacity. */
        postcodeSubmit.removeAttr('disabled').css({"opacity": 1});
        postcodeField.val(spacePostcode(postcodeField.val().toUpperCase().replace(/ /g, '')))
    } else {
        /* If the current input is invalid, disbale the submission box and reduce opacity. */
        postcodeSubmit.attr('disabled', 'disabled').css({"opacity": 0.7});
    }
};

function spacePostcode(postcode) {
    if (postcode === "") {
        return "";
    }
    return postcode.slice(0, -3) + " " + postcode.slice(-3)
};