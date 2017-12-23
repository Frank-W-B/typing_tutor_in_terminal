import string
import pickle
from pathlib import Path
import pdb


class Typist(object):
    '''Saves preferences and statistics associated with a typist in the
       typing_in_terminal typing program.
    ''' 
    def __init__(self, username):
        self.username = username
        self.filename = Path(''.join([username, '.pkl']))
        self._set_attributes()

    def _set_attributes(self):
        '''if user already exists set their attributes'''
        if self.filename.is_file():
            with open(self.filename, 'rb') as f:
                User = pickle.load(f)
                self.char_dict = User.char_dict
                self.rate = User.rate
                self.preferences = User.preferences
                print(" {0}'s history has been loaded.".format(username))
        else:
            '''for new user set defaults'''
            chars_to_type = (string.ascii_lowercase + string.digits 
                             +  string.punctuation) 
            char_lst = [char for char in chars_to_type] 
            self.char_dict = {char: [0,0] for char in char_lst}
            self.rate = []
            self.preferences = {'num_words'  : 5,
                                'word_length': 5,
                                'num_rounds' : 5,
                                'num_worst'  : 5}
            print(" New user created.") 
    
    def save(self):
        '''pickles the Typist object'''
        with open(self.filename, 'wb') as outfile:
            pickle.dump(self, outfile)
        

if __name__ == '__main__':
    username = 'greyfalcon'
    User1 = Typist(username)
    User1.save()
    print("User1 created.") 
    User2 = Typist(username)
    User2.save()
    print("User2 created.") 
