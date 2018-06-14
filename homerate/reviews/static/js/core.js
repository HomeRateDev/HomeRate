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
            readonly: true
        })
    })
}