from testenv import TestCase
from comm import CommandQueue

class CommandQueueTests(TestCase):

    def test_create_empty():
        cqueue = CommandQueue()

        assert len(cqueue) == 0
    
    def test_create_one():
        cqueue = CommandQueue("abc")

        assert cqueue.as_list() == ["abc"], "['abc'] != " + str(cqueue.as_list())
    
    def test_create_two_equal():
        cqueue = CommandQueue("abc", "abc")

        assert cqueue.as_list() == ["abc", "abc"]

    def test_create_two_different():
        cqueue = CommandQueue("abc", "def")

        assert cqueue.as_list() == ["abc", "def"]

    def test_add_one():
        cqueue = CommandQueue("1")

        cqueue.add("abc")

        assert cqueue == CommandQueue("1", "abc"), str(cqueue) + " != " + "CommandQueue(['1', 'abc'])"
    
    def test_add_two_equal():
        cqueue = CommandQueue("1")

        cqueue.add("abc")
        cqueue.add("abc")

        assert cqueue == CommandQueue("1", "abc", "abc"), str(cqueue) + " != " + "CommandQueue(['1', 'abc', 'abc'])"
    
    def test_add_two_different():
        cqueue = CommandQueue("1")

        cqueue.add("abc")
        cqueue.add("def")

        assert cqueue == CommandQueue("1", "abc", "def")
    
    def test_combine_empty():
        cqueue = CommandQueue()

        assert cqueue.combine() == ""

    def test_combine_one():
        cqueue = CommandQueue("abc")

        assert cqueue.combine() == "abc"
    
    def test_combine_two_equal():
        cqueue = CommandQueue("abc", "abc")

        assert cqueue.combine() == "abc" + CommandQueue.separator + "abc"
    
    def test_combine_two_different():
        cqueue = CommandQueue("abc", "def")

        assert cqueue.combine() == "abc" + CommandQueue.separator + "def"