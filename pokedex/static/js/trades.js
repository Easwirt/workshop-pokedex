document.addEventListener("DOMContentLoaded", function() {
    var tradeButton = document.getElementById("Trade-btn");
    var span = document.getElementById("closeTrades");
    var modal = document.getElementById("tradesModal");
    var friendname = getUserName();
    let userPokemonsSelected = [];
    let friendPokemonsSelected = [];
    let sendButton = document.getElementById("sendButton");
    let receivedData;
    let pagination = document.getElementById("pagination");
    let userPage = 0;
    let userPagesNumber = 0;
    let friendsPagesNumber = 0;
    let friendPage = 0;
    let friendPagination = document.getElementById("friendPagination");
    let friendPokemonsList = document.getElementById("friendsPokemonsList");

    if (tradeButton) {
        tradeButton.onclick = function() {
            fetch(`/trades/tradeList/${friendname}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                }
            })
            .then(response => {
                if (response.ok) {
                    modal.style.display = "block";
                    return response.json();
                } else {
                    throw new Error('Network response was not ok');
                }
            })
            .then(data => {
                receivedData = data;
                showData(data);
                console.log('Success:', data);
            })
            .catch((error) => {
                console.error('Error:', error);
            });
        };
    }

    function showData(data) {
        let userPokemonsList = document.getElementById("userPokemonsList");
        let userCoins = document.getElementById("userCoins");
        let friendCoins = document.getElementById("friendCoins");

        userPokemonsList.innerHTML = '';
        friendPokemonsList.innerHTML = '';
        userCoins.innerText = 'Coins: ' + data.user_money;
        friendCoins.innerText = 'Coins: ' + data.friend_money;

        userPagesNumber = Math.ceil(data.pokemons.length / 12);
        friendsPagesNumber = Math.ceil(data.friendpokemons.length / 12);

        setupPagination(userPagesNumber, pagination, showPage);
        setupPagination(friendsPagesNumber, friendPagination, showFriendPage);

        showPage(data, userPage);
        showFriendPage(data, friendPage);
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
                if (userPage > 0) {
                    userPage--;
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
                if (userPage < pagesNumber - 1) {
                    userPage++;
                    showPageFunction(receivedData, userPage);
                }
            };
            nextButton.appendChild(nextButtonLink);
            paginationElement.appendChild(nextButton);
        }
    }

    function showPage(data, page) {
        let userPokemonsList = document.getElementById("userPokemonsList");
        userPokemonsList.innerHTML = '';

        for (let index = page * 12; index < data.pokemons.length && index < page * 12 + 12; index++) {
            let pokemon = data.pokemons[index];
            let listItem = createPokemonCard(pokemon, userPokemonsSelected);
            userPokemonsList.appendChild(listItem);
        }
    }

    function showFriendPage(data, page) {
        friendPokemonsList.innerHTML = '';

        for (let index = page * 12; index < data.friendpokemons.length && index < page * 12 + 12; index++) {
            let pokemon = data.friendpokemons[index];
            let listItem = createPokemonCard(pokemon, friendPokemonsSelected);
            friendPokemonsList.appendChild(listItem);
        }
    }

    function createPokemonCard(pokemon, selectedList) {
        let listItem = document.createElement('div');
        listItem.className = "col-md-3 position-relative mb-3";

        let card = document.createElement("div");
        card.className = "card";
        let cardbody = document.createElement("div");
        cardbody.className = "card-body text-center";

        let header = document.createElement("h5");
        header.innerText = pokemon.name;

        let img = document.createElement("img");
        img.src = `https://assets.pokemon.com/assets/cms2/img/pokedex/full/${pokemon.id.toString().padStart(3, '0')}.png`;
        img.title = pokemon.name;
        img.alt = pokemon.name;
        img.className = "text-bg-light";
        img.style.width = "100px";
        img.style.height = "100px";

        cardbody.appendChild(header);
        cardbody.appendChild(img);
        card.appendChild(cardbody);
        listItem.appendChild(card);

        card.onclick = function() {
            const selectedIndex = selectedList.indexOf(pokemon.id);

            if (selectedIndex !== -1) {
                card.style.backgroundColor = "white";
                selectedList.splice(selectedIndex, 1);
            } else {
                card.style.backgroundColor = "#ead4f2";
                selectedList.push(pokemon.id);
            }
        };

        return listItem;
    }

    span.onclick = function() {
        modal.style.display = "none";
    };

    sendButton.onclick = function() {
        let send = {
            'receiver': getUserName(),
            'pokemons_send': userPokemonsSelected,
            'pokemons_received': friendPokemonsSelected
        };
        fetch('/trades/saveTrade/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(send)
        })
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error('Network response was not ok');
            }
        })
        .then(data => {
            console.log(JSON.stringify(userPokemonsSelected));
            console.log(data);
        })
        .catch(error => {
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
