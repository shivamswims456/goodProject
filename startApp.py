import tornado
from views.controllers.models.core.server import server
from views.index import index
from views.testPage import testpage
from views.aboutUs import aboutUs
from views.contactUs import contactUs

class startApp( object ):

    def __init__(self) -> None:
        
        self.startHttp()
        

    def startHttp(self):

        self.httpServer = server().getApplication([(r"/", index),
                                                   (r"/test_page", testpage),
                                                   (r"/about_us", aboutUs),
                                                   (r"/contact_us", contactUs)])

        tornado.ioloop.IOLoop.instance().start()

startApp()