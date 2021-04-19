$(function () {
    $('#flash').delay(500).fadeIn('normal', function () {
        $(this).delay(2500).fadeOut();
    });
});
$("#id_telephone").on("blur keyup change", function () {
    if ($(this).val() == '') {
        var getCode = $("#id_telephone").intlTelInput('getSelectedCountryData').dialCode;
        $(this).val('+' + getCode);
    } else {
        $(this).removeClass("is-invalid");
        $('button[type="submit"]').prop('disabled', false);
        if ($(this).val().trim()) {
            if (!$(this).intlTelInput("isValidNumber")) {
                $(this).addClass("is-invalid");
                $('button[type="submit"]').prop('disabled', true);;
            }
        }
    }
});

$(document).ready(function () {
    $('.socialSlider').slick({
        dots: false,
        arrows: false,
        infinite: true,
        autoplay: false,
        autoplaySpeed: 2000,
        speed: 300,
        slidesToShow: 4,
        slidesToScroll: 1,
        responsive: [
            {
                breakpoint: 992,
                settings: {
                    slidesToShow: 3,
                    slidesToScroll: 1
                }
            },
            {
                breakpoint: 768,
                settings: {
                    slidesToShow: 2,
                    slidesToScroll: 1
                }
            },
            {
                breakpoint: 576,
                settings: {
                    slidesToShow: 1,
                    slidesToScroll: 1
                }
            },
            {
                breakpoint: 480,
                settings: {
                    slidesToShow: 1,
                    slidesToScroll: 1
                }
            }
        ]
    });
});
