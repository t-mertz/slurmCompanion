// Note that the path doesn't matter for routing; any WebSocket
// connection gets bumped over to WebSocket consumers
socket = new WebSocket("ws://" + window.location.host + "/chat/");
socket.onmessage = function(e) {
    var data = JSON.parse(e.data);
    //alert(data);
    console.log(data);
    var lines = JSON.parse(data.list);
    for(i in lines) {
        console.log(lines[i]);
    }
}
socket.onopen = function() {
    socket.send("hello world");
}
// Call onopen directly if socket is already open
if (socket.readyState == WebSocket.OPEN) socket.onopen();