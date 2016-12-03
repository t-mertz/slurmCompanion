from django.test import TestCase

import cmdtext

# Create your tests here.

class CmdTextTests(TestCase):

    def test_num_lines_with_two_lines(self):

        cmd_text = cmdtext.CmdText()
        cmd_text.insert("a\nb")

        self.assert_is(cmd_text.num_lines(), 2)
    
    def test_num_lines_with_one_line(self):

        cmd_text = cmdtext.CmdText()
        cmd_text.insert("a")

        self.assert_is(cmd_text.num_lines(), 1)

    def test_linebreak_characters(self):
        
        text = "\n"*4

        cmd_text = cmdtext.CmdText()

        cmd_text.insert(text)

        self.assert_is(cmd_text.num_lines(), 4)
