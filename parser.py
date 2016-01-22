import os
import sys
import collections

error_keys   = ["error", "fail", "crash", "exception", "kill", "fault", r"^E/", " die"]
warning_keys = ["warn", "bad", "refuse", " miss", " not ", 
                " no ", "invalid", "ignore", "undefined", "unsuccess",
                "unauthor", "unable", "skip", "cannot", "unknown"]

def parse_data(filename):
    error_list = []
    warning_list = []

    with open(filename) as f:
        lines = f.readlines()

    for l in lines:
        error = False
        lowercase_line = l.lower()
        for k in error_keys:
            if k in lowercase_line:
                error_list.append(l)
                error = True
        if error:
            continue

        for k in warning_keys:
            if k in lowercase_line:
                warning_list.append(l)

    error_counter = collections.Counter(error_list)
    waiting_counter = collections.Counter(waiting_list)
    # counter / counter.keys() / counter.most_common()

    print filename + ": error=" + str(len(error_list)) + " nondup_error=" + str(len(counter.keys())) + " warning=" + str(len(warning_list))

    return error_counter.keys()

if __name__ == '__main__':
    current_dir = os.getcwd()
    for filename in os.listdir(current_dir):
        if filename.endswith(".txt") and filename.startswith("cleaned_") and not os.path.isdir(filename):
            parse_data(filename)
