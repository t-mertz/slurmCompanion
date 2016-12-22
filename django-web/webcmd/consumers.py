from channes import Channel

import sshcomm.comm as comm
from .cmdtext import CmdText

SHELL_PROMPT_STRING = "{}@{}:{}$"

def format_command(cmd, sinfo):
    """
    Take a command string and prepend a shell string with the user name, 
    server address and current working directory.

    =Parameters
    cmd   : command string
    sinfo : dictionary containing the keys 'username', 'server', 'directory'
    """
    return SHELL_PROMPT_STRING.format(sinfo['username'],
                                      sinfo['server'],
                                      sinfo['directory']) + cmd

def ssh_cmd(message):
    """
    Retrieve SSH session of the channel and execute the command.
    Send the response over the channel.
    """
    cmd_string = message.content['command_string']

    """
    # retrieve SSH session
    ssh_session = message.channel_session['ssh_session']

    # run command on the SSH server
    try:
        response_string = ssh_session.execute_command(cmd_string)
    except Exception as e:
        response_string = "Command failed: {}".format(e)
    """

    # for now, open up a new channel each time
    cdata = comm.ConnectionData("192.168.178.112", "user", " ")
    sinfo = cdata.dict()
    sinfo.update({'directory': '~'})

    # send command back for quick update
    msg.reply_channel.send({
        "command_string": format_command(cmd_string, sinfo),
    })

    # execute command
    try:
        response_string = comm.run_command(cdata, cmd_string)
    except Exception as e:
        response_string = "[backend failed: {}] response to ".format(e) + cmd_string
    
    
    # send response back
    msg.reply_channel.send({
        #"command_string": cmd_string,
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