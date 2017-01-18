
/** Add a paragraph to the command window and insert the message.
 */
add_paragraph = function(msg) {
    
    var newpar = document.createElement("p");
    var newnode = document.createTextNode(msg);
    newpar.appendChild(newnode);

    document.getElementById("cmdWindow").appendChild(newpar);
}


// Note that the path doesn't matter for routing; any WebSocket
// connection gets bumped over to WebSocket consumers
socket = new WebSocket("ws://" + window.location.host + "/cmd/");

/**Called when message is received via WebSocket.
 * Look for *command_string* or *response_string* in the message data,
 * decode the JSON string and insert the text line by line.
 */
socket.onmessage = function(e) {
    var msg = JSON.parse(e.data);
    var error = false;

    if ("command_list" in msg) {
        var lines = msg.command_list;
    }
    else if ("response_list" in msg) {
        var lines = msg.response_list;
    }
    else {
        error = true;
        alert(msg);
    }

    // insert the lines
    if (!error) {
        for (line in lines) {
            // make new <p> element and insert the data
            add_paragraph(lines[line]);
        }
    }
}

/**Called when the WebSocket connection is first opened.
 * Currently does nothing.
 */
socket.onopen = function() {
    //socket.send("hello world");
}


// Call onopen directly if socket is already open
if (socket.readyState == WebSocket.OPEN) socket.onopen();

/**Called when the submit button is clicked.
 * Sends the text of the input field via WebSocket.
 */
submit = function() {
    var input = document.getElementById('command_input').value;
    socket.send(JSON.stringify({
        "command_string": input}));
}


