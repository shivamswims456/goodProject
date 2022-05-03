import json
from controllers.models.core.server import baseHandler
from controllers.models.createSearch import testSearch

search = testSearch()

class search(baseHandler):

    def get(self, param):

        self.write(json.dumps(search.cultureSearch(param)))
