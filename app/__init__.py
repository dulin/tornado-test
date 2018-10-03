from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import define, options
from tornado.web import Application
from app.views import HelloWorld

define('port', default=8080, help="listening port")
define('bind_address', default="127.0.0.1", help="bind address")

def main():
    app = Application([
        ('/', HelloWorld)
    ])
    http_server = HTTPServer(app)
    http_server.listen(options.port, options.bind_address)
    print("Listening on http://%s:%i" % (options.bind_address, options.port))
    IOLoop.current().start()