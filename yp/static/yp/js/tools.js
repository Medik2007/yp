function send_data(e, data, success, url='', csrf=true) {
    e.preventDefault();
    if (csrf) {data.csrfmiddlewaretoken=document.getElementById("csrf").value;}
    $.ajax({
        type: 'POST',
        url: url,
        data: data,
        success: success,
        error: function(error) {
            console.log('Send data error:', error);
        }
    });
}


function toggle_element(id, display='block') {
    obj = document.getElementById(id);
    if (obj.style.display == 'none') { obj.style.display = display; }
    else { obj.style.display = 'none'; }
}
function show_element(id, display='block') {
    document.getElementById(id).style.display = display;
}
function hide_element(id) {
    document.getElementById(id).style.display = 'none';
}


function notifications_number(response) {
    if (response['number'] > 0) {
        document.getElementById('notifications-button').innerHTML = `Notifications (${response['number']})`;
    } else {
        document.getElementById('notifications-button').innerHTML = 'Notifications';
    }
}
function get_notifications_response(response) {
    tab = document.getElementById('notifications-tab');
    no_notifs = document.getElementById('no-notifications');
    clear_notifs = document.getElementById('clear-notifications');
    example = document.getElementById('notification-example');
    tab.innerHTML = '';

    if (response['notifications']) {
        clear = clear_notifs.cloneNode(true);
        clear.style.display = 'block';
        tab.appendChild(clear);
        for (const notification of response['notifications'][0]) {
            notif = example.cloneNode(true);
            notif.style.display = 'block';
            notif.id = '';
            notif.href = notification[1];
            notif.getElementsByTagName('p')[0].innerHTML = notification[0];
            tab.appendChild(notif);
        }
        for (const notification of response['notifications'][1]) {
            notif = example.cloneNode(true);
            notif.style.display = 'block';
            notif.id = '';
            notif.href = notification[1];
            notif.getElementsByTagName('p')[0].innerHTML = notification[0];
            notif.getElementsByTagName('div')[0].classList.add("old-notification");
            tab.appendChild(notif);
        }
    } else {
        no = no_notifs.cloneNode(true);
        no.style.display = 'block';
        tab.appendChild(no);
    }
    toggle_element("notifications-tab");
    number_notifications();
}

function clear_notifications_response(response) {
    tab = document.getElementById('notifications-tab');
    no_notifs = document.getElementById('no-notifications');
    if (response['success']) {
        document.getElementById('notifications-tab').innerHTML = "";
        no = no_notifs.cloneNode(true);
        no.style.display = 'block';
        tab.appendChild(no);
    }
}

function get_notifications(e) { send_data(e, {'act':'get'}, get_notifications_response, url='/u/notifications/'); }
function clear_notifications(e) { send_data(e, {'act':'clear'}, clear_notifications_response, url='/u/notifications/'); }
function number_notifications() { send_data(document.createEvent("HTMLEvents"), {'act':'number'}, notifications_number, url='/u/notifications/'); }



function display_menu_response(response) {
    if (response['is_authenticated']) {
        document.getElementById('user-authenticated').style.display = 'block';
    } else {
        document.getElementById('user-not-authenticated').style.display = 'block';
    }
}

function display_menu() { send_data(document.createEvent("HTMLEvents"), {}, display_menu_response, url='/u/is_authenticated/'); }

number_notifications()
display_menu()
