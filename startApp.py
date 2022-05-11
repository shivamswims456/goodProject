import tornado
from views.controllers.models.core.server import server
from views.controllers.index import index
from views.controllers.testPage import testpage
from views.controllers.aboutUs import aboutUs
from views.controllers.contactUs import contactUs
from views.controllers.addTocart import addToCart
from views.controllers.search import search

class startApp( object ):

    def __init__(self) -> None:
        
        self.startHttp()
        

    def startHttp(self):

        self.httpServer = server().getApplication([(r"/", index),
                                                   (r"/search", search),
                                                   (r"/test_page", testpage),
                                                   (r"/about_us", aboutUs),
                                                   (r"/contact_us", contactUs),
                                                   (r"/addToCart", addToCart)])

        tornado.ioloop.IOLoop.instance().start()

startApp()