const wsProtocol = window.location.protocol === 'https:' ? 'wss://' : 'ws://';
const ws_url = `${wsProtocol}${window.location.host}/ws/online/`;
const ws_status = new WebSocket(ws_url);

ws_status.onopen = function (e){
    console.log('connected');
        try {
            const username = getUserName(); // Assuming this function gets the current username
            ws_status.send(JSON.stringify({
                'username': username,
                'status': 'online'
            }));
        }
        catch (err) {
            console.log("Error get user name")
        }
}

ws_status.onclose = function (e){
    console.log('disconected')
}

ws_status.onmessage = function(e) {
    const data = JSON.parse(e.data);
    const username = getUserName(); // Assuming this function gets the current username
    const status = data.message;
    console.log(username, status, data);

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
        ws_status.send(JSON.stringify({
            'username': username,
        }));
    }, 10000);
};

