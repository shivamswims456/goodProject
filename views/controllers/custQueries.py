import json
from models.core.server import baseHandler
from models import custQueries

custQueries = custQueries()

class custQuery( baseHandler ):

    def post(self):

        self.write(json.dumps(custQueries.create(**{each:self.get_argument(each) for each in self.request.arguments})))

