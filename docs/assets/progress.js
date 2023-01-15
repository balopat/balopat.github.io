jQuery(document).ready(function($) {
    var h2sWrapper = $('#h2s');
    if (h2sWrapper.length > 0) {
        // cache jQuery objects
        var windowHeight = $(window).height(),
            h2s = $('h2'),
            aside = $('.read-more'),
            h2SidebarLinks = aside.find('li');
        // initialize variables
        var scrolling = false,
            sidebarAnimation = false,
            resizing = false,
            mq = checkMQ(),
            svgCircleLength = parseInt(Math.PI * (h2SidebarLinks.eq(0).find('circle').attr('r') * 2));

        // check media query and bind corresponding events
        if (mq == 'desktop') {
            $(window).on('scroll', checkRead);
            $(window).on('scroll', checkSidebar);
        }

        $(window).on('resize', resetScroll);

        updateh2();
        updateSidebarPosition();

        aside.on('click', 'a', function(event) {
            event.preventDefault();
            var selectedh2 = h2s.eq($(this).parent('li').index());
            var selectedh2Top = selectedh2.offset().top;

            $(window).off('scroll', checkRead);

            $('body,html').animate({ 'scrollTop': selectedh2Top + 2 },
                300,
                function() {
                    checkRead();
                    $(window).on('scroll', checkRead);
                }
            );
        });
    }

    function checkRead() {

        if (!scrolling) {
            scrolling = true;
            (!window.requestAnimationFrame) ? setTimeout(updateh2, 300): window.requestAnimationFrame(updateh2);
        }
    }

    function checkSidebar() {
        if (!sidebarAnimation) {
            sidebarAnimation = true;
            (!window.requestAnimationFrame) ? setTimeout(updateSidebarPosition, 300): window.requestAnimationFrame(updateSidebarPosition);
        }
    }

    function resetScroll() {
        if (!resizing) {
            resizing = true;
            (!window.requestAnimationFrame) ? setTimeout(updateParams, 300): window.requestAnimationFrame(updateParams);
        }
    }

    function updateParams() {
        windowHeight = $(window).height();
        mq = checkMQ();
        $(window).off('scroll', checkRead);
        $(window).off('scroll', checkSidebar);

        if (mq == 'desktop') {
            $(window).on('scroll', checkRead);
            $(window).on('scroll', checkSidebar);
        }
        resizing = false;
    }

    function updateh2() {
        var scrollTop = $(window).scrollTop();

        h2s.each(function() {
            var h2 = $(this);

            var h2Top = h2.offset().top;

            var h2SidebarLink = h2SidebarLinks.eq(h2s.index(h2)).children('a')

            if (h2.is(':last-of-type')) {
                h2Height = windowHeight - h2Top
            } else {
                var h2Height = h2s.eq(h2s.index(h2) + 1).offset().top - h2Top;
            }

            if (h2Top > scrollTop) {
                h2SidebarLink.removeClass('read reading');
            } else if (scrollTop >= h2Top && h2Top + h2Height > scrollTop) {
                var dashoffsetValue = svgCircleLength * (1 - (scrollTop - h2Top) / h2Height);
                h2SidebarLink.addClass('reading').removeClass('read').find('circle').attr({ 'stroke-dashoffset': dashoffsetValue });
                changeUrl(h2SidebarLink.attr('href'));
            } else {
                h2SidebarLink.removeClass('reading').addClass('read');
            }
        });
        scrolling = false;
    }

    function updateSidebarPosition() {

        var titleTop = $("h1").eq(0).offset().top,
            // h2sWrapperHeight = h2sWrapper.outerHeight(),
            scrollTop = $(window).scrollTop();
        if (scrollTop < titleTop) {
            // aside.removeClass('fixed').attr('style', '');
        } else if (scrollTop >= titleTop && scrollTop < titleTop + windowHeight) {
            aside.addClass('fixed').attr('style', '');
        } else {
            var h2PaddingTop = Number(h2s.eq(1).css('padding-top').replace('px', ''));
            if (aside.hasClass('fixed')) aside.removeClass('fixed').css('top', h2PaddingTop - windowHeight + 'px');
        }
        sidebarAnimation = false;
    }

    function changeUrl(link) {
        var pageArray = location.pathname.split('/'),
            actualPage = pageArray[pageArray.length - 1];
        if (actualPage != link && history.pushState) window.history.pushState({ path: link }, '', link);
    }

    function checkMQ() {
        return window.getComputedStyle(h2sWrapper.get(0), '::before').getPropertyValue('content').replace(/'/g, "").replace(/"/g, "");
    }
});