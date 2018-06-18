(function ($) {
    var target = $('.siteDetails');
    var targetHeight = target.outerHeight();

    $(document).scroll(function (e) {
        var scrollPercent = (targetHeight - window.scrollY) / targetHeight;
        console.log(scrollPercent);
        if (scrollPercent >= 0) {
            target.css('opacity', 1 - scrollPercent + 0.3);
        }
    });
})(jQuery);