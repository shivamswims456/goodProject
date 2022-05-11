import logging as log
from models.core.db import db
from models.cultures import cultures


class testDispController( object ):

    def __init__(self) -> None:
        self.cultures = cultures()
        self.db = db()


    def getTest(self, id:str = None):

        """
            Controller to get test in dict form
        """
        
        query = self.db.query("show columns from cultures")

        

        if query["result"]:

            result = self.cultures.read(id = id)

            data = []

            if result["result"]:

                for row in result["data"]:

                    temp = {}

                    for each in enumerate(row):
                        
                        temp[query["data"][each[0]][0]] = each[1]

                    data.append(temp)

                result = {"result":True, "data":data}

            else:

                result = result

        else:

            result = query

            log.error(f'{{testDispController_columnRead_Error:{{"id":{id}}}}}')

        return result
        