import string
import random
import os
import helpers
import graphing
from typist import Typist
import pdb
import time
import subprocess

def make_lines_to_type(user, python_text, option):
    """Depending on option, makes the lines to type.  Options are chars for
       characters and python for python code. Returns a list of the lines to
       type and a terminal printable string for what needs to be typed.
    """
    if option == "python":
        entries = range(max(python_text))
        ss_entries = random.sample(entries, 10)
        code_lines = [line.strip('\n') for entry in ss_entries for line 
                      in python_text[entry][1]]
        lines_onestr = code_lines[:user.pref['num_lines']]
    else:
        lines_onestr = []
        for _ in range(user.pref['num_lines']):
            words = []
            for _ in range(user.pref['num_words']):
                words.append("".join(random.choices(user.chars, 
                                                weights=user.probs, 
                                                k=user.pref['word_length'])))
            line_onestr = " ".join([word for word in words])
            lines_onestr.append(line_onestr)
    lines = [line.lstrip().split(' ') for line in lines_onestr]
    lines_str = '\n'.join(["{0:3d} ".format(i) + code for i, code in 
                            enumerate(lines_onestr, 1)])
    return lines, lines_str

def flatten_lines_into_words(lines):
    """Flattens a list of text lines into words."""
    return [word.lower().lstrip() for words in lines for word in words]

def typing(user, python_text, option):
    """Tests typing on characters accuracy."""
    os.system('cls||clear')
    keep_typing = True
    while keep_typing:
        print("\n Typing")
        print("\n Type these lines as fast as reasonably possible.")
        print(" Do NOT backspace or delete to fix your mistakes.")
        lines, lines_str = make_lines_to_type(user, python_text, option)
        print('\n' + lines_str)
        print("\n Type the lines below:\n")
        lines_typed = []
        start_time = time.time() 
        for line in range(1, user.pref['num_lines']+1):
            raw_inp = input("{0:3d} ".format(line))
            words_input = raw_inp.lower().lstrip().split(' ') 
            lines_typed.append(words_input)
        elapsed_time = time.time() - start_time
        words_typed = flatten_lines_into_words(lines_typed)
        words_correct = flatten_lines_into_words(lines)
        num_correct = helpers.number_correct_chars(user, words_typed, 
                                                  words_correct)
        num_chars = helpers.number_chars(words_correct)
        accuracy = num_correct / num_chars * 100
        chars_per_sec = num_correct / elapsed_time
        user.rate.append(chars_per_sec)
        user.save()
        helpers.show_typing_results(accuracy, chars_per_sec)
        entry = input("\n Type again? (y/n): ")
        if entry not in ['y', 'Y']:
            keep_typing = False
        os.system('cls||clear')


def practice_chars(user, problem_chars=None):
    """Allows user to practice characters of choice."""
    os.system('cls||clear')
    print("\n Practice characters")
    if problem_chars:
        chars = problem_chars
    else:
        print(" Enter characters to practice, separated by a space.")
        chars = helpers.get_practice_char_input()
    practice = True
    while practice:
        os.system('cls||clear')
        print("Type the following characters.")
        for _ in range(user.pref['num_lines']):
            words = []
            for _ in range(user.pref['num_words']):
                words.append("".join(random.choices(chars, 
                                                    k=user.pref['word_length'])))
            line = " ".join([word for word in words])
            print("\n   {0}".format(line))
            line_practice = input(" > ")
        entry = input("\n Practice again? (y/n): ")
        if entry not in ['y', 'Y']:
            practice = False
    os.system('cls||clear')

