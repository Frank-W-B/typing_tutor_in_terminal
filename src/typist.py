import string
import pickle
from collections import OrderedDict
from pathlib import Path


class Typist(object):
    '''Saves preferences and statistics associated with a typist in the
       typing_in_terminal typing program.
    ''' 
    def __init__(self, username, chars):
        self.username = username
        self.filename = Path(''.join(['../users/', username, '.pkl']))
        self._set_attributes(chars)

    def _set_attributes(self, chars):
        '''if user already exists set their attributes'''
        if self.filename.is_file():
            with open(self.filename, 'rb') as f:
                user = pickle.load(f)
                self.char_dict = user.char_dict
                self.rate = user.rate
                self.pref = user.pref
                self.chars = ''.join([k for k,v in self.char_dict.items()])
                self.probs = user.probs
                print(" {0}'s history has been loaded.".format(self.username))
        else:
            '''for new user initialize values'''
            num_corr = 0  # number times typed corrected
            num_tested = 0 # number of times typed
            prob_char = round(1/len(chars), 3) # probability selection
            char_lst = [(char, [num_corr, num_tested]) for char in chars]
            self.chars = ''.join([char for char in chars])
            self.probs = [prob_char] * len(chars)
            self.char_dict = OrderedDict(char_lst)
            self.rate = []
            self.pref = {'num_words'   : 5,
                         'word_length' : 5,
                         'num_lines'   : 3,
                         'num_worst'   : 5}
            print(" New user created.") 
   
    def update_probs(self):
        '''Updates the probabilities that characters will be selected based 
           on the number of times each character has been typed correctly
           and the total number of times it's been tested.
        '''
        for i, (char, val) in enumerate(self.char_dict.items()):
            num_correct = val[0]
            num_tested = val[1]
            self.probs[i] = ((num_tested + 1) - num_correct) / (num_tested + 1)
        sum_probs = sum(self.probs)
        self.probs = [round(prob / sum_probs, 3) for prob in self.probs]

    def update_count(self, char, bool_correct):
        '''Updates the running count of how many times char has been typed
           correctly and been tested
        '''
        self.char_dict[char][1] += 1
        if bool_correct:
            self.char_dict[char][0] += 1

    def save(self):
        '''pickles the Typist object'''
        with open(self.filename, 'wb') as outfile:
            pickle.dump(self, outfile)
        print('\n Typing history and preferences saved.')        

if __name__ == '__main__':
    username = 'greyfalcon'
    lst_strings = [string.ascii_lowercase,
                   string.digits,
                   string.punctuation]
    chars_str = ''.join([elem for elem in lst_strings])
    chars = [char for char in chars_str]

    User1 = Typist(username, chars)
    User1.save()
    print("User1 created.") 
    User2 = Typist(username, chars)
    print("User2 created.")
    print(User2.probs)
    User2.update_count('a', False)
    User2.update_count('a', False)
    User2.update_count('a', False)
    User2.update_count('b', True)
    User2.update_count('c', False)
    User2.update_probs()
    print(User2.probs)
