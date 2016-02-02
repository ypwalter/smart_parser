from simple_analyzer import *
from output_formatter import *

class SmartParser:
    def __init__(self):
        self.sa = SimpleAnalyzer()
        self.of = OutputFormatter()

    # parsing the whole file and return in the style you choose
    def ret_parsed_file(self, filename, style, timestamp=True):
        self.sa.parse_file(filename)
        if timestamp:
            error_list = self.sa.return_error()
            warning_list = self.sa.return_warning()
        else:
            error_list = self.sa.return_sorted_error()
            warning_list = self.sa.return_sorted_warning()
        return self.of.output(style, error_list, warning_list)

    # parsing the input line and return
    def ret_parsed_line(self, line):
        self.sa.result = parse_line(filename)
        return self.sa.result

    # after parsing all the streaming line, return all the result
    def ret_parsed_lines_result(self, style):
        error_list = self.sa.return_error()
        warning_list = self.sa.return_warning()
        return self.of.output(style, error_list, warning_list)

    # if you are parsing line by line, you may clean the current queued list
    def clean_lists():
        self.sa.clean_lists()

# This is a basic function test.
# It will parse through current directory for clean_(.)*.txt and extract data out.
if __name__ == '__main__':
    current_dir = os.getcwd()
    sp = SmartParser()
    for filename in os.listdir(current_dir):
        if filename.endswith(".txt") and filename.startswith("cleaned_") and not os.path.isdir(filename):
            print sp.ret_parsed_file(filename, "json", False)

