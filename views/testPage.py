import json
from controllers.models.core.server import baseHandler
from controllers.models.cultures import cultures

cultures = cultures()
class testpage(baseHandler):

    def get(self):

        id = self.get_argument("id")
        self.write(json.dumps(cultures.read(id=id)))

        

