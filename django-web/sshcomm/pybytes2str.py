import json
import unittest
from Crypto import Random

def encode(b):
    """
    Encode a bytes object into a string. No encoding is necessary, since the bytes are 
    represented as numbers in the returned string.
    """
    
    # assemble data in list of bytes
    l = []

    for byte in b:
        l.append(byte)
    
    return json.dumps(l)


def decode(s):
    """
    Decode a string which has been produced by *encode* to a bytes object.
    """

    l = json.loads(s)

    b = bytes(l)

    return b


# ============================================================================

# Tests

class TestConversion(unittest.TestCase):

    def test_empty(self):
        b = b''
        self.assertEqual(decode(encode(b)), b)
    
    def test_string(self):
        b = b'abcd'
        self.assertEqual(decode(encode(b)), b)
    
    def test_random(self):
        b = Random.new().read(10)
        self.assertEqual(decode(encode(b)), b)

if __name__ == '__main__':
    unittest.main()