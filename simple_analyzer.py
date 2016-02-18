import os
import re
import sys
import collections

class SimpleAnalyzer:
    def __init__(self):
        # rule-based tokens
        self.error_keys_regex = ["(.)*[^a-z]error", r"^e/"]
        self.error_keys       = ["fail",      "crash",     "exception", " kill",  " fault", " die"]
        self.warning_keys     = ["warn",      "bad",       "refuse",    " miss",  " not ",  " no ",   "invalid", "ignore",
                                 "undefined", "unsuccess", "unauthor",  "unable", "skip",   "cannot", "unknown"]
        # with timestamp
        self.error_list = []
        self.warning_list = []
        self.all_data_list = []

        # de-timestamp
        self.formatted_error_list = []
        self.formatted_warning_list = []

    # Clean up lists
    def clean_lists(self):
        self.error_list = []
        self.warning_list = []

    # TODO: need to adjust to JSON format later
    # Return current de-timestamp error log list
    def return_sorted_error(self):
        self.formatted_error_list = [re.sub("^[(0-9)|( :.\\-)]+", "", s) for s in self.error_list]
        error_counter = collections.Counter(self.formatted_error_list)
        return error_counter.keys()

    # Return current de-timestamp warning log list
    def return_sorted_warning(self):
        self.formatted_warning_list = [re.sub("^[(0-9)|( :.\\-)]+", "", s) for s in self.warning_list]
        warning_counter = collections.Counter(self.formatted_warning_list)
        return warning_counter.keys()

    # Return current error log list
    def return_error(self):
        error_counter = collections.Counter(self.error_list)
        # counter / counter.keys() / counter.most_common()
        # print filename + ": error=" + str(len(self.error_list)) + " nondup_error=" + str(len(counter.keys())) + " warning=" + str(len(self.warning_list))
        return error_counter.keys()

    # Return current warning log list
    def return_warning(self):
        warning_counter = collections.Counter(self.warning_list)
        return warning_counter.keys()

    # Return all the log
    def return_list(self):
        return self.all_data_list

    # Parse the whole file and store analyzed log in lists
    def parse_file(self, filename):
        self.error_list = []
        self.warning_list = []

        with open(filename) as f:
            lines = f.readlines()

        for l in lines:
            error = False

            # make the line lowercased
            lowercase_line = l.lower()
            # minize continuous spaces to get consistency
            cleaned_line = re.sub("[ ]+", " ", l).strip()
            # remove (number) before starting of message
            cleaned_line = re.sub("[ ]*\\([ ]*[0-9]+\\):", ":", cleaned_line).strip()

            self.all_data_list.append(cleaned_line)

            for k in self.error_keys:
                if k in lowercase_line:
                    self.error_list.append(cleaned_line)
                    # print "Error:   " + l
                    error = True
                    break
            if error:
                continue

            for k in self.error_keys_regex:
                if re.match(k, lowercase_line):
                    self.error_list.append(cleaned_line)
                    # print "Error:   " + l
                    error = True
                    break
            if error:
                continue

            for k in self.warning_keys:
                if k in lowercase_line:
                    self.warning_list.append(cleaned_line)
                    break

    # Parse the whole file and store analyzed log in lists
    # Return Warning or Error immediately
    # TODO: colored output
    def parse_line(self, line):
        # make the line lowercased
        lowercase_line = line.lower()
        # minize continuous spaces to get consistency
        cleaned_line = re.sub("[ ]+", " ", line).strip()
        # remove (number) before starting of message
        cleaned_line = re.sub("[ ]*\\([ ]*[0-9]+\\):", ":", cleaned_line).strip()

        for k in self.error_keys:
            if k in lowercase_line:
                self.error_list.append(cleaned_line)
                return "Error:   " + line

        for k in self.error_keys_regex:
            if re.match(k, lowercase_line):
                self.error_list.append(cleaned_line)
                return "Error:   " + line

        for k in self.warning_keys:
            if k in lowercase_line:
                self.warning_list.append(cleaned_line)
                return "Warning: " + line

        return ""

# This is a basic function test.
# It will parse through current directory for clean_(.)*.txt and extract data out.
if __name__ == '__main__':
    current_dir = os.getcwd()
    lp = SimpleAnalyzer()
    for filename in os.listdir(current_dir):
        if filename.endswith(".txt") and filename.startswith("cleaned_") and not os.path.isdir(filename):
            lp.parse_file(filename)
            import pdb; pdb.set_trace()
            print lp.return_sorted_error()
