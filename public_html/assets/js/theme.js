/*Подсвечивание header ссылок*/
$(document).ready(function($) {
    if (location.pathname == "/" || location.pathname == "" || location.pathname =="/new-order/")
    {
        $('.navbar-collapse a[href="/"]').addClass('active');
    }
    else
    {
        $('.navbar-collapse a[href^="/' + location.pathname.split("/")[1] + '"]').addClass('active');
    }
});

/*Подсвечивание menu ссылок*/
$(document).ready(function($) {

    let arPathURI = location.pathname.split('/');

    switch (arPathURI[1])
    {
        case "home":
            if (location.pathname == "/" || location.pathname == "" || location.pathname =="/home/")
                $('.link-all-requests').addClass('active');
            else
                $('a[href^="'+location.pathname+'"]').parent().addClass('active');
            break;

        case "info.html":
            if (location.pathname =="info.html")
                $('.link-all-authors').addClass('active');
            else
                $('a[href^="'+location.pathname+'"]').parent().addClass('active');
            break;

        // case "books":
        //     if (location.pathname =="/books/" || location.pathname =="/books/all-books/")
        //         $('.link-all-books').addClass('active');
        //     else
        //         $('a[href^="'+location.pathname+'"]').parent().addClass('active');
        //     break;
        //
        // case "readers":
        //     if (location.pathname =="/readers/" || location.pathname =="/readers/all-readers/")
        //         $('.link-all-readers').addClass('active');
        //     else
        //         $('a[href^="'+location.pathname+'"]').parent().addClass('active');
        //     break;
        //
        // case "penalties":
        //     if (location.pathname =="/penalties/" || location.pathname =="/penalties/all-penalties/")
        //         $('.link-all-penalties').addClass('active');
        //     else
        //         $('a[href^="'+location.pathname+'"]').parent().addClass('active');
        //     break;
    }



});


$(document).ready(function($) {
    $('.table-select-reader tr').click(function (e) {
        $(this).find('.radio-select-reader').prop('checked', true);
    });
});

$(document).ready(function($) {
    $('.table-select-books tr').click(function (e) {
        $(this).find('.checkbox-select-books').prop('checked', !$(this).find('.checkbox-select-books').prop('checked'));
    });
});
