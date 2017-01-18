from channels import Channel
from channels.sessions import channel_session
from channels.auth import channel_session_user, channel_session_user_from_http

import json
import sshcomm.comm as comm
from .cmdtext import Command, Response
from sshcomm.models import UserData, RemoteServer
from sshcomm.security import decrypt_Crypto

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
                                      sinfo['url'],
                                      sinfo['directory']) + cmd

@channel_session_user_from_http
def ssh_connect(message):
    '''
    Handle WebSocket connection and store necessary data in session.
    '''
    pass


@channel_session_user
def ssh_cmd(message):
    """
    Retrieve SSH session of the channel and execute the command.
    Send the response over the channel.
    """
    #cmd_string = json.loads(message.content)['command_string']
    print(message.content)
    message_data = json.loads(message.content['text'])
    cmd_string = message_data['command_string']    # string entered into the command prompt

    '''
    profile_name = message.session['profile_name'] # profile name corresponding to the shell
    shell_dir = message.session['shell_dir']       # current working directory of the shell
    '''

    # for now, open up a new channel each time
    cdata = comm.ConnectionData("192.168.178.112", "user", " ")
    sinfo = cdata.dict()
    sinfo.update({'directory': '~'})

    '''
    # retrieve user and server data
    user_data = UserData.objects.get(profile_name__equals=profile_name, owner__equals=message.user)
    server_data = user_data.server

    # decrypt user data
    key = message.session['hashkey']
    uname = decrypt_Crypto(user_data.user_name, key)
    pw = decrypt_Crypto(user_data.user_password, key)

    # setup connection data
    cdata = comm.ConnectionData(server_data.server_url, uname, pw)
    sinfo = cdata.dict()
    sinfo.update({'directory': shell_dir})
    '''
    command_list = Command(format_command(cmd_string, sinfo))[:]
    print(command_list)
    
    # send command back for quick update
    message.reply_channel.send({"text": json.dumps({
        "command_list": command_list,
    })})

    # execute command
    try:
        response_string = comm.run_command(cdata, cmd_string) # use InteractiveSession to manage directory
        #response_string, new_cwd = comm.run_command_in_dir(cdata, cmd_string)
    except Exception as e:
        response_string = "[backend failed: {}] response to ".format(e) + cmd_string
    
    response_list = Response(response_string)[:]
    # update directory
    #message.session['shell_dir' = new_cwd]
    
    # send response back
    message.reply_channel.send(
        {"text": json.dumps({
        #"command_string": cmd_string,
        "response_list": response_list,
        })})


'''
@channel_session_user_from_http
def ws_connect(message):
    """
    Upon creation of the WebSocket channel, connect to the SSH server
    and store the session in the channel session.
    """
    
    ssh_session = None
    
    try:
        message.channel_session['ssh_session'] = ssh_session
    except:
        raise

'''