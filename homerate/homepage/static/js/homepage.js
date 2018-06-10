(function($) {
    $("li").mousedown(function() {
		window.location.href = $(this).children("a").attr("href");
	});
	$(".searchBox").keyup(function() {
        const query = $(this).val();
        const postCode = new RegExp('(GIR ?0AA|[A-PR-UWYZ]([0-9]{1,2}|([A-HK-Y][0-9]([0-9ABEHMNPRV-Y])?)|[0-9][A-HJKPS-UW]) ?[0-9][ABD-HJLNP-UW-Z]{2})', 'i');

        if (postCode.test(query)) {

        }

        $(".autocomplete").css('height', 'auto');
		if (query === "") {
			$(".autocomplete").css({
                'height': 'auto',
                'visibility': 'visible'
            });
		} else {
			$("ul li:contains('" + query + "')").show();
			$("ul li").not(":contains('" + query + "')").hide();
		}
	}).focusout(function() {
        console.log(document.activeElement);
	    if (!$(document.activeElement).hasClass('.entry')) {
	        $(".autocomplete").css({
                'height': '0',
                'visibility': 'hidden'
            });
        }

    }).focus(function() {
        $(".autocomplete").css({
            'height': 'auto',
            'visibility': 'visible'
	    });
    });
})(jQuery);