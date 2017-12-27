import string
import random
from pathlib import Path
from src.typist import Typist
import unittest

class TestTypist(unittest.TestCase):
    
    def setUp(self):
        new_str = "".join(random.choices(string.ascii_lowercase, k=5))
        username = "test_" + new_str
        lst_strings = [string.ascii_lowercase,
                       string.digits,
                       string.punctuation]
        chars_str = ''.join([elem for elem in lst_strings])
        self.chars = string.ascii_lowercase + string.digits + string.punctuation
        chars = [char for char in chars_str]
        self.username = username
        self.typist = Typist(username, chars)

    def test_init(self):
        self.assertEqual(self.typist.username, self.username)
        pth = Path(''.join([self.username, '.pkl']))
        self.assertEqual(self.typist.filename, pth)
        self.assertEqual(self.chars, self.typist.chars)
        self.assertEqual([0,0], self.typist.char_dict['a'])
        self.assertEqual([], self.typist.rate)



if __name__ == '__main__':
    unittest.main()
        

