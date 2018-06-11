(function($) {
    function createVisualStars() {
        const starFields = $('.createStars');
        starFields.each(function(i, field) {
            field = $(field);
            const value = parseInt(field.html()),
                  select = $('<select/>').addClass('starRating');

            if (isNaN(value)) {
                return;
            }

            for (let i = 1; i <= 5; i++) {
                const option = $("<option/>").html(i);
                if (i === value) {
                    option.attr('selected', 'true');
                }
                select.append(option);
            }

            select.insertAfter(field);

            field.remove();

            $('.starRating').barrating({
                theme: 'fontawesome-stars',
                // initialRating: value,
                readonly: true
            })
        })
    }

    /* Initialise slick gallery */
    $('.galleryWrapper').slick();

    createVisualStars();
})(jQuery);