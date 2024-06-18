document.addEventListener("DOMContentLoaded", function (){
    var modal = document.getElementById('messageModal');
    var messageBtn = document.getElementById('incomeMessages');
    var span = document.getElementById('close');
    var addFriendBtns = [];
    var nameList = [];
    var hide = [];
    var declineFriendBtns = [];

    if(messageBtn) {
        messageBtn.onclick = function (e) {
            fetch('/profile/showfriends/', {  // Ensure the correct URL
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                }
            })
            .then(response => {
                if (response.ok) {
                    return response.json();
                } else {
                    throw new Error('Error fetching friends list');
                }
            })
            .then(data => {
                console.log(data);
                // Populate modal or other DOM elements with data.friends
                // Example:
                let friendsList = document.getElementById('friendsList'); // Ensure you have an element with this ID
                friendsList.innerHTML = '';
                data.friends.forEach(friend => {
                    let listItem = document.createElement('li')
                    listItem.style.display = "block"

                    let avatarImg = document.createElement('img')
                    avatarImg.src = getImgLink() + `${friend.avatar}` + '.png'
                    avatarImg.alt = `${friend.username}'s avatar`
                    avatarImg.style.width = '50px';
                    avatarImg.style.height = '50px';
                    listItem.appendChild(avatarImg);

                    let usernameSpan = document.createElement('span')
                    usernameSpan.textContent = friend.username
                    listItem.appendChild(usernameSpan)

                    let acceptBtn = document.createElement('button')
                    acceptBtn.textContent = 'Accept';
                    acceptBtn.className = 'addFriendBtn';
                    listItem.appendChild(acceptBtn);
                    nameList.push(friend.username);
                    addFriendBtns.push(acceptBtn);

                    let declineBtn = document.createElement('button')
                    declineBtn.textContent = 'Decline';
                    listItem.appendChild(declineBtn);
                    declineFriendBtns.push(declineBtn);

                    friendsList.appendChild(listItem);
                    hide.push(listItem);
                })
                click(nameList, hide);
                decline(nameList, hide);
            })
            .catch(error => {
                console.error('Error:', error);
            });
            modal.style.display = "block";
        }
    }
    function click(nameList, friendsList) {
        for (var i = 0; i < addFriendBtns.length; i++) {
            (function(i) {
                addFriendBtns[i].onclick = function () {
                    var friend_name = nameList[i];
                    console.log(friendsList);
                    friendsList[i].style.display = "none"

                    console.log(friend_name);
                    fetch(`/profile/acceptfriendrequest/${friend_name}/`, {
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
            })(i);
        }
    }

    function decline(nameList, friendsList) {
        for (var i = 0; i < declineFriendBtns.length; i++) {
            (function(i) {
                declineFriendBtns[i].onclick = function () {
                    var friend_name = nameList[i];
                    console.log(friendsList);
                    friendsList[i].style.display = "none"

                    console.log(friend_name);
                    fetch(`/profile/declinerequest/${friend_name}/`, {
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
            })(i);
        }
    }

    span.onclick = function() {
        modal.style.display = "none";
    }

    window.addEventListener("click", function (event){
        if (event.target === modal) {
            modal.style.display = "none";
        }
    })

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