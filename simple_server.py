import re
import urllib
import os.path
import tornado.autoreload
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.template

from html_escape import *
from database import *

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("feedback.html")

    def post(self):
        msg = self.request.body
        self.write("Information submitted!<br/>")
        self.write("<a href='javascript:history.go(-1);'>Go back to last page</a><br/>")
        self.write("<a href='/exit'>Shutdown the server</a><br/>")
        
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
        # print db.output_data()
        db.close()

class ExitHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Server shut down.")
        server.stop()

class WSHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        pass
        # print 'WebSocket Connection Opened...'

    def on_message(self, message):
        if os.path.isfile("fbtmp.html"):
            with open("fbtmp.html", "r") as infile:
                self.write_message(infile.read())
            os.remove("fbtmp.html")            
        # print 'WebSocket received:', message

    def on_close(self):
        pass
        # print 'WebSocket Connection Closed...'


class SimpleServer:
    def __init__(self):
        tornado.autoreload.start()
        tornado.autoreload.watch("feedback.html")
        self.application = tornado.web.Application([(r"/",MainHandler), (r'/ws', WSHandler), (r'/exit', ExitHandler)], autoreload=True)

    def start(self, port=8888):
        global server
        self.application.listen(port)        
        server = tornado.ioloop.IOLoop.instance()
        server.start()

    def __del__(self):
        server.stop()

# Test of this simpleserver. Server starts at port 8887.
if __name__ == "__main__":
    ss = SimpleServer()
    ss.start(8080)
