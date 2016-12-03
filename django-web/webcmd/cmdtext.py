MAX_NUM_STORED_LINES = 200
MAX_NUM_LINES = 10
LINEWIDTH = 80

class CmdText(object):
    """
    Represents a command line text device. Text is split into lines
    corresponding to the linewidth of the device.
    """
    def __init__(self):
        """
        Construct empty object.
        """
        self.num_lines = 0
        self.remaining_lines = MAX_NUM_LINES
        self.lines = []

    def insert(self, string):
        """
        Insert string at the end. This always begins a new line.
        """
        if (self.num_lines >= MAX_NUM_LINES):
            pass
        
        input_num_lines = num_lines(string)

        #if (input_num_lines > self.remaining_lines):
        #    num = self.remaining_lines
        #else:
        #    num = input_num_lines
        num = input_num_lines
        
        new_lines = get_lines(string)

        self.lines += new_lines[-num:]
        self.update_num_lines()
    
    def merge_after(self, obj):
        """
        Merge with another CmdText object by appending the input objects content.
        """
        self.lines 
    
    def strip_lines(self):
        """
        Remove excessive number of lines. This deletes the oldest half.
        """
        if (self.num_lines > MAX_NUM_STORED_LINES):
            for i in range(MAX_NUM_STORED_LINES // 2):
                self.lines.pop(i)
    
    def update_num_lines(self):
        """
        Update the number of lines member.
        """
        self.num_lines = len(self.lines)

    def get_line(self, n):
        """
        Return the line with index n.
        """
        if n < self.num_lines:
            return self.lines[n]
        else:
            raise IndexError("Line index out of range.")
        
    def print_screen(self):
        """
        Return MAX_NUM_LINES lines.
        """
        return self.lines[-MAX_NUM_LINES:]
    
    def __iter__(self):
        """
        Iterator for CmdText object.
        """
        for l in self.lines:
            yield l
    
    def __getitem__(self, ind):
        return self.lines[ind]

def num_lines(string):
    """
    Return number of lines.
    """
    line_list = string.split("\n")
    num = len(line_list)
    for l in line_list:
        num += (len(string) / LINEWIDTH > 1)
    
    return num


def get_lines(string):
    """
    Return list of lines extracted from string.
    """
    line_list = string.split('\n')

    new_list = []
    for l in line_list:
        new_list += [l[i:i+LINEWIDTH] for i in range(len(l) // LINEWIDTH + 1)]
    
    return new_list

class Command(CmdText):
    def __init__(self, string, rind=None):
        CmdText.__init__(self)
        self.insert(string)

        if (rind is not None):
            self.response = rind
    

class Response(CmdText):
    def __init__(self, string, cind=None):
        CmdText.__init__(self)
        self.insert(string)

        if (cind is not None):
            self.command = cind