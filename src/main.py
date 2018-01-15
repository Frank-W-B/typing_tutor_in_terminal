import string
import random
import os
import helpers
import graphing
from typist import Typist
import pdb

def typing(user):
    """Tests typing on characters accuracy."""
    os.system('cls||clear')
    keep_typing = True
    while keep_typing:
        print("\n Typing")
        print("\n Type these characters as fast as reasonably possible.")
        print(" Do NOT backspace or delete to fix your mistakes.")
        num_correct_in_round = []
        time_for_round = []
        for rnd in range(user.pref['num_rounds']):
            print("\n Round {0} of {1}".format(rnd+1, user.pref['num_rounds']))
            number_correct, elapsed_time = helpers.typing_round(user)
            num_correct_in_round.append(number_correct)
            time_for_round.append(elapsed_time)
        num_correct_chars = sum(num_correct_in_round)
        total_chars = (user.pref['word_length'] * user.pref['num_words'] * 
                       user.pref['num_rounds'])
        accuracy = num_correct_chars / total_chars * 100
        total_time = sum(time_for_round)
        chars_per_sec = num_correct_chars / total_time
        user.rate.append(chars_per_sec)
        user.save()
        helpers.show_typing_results(accuracy, chars_per_sec)
        entry = input("\n Type again? (y/n): ")
        if entry not in ['y', 'Y']:
            keep_typing = False
        os.system('cls||clear')

def typing_python(user, python):
    """Tests typing on Python accuracy."""
    os.system('cls||clear')
    keep_typing = True
    while keep_typing:
        print("\n Typing")
        print("\n Type this Python snippet as fast as reasonably possible.") 
        print(" Do NOT backspace or delete to fix your mistakes.")
        entries = range(max(python))
        num_lines_desired = user.pref['lines_python'] 
        ss_entries = random.sample(entries, 10)
        lines_code = [line.strip('\n') for e in ss_entries for line in python[e][1]]
        lines_code = lines_code[:num_lines_desired]
        code = '\n'.join(["{0:3d} ".format(i) + code for i, code in 
                          enumerate(lines_code, 1)])
        print('\n' + code)
        num_correct_in_round = []
        time_for_round = []
        #for rnd in range(user.pref['num_rounds']):
        #    print("\n Round {0} of {1}".format(rnd+1, user.pref['num_rounds']))
        #    number_correct, elapsed_time = helpers.typing_round(user)
        #    num_correct_in_round.append(number_correct)
        #    time_for_round.append(elapsed_time)
        #num_correct_chars = sum(num_correct_in_round)
        #total_chars = (user.pref['word_length'] * user.pref['num_words'] * 
        #               user.pref['num_rounds'])
        #accuracy = num_correct_chars / total_chars * 100
        #total_time = sum(time_for_round)
        #chars_per_sec = num_correct_chars / total_time
        #user.rate.append(chars_per_sec)
        #user.save()
        #helpers.show_typing_results(accuracy, chars_per_sec)
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
        for _ in range(user.pref['num_rounds']):
            words = []
            for _ in range(user.pref['num_words']):
                words.append("".join(random.choices(chars, 
                                                    k=user.pref['word_length'])))
            line = " ".join([word for word in words])
            typed_words, _  = helpers.get_typing_input(user, line)
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
        print(" 1) Number of rounds: {0}".format(user.pref['num_rounds']))
        print(" 2) Number of words: {0}".format(user.pref['num_words']))
        print(" 3) Word length: {0}".format(user.pref['word_length']))
        print(" 4) Number of worst characters to display & practice: {0}".
              format(user.pref['num_worst']))
        print(" 5) Number of lines of python to type: {0}".
              format(user.pref['lines_python']))
        print(" Valid values are from 1-10 for options 1 through 4.")
        print(" You can type 1-25 lines of Python.")

        print("\n Which preference would like to change?")
        print(" Enter '6' to exit.")
        selection = helpers.get_input_from_list([str(i) for i in range(1,7)])
        valid_vals = [str(i) for i in range(1, 11)]
        valid_python = [str(i) for i in range(1, 26)]
        if selection == '1':
            print(" New value for number of rounds:")
            user.pref['num_rounds'] = int(helpers.get_input_from_list(valid_vals))
        if selection == '2':
            print(" New value for number of words:")
            user.pref['num_words'] = int(helpers.get_input_from_list(valid_vals))
        if selection == '3':
            print(" New value for word length:")
            user.pref['word_length'] = int(helpers.get_input_from_list(valid_vals))
        if selection == '4':
            print(" New value for number of worst characters to display:")
            user.pref['num_worst'] = int(helpers.get_input_from_list(valid_vals))
        if selection == '5':
            print(" New value for lines of Python to type:")
            user.pref['lines_python'] = int(helpers.get_input_from_list(valid_python))
        if selection in ['1', '2', '3', '4', '5']:
            user.save()
        if selection == '6':
            adjust_preferences = False
            os.system('cls||clear')

def menu(user, python):
    """Selection menu""" 
    while True:
        print("\n User: {0}".format(user.username))
        print(" Menu:")
        print(" 1) Type characters")
        print(" 2) Type Python")
        print(" 3) Practice characters")
        print(" 4) Plot performance")
        print(" 5) Change user preferences")
        print(" 6) Change user")
        print(" 7) Quit")
        menu_item = helpers.get_input_from_list([str(i) for i in range(1,8)])
        if menu_item == '1':
            typing(user) 
        if menu_item == '2':
            typing_python(user, python)
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
    main()
