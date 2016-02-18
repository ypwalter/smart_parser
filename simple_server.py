import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("feedback.html")
    def post(self):
        self.write("Information submitted!")

class SimpleServer():
    def __init__(self):
        self.application = tornado.web.Application([(r"/", MainHandler)], autoreload=True)

    def start(self, port=8888):
        self.application.listen(port)
        tornado.ioloop.IOLoop.instance().start()

# Test of this simpleserver. Server starts at port 8887.
if __name__ == "__main__":
    ss = SimpleServer()
    ss.start(8887)
