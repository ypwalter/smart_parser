from xml.sax.saxutils import escape, unescape

class HTMLEscape:
    def __init__(self):
        # escape() and unescape() takes care of &, < and >.
        self.html_escape_table = {
            '"': "&quot;",
            "'": "&apos;"
        }
        self.html_unescape_table = {v:k for k, v in self.html_escape_table.items()}

    def html_escape(self, text):
        return escape(text, self.html_escape_table)

    def html_unescape(self, text):
        return unescape(text, self.html_unescape_table)
