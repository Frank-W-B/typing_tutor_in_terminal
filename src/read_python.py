import random
def read_python_code(fname):
    path = ''.join(['../data/', fname])
    code_dict = dict()
    with open(path) as f:
        entry_num = 0
        entry_code = []
        num_entry_lines = 0
        line_previous = ''
        for line in f:
            if line[0] == '#' and line[1] == '#':
                continue
            if line == '\n' and line_previous == '\n':
                code_dict[entry_num] = [num_entry_lines, entry_code]
                entry_num += 1  
                num_entry_lines = 0
                entry_code = []
                line_previous = ''
            else:
                num_entry_lines += 1
                entry_code.append(line) 
                line_previous = line
    return code_dict
                
if __name__ == '__main__':
    num_entries_to_print = 5
    code_dict = read_python_code('itertools_code.py')
    key_min = min(code_dict)
    key_max = max(code_dict)
    entries = range(key_min, key_max)
    chosen_entries = random.sample(entries, num_entries_to_print)
    for i in range(num_entries_to_print):
        code = code_dict[chosen_entries[i]][1]
        for line in code:
            print(line.strip('\n'))
        
