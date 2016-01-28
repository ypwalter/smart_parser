# Just put the logcat files (ending in .txt) on the same folder
# This program will filter files and output clean_(original name).txt

import os
import re
import md5
import sys

# remove all empty files
def remove_empties(dir, subname):
    target_size = 0
    for dirpath, dirs, files in os.walk(dir):
        for file in files: 
            if not file.endswith(subname):
                continue

            path = os.path.join(dirpath, file)
            if os.stat(path).st_size == target_size:
                os.remove(path)
                print "Empty File: " + path + " removed."

# remove duplicate files
def remove_duplicates(dir, subname):
    unique = []
    for filename in os.listdir(dir):
        if not filename.endswith(subname):
            continue
        if os.path.isdir(filename):
            continue
        if os.path.isfile(filename):
            filehash = md5.md5(file(filename).read()).hexdigest()
        if filehash not in unique: 
            unique.append(filehash)
        else: 
            os.remove(filename)
            print "Duplicated File: " + filename + " removed."

# remore logcat time stamps, spaces, and unnecessary stuffs
def remove_format(dir, subname):
    for filename in os.listdir(dir):
        if not filename.endswith(subname) or filename.startswith("cleaned_"):
            continue
        with open(filename) as f:
            lines = f.readlines()

        newlines = []
        for l in lines:
            # NOT taking out timestamp for now
            # take out digits(time stamp) in the beginning of each line
            # temp = re.sub("^[(0-9)|( :.\\-)]+", "", l).strip()
            # minize continuous spaces to get consistency
            temp = re.sub("[ ]+", " ", l).strip()
            # remove (number) before starting of message
            temp = re.sub("[ ]*\\([ ]*[0-9]+\\):", ":", temp).strip()
            newlines.append(temp)

        with open('cleaned_' + filename, 'w') as f:
            f.write("\n".join(newlines))

if __name__ == '__main__':
    current_dir = os.getcwd()
    subname = ".txt"
    remove_empties(current_dir, subname)
    remove_duplicates(current_dir, subname)
    remove_format(current_dir, subname)
