from django.test import TestCase

import cmdtext
from .forms import CmdForm


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

class CmdViewTests(TestCase):

    def test_command_gets_printed(self):
        cmd_text = "abcdefg"
        data = CmdForm(cmd_text)
        url = reverse('webcmd:cmd')
        response = self.client.post(url, data=data)

        self.assert_contains(response, cmd_text)