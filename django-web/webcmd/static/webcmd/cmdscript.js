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

    if ("command_string" in msg) {
        var lines = JSON.parse(msg.command_string);
    }
    else if ("response_string" in msg) {
        var lines = JSON.parse(msg.response_string);
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