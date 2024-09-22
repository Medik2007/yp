function like(response) {
    if (response['authenticated']) {
        if (response['id'] != 'object') {
            button = document.getElementById(`comment-like-button-${response['id']}`);
            count = document.getElementById(`comment-like-count-${response['id']}`);
        }
        else {
            button = document.getElementById('like-button');
            count = document.getElementById('like-count');
        }
        if (response['liked']) {
            button.src = '/static/ui/img/like.png';
        } else {
            button.src = '/static/ui/img/dislike.png';
        }
        count.innerHTML = response['count'];
    } else {
        document.getElementById("authentication_error").style.display = 'block';
    }
}

function comment(response) {
    if (response['authenticated']) {
        id = response['id'];
        author = response['author']
        if (response['parent'] == 'object') {
            text_obj = document.getElementById('comment-input')
            text = text_obj.value;
            text_obj.value = '';
            document.getElementById('comments-container').insertAdjacentHTML('afterbegin',
`
<div id="comment-${id}" class="comment">

<div id="comment-div-${id}" class="comment-div">
    <a href="/u/@${author}">
        <img alt="Comment Author Profile Image" src="${document.getElementById('user-profile').src}">
    </a>
    <div style="width: 100%;">
        <div class="comment-text">
            <h4>@${author}</h4>
            <p id="comment-text-${id}">${text}</p>
            <form class="edit-comment-form" id="edit-comment-form-${id}" style="display: none;"
                onsubmit="comment_edit(event, '${id}')">
                <input type="text" id="edit-comment-input-${id}" placeholder="Edit your comment..." value="${text}">
                <button type="button" class="submit"
                    onclick="hide_element('edit-comment-form-${id}'); show_element('comment-text-${id}')">Cancel</button>
                <input type="submit" value="Edit">
            </form>
        </div>
        <div class="comment-buttons">

            <div class="comment-like-div">
                <p class="comment-like-count" id="comment-like-count-${id}">0</p>
                <img id="comment-like-button-${id}" class="comment-like-button" alt="settings"
                    src="/static/ui/img/dislike.png" onclick="comment_like(event, '${id}')">
            </div>

            <button class="submit" onclick="show_element('answer-comment-form-${id}', 'flex')">Answer</button>

            <div>
                <button class="submit" onclick="toggle_element('comment-manage-${id}', 'flex')">Manage</button>
                <div id="comment-manage-${id}" class="comment-manage" style="display: none;">
                    <button class="submit" style="background-color: orange;"
                        onclick="show_element('edit-comment-form-${id}', 'flex'); hide_element('comment-text-${id}');
                        hide_element('comment-manage-${id}')" id="comment-edit-button-${id}">Edit</button>
                    <button class="submit" style="background-color: red;" onclick="comment_delete(event, '${id}')"
                        id="comment-delete-button-${id}">Delete</button>
                </div>
            </div>
        </div>
        <form id="answer-comment-form-${id}" style="display: none;" onsubmit="comment_answer(event, '${id}')">
            <input type="text" id="answer-comment-input-${id}" placeholder="Write an answer...">
            <button type="button" class="submit" onclick="hide_element('answer-comment-form-${id}')">Cancel</button>
            <input type="submit" value="Answer">
        </form>
    </div>
</div>

<div id="comment-answers-${id}" class="comment-answers"></div>

</div>
`);
        }
        else {
            text_obj = document.getElementById(`answer-comment-input-${response['parent']}`)
            text = text_obj.value;
            text_obj.value = '';
            document.getElementById(`answer-comment-form-${response['parent']}`).style.display = 'none';
            document.getElementById(`comment-answers-${response['parent']}`).insertAdjacentHTML('afterbegin',
`
<div id="comment-${id}">

<div id="answer-div-${id}" class="comment-div answer-div">
    <a href="/u/@${author}">
        <img alt="Comment Author Profile Image" src="${document.getElementById('user-profile').src}">
    </a>
    <div style="width: 100%;">
        <div class="comment-text">
            <h4>@${author}</h4>
            <p id="comment-text-${id}">${text}</p>
            <form class="edit-comment-form" id="edit-comment-form-${id}" style="display: none;"
                onsubmit="comment_edit(event, '${id}')">
                <input type="text" id="edit-comment-input-${id}" placeholder="Edit your comment..." value="${text}">
                <button type="button" class="submit"
                    onclick="hide_element('edit-comment-form-${id}'); show_element('comment-text-${id}')">Cancel</button>
                <input type="submit" value="Edit">
            </form>
        </div>
        <div class="comment-buttons">

            <div class="comment-like-div">
                <p class="comment-like-count" id="comment-like-count-${id}">0</p>
                <img id="comment-like-button-${id}" class="comment-like-button" alt="settings"
                    src="/static/ui/img/dislike.png" onclick="comment_like(event, '${id}')">
            </div>

            <div>
                <button class="submit" onclick="toggle_element('comment-manage-${id}', 'flex')">Manage</button>
                <div id="comment-manage-${id}" class="comment-manage" style="display: none;">
                    <button class="submit" style="background-color: orange;"
                        onclick="show_element('edit-comment-form-${id}', 'flex'); hide_element('comment-text-${id}');
                        hide_element('comment-manage-${id}')" id="comment-edit-button-${id}">Edit</button>
                    <button class="submit" style="background-color: red;" onclick="comment_delete(event, '${id}')"
                        id="comment-delete-button-${id}">Delete</button>
                </div>
            </div>
        </div>
    </div>
</div>

</div>
`);
        }
    } else {
        document.getElementById("authentication_error").style.display = 'block';
    }
}

function edit_comment(response) {
    if (response['authenticated']) {
        text = document.getElementById(`comment-text-${response['id']}`);
        text.innerHTML = document.getElementById(`edit-comment-input-${response['id']}`).value;
        text.style.display = 'block';
        document.getElementById(`edit-comment-form-${response['id']}`).style.display = 'none';
    }
}

function delete_comment(response) {
    if (response['authenticated']) {
        document.getElementById(`comment-${response['id']}`).remove();
    }
}

document.getElementById('like-div').addEventListener("click", function(e) {
    send_data(e, {act:'like', model:'video'}, like) });

document.getElementById('comment-form').addEventListener("submit", function(e) {
    send_data(e, {act:'comment', text:document.getElementById("comment-input").value}, comment) });

function comment_like(e, id) { send_data(e, {act:'like', model:'comment', id:id}, like); }
function comment_edit(e, id) { send_data(e, {act:'edit', id:id, text:document.getElementById(`edit-comment-input-${id}`).value}, edit_comment); }
function comment_delete(e, id) { send_data(e, {act:'delete', id:id}, delete_comment); }
function comment_answer(e, parent) {
    send_data(e, {act:'comment', parent:parent, text:document.getElementById(`answer-comment-input-${parent}`).value}, comment);
}
