import os, sys
import tornado.web
from baseCore import base


class server( object ):

    def __init__(self) -> None:
        self.base = base()
        self.env = self.base.env


    def getApplication(self, routes):

        print()

        routes.append((f'{self.base.getEnv("themeAssets")}(.*)'.format(self.base.getEnv("themeAssets")), tornado.web.StaticFileHandler, {"path": self.base.getEnv("staticPath")}))

        settings = {"debug": self.base.getEnv("serverDebug"),
                    "reload": self.base.getEnv("serverReload"),
                    "cookie_secret": self.base.getEnv("cookieSecret"),
                    "login_url":self.base.getEnv("loginUrl"),
                    "template_path":self.base.getEnv("templatePath"),
                    "xsrf_cookies":self.base.getEnv("xsrfCookie")}

        application = tornado.web.Application(routes, **settings)
        server = tornado.httpserver.HTTPServer(application)
        server.listen(self.base.getEnv("serverPort"))
        





class baseHandler(tornado.web.RequestHandler):

    def get_current_user(self):

        return self.get_secure_cookie("auth")



