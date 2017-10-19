import string
import random
import time
import pickle
import os
from pathlib import Path

def get_alphanumeric_input():
    """Returns alphanumeric input from user."""
    entry = '***'
    while not entry.isalnum():
        entry = input('> ')
        if entry.isalnum():
            return entry
        print("Not alphanumeric, try again.")

def get_menu_input():
    """Gets user selected menu item."""
    valid_options = ['1', '2', '3', '4'] 
    menu_item = '5' 
    while menu_item not in valid_options:
        menu_item = input("> ")
        if menu_item in valid_options:
            return menu_item
        print("Sorry, enter a value of 1, 2, 3, or 4.")

def get_typing_input(num_words, word_len, line):
    """Returns typing input."""
    good_input = False
    while not good_input:
        print("\nType the following characters:\n\t{0}".format(line))
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
        print("Incorrect number of words or word length. Re-enter line.")

def get_practice_char_input():
    """Gets individual characters to practice."""
    char_lengths = [2]
    while not all([cl == 1 for cl in char_lengths]):
        entry = input('> ')
        chars = entry.split(" ")
        char_lengths = list(map(len, chars))
        if all([cl == 1 for cl in char_lengths]):
            return chars
        print("Incorrect character length. Re-enter line.")

def login():
    """Gets user name so that progress can be loaded and saved."""
    os.system('cls||clear')
    print("Welcome to Terminal Typing Practice")
    print("Can I get your name please?")
    print("(use alphanumeric values)")
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
            print("Your typing history has been loaded.")
    else:
        char_dict = {char: [0,0] for char in char_lst}  # init. correct, tested
        print("New user created.") 
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
    print("\nResults")
    print("Accuracy: {0:0.2f}%".format(accuracy))
    print("Time elapsed: {0:0.1f} seconds.".format(total_time))
    print("Correct letters per second: {0:0.2f}".format(chars_per_sec))

def general_typing(chars, probs, char_dict, name, 
                   num_rounds=3, word_length=5, num_words=5):
    """Tests typing accuracy."""
    os.system('cls||clear')
    print("\nGeneral typing")
    print("\nType these characters as fast as reasonably possible.")
    print("Do NOT backspace or delete to fix your mistakes.")
    num_correct_in_round = []
    time_for_round = []
    for rnd in range(num_rounds):
        print("\nRound {0} of {1}".format(rnd+1, num_rounds))
        number_correct, elapsed_time = typing_round(chars, probs, char_dict,
                                                    num_words, word_length)
        num_correct_in_round.append(number_correct)
        time_for_round.append(elapsed_time)
        probs = make_probs(chars, char_dict)
    
    total_chars = word_length * num_words * num_rounds
    show_typing_results(num_correct_in_round, time_for_round, total_chars)
    save_history(name, char_dict)
    input("Press enter to return to the Menu. ") 
    os.system('cls||clear')

def practice_problem_chars():
    """Allows user to practice characters of choice."""
    os.system('cls||clear')
    print("\nPractice problematic characters.")
    print("Enter characters to practice, separated by a space.")
    chars = get_practice_char_input()
    num_words = 10 
    word_length = 5 
    another_round = True
    while another_round:
        words = []
        for _ in range(num_words):
            words.append("".join(random.choices(chars, k=word_length)))
        line = " ".join([word for word in words])
        typed_words, _  = get_typing_input(num_words, word_length, line)
        entry = input("\nPractice again? (y/n): ")
        if entry not in ['y', 'Y']:
            another_round = False
    os.system('cls||clear')

def graph_history(chars, char_dict):
    """Shows the percentage typing accuracy for each character."""
    os.system('cls||clear')
    small = 1e-6 # prevent dividing by zero
    print("\n" + " " * 15 + "Percent correctly typed for each character")
    percents = [round(char_dict[c][0] / (char_dict[c][1] + small), 2) * 100
                for c in chars]
    thresholds = list(range(95, -5, -10))
    lines_graph = ["____"]
    for thresh in thresholds:
        left = "    "
        if thresh == 95:
            left = "100%"
        if thresh == 55:
            left = "____"
        if thresh == 45:
            left = " 50%"
        line = left + "".join(["|" if p >= thresh else " " for p in percents])
        lines_graph.append(line)
    lines_graph.append(left + "".join(chars))
    for line in lines_graph:
        print(line)
    input("\nPress enter to return to the Menu. ") 
    os.system('cls||clear')
    
def menu(chars, probs, char_dict, name):
    continue_typing = True 
    while continue_typing:
        print("\nMenu:")
        print("1) General typing")
        print("2) Practice problematic characters")
        print("3) Graph historical typing accuracy")
        print("4) Quit")
        menu_item = get_menu_input()
        if menu_item == '1':
            general_typing(chars, probs, char_dict, name) 
        if menu_item == '2':
            practice_problem_chars()
        if menu_item == '3':
            graph_history(chars, char_dict)
        if menu_item == '4':
            continue_typing = False
            print("Goodbye.")

def save_history(user, char_dict):
    """Saves the dictionary of results for this user."""
    pickle_name = user + '.pickle'
    filename = Path(pickle_name)
    with open(filename, 'wb') as f:
        pickle.dump(char_dict, f)
        print("Your typing history has been saved.")


if __name__ == '__main__':
    name = login()  
    chars, char_dict = init_chars(user=name)    
    probs = make_probs(chars, char_dict)
    menu(chars, probs, char_dict, name) 
    


