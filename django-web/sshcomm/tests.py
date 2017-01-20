from django.test import TestCase

from .models import RemoteServer
from .security import create_key, create_string_key, encode_key, decode_key, crop_key, encrypt_Crypto, decrypt_Crypto
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


class TestKeyCreation(TestCase):

    def test_create_key_nonzero(self):
        self.assertTrue(len(create_key('uname', 'pw')) > 0)
    
    def test_create_key_differs_with_similar_input(self):
        self.assertNotEqual(create_key('uname', 'pw'), create_key('uname1', 'pw'))
    
    def test_create_string_key_nonzero(self):
        self.assertTrue(len(create_string_key('uname', 'pw')) > 0)
    
    def test_create_string_key_differs_with_similar_input(self):
        self.assertNotEqual(create_string_key('uname', 'pw'), create_string_key('uname1', 'pw'))

class TestKeyConversion(TestCase):

    def test_encode_key_letter_a(self):
        import json
        key = json.dumps([97])
        self.assertEqual(encode_key(b'a'), key)

    def test_encode_key_letter_short_string(self):
        import json
        key = json.dumps([73, 32, 107, 110, 111, 119, 32, 116, 104, 105, 115, 32, 116, 101, 120, 116])
        self.assertEqual(encode_key(b'I know this text'), key)
    
    def test_decode_key_letter_a(self):
        import json
        key = json.dumps([97])
        self.assertEqual(decode_key(key), b'a')
    
    def test_decode_key_letter_short_string(self):
        import json
        key = json.dumps([73, 32, 107, 110, 111, 119, 32, 116, 104, 105, 115, 32, 116, 101, 120, 116])
        self.assertEqual(decode_key(key), b'I know this text')
    
    def test_encode_decode(self):
        test_bytes = b"This is a test sentence designed to test the conversion from string -> bytes. It can contain any ASCII character: $%&#/[]{}^()_=''"
        self.assertEqual(decode_key(encode_key(test_bytes)), test_bytes)
    

class TestEnDecryption(TestCase):

    def test_crop_key_empty_raises_valueerror(self):
        self.assertRaises(ValueError, crop_key, b'', 16)

    def test_crop_key_too_short_odd(self):
        self.assertEqual(len(crop_key(b'key', 16)), 16)

    def test_crop_key_too_short_even(self):
        self.assertEqual(len(crop_key(b'key1', 16)), 16)

    def test_crop_key_too_long_odd(self):
        self.assertEqual(len(crop_key(b'key', 2)), 2)

    def test_crop_key_too_long_even(self):
        self.assertEqual(len(crop_key(b'key1', 2)), 2)

    def test_crop_key_exact(self):
        key = b'Sixteen byte key'
        self.assertEqual(crop_key(key, 16), key)
    
    def test_encrypt_decrypt(self):
        key = b'Sixteen byte key'
        test_text = "this is my test text"
        crypt_text = encode_key(encrypt_Crypto(test_text, key))
        plain_text = decrypt_Crypto(crypt_text, key).decode('utf-8')
        self.assertEqual(test_text, plain_text)