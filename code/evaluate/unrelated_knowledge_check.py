import re
import csv
import json
import argparse

import matplotlib.pyplot as plt

def normalize_answer(output, answers):
    tmp0 = output.split(" ")
    tmp1 = answers.split(" ")
    if len(tmp1) > 1:
        if answers in output:
            return True
        else:
            return False
    else:
        flag = False
        for i,line in enumerate(tmp0):
            if answers == line:
                flag = True
                return flag
            tmp = line.split(".")[0]
            if answers == tmp:
                flag = True
                return flag
            tmp = line.split("'")[0]
            if answers == tmp:
                flag = True
                return flag
    
    return flag

def check(output, answers, aliases):
    if normalize_answer(output=output, answers=answers):
        return True
    
    for line in aliases:
        if normalize_answer(output=output, answers=line):
            return True
    
    return False

def check_answer(args):
    file_path_first = args.file_path_first
    file_path_old = args.file_path_old 
    file_path_new = args.file_path_new 

    with open(file_path_first, 'r') as f:
        first_data = json.load(f)

    with open(file_path_old, 'r') as f:
        data_old = json.load(f)

    with open(file_path_new, 'r') as f:
        data_new = json.load(f)

    output_o_flags = []
    output_e_flags = []

    output_old_o_flags = []
    output_old_e_flags = []

    output_new_o_flags = []
    output_new_e_flags = []

    #apo_flags = []

    for i,line in enumerate(first_data):
        output_o_flags.append(1 if check(line['output'], line['old_first_answer'], line['old_first_answer_aliases']) else 0)
        output_e_flags.append(1 if check(line['output'], line['new_first_answer'], line['new_first_answer_aliases']) else 0)

        output_old_o_flags.append(1 if check(data_old[i]['output'], data_old[i]['old_second_answer'], data_old[i]['old_second_answer_aliases']) else 0)
        output_old_e_flags.append(1 if check(data_old[i]['output'], data_old[i]['new_second_answer'], data_old[i]['new_second_answer_aliases']) else 0)

        output_new_o_flags.append(1 if check(data_new[i]['output'], data_new[i]['old_second_answer'], data_new[i]['old_second_answer_aliases']) else 0)
        output_new_e_flags.append(1 if check(data_new[i]['output'], data_new[i]['new_second_answer'], data_new[i]['new_second_answer_aliases']) else 0)

    return output_o_flags, output_e_flags, output_old_o_flags, output_old_e_flags, output_new_o_flags, output_new_e_flags

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="evaluate step answer")

    parser.add_argument("-file_path_first", default="", required=False, help="")
    parser.add_argument("-file_path_old",   default="", required=False, help="")
    parser.add_argument("-file_path_new",   default="", required=False, help="")

    args = parser.parse_args()

    output_o_flags, output_e_flags, output_old_o_flags, output_old_e_flags, output_new_o_flags, output_new_e_flags = check_answer(args)

    print(f"len o = {len(output_o_flags)} len e = {len(output_e_flags)}")
    print(f"o = {sum(output_o_flags)/len(output_o_flags)} e = {sum(output_e_flags)/len(output_e_flags)}")
    print(f"old second o = {sum(output_old_o_flags)/len(output_old_o_flags)} old second e = {sum(output_old_e_flags)/len(output_old_e_flags)}")
    print(f"new second o = {sum(output_new_o_flags)/len(output_new_o_flags)} new second e = {sum(output_new_e_flags)/len(output_new_e_flags)}")

    o_1_2 = []
    e_1_2 = []

    for i in range(len(output_e_flags)):
        if output_o_flags[i] == 1 and output_old_o_flags[i] == 1:
            o_1_2.append(1)
        else:
            o_1_2.append(0)

    for i in range(len(output_e_flags)):
        if output_e_flags[i] == 1 and output_new_e_flags[i] == 1:
            e_1_2.append(1)
        else:
            e_1_2.append(0)
    
    print(f"two old = {sum(o_1_2)/len(o_1_2)} two new = {sum(e_1_2)/len(e_1_2)}")