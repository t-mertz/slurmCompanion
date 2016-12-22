// Note that the path doesn't matter for routing; any WebSocket
// connection gets bumped over to WebSocket consumers
socket = new WebSocket("ws://" + window.location.host + "/cmd/");

socket.onmessage = function(e) {
    var msg = JSON.parse(e.data);

    if ("command_string" in msg) {
        // make new <p> element and insert the data
        add_paragraph(msg["command_string"]);
    }
    else if ("response_string" in msg) {
        // make new <p> element and insert the data
        add_paragraph(msg["response_string"]);
    }
    else {
        alert(msg);
    }
}

socket.onopen = function() {
    //socket.send("hello world");
}


// Call onopen directly if socket is already open
if (socket.readyState == WebSocket.OPEN) socket.onopen();

submit = function(input) {
    socket.send(input.text);
}

/** Add a paragraph to the command window and insert the message.
 */
add_paragraph = function(msg) {
    
    var newpar = document.createElement("p");
    var newnode = document.createTextNode(msg);
    newpar.appendChild(newnode);

    document.getElementById("cmdWindow").appendChild(newpar);
}