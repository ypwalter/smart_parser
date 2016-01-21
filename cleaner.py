import os
import md5
import sys

# remove all empty files
def remove_empties(dir):
    target_size = 0
    for dirpath, dirs, files in os.walk(dir):
        for file in files: 
            path = os.path.join(dirpath, file)
            if os.stat(path).st_size == target_size:
                os.remove(path)
                print "Empty File: " + path + " removed."

# remove duplicate files
def remove_duplicates(dir):
    unique = []
    for filename in os.listdir(dir):
        if os.path.isdir(filename):
            continue
        if os.path.isfile(filename):
            filehash = md5.md5(file(filename).read()).hexdigest()
        if filehash not in unique: 
            unique.append(filehash)
        else: 
            os.remove(filename)
            print "Duplicated File: " + filename + " removed."

if __name__ == '__main__':
    remove_empties(os.getcwd())
    remove_duplicates(os.getcwd())
