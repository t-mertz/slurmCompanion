from django.test import TestCase

from .models import RemoteServer
import datetime

# Create your tests here.

class RemoteServerTests(TestCase):
    """Tests for RemoteServer model"""
    
    def test_get_installed_servers_empty(self):
        self.assertEqual(RemoteServer.get_installed_servers(), [])

    def test_get_installed_servers_one(self):
        new_server = RemoteServer(server_url="", server_name="abc", date_added=datetime.date(2016,1,1))
        new_server.save()

        self.assertEqual(RemoteServer.get_installed_servers(), [("abc", "abc")])

    def test_get_installed_servers_two(self):
        new_server = RemoteServer(server_url="", server_name="abc", date_added=datetime.date(2016,1,1))
        new_server.save()

        new_server = RemoteServer(server_url="", server_name="def", date_added=datetime.date(2016,1,1))
        new_server.save()
        
        self.assertEqual(RemoteServer.get_installed_servers(), [("abc", "abc"), ("def", "def")])