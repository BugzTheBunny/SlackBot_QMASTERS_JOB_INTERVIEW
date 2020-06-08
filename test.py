import unittest
import requests


class TestNewTweet(unittest.TestCase):

    def test_new(self):
        post = 'Python Tweet!'
        requests.post('http://127.0.0.1:5000/tweet', post)




if __name__ == '__main__':
    unittest.main()