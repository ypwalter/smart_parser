import os.path
from html_escape import *

class SimpleFeedback:
    def __init__(self, fl=[], el=[], tp="template.html", fb="feedback.html"):
        self.chronological = True
        self.full_list = fl
        self.error_list = el
        self.template = tp
        self.feedback = fb
        self.line_number = 1

    # Each row is highlit separately
    def generate_table_row(self, display, data):
        ret = ""
        line_number = str(self.line_number)

        # Decide if this is important to display in the beginning
        if display:
            ret += "<tr>"
            highlight = "background-color: #F78181;"
        else:
            ret += "<tr class='hidden' style='display:none;'>"
            highlight = "" 

        # put other data in the table
        he = HTMLEscape()
        ret += "<td width='80px'><input type='radio' name=\"" + he.html_escape(data) + "\" value='1'></td>" + \
               "<td width='80px'><input type='radio' name=\"" + he.html_escape(data) + "\" value='-1'></td>" + \
               "<td style='text-align: left;" + highlight + "'>" + data + "</td>" + \
               "</tr>\n"

        self.line_number += 1
        return ret

    # Generate html and modify the content based on full list and error list to template.html
    def generate_feedback_form(self, chronological=True):
        # if chronological is not synchronized, reverse the list and reverse True/False for chronological
        if chronological ^ self.chronological:
            self.full_list.reverse()
            self.chronological = not self.chronological

        # Generate html for substitute
        html = ""
        self.line_number = 1
        for data in self.full_list:
            if data in self.error_list:
                html += self.generate_table_row(True, data)
            else:
                html += self.generate_table_row(False, data)

        # Substitute heml inside template.html and output as feedback.html
        with open(self.template, "r") as infile:
            template_file = infile.read()
        with open(self.feedback, "w+") as outfile:
            token = "<!--CONTENT-->"
            output_file = template_file.replace(token, html)
            outfile.write(output_file)

        # Return data generated this time
        return self.line_number

    # Generate html
    def return_new_feedback(self, chronological=True, line_number=0):
        html = []
        self.line_number = 1
        for data in self.full_list:
            if self.line_number < line_number:
                self.line_number += 1
                continue
            if data in self.error_list:
                html.append(self.generate_table_row(True,  data))
            else:
                html.append(self.generate_table_row(False, data))

        # if chronological is not synchronized, reverse the list and reverse True/False for chronological
        if chronological ^ self.chronological:
            html.reverse()
            self.chronological = not self.chronological

        with open(self.feedback, "w+") as outfile:
            outfile.write("".join(html))

        # Return data generated this time
        return self.line_number

# This is an example of simple feedback using simple analyzer and simple server
if __name__ == "__main__":
    from simple_analyzer import * 
    current_dir = os.getcwd()
    lp = SimpleAnalyzer()
    for filename in os.listdir(current_dir):
        if filename.endswith(".txt") and filename.startswith("cleaned_") and not os.path.isdir(filename):
            lp.parse_file(filename)

    sf = SimpleFeedback(lp.return_list(), lp.return_error())
    sf.generate_feedback_form(False)

    import subprocess
    p = subprocess.Popen(["python", "simple_server.py"])
 
    import webbrowser
    webbrowser.open("http://localhost:8080/")

    print "Now waiting for feedback form to be finished."
    p.communicate()
