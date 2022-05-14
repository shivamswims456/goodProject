import json
from models.core.server import baseHandler
from models.createSearch import testSearch, pinSearch
testSearchCont = testSearch()
pinSearchCont = pinSearch()


class pincode(baseHandler):

    def post(self):

        searchTerm = self.get_argument("pincode")

        print(searchTerm)

        searchResults = pinSearchCont.pincodeSearch(searchTerm)

        result = {}

        for each in searchResults:

            result[each[0]] = each[1]

        self.write(json.dumps({"result":True, "data":result})) 




class search(baseHandler):

    def post(self):

        searchTerm=self.get_argument("searchTerm")

        searchResults = testSearchCont.cultureSearch(searchTerm)

        result = {}

        for each in searchResults:

            result[each[0]] = f"test_page?id={each[1]}&name={each[0].replace(' ', '_')}"

        self.write(json.dumps({"result":True, "data":result}))
