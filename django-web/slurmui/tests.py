from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

from .views import serversettings_addserver, add_user_data
from sshcomm.models import RemoteServer, UserData

def get_post_user_data(profilename='testprofile'):
    new_server = RemoteServer(server_name='testserver', server_url='192.168.178.122', date_added=timezone.now())
    new_server.save()

    return {'server_name': 'testserver',
        'input_profile_name': profilename,
        'input_username': 'username',
        'input_password': 'password',
        'input_loc_password': 'loc_password',
        }

class TestAddUserData(TestCase):

    def test_add_userdata_exists(self):
        post = get_post_user_data('testprofile')
        
        response = self.client.post(reverse('settings_addserver'), post)
        
        self.assertEqual(len(UserData.objects.filter(profile='testprofile')), 1)
        self.assertContains(response, 'testprofile')
    
    def test_add_multiple_userdata(self):
        post = get_post_user_data('testprofile1')
        response1 = self.client.post(reverse('settings_addserver'), post)

        post = get_post_user_data('testprofile2')
        response2 = self.client.post(reverse('settings_addserver'), post)

        self.assertContains(response2, 'testprofile1')
        self.assertContains(response2, 'testprofile2')


    def test_add_duplicate_userdata(self):
        post = get_post_user_data('testprofile')
        response1 = self.client.post(reverse('settings_addserver'), post)

        post = get_post_user_data('testprofile')
        response2 = self.client.post(reverse('settings_addserver'), post)

        self.assertContains(response2, 'existed')

    def test_add_duplicate_userdata_function(self):
        server = RemoteServer(server_url='url', server_name='name', date_added=timezone.now())
        server.save()
        userdata = {'server': server,
        'profile': 'profilename',
        'username': 'username',
        'password': 'password',
        'loc_password': 'loc_password',
        }

        user = User(username='loc_username', password='loc_password', email='abc@def.gh')
        user.save()

        retval = add_user_data(userdata, user)
        self.assertEqual(len(UserData.objects.all()), 1)

        retval = add_user_data(userdata, user)
        self.assertEqual(len(UserData.objects.all()), 1)

        self.assertIn('error_message', retval)