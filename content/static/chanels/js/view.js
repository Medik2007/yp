function subscribe(response) {
    button = document.getElementById('subscribe-button');
    count = document.getElementById('subscribers-count');
    if (response['authenticated']) {
        count.innerHTML = `${response['count']} subscribers`;
        if (response['subscribed']) {
            button.innerHTML = "Subscribed";
            button.style.backgroundColor = '#d6ccc2';
        } else {
            button.innerHTML = "Subscribe";
            button.style.backgroundColor = '#d7443e';
        }
    } else {
        document.getElementById("authentication_error").style.display = 'block';
    }
}


document.getElementById('subscribe-button').addEventListener("click", function(e) {
    send_data(e, {act:'subscribe'}, subscribe) });
