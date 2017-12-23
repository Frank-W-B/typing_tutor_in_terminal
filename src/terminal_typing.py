import string
import random
import time
import pickle
import os
from pathlib import Path
import pdb
# this was added on dev branch

def argsort(seq):
    """Argsort using native Python"""
    return [i for i,v in sorted(enumerate(seq), key = lambda x: x[1])]

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

def get_typing_input(num_words, word_len, line):
    """Returns typing input."""
    good_input = False
    while not good_input:
        print("\n Type the following characters:\n\t{0}".format(line))
        start_time = time.time() 
        typed_line = input("\t")
        elapsed_time = time.time() - start_time
        typed_words = typed_line.split(" ")
        num_typed = len(typed_words)
        word_len_typed = list(map(len, typed_words))
        correct_wls = all([wl == word_len for wl in word_len_typed])
        good_input = (num_typed == num_words and correct_wls)
        if good_input:
            return typed_words, elapsed_time
        print(" Incorrect number of words or word length. Re-enter line.")

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

def login():
    """Gets user name so that progress can be loaded and saved."""
    os.system('cls||clear')
    print(" Welcome to Terminal Typing Practice")
    print(" Can I get your name please?")
    print(" (use alphanumeric values)")
    name = get_alphanumeric_input()
    return name
    
def init_chars(user):
    """Makes the list of typing characters."""
    chars_to_type = (string.ascii_lowercase + string.digits 
                         + string.punctuation) 
    char_lst = [char for char in chars_to_type] 
    pickle_name = user + '.pickle'
    filename = Path(pickle_name)
    if filename.is_file():
        with open(filename, 'rb') as f:
            char_dict = pickle.load(f)
            print(" {0}, your typing history has been loaded.".format(user))
    else:
        char_dict = {char: [0,0] for char in char_lst}  # init. correct, tested
        print(" New user created.") 
    return char_lst, char_dict

def calc_prob(right, tested):
    """Calculate a character's probability of being selected based on
    the counts of 1) the times it was tested and 2) typed right.
    """
    return ((tested + 1) - right) / (tested + 1)

def make_probs(char_lst, char_dict):
    "Make character probabilities list.""" 
    raw_probs = [calc_prob(char_dict[c][0], char_dict[c][1]) for c in char_lst] 
    max_prob = max(raw_probs) 
    return [round(prob / max_prob, 2) for prob in raw_probs]

def number_correct_chars(typed_words, words, char_dict):
    """Determine the number of characters typed correctly."""
    number_correct = 0
    for typed_word, word in zip(typed_words, words):
        for i, letter in enumerate(word): 
            char_dict[letter][1] += 1 # increment tested counter
            if typed_word[i] == letter:
                char_dict[letter][0] += 1 # increment number correct counter
                number_correct += 1
    return number_correct

def typing_round(chars, probs, char_dict, num_words, word_length):
    """Return the number characters typed correctly and how long it took."""
    words = []
    for _ in range(num_words):
        words.append("".join(random.choices(chars, weights=probs, k=word_length)))
    line = " ".join([word for word in words])
    typed_words, elapsed_time = get_typing_input(num_words, word_length, line)
    number_correct = number_correct_chars(typed_words, words, char_dict)
    return number_correct, elapsed_time

def show_typing_results(num_correct_in_round, time_for_round, total_chars):
    """Displays general typing results."""
    num_correct_chars = sum(num_correct_in_round) 
    accuracy = num_correct_chars / total_chars * 100
    total_time = sum(time_for_round)
    chars_per_sec = num_correct_chars / total_time
    print("\n Results")
    print(" Accuracy: {0:0.2f}%".format(accuracy))
    print(" Time elapsed: {0:0.1f} seconds.".format(total_time))
    print(" Correct letters per second: {0:0.2f}".format(chars_per_sec))

def typing(chars, probs, char_dict, name, num_rounds=5, word_length=5, num_words=5):
    """Tests typing accuracy."""
    os.system('cls||clear')
    keep_typing = True
    while keep_typing:
        print("\n Typing")
        print("\n Type these characters as fast as reasonably possible.")
        print(" Do NOT backspace or delete to fix your mistakes.")
        num_correct_in_round = []
        time_for_round = []
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

def count_of_characters_tested(char_dict):
    """Count the number of characters tested by this user so far."""
    return sum([1 if v[1] > 0 else 0 for k, v in char_dict.items()])

def determine_scale(percents):
    """Deterimes the min, max, and step for the graph"""
    p_min = min(percents)
    if p_min < 50: 
        return 0, 100, 10
    elif p_min < 80:
        return 50, 100, 5
    elif p_min < 90:
        return 80, 100, 2
    else:
        return 90, 100, 1

def graph_left_border(i, p_high, p_low):
    """Line-by-line string that defines left border of graph"""
    if i == 0:
        left = "{0:4d}% ".format(p_high)
    elif i == 4:
        left = " ____ "
    elif i == 5:
        left = "{0:4d}% ".format(int(round((p_high+p_low)/2,0)))
    elif i == 9:
        left = " ____ "
    else:
        left = "      "
    return left

def make_graph(percents):
    """Makes the character percentage accuracy graph"""
    print("\n" + " " * 16 + "Percent correctly typed for each character")
    p_low, p_high, p_step = determine_scale(percents)
    t_high = int(round(p_high - p_step/2, 0))
    t_low = int(round(p_low - p_step/2, 0))
    thresholds = list(range(t_high, t_low, -p_step))
    lines_graph = [" ____ "]
    for i, thresh in enumerate(thresholds):
        left = graph_left_border(i, p_high, p_low)
        line = left + "".join(["|" if p >= thresh else " " for p in percents])
        lines_graph.append(line)
    lines_graph.append("{0:4d}% ".format(p_low) + "".join(chars))
    graph = "\n".join(line for line in lines_graph)
    return graph

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
    
def menu(chars, probs, char_dict, name):
    """Selection menu""" 
    while True:
        print("\n User: {0}".format(name))
        print(" Menu:")
        print(" 1) Type")
        print(" 2) Practice characters")
        print(" 3) Plot performance")
        print(" 4) Change user")
        print(" 5) Quit")
        menu_item = get_input_from_list([str(i) for i in range(1,6)])
        if menu_item == '1':
            typing(chars, probs, char_dict, name) 
        if menu_item == '2':
            practice_chars()
        if menu_item == '3':
            plot_performance(chars, char_dict, name)
        if menu_item == '4':
            return True 
        if menu_item == '5':
            print(" Goodbye.")
            return False

def save_history(user, char_dict):
    """Saves the dictionary of results for this user."""
    pickle_name = user + '.pickle'
    filename = Path(pickle_name)
    with open(filename, 'wb') as f:
        pickle.dump(char_dict, f)
        print(" Your typing history has been saved, {0}.".format(name))

if __name__ == '__main__':
    keep_typing = True
    while keep_typing:
        name = login()  
        chars, char_dict = init_chars(user=name)    
        probs = make_probs(chars, char_dict)
        keep_typing = menu(chars, probs, char_dict, name) 


