def determine_scale(percents):
    """Deterimes the min, max, and step for the graph"""
    p_min = min(percents)
    if p_min < 50: 
        return 0, 100, 10
    elif p_min < 80:
        return 50, 100, 5
    elif p_min < 90:
        return 80, 100, 2
    elif p_min < 95:
        return 90, 100, 1
    else: 
        return 95, 100, 0.5

def scale_label(p_high, p_low, percent):
    val_f = round((p_high + p_low) / 2, 1)
    val_int = int(val_f)
    if percent:
        if val_int == val_f:
            return "{0:4d}% ".format(val_int)
        else:
            return "{0}% ".format(val_f)
    else:
        if val_int == val_f:
            return " {0:4d} ".format(val_int)
        else:
            return " {0} ".format(val_f)

def graph_left_border(i, p_high, p_low, percent=True):
    """Line-by-line string that defines left border of graph"""
    if i == 0:
        left = scale_label(p_high, p_high, percent)
    elif i == 4:
        left = " ____ "
    elif i == 5:
        left = scale_label(p_high, p_low, percent)
    elif i == 9:
        left = " ____ "
    else:
        left = "      "
    return left

def plot_graphing_accuracy(user, percents):
    """Makes the character percentage accuracy graph"""
    print("\n" + " " * 16 + "Percent correctly typed for each character")
    p_low, p_high, p_step = determine_scale(percents)
    t_high = p_high - p_step/2
    t_low = p_low - p_step/2
    thresholds = [t_high - i * p_step for i in range(10)]
    lines_graph = [" ____ "]
    for i, thresh in enumerate(thresholds):
        left = graph_left_border(i, p_high, p_low)
        line = left + "".join(["|" if p >= thresh else " " for p in percents])
        lines_graph.append(line)
    #lines_graph.append("{0:4d}% ".format(p_low) + user.chars)
    lines_graph.append(scale_label(p_low, p_low, True) + user.chars)
    graph = "\n".join(line for line in lines_graph)
    return graph

def plot_char_per_s(user):
    """Plots the correct characters per second"""
    print("\n" + " " * 16 + "   Correct characters typed per second")
    plot_w = 70
    rates = user.rate
    if len(rates) > plot_w:
        over = len(rates) - plot_w
        rates = rates[over:]
    min_cps = min(rates)
    max_cps = max(rates)
    intvl = (max_cps - min_cps) / 9
    min_graph = round(min_cps - intvl / 2, 1)
    max_graph = round(max_cps + intvl / 2, 1)
    bins = [(max_graph - i*intvl, max_graph - (i+1)*intvl) for i in range(10)]
    lines_graph = [" ____ "]
    for i in range(10):
        left = graph_left_border(i, max_graph, min_graph, percent=False)
        line = left + "".join(["*" if (cps <= bins[i][0] and cps > bins[i][1])
                               else " " for cps in rates])
        lines_graph.append(line)
    lines_graph.append(scale_label(min_graph, min_graph, percent=False) +
                       " " * 16 + " Most recent typing results ->") 
    graph = "\n".join(line for line in lines_graph)
    return graph

