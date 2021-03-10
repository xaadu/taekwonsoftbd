$(function () {
    $('#flash').delay(500).fadeIn('normal', function () {
        $(this).delay(2500).fadeOut();
    });
});
$("#id_telephone").on("blur keyup change", function () {
    if ($(this).val() == '') {
        var getCode = $("#id_telephone").intlTelInput('getSelectedCountryData').dialCode;
        $(this).val('+' + getCode);
    }
});