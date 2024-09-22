function form_response(response) { // Change the thing so that server would send the HTML object to append, rather than it being created in this function
        message = $('#message');
        message.empty();
        if (response.success) {
           if (response.redirect) {
                window.location.href = response.link;
            } else {
                message.append(`<a href='${response.link}'>${response.name} saved<a/>`);
            }
        } else {
            errors = response.errors;
            for (field in errors) {
                message.append(`<p>${field}: ${errors[field]}</p>`);
            }
        }
}

document.getElementById("form").addEventListener('submit', function(e) {
    send_data(e, $(this).serialize(), form_response, false); });
