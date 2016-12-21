from channes import Channel

def cmd_consumer(message):
    """
    Retrieve SSH session of the channel and execute the command.
    Send the response over the channel.
    """
    command_string = message.content['command_string']

    # retrieve SSH session
    ssh_session = message.channel_session['ssh_session']

    # run command on the SSH server
    try:
        response_string = ssh_session.execute_command(command_string)
    except Exception as e:
        response_string = "Command failed: {}".format(e)
    

    msg.reply_channel.send({
        "command_string": command_string,
        "response_string": response_string,
    })



@channel_session_user_from_http
def ws_connect(message):
    """
    Upon creation of the WebSocket channel, connect to the SSH server
    and store the session in the channel session.
    """
    
    ssh_session = None
    
    try:
        message.channel_session['ssh_session'] = ssh_session