import string
import random
import os
from pathlib import Path
from src.typist import Typist
import unittest

class TestTypist(unittest.TestCase):
    
    def setUp(self):
        random.seed(1) 
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
        self.path = Path(''.join(['../users/', self.username, '.pkl']))

    def test_init(self):
        self.assertEqual(self.typist.username, self.username)
        self.assertEqual(self.typist.filename, self.path)
        self.assertEqual(self.chars, self.typist.chars)
        self.assertEqual([0,0], self.typist.char_dict['a'])
        self.assertEqual([], self.typist.rate)

    def test__set_attributes(self):
        dict_correct = {'num_words'  : 5,
                        'word_length': 5,
                        'num_rounds' : 5,
                        'num_worst'  : 5}
        self.assertEqual(dict_correct, self.typist.pref)

    def test_save(self):
        self.typist.save()
        self.assertTrue(os.path.exists(self.path))

    
if __name__ == '__main__':
    unittest.main()
        

