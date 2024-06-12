document.addEventListener("DOMContentLoaded", function() {
    var addToFriendBtn = document.getElementById("Add-to-friend-btn");
    var message = document.getElementById("message")
    var messages = document.getElementById("messages");

    addToFriendBtn.onclick = function() {
        var username = getRequestUserName();
        var friend_name = getUserName();
        fetch(`http://127.0.0.1:8000/profile/friendrequest/${username}/${friend_name}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken') // Include CSRF token if required
                }
            })
            .then(response => {
                if (response.ok) {
                    return response.json();
                } else {
                    throw new Error('Network response was not ok.');
                }
            })
            .then(data => {
                console.log('Success:', data);

                if (data.status === 'success') {
                    message.innerText = "New friend request send"
                    messages.style.display = 'block';
                } else if(data.status === 'error'){
                    message.innerText = "You already send request"
                    messages.style.display = 'block';
                }
            })
            .catch((error) => {
                console.error('Error:', error);
            });
    };

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
