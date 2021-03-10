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