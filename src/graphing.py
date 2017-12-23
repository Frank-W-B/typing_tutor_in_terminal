import string
import random
import time
import pickle
import os
from pathlib import Path
import pdb
# this was added on dev branch

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




