const online_Protocol = window.location.protocol === 'https:' ? 'wss://' : 'ws://';
const online_url = `${online_Protocol}${window.location.host}/ws/online/`;
console.log(online_url)
const online_status = new WebSocket(online_url);

online_status.onopen = function (e){
    console.log('connected');
}

online_status.onclose = function (e){
    console.log('disconected')
}

