import time
import os
import random
import pdb

def argsort(seq):
    """Argsort using native Python"""
    return [i for i,v in sorted(enumerate(seq), key = lambda x: x[1])]

def flatten_list(nested_lst):
    """Flattens a list of lists into a list"""
    return [lst_item for lst in nested_lst for lst_item in lst]

def make_vocabulary(lst_strings):
    """Makes the characters to type"""
    chars_str = ''.join([elem for elem in lst_strings])
    return [char for char in chars_str]

def login():
    """Gets user name so that progress can be loaded and saved."""
    os.system('cls||clear')
    print(" Welcome to Terminal Typing Practice")
    print(" Please enter your user name.")
    print(" (use alphanumeric values)")
    name = get_alphanumeric_input()
    return name

def get_alphanumeric_input():
    """Returns alphanumeric input from user."""
    entry = '***'
    while not entry.isalnum():
        entry = input(' > ')
        if entry.isalnum():
            return entry
        print(" Not alphanumeric, try again.")

def get_input_from_list(valid_list):
    """Gets user input from provided list"""
    not_in_list = True
    while not_in_list:
        user_input = input(" > ")
        if user_input in valid_list:
            not_in_list = False
        else:
            print(" Sorry, invalid input.")
    return user_input

def get_practice_char_input():
    """Gets individual characters to practice."""
    char_lengths = [2]
    while not all([cl == 1 for cl in char_lengths]):
        entry = input(' > ')
        chars = entry.split(" ")
        char_lengths = list(map(len, chars))
        if all([cl == 1 for cl in char_lengths]):
            return chars
        print(" Incorrect character length. Re-enter line.")

def get_typing_input(user, line):
    """Returns typing input."""
    good_input = False
    while not good_input:
        print("\n Type the following characters:\n\t{0}".format(line))
        start_time = time.time() 
        typed_line = input("\t")
        elapsed_time = time.time() - start_time
        typed_words = typed_line.split(" ")
        num_typed = len(typed_words)
        wl_typed = list(map(len, typed_words))
        correct_wls = all([wl == user.pref['word_length'] for wl in wl_typed])
        good_input = (num_typed == user.pref['num_words'] and correct_wls)
        if good_input:
            return typed_words, elapsed_time
        print(" Incorrect number of words or word length. Re-enter line.")

def number_chars(words):
    """Returns the total number of characters in the list of words"""
    one_word = "".join([word for word in words])
    return len(one_word)

def number_correct_chars(user, typed_words, words):
    """Determine the number of characters typed correctly."""
    number_correct = 0
    for typed_word, word in zip(typed_words, words):
        if len(typed_word) < len(word):
            diff = len(word) - len(typed_word)
            typed_word += ' ' * diff
        for i, letter in enumerate(word): 
            match = typed_word[i] == letter 
            user.update_count(letter, match)
            if match:
                number_correct += 1
    return number_correct

def typing_round(user):
    """Return the number characters typed correctly and how long it took."""
    words = []
    for _ in range(user.pref['num_words']):
        words.append("".join(random.choices(user.chars, 
                                            weights=user.probs, 
                                            k=user.pref['word_length'])))
    line = " ".join([word for word in words])
    typed_words, elapsed_time = get_typing_input(user, line)
    number_correct = number_correct_chars(user, typed_words, words)
    user.update_probs()
    return number_correct, elapsed_time

def show_typing_results(accuracy, chars_per_sec):
    """Displays general typing results."""
    print("\n Results")
    print(" Accuracy: {0:0.2f}%".format(accuracy))
    print(" Correct letters per second: {0:0.2f}".format(chars_per_sec))

def check_if_all_characters_tested(user):
    """Count the number of characters tested by this user so far."""
    num_tested = sum([1 if v[1] > 0 else 0 for v in user.char_dict.values()])
    return num_tested == len(user.chars)


def read_python_code(fname):
    """Reads in Python code and returns a dictionary where key is
       entry number and the value is the python snippet
    """
    path = ''.join(['../data/', fname])
    code_dict = dict()
    with open(path) as f:
        entry_num = 0
        entry_code = []
        num_entry_lines = 0
        line_previous = ''
        for line in f:
            if line == '\n' and line_previous == '\n':
                code_dict[entry_num] = [num_entry_lines, entry_code]
                entry_num += 1  
                num_entry_lines = 0
                entry_code = []
                line_previous = ''
            else:
                num_entry_lines += 1
                entry_code.append(line) 
                line_previous = line
    return code_dict

