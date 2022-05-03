import tornado
from views.controllers.models.core.server import server
from views.index import index

class startApp( object ):

    def __init__(self) -> None:
        
        self.startHttp()
        

    def startHttp(self):

        self.httpServer = server().getApplication([(r"/", index)])

        tornado.ioloop.IOLoop.instance().start()

startApp()