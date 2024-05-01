$(document).ready(function () {

    $(".btn-close").on('click', function (e) {
        e.preventDefault();
        $(this).closest('.usuarios').addClass('d-none'); // Hide user
    });

    $(".mostrar").on('click', function (e) {
        e.preventDefault();
        $('.usuarios').removeClass('d-none'); // Hide user
    });

    // Enables input disabled and hides the edit button.
    $('form').on('click', '.edit-btn', function () {
        const inputId = $(this).data('input')
        $('form').find(`#${inputId}`).prop('disabled', false)
        $(this).hide()
    });
});
