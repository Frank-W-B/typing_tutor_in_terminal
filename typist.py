import string
import pickle
from pathlib import Path


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
                self.char_dict = User.char_dict
                print(" {0}'s typing history has been loaded.".format(username))
        else:
            '''initialize number correct, tested for a new typist'''
            chars_to_type = (string.ascii_lowercase + string.digits 
                             +  string.punctuation) 
            char_lst = [char for char in chars_to_type] 
            return {char: [0,0] for char in char_lst}  
            print(" New user created.") 

    def save(self, obj):
        '''pickles the Typist object'''
        self.char_dict['a'][1] += 1
        with open(self.filename, 'wb') as outfile:
            pickle.dump(obj, outfile)
        


if __name__ == '__main__':
    username = 'greyfalcon'
    #pdb.set_trace()
    User = Typist(username)
    char_dict = '\n'.join(['{0}, {1}'.format(k, v) for k, v in list(User.char_dict.items()[:10]))
    print("After created") 
    print(char_dict)
    User.save(User)
    User2 = Typist(username)
    char_dict2 = '\n'.join(['{0}, {1}'.format(k, v) for k, v in User2.char_dict.items()])
    print("\nAfter loaded")
    print(char_dict2)