def plot_performance(user):
    """Shows the percentage typing accuracy for each character."""
    os.system('cls||clear')
    print(" {0}'s performance".format(user.username))
    print("\n" + " " * 16 + "   Correct characters typed per second")
    values = user.rate[::-1][:68]  # correct characters per second
    plot = graphing.create_plot(user, values, type_plot="cchar_pers")
    print(plot)
    print("\n" + " " * 16 + "Percent correctly typed for each character")
    small = 1e-6
    values = [user.char_dict[c][0] / (user.char_dict[c][1] + small) * 100 
              for c in user.char_dict.keys()]
    worst = helpers.argsort(values)[:user.pref['num_worst']]
    plot = graphing.create_plot(user, values, type_plot="accuracy")
    print(plot)
    all_tested = helpers.check_if_all_characters_tested(user)
    if not all_tested:
        print("\n You haven't typed all the characters yet.")
        print(" These are the results of the characters you've typed so far.")
    print("\n {0}, your worst {1} characters are:".format(user.username, 
                                                          user.pref['num_worst']))
    print(" ".join([" {0}: {1:4.1f}% ".format(user.chars[i], values[i])
          for i in worst]))
    entry = input("\n Would you like to practice them? (y/n) ") 
    if entry in ['y', 'Y']:
        practice_chars(user, [user.chars[i] for i in worst])
    os.system('cls||clear')

def change_preferences(user):
    """Allow a user to change individual preferences"""
    adjust_preferences = True
    while adjust_preferences:
        os.system('cls||clear')
        print("\n {0}'s preferences".format(user.username))
        print(" Per typing session:")
        print(" 1) Number of words: {0}".format(user.pref['num_words']))
        print(" 2) Word length: {0}".format(user.pref['word_length']))
        print(" 3) Number of worst characters to display & practice: {0}".
              format(user.pref['num_worst']))
        print(" 4) Number of lines: {0}".format(user.pref['num_lines']))
        print(" Valid values are from 1-10 for options 1 through 3.")
        print(" You can type 1-25 lines.")
        print("\n Which preference would like to change? (1-4)")
        print(" Enter 5 to exit.")
        selection = helpers.get_input_from_list([str(i) for i in range(1,6)])
        valid_vals = [str(i) for i in range(1, 11)]
        valid_lines = [str(i) for i in range(1, 26)]
        if selection == '1':
            print(" New value for number of words:")
            user.pref['num_words'] = int(helpers.get_input_from_list(valid_vals))
        if selection == '2':
            print(" New value for word length:")
            user.pref['word_length'] = int(helpers.get_input_from_list(valid_vals))
        if selection == '3':
            print(" New value for number of worst characters to display:")
            user.pref['num_worst'] = int(helpers.get_input_from_list(valid_vals))
        if selection == '4':
            print(" New value for number of lines:")
            user.pref['num_lines'] = int(helpers.get_input_from_list(valid_lines))
        if selection in ['1', '2', '3', '4']:
            user.save()
        else: 
            adjust_preferences = False
            os.system('cls||clear')

def menu(user, python):
    """Selection menu""" 
    while True:
        print("\n User: {0}".format(user.username))
        print(" Menu:")
        print(" 1) Type Python")
        print(" 2) Type characters")
        print(" 3) Practice characters")
        print(" 4) Plot performance")
        print(" 5) Change user preferences")
        print(" 6) Change user")
        print(" 7) Quit")
        menu_item = helpers.get_input_from_list([str(i) for i in range(1,8)])
        if menu_item == '1':
            typing(user, python, "python")
        if menu_item == '2':
            typing(user, python, "chars")
        if menu_item == '3':
            practice_chars(user)
        if menu_item == '4':
            plot_performance(user)
        if menu_item == '5':
            change_preferences(user)
        if menu_item == '6':
            return True 
        if menu_item == '7':
            print(" Goodbye.")
            return False

def main():
    """ The main execution block """
    chars = helpers.make_vocabulary([string.ascii_lowercase,
                                     string.digits,
                                     string.punctuation])
    python = helpers.read_python_code('itertools_code.py') 
    keep_typing = True
    while keep_typing:
        name = helpers.login()
        user = Typist(name, chars)
        keep_typing = menu(user, python) 

if __name__ == '__main__':
    subprocess.call(["tabs", "-4"]) 
    main()
