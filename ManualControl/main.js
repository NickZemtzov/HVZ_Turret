$(document).ready(function() {

    $('.btn').click(function() {
        $.ajax({
            url: '',
            type: 'get',
            contentType: 'application/json',
            data: {
                button_text: $(this).text()
            },
            success: function(response) {
                $('.btn').text(response.seconds)
            }
        })
    })
})
