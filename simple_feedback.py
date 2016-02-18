class SimpleFeedback:
    def __init__(self, fl, el):
        self.full_list = fl
        self.error_list = el

    # Each row is highlit separately
    def generate_table_row(self, display, number, data):
        ret = ""

        # Decide if this is important to display in the beginning
        if display:
            ret += "<tr>"
            highlight = "background-color: #F78181;"
        else:
            ret += "<tr class='hidden' style='display:none;'>"
            highlight = "" 

        # put other data in the table
        ret += "<td width='80px'><input type='radio' name='important-" + str(number) + "'></td>" + \
               "<td width='80px'><input type='radio' name='useless-" + str(number) + "'></td>" + \
               "<td style='text-align: left;" + highlight + "'>" + data + "</td>" + \
               "</tr>\n"

        return ret

    # Generate html and modify the content based on full list and error list to template.html
    def generate_feedback_form(self):
        # Generate html for substitute
        html = ""
        i = 1
        for data in self.full_list:
            if data in self.error_list:
                html += self.generate_table_row(True, i, data)
            else:
                html += self.generate_table_row(False, i, data)
            i += 1

        # Substitute heml inside template.html and output as feedback.html
        with open("template.html", "r") as infile:
            template_file = infile.read()
        with open("feedback.html", "w+") as outfile:
            token = "<!--CONTENT-->"
            output_file = template_file.replace(token, html)
            outfile.write(output_file)

if __name__ == "__main__":
    from simple_analyzer import * 
    current_dir = os.getcwd()
    lp = SimpleAnalyzer()
    for filename in os.listdir(current_dir):
        if filename.endswith(".txt") and filename.startswith("cleaned_") and not os.path.isdir(filename):
            lp.parse_file(filename)

    sf = SimpleFeedback(lp.return_list(), lp.return_error())
    sf.generate_feedback_form()


