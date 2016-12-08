import sys

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
        num += (len(string) // LINEWIDTH + 1)
    
    return num


def get_lines(string):
    """
    Return list of lines extracted from string.
    """
    line_list = string.split('\n')

    new_list = []
    for l in line_list:
        new_list += [l[i*LINEWIDTH:(i+1)*LINEWIDTH] for i in range(len(l) // LINEWIDTH + 1)]
    
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


class TestCase(object):
    """
    Base class for tests.
    """

    @classmethod
    def run(cls):
        """
        Runs all tests (methods which begin with 'test').
        """
        #print(cls)
        max_len = max([len(a) for a in cls.__dict__])
        for key in cls.__dict__:
            if key.startswith("test"):
                fill = max_len - len(key)
                sys.stdout.write("Testing {} ...{} ".format(key, '.'*fill))
                try:
                    cls.__dict__[key]()
                except:
                    raise
                else:
                    print("Test passed!")
        print("All tests passed!")


class StaticTest(TestCase):
    """
    Tests for static methods.
    """

    def test_get_lines_with_empty_string():
        assert get_lines("") == [""]
    
    def test_get_lines_with_short_string():
        assert len(get_lines("a"*(LINEWIDTH-1))) == 1
    
    def test_get_lines_with_long_string():
        assert len(get_lines("a"*(2*LINEWIDTH-1))) == 2
    
    def test_get_lines_with_very_long_string():
        assert len(get_lines("a"*(4*LINEWIDTH-1))) == 4
    
    def test_get_lines_with_long_text_string():
        text = "This is a test string, which should simulate real text. The command should" \
         + " correctly split this text into two lines."
        LINEWIDTH = 80
        correct_lines = [text[:LINEWIDTH], text[LINEWIDTH:]]
        assert len(get_lines(text)) == len(text) // LINEWIDTH + 1
        assert get_lines(text) == correct_lines
    


class CmdTextTest(object):
    """
    Tests for CmdText class methods.
    """

    pass