from tornado.web import RequestHandler

class HelloWorld(RequestHandler):

    def get(self):
        self.write("Hello :)")