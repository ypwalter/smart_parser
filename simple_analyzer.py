import os
import re
import sys
import collections

class SimpleAnalyzer:
    def __init__(self):
        self.error_keys_regex = ["(.)*[^a-z]error", r"^e/"]
        self.error_keys       = ["fail",      "crash",     "exception", " kill",  " fault", " die"]
        self.warning_keys     = ["warn",      "bad",       "refuse",    " miss",  " not ",  " no ",   "invalid", "ignore",
                                 "undefined", "unsuccess", "unauthor",  "unable", "skip",   "cannot", "unknown"]
        self.error_list = []
        self.warning_list = []

    def return_error(self):
        error_counter = collections.Counter(self.error_list)
        # counter / counter.keys() / counter.most_common()
        # print filename + ": error=" + str(len(self.error_list)) + " nondup_error=" + str(len(counter.keys())) + " warning=" + str(len(self.warning_list))

        return error_counter.keys()

    def return_warning(self):
        warning_counter = collections.Counter(self.warning_list)

        return warning_counter.keys()

    def parse_file(self, filename):
        self.error_list = []
        self.warning_list = []

        with open(filename) as f:
            lines = f.readlines()

        for l in lines:
            error = False

            lowercase_line = l.lower()
            for k in self.error_keys:
                if k in lowercase_line:
                    self.error_list.append(l)
                    print "Error: " + l
                    error = True
                    break
            if error:
                continue

            for k in self.error_keys_regex:
                if re.match(k, lowercase_line):
                    self.error_list.append(lowercase_line)
                    print "Error: " + lowercase_line
                    error = True
                    break
            if error:
                continue

            for k in self.warning_keys:
                if k in lowercase_line:
                    self.warning_list.append(l)
                    break

    def parse_line(self, line):
        lowercase_line = line.lower()
        for k in self.error_keys:
            if k in lowercase_line:
                self.error_list.append(line)
                return 99

        for k in self.warning_keys:
            if k in lowercase_line:
                self.warning_list.append(line)
                return 1

        return 0

if __name__ == '__main__':
    current_dir = os.getcwd()
    lp = SimpleAnalyzer()
    for filename in os.listdir(current_dir):
        if filename.endswith(".txt") and filename.startswith("cleaned_") and not os.path.isdir(filename):
            lp.parse_file(filename)
            print lp.return_error()
