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

def check_answer(file_path):

    with open(file_path, 'r') as f:
        data = json.load(f)

    output_o_flags = []
    output_e_flags = []
    apo_flags = []

    for i,line in enumerate(data):
        output_o_flags.append(1 if check(line['output'], line['o_answer'], line['o_answer_aliases']) else 0)
        output_e_flags.append(1 if check(line['output'], line['e_answer'], line['e_answer_aliases']) else 0)
        if "apologize" in line['output'] or "sorry" in line['output']:
            output_e_flags[-1] = 0
            apo_flags.append(1)
        else:
            apo_flags.append(0)
        if output_o_flags[-1] == 1:
            output_e_flags[-1] = 0

    return output_o_flags, output_e_flags, apo_flags

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="evaluate step answer")

    parser.add_argument("-file_path_0", default="", required=False, help="")
    parser.add_argument("-file_path_1", default="", required=False, help="")

    parser.add_argument("-check_type", default='e', required=False, help="")

    args = parser.parse_args()

    output_o_results, output_e_results, apo_results = check_answer(args.file_path_0)

    print(f"original len = {len(output_o_results)} edit len = {len(output_e_results)} apo len = {len(apo_results)}")
    print(f"original = {sum(output_o_results) / len(output_o_results)} \nedit = {sum(output_e_results) / len(output_e_results)}\napo = {sum(apo_results) / len(apo_results)}")

    output_o_results, output_e_results, apo_results = check_answer(args.file_path_1)

    print(f"original len = {len(output_o_results)} edit len = {len(output_e_results)} apo len = {len(apo_results)}")
    print(f"original = {sum(output_o_results) / len(output_o_results)} \nedit = {sum(output_e_results) / len(output_e_results)}\napo = {sum(apo_results) / len(apo_results)}")
