document.addEventListener("DOMContentLoaded", function (){
    let modal = document.getElementById('messageModal');
    let messageBtn = document.getElementById('incomeMessages');
    let span = document.getElementById('close');
    let addFriendBtns = [];
    let nameList = [];
    let hide = [];
    let declineFriendBtns = [];
    let tradeModal = document.getElementById('tradesAcceptModal');
    let closeTrade = document.getElementById('closeAcceptTrades');
    let acceptUserPagesNumber
    let acceptFriendsPagesNumber
    let acceptUserPage = 0
    let acceptFriendPage = 0
    let acceptPagination = document.getElementById('acceptPagination')
    let acceptFriendPagination = document.getElementById('acceptFriendPagination')
    let acceptTradeBtn = document.getElementById('acceptButton')
    let data
    let acceptId

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
                    listItem.style.margin = '10px'

                    let avatarImg = document.createElement('img')
                    avatarImg.src = getImgLink() + `${friend.avatar}` + '.png'
                    avatarImg.alt = `${friend.username}'s avatar`
                    avatarImg.style.width = '50px';
                    avatarImg.style.height = '50px';
                    avatarImg.style.marginRight = '5px';
                    avatarImg.style.borderRadius = '50%'
                    listItem.appendChild(avatarImg);

                    let usernameSpan = document.createElement('span')
                    usernameSpan.textContent = friend.username
                    usernameSpan.style.marginRight = '5px';
                    listItem.appendChild(usernameSpan)

                    let acceptBtn = document.createElement('button')
                    acceptBtn.textContent = 'Accept';
                    acceptBtn.className = 'addFriendBtn btn btn-success';
                    acceptBtn.style.marginRight = '5px'
                    listItem.appendChild(acceptBtn);
                    nameList.push(friend.username);
                    addFriendBtns.push(acceptBtn);

                    let declineBtn = document.createElement('button')
                    declineBtn.textContent = 'Decline';
                    declineBtn.className = 'btn btn-danger';
                    listItem.appendChild(declineBtn);
                    declineFriendBtns.push(declineBtn);

                    friendsList.appendChild(listItem);
                    hide.push(listItem);
                })
                if(data.friends.length === 0){
                    let empty = document.createElement('h5')
                    empty.textContent = 'Empty'
                    friendsList.appendChild(empty)
                }
                click(nameList, hide);
                decline(nameList, hide);
            })
            .catch(error => {
                console.error('Error:', error);
            });

            fetch('/trades/showTrade/', {
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
                console.log("lox", data)
                let requestList = document.getElementById("requestList")
                requestList.innerHTML = ''
                data.trades.forEach((trade, index) =>{
                    let listItem = document.createElement('li')
                    listItem.style.display = "block"
                    listItem.style.margin = '10px'

                    let avatarImg = document.createElement('img')
                    avatarImg.src = getImgLink() + `${trade.sender_avatar}` + '.png'
                    avatarImg.alt = `${trade.sender}'s avatar`
                    avatarImg.style.width = '50px';
                    avatarImg.style.height = '50px';
                    avatarImg.style.marginRight = '5px';
                    avatarImg.style.borderRadius = '50%'
                    listItem.appendChild(avatarImg);

                    let usernameSpan = document.createElement('span')
                    usernameSpan.textContent = trade.sender
                    usernameSpan.style.marginRight = '5px';
                    listItem.appendChild(usernameSpan)

                    let showBtn = document.createElement('button')
                    showBtn.textContent = 'Show';
                    showBtn.className = 'showBtn btn btn-success';
                    showBtn.style.marginRight = '5px'
                    showBtn.addEventListener("click", function(){
                        showTrade(trade, index);
                    })
                    listItem.appendChild(showBtn);

                    requestList.appendChild(listItem);
                })
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

    closeTrade.onclick = function(){
        tradeModal.style.display = "none";
    }

    function showTrade(trade, id){
        acceptId = id
        data = trade
        tradeModal.style.display = "block";
        let acceptUserPokemonList = document.getElementById('acceptUserPokemonsList')
        let acceptFriendsPokemonsList = document.getElementById('acceptFriendsPokemonsList')

        acceptUserPokemonList.innerHTML = ''
        acceptFriendsPokemonsList.innerHTML = ''

        acceptUserPagesNumber = Math.ceil(trade.pokemons_send.length / 12);
        acceptFriendsPagesNumber = Math.ceil(trade.pokemons_received.length / 12);

        setupPagination(acceptUserPagesNumber, acceptPagination, showPage);
        setupPagination(acceptFriendsPagesNumber, acceptFriendPagination, showFriendPage);
        showPage(trade, acceptUserPage)
        showFriendPage(trade, acceptFriendPage)
    }

    function setupPagination(pagesNumber, paginationElement, showPageFunction) {
        paginationElement.innerHTML = '';

        if (pagesNumber > 1) {
            let prevButton = document.createElement("li");
            prevButton.className = "page-item";
            let prevButtonLink = document.createElement("button");
            prevButtonLink.innerText = "<";
            prevButtonLink.className = "page-link mt-auto p-2";
            prevButtonLink.onclick = function() {
                if (acceptUserPage > 0) {
                    acceptUserPage--;
                    showPageFunction(receivedData, userPage);
                }
            };
            prevButton.appendChild(prevButtonLink);
            paginationElement.appendChild(prevButton);

            let nextButton = document.createElement("li");
            nextButton.className = "page-item";
            let nextButtonLink = document.createElement("button");
            nextButtonLink.innerText = ">";
            nextButtonLink.className = "page-link mt-auto p-2";
            nextButtonLink.onclick = function() {
                if (acceptUserPage < pagesNumber - 1) {
                    acceptUserPage++;
                    showPageFunction(receivedData, userPage);
                }
            };
            nextButton.appendChild(nextButtonLink);
            paginationElement.appendChild(nextButton);
        }
    }

    function showPage(data, page) {
        let userPokemonsList = document.getElementById("acceptUserPokemonsList");
        userPokemonsList.innerHTML = '';
        for (let index = page * 12; index < data.pokemons_send.id.length && index < page * 12 + 12; index++) {
            let id = data.pokemons_send.id[index];
            let name = data.pokemons_send.name[index]
            let listItem = createPokemonCard(id, name);
            userPokemonsList.appendChild(listItem);
        }
    }

    function showFriendPage(data, page) {
        let friendPokemonsList = document.getElementById("acceptFriendsPokemonsList")
        friendPokemonsList.innerHTML = '';

        for (let index = page * 12; index < data.pokemons_received.id.length && index < page * 12 + 12; index++) {
            let id = data.pokemons_received.id[index]
            let name = data.pokemons_received.name[index]
            let listItem = createPokemonCard(id, name);
            friendPokemonsList.appendChild(listItem);
        }
    }

    function createPokemonCard(id, name) {
        let listItem = document.createElement('div');
        listItem.className = "col-md-3 position-relative mb-3";

        let card = document.createElement("div");
        card.className = "card";
        let cardbody = document.createElement("div");
        cardbody.className = "card-body text-center";

        let header = document.createElement("h5");
        header.innerText = name;

        let img = document.createElement("img");
        img.src = `https://assets.pokemon.com/assets/cms2/img/pokedex/full/${id.toString().padStart(3, '0')}.png`;
        img.title = name;
        img.alt = name;
        img.className = "text-bg-light";
        img.style.width = "100px";
        img.style.height = "100px";

        cardbody.appendChild(header);
        cardbody.appendChild(img);
        card.appendChild(cardbody);
        listItem.appendChild(card);
        return listItem;
    }

    acceptTradeBtn.onclick = function(){
        let acceptData = {
            friend: data.sender,
            id: acceptId
        };
        fetch('/trades/acceptTrade/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(acceptData)
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
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
})
