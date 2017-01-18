import paramiko
import subprocess
import sys
#import exceptions # no longer needed, as exceptions has been moved to builtins in Python 3
import collections # deque
import os # path.split, path.join

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
    def __init__(self, url, uname, pwd, dir='~'):
        self._url = url
        self._uname = uname
        self._pwd = pwd
        self._dir = dir
    
    def username(self):
        return self._uname

    def url(self):
        return self._url
    
    def password(self):
        return self._pwd
    
    def dir(self):
        return self._dir
    
    def dict(self):
        """
        Return a dictionary containing username, dir and url.
        """
        return dict([['username', self._uname], ['url', self._url], ['dir', self._dir]])


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
        self._cwd = cdata.dir()
    
    def exec_command(self, cmd_string):
        """
        Execute a command within the session on the remote machine.

        Return the stdout response.
        """
        # exec_command() returns a tuple (stdin, stdout, stderr)
        stdin, stdout, stderr = self._client.exec_command(cmd_string)

        stdout_txt = stdout.read().decode("utf-8")
        stdout_txt += stderr.read().decode("utf-8")
        
        return stdout_txt

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

        raise NotImplementedError
    
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

    def get_cwd(self):
        """
        Return the current working directory.

        Since Paramiko doesn't maintain an open channel, we store the current 
        working directory in a member `cwd`.
        The working directory is managed completely by the Session and all
        commands attempting to change it are intercepted.
        """
        return self._cwd
    
    def exec_command(self, cmd_string):
        """
        Execute a command within the session on the remote machine.

        Return the stdout response.
        """
        dir = check_cd(cmd_string)

        if dir:
            self._cwd = update_cwd(self._cwd, dir)
        else:
            # nothing to be done. working directory has not been changed
            pass

        if self._cwd == '~':
            return self._client.exec_command(cmd_string)
        else:
            cmd_queue = ManagedCWD.correct_cwd(self)
            return self._client.exec_command(cmd_queue.combine())

class Response(object):
    
    def __init__(self, cmd, res):
        self._cmd = cmd
        self._res = res
    


class CommandQueue(object):
    """
    Stores commands that are to be executed in order.

    Since paramiko closes the channel after each command is executed, we have to
    chain commands by hand.
    """
    
    separator = " ; " # separates two commands

    def __init__(self, *args):
        if (args == None):
            self._cmd_list = []
        else:
            try:
                args = [str(a) for a in args]
            except:
                raise TypeError("Commands need to be strings or convertable to strings")
            
            self._cmd_list = args
    
    def combine(self):
        """
        Combine the commands in the queue to one single chained command.

        Returns:
        * (string) command

        Example:
        CommandQueue("abc", "def").combine() -> "abc ; def"
        """
        cmd_string = ""
        cmd_queue = collections.deque(self._cmd_list)

        while (len(cmd_queue) > 1):
            cmd_string += cmd_queue.popleft()
            cmd_string += CommandQueue.separator
        
        if (len(cmd_queue) > 0):
            cmd_string += cmd_queue.pop()
    
        return cmd_string
    
    def add(self, *args):
        """
        Add arguments to the CommandQueue.
        """
        try:
            args = [str(a) for a in args]
        except:
            raise TypeError("Commands need to be strings or convertable to strings")
        
        self._cmd_list += args
    

    def clear(self):
        """
        Delete all commands from the CommandQueue.import
        """
        self._cmd_list = []
    
    def __len__(self):
        return len(self._cmd_list)
    
    def __str__(self):
        return "CommandQueue(" + str(self._cmd_list) + ")"
    
    def __eq__(self, other):
        if isinstance(other, CommandQueue):
            return self._cmd_list == other._cmd_list
        else:
            return False
    
    def as_list(self):
        """
        Return the list of commands stored in the queue.
        """
        return self._cmd_list


def run_command(cdata, cmd_string):
    """
    Execute a command cmd_string in a session specified by cdata.

    Parameters:
    * cdata         : cdata object containing the connection data
    * cmd_string    : (string) command to be executed
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



def run_mult_commands(cdata, command_list):
    """
    Execute a list of commands in a session configured by the connection data `cdata`.

    Parameters:
    * cdata         : cdata object
    * command_list  : list of commands (string)

    Returns:
    * out_string    : (string) output string read from the channel after running
                      the command
    """
    
    cmd_queue = CommandQueue(*command_list)

    out_string = run_command(cdata, cmd_queue.combine())

    return out_string


def run_command_in_dir(cdata, cmd_string):
    """

    """
    change_dir = check_cd(cmd_string)

    # cd command detected, return new directory
    if change_dir is not None:
        return '', change_dir
    
    return run_command(cdata, cmd_string), cdata


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



class ManagedCWD:
    """
    Function decorator for functions that return command strings. 
    
    Prepends a cd command before the command that is retured by the function.
    When the command is executed, the working directory on the remote server is
    changed before the actual command is executed.
    """
    def correct_cwd(session):
        """
        Return a CommandQueue that changes to the current working directory.

        Parameters:
        * session   : (SSHSession) session

        Returns:
        * cd_cmd    : (string) command to change to cwd
        """
        cd_cmd = "cd " + str(session.get_cwd())
        
        return CommandQueue([cd_cmd])

    def __init__(self, f):
        self._f = f # store function to decorate
    
    def __call__(self, *args):

        if (len(args) >= 1): # function has arguments
            session = args[0] # session is first argument
            cd_cmd = correct_cwd(session)
            other_cmd = self._f(*args[1:]) # actual command

            return cd_cmd.add([other_cmd]).combine() # return combined command, cd first

        else: # function has no arguments
            pass
            # this should raise an exception, since at least the session \
            # is needed

def check_cd(cmd_string):
    """
    Check command string for cd command and return the new directory.
    """
    arg_list = cmd_string.split()

    if len(arg_list) <= 2:
        if arg_list[0] == "cd":
            return arg_list[1] if len(arg_list) == 1 else '.'
        else:
            return None
    else:
        return None

def command_list_to_string(clist):
    """
    Recombine command list into one single string.
    Essentially reverses the string.split() method.
    """
    cmd_str = ""
    i = 0
    while i < len(clist)-1:
        cmd_str += clist[i]
        cmd_str += " "
    cmd_str += clist[-1]

def update_cwd(cwd, dir):

    path_list = splitpath(dir)
    cwd_list = splitpath(cwd)

    if path_list[0] == '' or path_list[0] == '~':
        # absolute path
        return dir
    else:
        #while not len(path_list) == 0:
        #    cur_dir = path_list.pop(0)
        #   cwd = os.path.join(cwd, cur_dir)
        os.path.join(*cwd_list, *path_list)

def splitpath(path):
    """
    Split path into tuple of strings. Splits along slashes. 
    """
    head = path
    path_list = []
    while head != '':
        head, tail = os.path.split(head)
        path_list.append(tail)
    
    return path_list[::-1]

def splitpath_r(path):
    """
    Recursive implementation of splitpath().

    ! UNSTABLE !
    """
    head, tail = os.path.split(path)
    if head == '':
        return [tail]
    else:
        return splitpath(head) + [tail]