

function create_div_from_message_dict(dict) {
    var new_message_element = document.createElement('div');
    new_message_element.className = 'message';

    var new_sender_element = document.createElement('div');
    var new_content_element = document.createElement('div');
    var new_time_sent_element = document.createElement('div');

    new_sender_element.innerHTML = dict['sender'];
    new_time_sent_element.innerHTML = dict['time_sent'];
    new_content_element.innerHTML = dict['content'];

    new_message_element.appendChild(new_sender_element);
    new_message_element.appendChild(new_time_sent_element);
    new_message_element.appendChild(new_content_element);

    return new_message_element;
}

// decode the message sent via the websocket
var dict = 0;

// create a new message html element
var new_message_element = create_div_from_message_dict(dict);

// retrieve the message list
var message_list_element = document.getElementsByClassName('message_list');
// append message to the message list
message_list_element.appendChild(new_message_element);