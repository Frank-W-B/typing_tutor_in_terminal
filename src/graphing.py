def determine_scale(values):
    """Determines labels and interval for plot"""
    all_values_same = False
    top = max(values)
    bottom = min(values)
    if top == bottom:
        all_values_same = True
    mid = (top + bottom) / 2
    interval = (top - bottom) / 10
    return (top, mid, bottom), interval, all_values_same

def axis_label(label, type_plot):
    if type_plot == "accuracy":
        return " {0:5.1f}% ".format(label)
    else:
        return "  {0:5.2f} ".format(label)

def graph_left_border(i, labels, type_plot):
    """Line-by-line string that defines left border of graph"""
    if i == 0:
        left = axis_label(labels[0], type_plot)
    elif i == 4 or i == 9:
        left = " ______ "
    elif i == 5:
        left = axis_label(labels[1], type_plot)
    else:
        left = "        "
    return left

def create_plot(user, values, type_plot="accuracy"):
    """Creates plot in terminal of either the user's typing accuracy per
       character (type_plot = 'accuracy') or the user's speed (type_plot
       = cchar_pers) """
    if values:
        labels, interval, all_values_same = determine_scale(values)
        top, mid, bottom = labels
        if all_values_same:
            val = round(values[0], 2)
            if type_plot == "accuracy":
                return "\n The typing accuracy of all characters is {0}%.".format(val)
            else:
                return "\n  The correct char. typing rate is {0} chars. per second.".\
                       format(val)
        lines_graph =  [" ______"]
        for i in range(10):    
            threshold = top - interval/2 - i * interval     
            left = graph_left_border(i, labels, type_plot)
            line = left + "".join(["|" if v >= threshold else " " for v in values])
            lines_graph.append(line)
        last_line = axis_label(bottom, type_plot)
        if type_plot == "accuracy":
            last_line += user.chars
        else:
            last_line += " " * 16 + "<- Most recent typing results" 
        lines_graph.append(last_line)
        graph = "\n".join(line for line in lines_graph)
        return graph
    else:
        return(" No values yet to plot.")
