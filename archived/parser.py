import os
import re
import sys
import collections

class LogParser:
    def __init__(self):
        self.error_keys   = ["error", "fail", "crash", "exception", "kill", "fault", r"^E/", " die"]
        self.warning_keys = ["warn", "bad", "refuse", " miss", " not ", " no ", "invalid", "ignore",
                             "undefined", "unsuccess", "unauthor", "unable", "skip", "cannot", "unknown"]
        self.error_list = []
        self.warning_list = []
        self.prioritized_list = []

    #TODO: Prioritize from database using current filtered list
    def prioritize_from_list(self, list_to_do):
        return []

    #TODO: Prioritize from database
    def prioritize_from_file(self, file_to_do):
        return []
    
    def return_simple_error(self):
        error_counter = collections.Counter(self.error_list)
        # counter / counter.keys() / counter.most_common()
        # print filename + ": error=" + str(len(self.error_list)) + " nondup_error=" + str(len(counter.keys())) + " warning=" + str(len(self.warning_list))

        return error_counter.keys()

    def return_simple_warning(self):
        warning_counter = collections.Counter(self.warning_list)

        return warning_counter.keys()

    def return_prioritized_erro(self):
        return self.prioritized_list()

    def simple_parse(self, filename):
        with open(filename) as f:
            lines = f.readlines()

        for l in lines:
            error = False
            lowercase_line = l.lower()
            for k in self.error_keys:
                if k in lowercase_line:
                    self.error_list.append(l)
                    error = True
            if error:
                continue

            for k in self.warning_keys:
                if k in lowercase_line:
                    self.warning_list.append(l)

    def precise_parse(self, filename):
        self.simple_parse_data(filename)

        #TODO: send simple filtered data to database, analyze, and send back prioritized list
        self.prioritized_list = self.prioritize_from_list(self.error_list) + self.prioritize_from_list(self.warning_list)

    def auto_parse(self, filename):
        #TODO: send all data to database, analyze, and send back prioritized list
        self.prioritized_list = self.prioritize_from_file(filename)

 if __name__ == '__main__':
    current_dir = os.getcwd()
    lp = LogParser()
    for filename in os.listdir(current_dir):
        if filename.endswith(".txt") and filename.startswith("cleaned_") and not os.path.isdir(filename):
            lp.simple_parse(filename)
            print lp.return_simple_error()
