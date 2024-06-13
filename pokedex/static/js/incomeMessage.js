document.addEventListener("DOMContentLoaded", function (){
    var modal = document.getElementById('messageModal');
    var messageBtn = document.getElementById('incomeMessages');
    var span = document.getElementById('close');
    var addFriendBtns = document.getElementsByClassName('addFriendBtn')

    if(messageBtn) {
        messageBtn.onclick = function () {
            modal.style.display = "block";
        }
    }

    span.onclick = function() {
        modal.style.display = "none";
    }

    window.addEventListener("click", function (event){
        if (event.target == modal) {
            modal.style.display = "none";
        }
    })

    for (var i = 0; i < addFriendBtns.length; i++) {
        addFriendBtns[i].onclick = function (){
            var friend_name = this.innerText;
            var username = getRequestUserName();
        fetch(`/profile/acceptfriendrequest/${username}/${friend_name}/`, {
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
                // Optionally, you can update the UI based on the response
                if (data.status === 'success') {
                    // Handle success case
                } else {
                    // Handle failure case
                }
            })
            .catch((error) => {
                console.error('Error:', error);
            });
        }
    }

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
})