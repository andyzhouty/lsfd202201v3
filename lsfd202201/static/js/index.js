$('#more').click(function () {
    $('div#previous').show();
    $('button#more').hide();
})

$(function () {
    var selector = $('div#index p');
    selector.hide()
    window.scrollTo(0, 0);
    var j = 0;
    var len = selector.length;
    var interval = setInterval(function () {
            selector.eq(j > len - 1 ? j = 0 : j++).fadeIn(1500);
        }
        , 750
    );
})