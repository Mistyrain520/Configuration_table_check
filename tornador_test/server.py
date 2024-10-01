import tornado.ioloop
from tornado import gen
import tornado.web
import tornado.websocket
from logzero import logger

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

class APIUserHandler(tornado.web.RequestHandler):
    def post(self):
        dd = {
            "email": "fa@anonymous.com",
        }
        self.write("你使用了post方式{}".format(dd))

    @gen.coroutine
    def get(self):
        logger.info("收到消息")
        self.write("你调用了get方式")
class TestWebSocketHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin: str):
        return True
    def open(self):
        print("WebSocket opened")
    def on_message(self, message):
        logger.info("你收到的消息{}".format(message))
        self.write_message(u"You said: " + message)

    def on_close(self):
        print("WebSocket closed")

def make_app():
    urlpatterns = [
        (r"/", MainHandler), (r"/api/v1/user", APIUserHandler), (r"/api/v2/user", TestWebSocketHandler),
    ]
    settings = {
        "template": "templates",
        "static_path": "statics",
    }
    return tornado.web.Application(urlpatterns, **settings)


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()

