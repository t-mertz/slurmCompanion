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


def encrypt(message, key):
    """
    Wrapper for simplecrypt.encrypt

    Encrypt message with key as password.
    """
    simplecrypt.encrypt(key, message)


def decrypt(message, key):
    """
    Wrapper for simplecrypt.decrypt

    Decrypt message with key as password.
    """
    simplecrypt.decrypt(key, message)