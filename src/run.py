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
import pdb
from collections import OrderedDict
# this was added on dev branch

def make_vocabulary(lst_strings):
    """Makes the characters to type"""
    chars_str = ''.join([elem for elem in lst_strings])
    return [char for char in chars_str]

def typing(chars, probs, char_dict, name, num_rounds=5, word_length=5, num_words=5):
    """Tests typing accuracy."""
    num_rounds = user.preferences['num_rounds']
    word_length = user.preferences['word_length']
    num_words = user.preferences['num_words']
    os.system('cls||clear')
    keep_typing = True
    while keep_typing:
        print("\n Typing")
        print("\n Type these characters as fast as reasonably possible.")
        print(" Do NOT backspace or delete to fix your mistakes.")
        num_correct_in_round = []
        time_for_round = []
        # working here! 
        for rnd in range(num_rounds):
            print("\n Round {0} of {1}".format(rnd+1, num_rounds))
            number_correct, elapsed_time = typing_round(chars, probs, char_dict,
                                                        num_words, word_length)
            num_correct_in_round.append(number_correct)
            time_for_round.append(elapsed_time)
            probs = make_probs(chars, char_dict)
        total_chars = word_length * num_words * num_rounds
        show_typing_results(num_correct_in_round, time_for_round, total_chars)
        save_history(name, char_dict)
        entry = input("\n Type again? (y/n): ")
        if entry not in ['y', 'Y']:
            keep_typing = False
        os.system('cls||clear')

def practice_chars(problem_chars=None):
    """Allows user to practice characters of choice."""
    os.system('cls||clear')
    print("\n Practice characters")
    if problem_chars:
        chars = problem_chars
    else:
        print(" Enter characters to practice, separated by a space.")
        chars = get_practice_char_input()
    num_words = 10 
    word_length = 5 
    another_round = True
    while another_round:
        os.system('cls||clear')
        words = []
        for _ in range(num_words):
            words.append("".join(random.choices(chars, k=word_length)))
        line = " ".join([word for word in words])
        typed_words, _  = get_typing_input(num_words, word_length, line)
        entry = input("\n Practice again? (y/n): ")
        if entry not in ['y', 'Y']:
            another_round = False
    os.system('cls||clear')

def plot_performance(chars, char_dict, name, num_worst = 5):
    """Shows the percentage typing accuracy for each character."""
    os.system('cls||clear')
    small = 1e-6 # prevent dividing by zero
    percents = [round(char_dict[c][0] / (char_dict[c][1] + small), 3) * 100
                for c in chars]
    worst = argsort(percents)[:num_worst]
    graph = make_graph(percents)
    print(graph)
    num_tested = count_of_characters_tested(char_dict)
    if num_tested < len(chars):
        print("\n You haven't typed all the characters yet.")
        print(" These are the results of the characters you've typed so far.")
    print("\n {0}, your worst {1} characters are:".format(name, num_worst))
    for i in worst:
        print(" {0} {1:4.1f}%".format(chars[i], percents[i]))
    entry = input("\n Would you like to practice them? (y/n) ") 
    if entry in ['y', 'Y']:
        practice_chars([chars[i] for i in worst])
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
            practice_chars()
        if menu_item == '3':
            plot_performance(user)
        if menu_item == '4':
            return True 
        if menu_item == '5':
            print(" Goodbye.")
            return False

if __name__ == '__main__':
    chars = make_vocabulary([string.ascii_lowercase,
                             string.digits,
                             string.punctuation])
    keep_typing = True
    while keep_typing:
        name = helpers.login()
        user = Typist(name, chars)
        keep_typing = menu(user) 



