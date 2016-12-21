import paramiko
import subprocess
import sys
#import exceptions # no longer needed, as exceptions has been moved to builtins in Python 3

SYSTEM = sys.platform # the platform the server is running on
MEGABYTE = 1024**2    # size of one megabyte in bytes
MAX_FILE_SIZE = 1 * MEGABYTE


class UnsupportedOSError(Exception):
    def __init__(self, value):
        self._value = value
    
    def __str__(self):
        return "OS not supported: " + repr(self._value)

class FileSizeExceededError(Exception):
    def __init__(self, value):
        self._value = value[1]
        self._name = value[0]
    
    def __str__(self):
        return "Maximum allowed file size of {}MB exceeded.\nFilename: {}\nSize: {}MB".format(MAX_FILE_SIZE, self._name, self._size)

class ConnectionData(object):
    """
    Stores the connection data for an SSH session.
    """
    def __init__(self, url, uname, pwd):
        self._url = url
        self._uname = uname
        self._pwd = pwd
    
    def username(self):
        return self._uname

    def url(self):
        return self._url
    
    def password(self):
        return self._pwd


class ShhSession(object):
    """
    Session base class.
    """
    def __init__(self):
        self._client = paramiko.client.SSHClient()
        self._client.load_system_host_keys()

        # this should be removed in production
        self._client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
        print("Warning, using auto-add host key!")
        #
        
        self._username = None
    
    def connect(self, cdata):
        """
        Sets up the session and stores the username for later use.
        The password is not stored!
        """
        self._client.connect(cdata.url(), username=cdata.username(), password=cdata.password())
        self._username = cdata.username()
    
    def exec_command(self, cmd_string):
        """
        Execute a command within the session on the remote machine.

        Return the stdout response.
        """
        # exec_command() returns a tuple (stdin, stdout, stderr)
        return self._client.exec_command(cmd_string)[1]

    def close(self):
        self._client.close()

    def __del__(self):
        self.close()

class InteractiveShhSession(ShhSession):
    """
    Contains all commands that can be executed in an interactive SSH session.
    The session itself is managed by the `_client` object and terminated automatically.
    """
    def squeue_usr(self):
        """
        Retrieve user's job list.
        """
        
        cmd_string = "squeue -u " + self._username
        
        response = self.exec_command(cmd_string)

        return response

    def squeue_all(self):
        """
        Retrieve job list for all users.
        """
        
        cmd_string = "squeue"
        
        response = self.exec_command(cmd_string)

        return response
    

    def show_files(self):
        """
        Some sort of file manager, the returned file and directory names can then be 
        displayed on the website.
        """
        pass
    
    def print_file(self, filename):
        """
        Print a file's contents and return the response.
        This essentially relays the `cat` command.
        """

        cmd_string = "cat " + filename

        response = self.exec_command(cmd_string)

        return response
    
    def get_file_size(self, filename):
        """
        Check a file's size on the remote system and return the value in bytes.
        """

        cmd_string = "du " + filename

        response = self.exec_command(cmd_string)

        return int(response[1])

    def get_file(self, filename):
        """
        Download a specific file from the remote server to a local temp directory and let
        the user download it from there.
        """

        size = self.get_file_size(filename)
        if (size < MAX_FILE_SIZE):
            cmd_string = ""
        else:
            raise FileSizeExceededError([filename, size / MEGABYTE])
        
        send_file(filename)


class Response(object):
    
    def __init__(self, cmd, res):
        self._cmd = cmd
        self._res = res
    


def run_command(cdata, cmd_string):
    """
    Executes a command cmd_string in a session specified by cdata.
    """

    # create client object
    client = paramiko.client.SSHClient()

    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    client.connect(cdata.url(), username=cdata.username(), password=cdata.password())

    # execute command
    stdin, stdout, stderr = client.exec_command(cmd_string, timeout=10)

    #import time
    #time.sleep(2)
    stdout_txt = stdout.read().decode("utf-8")
    stdout_txt += stderr.read().decode("utf-8")

    """
    # retrieve output
    if stdout.channel.recv_ready():
        stdout_txt = stdout.read().decode("utf-8")
    else:
        stdout_txt = "[nothing here] {}".format(stdout.channel.recv_ready())
    """
    """
    # check for remaining output
    loop_count = 0
    while not stdout.channel.recv_exit_status():
        if stdout.channel.recv_ready():
            stdout_txt += stdout.read().decode("utf-8")
            loop_count += 1

        if loop_count > 1:
            stdout_txt += "[aborting]"
            break
    """

    # make sure a new line is triggered
    if stdout_txt == "":
        stdout_txt += " \n"
    
    # make sure session is terminated properly
    client.close()

    # response = [stdin, stdout, stderr]
    #return response
    return stdout_txt


def execute_in_session(session, cmd_string):
    """
    Executes a command in a running session.
    """

    response = session.exec_command(cmd_string)

    return response

def ping(url):
    """
    Ping a url and return boolean response.
    """

    cmd_string = "ping"

    if SYSTEM == 'linux2':
        option_string = "-c 1"
        cmd = [cmd_string, option_string, url]
    elif SYSTEM == 'win32':
        option_string = "-n 1"
        cmd = [cmd_string, url, option_string]
    else:
        raise UnsupportedOSError(SYSTEM)

    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    response_out, response_err = p.communicate()

    p.terminate()
    p.kill()

    if ("reply" in response_out.lower()):
        return True
    else:
        return False

def send_file(filename):
    """
    Send a filename to user via HTTP download.

    The webserver should update the displayed site with an <a download="filename">Download file</a> tag.
    """
    raise NotImplementedError


