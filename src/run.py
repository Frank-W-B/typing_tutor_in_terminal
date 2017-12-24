import string
import random
import time
import pickle
import os
import sys
from pathlib import Path
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
    another_round = True
    while another_round:
        os.system('cls||clear')
        words = []
        for _ in range(user.pref['num_words']):
            words.append("".join(random.choices(chars, 
                                                k=user.pref['word_length'])))
        line = " ".join([word for word in words])
        typed_words, _  = helpers.get_typing_input(user, line)
        entry = input("\n Practice again? (y/n): ")
        if entry not in ['y', 'Y']:
            another_round = False
    os.system('cls||clear')

def plot_performance(user):
    """Shows the percentage typing accuracy for each character."""
    os.system('cls||clear')
    small = 1e-6 # prevent dividing by zero
    percents = [round(user.char_dict[c][0] / (user.char_dict[c][1] + small),3) 
                * 100 for c in user.char_dict.keys()]
    worst = helpers.argsort(percents)[:user.pref['num_worst']]
    graph = graphing.make_graph(user, percents)
    print(graph)
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
    
def menu(user):
    """Selection menu""" 
    while True:
        print("\n User: {0}".format(user.username))
        print(" Menu:")
        print(" 1) Type")
        print(" 2) Practice characters")
        print(" 3) Plot performance")
        print(" 4) Change user")
        print(" 5) Quit")
        menu_item = helpers.get_input_from_list([str(i) for i in range(1,6)])
        if menu_item == '1':
            typing(user) 
        if menu_item == '2':
            practice_chars(user)
        if menu_item == '3':
            plot_performance(user)
        if menu_item == '4':
            return True 
        if menu_item == '5':
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
