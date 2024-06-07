const wsProtocol = window.location.protocol === 'https:' ? 'wss://' : 'ws://';
const ws_url = `${wsProtocol}${window.location.host}/ws/online/`;
console.log(ws_url)
const online_status = new WebSocket(ws_url);

online_status.onopen = function (e){
    console.log('connected');
        const username = getUserName(); // Assuming this function gets the current username
        online_status.send(JSON.stringify({
            'username': username,
            'status': 'online'
        }));
}

online_status.onclose = function (e){
    console.log('disconected')
}

online_status.onmessage = function(e) {
    const data = JSON.parse(e.data);
    const username = getUserName(); // Assuming this function gets the current username
    const status = data.message;
    console.log(data);
    console.log(username);
    console.log(status);

    statusOnline = 'Online';
    if(status === "0"){
        statusOnline = 'Offline'
    }
    else{
        statusOnline = 'Online'
    }

    const statusElement = document.getElementById('user-status-' + username);

    if (statusElement) {
        statusElement.textContent = statusOnline
        if(status > 0){
            statusElement.className = 'card-text text-success'
        }
        else{
            statusElement.className = 'card-text  text-muted'
        }
    }

    setTimeout(() => {
        online_status.send(JSON.stringify({
            'username': username,
        }));
    }, 10000);
};

