document.addEventListener('DOMContentLoaded', function() {
    const pokemonImage = document.getElementById('pokemonImage');
    const actionSplashes = document.getElementById('actionSplashes');
    const radius = 360;

    const progressBar = document.querySelector('.progress-bar');
    const maxHealth = parseInt(progressBar.getAttribute('aria-valuemax'));

    const section1 = document.getElementById('section1');
    const section2 = document.getElementById('section2');
    const section3 = document.getElementById('section3');
    const playButton = document.getElementById('playButton');

    const timeElement = document.getElementById('killTime');
    let clickCount = 0;

    const healthRegenElement = document.getElementById('healthRegen');

    const fightId = document.getElementById('fightId').value;
    const socket = new WebSocket(`ws://${window.location.host}/ws/fight/${fightId}/`);

    socket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        const clicks = data.clicks;
        const health = data.health;
        const status = data.status;
        const time = data.time;
    
        console.log(`Received data: clicks=${clicks}, health=${health}, status=${status}, time=${time}`);
    
        progressBar.style.width = `${(health / maxHealth) * 100}%`;
        progressBar.setAttribute('aria-valuenow', health);
        progressBar.querySelector('.progress-text').textContent = `${health}/${maxHealth} ❤️`;

        timeElement.textContent = `${time}⏳`;

        if (status === 0) {
            section2.style.display = 'none';
            section3.style.display = 'block';
            const defeatText = document.getElementById('defeatText');
            defeatText.style.display = 'flex';
            clearInterval(timer);
        } else if (status === 2 || health <= 0) {
            section2.style.display = 'none';
            section3.style.display = 'block';
            const victoryText = document.getElementById('victoryText');
            victoryText.style.display = 'flex';
            clearInterval(timer);
        }
    };

    playButton.addEventListener('click', function() {
        section1.style.display = 'none';
        section2.style.display = 'flex';
        startTimer();
    });


    function startTimer() {
        timer = setInterval(() => {
            socket.send(JSON.stringify({
                'action': 'second'
            }));
        }, 1000);
    }

    function shakePokemonImage() {
        pokemonImage.classList.add('shake');
        setTimeout(() => {
            pokemonImage.classList.remove('shake');
        }, 500);
    }

    function showActionWords() {
        const randomEvent = document.createElement('span');
        randomEvent.textContent = getRandomEvent();
        randomEvent.classList.add('actionWord', 'appear');

        const angle = Math.random() * Math.PI * 2;

        const x = pokemonImage.offsetLeft + pokemonImage.clientWidth / 2 + radius * Math.cos(angle) - actionSplashes.offsetLeft - randomEvent.offsetWidth / 2;
        const y = pokemonImage.offsetTop + pokemonImage.clientHeight / 2 + radius * Math.sin(angle) - actionSplashes.offsetTop - randomEvent.offsetHeight / 2;

        const rotation = Math.random() * 30 - 15;
        randomEvent.style.transform = `rotate(${rotation}deg)`;

        randomEvent.style.left = `${x}px`;
        randomEvent.style.top = `${y}px`;

        actionSplashes.appendChild(randomEvent);

        setTimeout(() => {
            randomEvent.remove();
        }, 1000);
    }

    pokemonImage.addEventListener('click', function(event) {
        shakePokemonImage();
        clickCount++;

        if (clickCount % 2 === 0) {
            showActionWords();
        }

        socket.send(JSON.stringify({
            'action': 'click'
        }));
    });

    function getRandomEvent() {
        const events = ["*click*", "*clack*", "CLICK!", "CLACK!", "BLAM!", "POW!", "WHAM!", "ZOWEE!", "BOOM!", "BAM!", "CRASH!", "KAPOW!", "BANG!", "THUD!", "SMASH!", "ZAP!", "SLAM!", "KABOOM!", "CRUNCH!", "KERPLUNK!"];
        return events[Math.floor(Math.random() * events.length)];
    }
});