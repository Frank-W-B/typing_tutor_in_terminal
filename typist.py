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
        self.char_dict = self._get_char_dict()
        #self.rate = _get_rate()
        #self.preferences = _get_preferences()


    def _get_char_dict(self):
        '''if user already exists load their number correct, tested dict'''
        if self.filename.is_file():
            with open(self.filename, 'rb') as f:
                User = pickle.load(f)
                print(" {0}'s typing history has been loaded.".format(username))
                return User.char_dict
        else:
            '''initialize number correct, tested for a new typist'''
            chars_to_type = (string.ascii_lowercase + string.digits 
                             +  string.punctuation) 
            char_lst = [char for char in chars_to_type] 
            print(" New user created.") 
            return {char: [0,0] for char in char_lst}  

    def save(self):
        '''pickles the Typist object'''
        self.char_dict['a'][1] += 1
        with open(self.filename, 'wb') as outfile:
            pickle.dump(self, outfile)
        


if __name__ == '__main__':
    username = 'greyfalcon'
    User = Typist(username)
    char_dict = '\n'.join(['{0} {1}'.format(k, v) for k, v in User.char_dict.items()])
    print("After created") 
    print(char_dict)
    User.save()
    User2 = Typist(username)
    char_dict2 = '\n'.join(['{0} {1}'.format(k, v) for k, v in User2.char_dict.items()])
    print("\nAfter loaded")
    print(char_dict2)

