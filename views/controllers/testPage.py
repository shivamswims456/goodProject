import json
from controllers.models.core.server import baseHandler
from controllers.testDispController import testDispController
testDispController = testDispController()

class testpage(baseHandler):

    def get(self):

        id = self.get_argument("id")
        self.render( "shop.html", testContent = testDispController.getTest(id = id) )

        

