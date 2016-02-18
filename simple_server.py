import re
import tornado.ioloop
import tornado.web
import urllib

from html_escape import *
from database import *

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("feedback.html")

    def post(self):
        msg = self.request.body
        self.write("Information submitted!<br/>")
        
        he = HTMLEscape()
        db = Database()

        if msg != "":
            for item in msg.split("&"):
                tmp = item.split("=")
                data = he.html_unescape(urllib.unquote_plus(tmp[0]))
                # TODO: make html escape, regex clean, and other functions in util    
                data = re.sub("^[(0-9)|( :.\\-)]+", "", data).strip()
                self.write(data + " is " + tmp[1] + ".<br/>")
                db.input_data("general", int(tmp[1]), data)
        print db.output_data()
        db.close()

        server.stop()

class SimpleServer:
    def __init__(self):
        self.application = tornado.web.Application([(r"/", MainHandler)], autoreload=True)

    def start(self, port=8888):
        self.application.listen(port)
        global server
        server = tornado.ioloop.IOLoop.instance()
        server.start()

    def __del__(self):
        server.stop()

# Test of this simpleserver. Server starts at port 8887.
if __name__ == "__main__":
    ss = SimpleServer()
    ss.start(8887)
