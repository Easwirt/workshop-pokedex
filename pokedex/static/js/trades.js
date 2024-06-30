document.addEventListener("DOMContentLoaded", function (){
    var tradeButton = document.getElementById("Trade-btn")
    var span = document.getElementById("close")
    var modal = document.getElementById("tradesModal")
    var friendname = getUserName()

    if(tradeButton){
        tradeButton.onclick = function (){
            fetch(`/trades/tradeList/${friendname}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                }
            })
            .then(response =>{
                if (response.ok){
                    modal.style.display = "block"
                    return response.json()
                }
                else{
                    throw new Error('Network response was not ok')
                }
            })
            .then(data => {
                let userPokemonsList = document.getElementById("userPokemonsList")
                userPokemonsList.innerHTML = ''

                data.pokemons.forEach(pokemon => {
                    let listItem = document.createElement('div')
                    listItem.className = "col-md-3 position-relative mb-3"

                    let card = document.createElement("div")
                    card.className = "card"
                    let cardbody = document.createElement("div")
                    cardbody.className = "card-body text-center"

                    let header = document.createElement("h5")
                    header.innerText = `${pokemon.name}`
                    let link = document.createElement("a")
                    link.href = `/pokemons/${pokemon.id}`

                    let img = document.createElement("img")
                    img.src =`https://assets.pokemon.com/assets/cms2/img/pokedex/full/${pokemon.id.toString().padStart(3, '0')}.png`
                    console.log(`https://assets.pokemon.com/assets/cms2/img/pokedex/full/${pokemon.id.toString().padStart(3, '0')}.png`)
                    img.title = `${pokemon.name}`
                    img.alt = `${pokemon.name}`
                    img.className = "text-bg-light"
                    img.style.width = "100px"
                    img.style.height = "100px"

                    link.appendChild(img)
                    cardbody.appendChild(header)
                    cardbody.appendChild(link)
                    card.appendChild(cardbody)
                    listItem.appendChild(card)
                    userPokemonsList.appendChild(listItem)
                })
                let friendPokemonsList = document.getElementById("friendsPokemonsList")
                friendPokemonsList.innerHTML = ''

                data.friendpokemons.forEach(pokemon => {
                    let listItem = document.createElement('div')
                    listItem.className = "col-md-3 position-relative mb-3"

                    let card = document.createElement("div")
                    card.className = "card"
                    let cardbody = document.createElement("div")
                    cardbody.className = "card-body text-center"

                    let header = document.createElement("h5")
                    header.innerText = `${pokemon.name}`
                    let link = document.createElement("a")
                    link.href = `/pokemons/${pokemon.id}`

                    let img = document.createElement("img")
                    img.src =`https://assets.pokemon.com/assets/cms2/img/pokedex/full/${pokemon.id.toString().padStart(3, '0')}.png`
                    console.log(`https://assets.pokemon.com/assets/cms2/img/pokedex/full/${pokemon.id.toString().padStart(3, '0')}.png`)
                    img.title = `${pokemon.name}`
                    img.alt = `${pokemon.name}`
                    img.className = "text-bg-light"
                    img.style.width = "100px"
                    img.style.height = "100px"

                    link.appendChild(img)
                    cardbody.appendChild(header)
                    cardbody.appendChild(link)
                    card.appendChild(cardbody)
                    listItem.appendChild(card)
                    friendPokemonsList.appendChild(listItem)
                })

                console.log('Success:', data)
            })
            .catch((error) => {
                console.error('Error', error)
            })
        }

        modal.onclick = function (){
            modal.style.display = "none"
        }
        span.onclick = function () {
            modal.style.display = "none"
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