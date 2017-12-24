import string
import random
import os
import helpers
import graphing
from typist import Typist

def typing(user):
    """Tests typing accuracy."""
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
    small = 1e-6 # prevent dividing by zero
    percents = [round(user.char_dict[c][0] / (user.char_dict[c][1] + small),3) 
                * 100 for c in user.char_dict.keys()]
    worst = helpers.argsort(percents)[:user.pref['num_worst']]
    char_per_s_plot = graphing.plot_char_per_s(user) 
    print(char_per_s_plot)
    print("\n")
    accuracy_plot = graphing.plot_graphing_accuracy(user, percents)
    print(accuracy_plot)
    all_tested = helpers.check_if_all_characters_tested(user)
    if not all_tested:
        print("\n You haven't typed all the characters yet.")
        print(" These are the results of the characters you've typed so far.")
    print("\n {0}, your worst {1} characters are:".format(name, 
                                                          user.pref['num_worst']))
    for i in worst:
        print(" {0} {1:4.1f}%".format(user.chars[i], percents[i]))
    entry = input("\n Would you like to practice them? (y/n) ") 
    if entry in ['y', 'Y']:
        practice_chars(user, [chars[i] for i in worst])
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
        print(" Valid values are from 1-10 for each preference.")
        print("\n Which preference would like to change?")
        print(" Enter '5' to exit.")
        selection = helpers.get_input_from_list([str(i) for i in range(1,6)])
        valid_vals = [str(i) for i in range(1,11)]
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
        if selection in ['1', '2', '3', '4']:
            user.save()
        if selection == '5':
            adjust_preferences = False
            os.system('cls||clear')

def menu(user):
    """Selection menu""" 
    while True:
        print("\n User: {0}".format(user.username))
        print(" Menu:")
        print(" 1) Type")
        print(" 2) Practice characters")
        print(" 3) Plot performance")
        print(" 4) Change user preferences")
        print(" 5) Change user")
        print(" 6) Quit")
        menu_item = helpers.get_input_from_list([str(i) for i in range(1,7)])
        if menu_item == '1':
            typing(user) 
        if menu_item == '2':
            practice_chars(user)
        if menu_item == '3':
            plot_performance(user)
        if menu_item == '4':
            change_preferences(user)
        if menu_item == '5':
            return True 
        if menu_item == '6':
            print(" Goodbye.")
            return False

if __name__ == '__main__':
    chars = helpers.make_vocabulary([string.ascii_lowercase,
                                     string.digits,
                                     string.punctuation])
    keep_typing = True
    while keep_typing:
        name = helpers.login()
        user = Typist(name, chars)
        keep_typing = menu(user) 
