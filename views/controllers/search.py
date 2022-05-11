import json
from models.core.server import baseHandler
from models.createSearch import testSearch
searchController = testSearch()


class search(baseHandler):

    def get(self):

        searchTerm=self.get_argument("searchTerm").upper()
        

        self.write(json.dumps(searchController.cultureSearch(searchTerm)))
