from django.test import TestCase
from django.urls import reverse
from django.contrib import auth
from django.contrib.auth.models import User
import datetime
from django.contrib.auth.models import UserManager

import webcmd.cmdtext as cmdtext
from .forms import CmdForm
from sshcomm.models import RemoteServer, UserData


# Create your tests here.

class CmdTextTests(TestCase):

    def test_num_lines_with_two_lines(self):

        cmd_text = cmdtext.CmdText()
        cmd_text.insert("a\nb")

        self.assertEqual(cmd_text.num_lines, 2)
    
    def test_num_lines_with_one_line(self):

        cmd_text = cmdtext.CmdText()
        cmd_text.insert("a")

        self.assertEqual(cmd_text.num_lines, 1)

    def test_linebreak_characters(self):
        
        text = "\n"*4

        cmd_text = cmdtext.CmdText()

        cmd_text.insert(text)

        self.assertEqual(cmd_text.num_lines, 5)

class CmdViewTests(TestCase):

    def test_command_gets_printed(self):
        cmd_text = "abcdefg"
        data = CmdForm(cmd_text)
        url = reverse('webcmd:cmd')
        response = self.client.post(url, data=data)

        self.assertIn(cmd_text, response)


class TestServerSelection(TestCase):

    def test_display_single_server(self):
        # test that a server is displayed
        pass
        new_server = RemoteServer(server_url="", server_name="abc", date_added=datetime.date(2016,1,1))
        new_server.save()

        #user = User(username='user', password='password', email='')
        #user.save()
        user = User.objects.create_user(username='user', password='password')

        logged_in = self.client.login(username='user', password='password')

        self.assertTrue(logged_in)

        userdata = UserData(owner=user, profile='profile1', server=new_server, user_name='uname', user_password='upw')
        userdata.save()

        url = reverse('webcmd:index')
        response = self.client.get(url)

        self.assertContains(response, 'profile1')

    
    def test_display_two_servers(self):
        # test that two servers are displayed
        pass
        new_server = RemoteServer(server_url="", server_name="abc", date_added=datetime.date(2016,1,1))
        new_server.save()

        #user = User(username='user', password='password', email='')
        #user.save()
        #user = self.client.create_user(username='user', password='password')
        user = User.objects.create_user(username='user', password='password')

        logged_in = self.client.login(username='user', password='password')

        self.assertTrue(logged_in)
        #user = auth.get_user(self.client)

        userdata = UserData(owner=user, profile='profile1', server=new_server, user_name='uname', user_password='upw')
        userdata.save()

        userdata = UserData(owner=user, profile='profile2', server=new_server, user_name='uname', user_password='upw')
        userdata.save()

        url = reverse('webcmd:index')
        #url = '/cmd/'
        response = self.client.get(url)

        self.assertContains(response, 'profile1')
        self.assertContains(response, 'profile2')

    def test_different_user_server_not_displayed(self):
        new_server = RemoteServer(server_url="", server_name="abc", date_added=datetime.date(2016,1,1))
        new_server.save()

        #user = User(username='user', password='password', email='')
        #user.save()
        #user = self.client.create_user(username='user', password='password')
        user = User.objects.create_user(username='user', password='password')
        user2 = User.objects.create_user(username='user2', password='password')

        logged_in = self.client.login(username='user', password='password')

        self.assertTrue(logged_in)
        #user = auth.get_user(self.client)

        userdata = UserData(owner=user, profile='profile1', server=new_server, user_name='uname', user_password='upw')
        userdata.save()

        userdata = UserData(owner=user2, profile='profile2', server=new_server, user_name='uname', user_password='upw')
        userdata.save()

        url = reverse('webcmd:index')
        #url = '/cmd/'
        response = self.client.get(url)

        self.assertContains(response, 'profile1')
        self.assertNotContains(response, 'profile2')