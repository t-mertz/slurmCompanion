import hashlib # sha512
from simplecrypt import encrypt, decrypt

def create_key(username, password):
    """
    Create a hash key from a username and password.

    Uses sha512 method from hashlib.
    """
    hstring = username + password # this could be something more involved

    m = hashlib.sha512() # use Crypto.hash instead?
    m.update(hstring)

    return m.digest()

def bkey_to_ukey(key):
    """
    Convert bytes key to unicode string.
    Makes key JSON serializable.
    """
    return key.decode('unicode_escape')

def ukey_to_bkey(key):
    """
    Convert unicode string to byte string.
    Needed for encrypt and decrypt methods.
    """
    bkey = bytes(key, 'unicode_escape')




def encrypt(message, key):
    """
    Wrapper for simplecrypt.encrypt

    Encrypt message with key as password.
    """
    encrypt(key, message)


def decrypt(message, key):
    """
    Wrapper for simplecrypt.decrypt

    Decrypt message with key as password.
    """
    decrypt(key, message)