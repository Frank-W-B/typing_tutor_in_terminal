import string
import pickle
from pathlib import Path



def Typist(object):
    '''Saves preferences and statistics associated with a typist in the
       typing_in_terminal typing program.
    ''' 
    def __init__(self, username):
        self.username = username
        self.filename = Path(''.join([username, '.pkl'])
        self.char_dict = _get_char_dict()
        #self.rate = _get_rate()
        #self.preferences = _get_preferences()


    def _get_char_dict(self):
        # if user already exists load their number correct, tested dict
        if self.filename.is_file():
            with open(self.filename, 'rb') as f:
                User = pickle.load(f)
                self.char_dict = User.char_dict
                print(" {0}'s typing history has been loaded.".format(username))
        else:
            # initialize number correct, tested for a new typist
            chars_to_type = (string.ascii_lowercase + string.digits 
                             +  string.punctuation) 
            char_lst = [char for char in chars_to_type] 
            self.char_dict= {char: [0,0] for char in char_lst}  
            print(" New user created.") 


    
