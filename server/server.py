from tornado.web import Application
from tornado.web import url
from tornado.options import define
from tornado.options import options
from tornado.options import parse_config_file
from tornado.options import parse_command_line
import tornado.ioloop
import logging
import redis

from handlers import *

define('port', default=8888, help='server runs on this port', type=int)
define('dev', default=True, help='sets the dev toggle', type=bool)
define('redis_host', default='localhost', type=str)
define('redis_port', default=6379, type=int)
define('conf', default='/etc/count_server.conf', help='File path to the conf', type=str)

class App(Application):
    def __init__(self):
        handlers = [
            url(r"/([\w]+)/?$", MainHandler),
            url(r"/websocket/?$", WebSocket)
        ]

        settings = {
            'debug': options.dev,
        }

        self.r = redis.StrictRedis(
            host=options.redis_host,
            port=options.redis_port,
            db=0
        )

        tornado.web.Application.__init__(self, handlers, **settings)

def main():
    try:
        parse_config_file(options.conf)
        logging.info("Loaded conf file from %s" % options.conf)
    except SyntaxError as error:
        logging.error("Error in conf file: %s" % error)
    except IOError as error:
        logging.error("Conf file missing: %s" % error)

    parse_command_line()
    app = App()
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
