from core.db import db
import json

class uty( object ):

    def __init__(self) -> None:
        self.db = db

    def makeQuery(self, parameters:dict) -> str:

        """
        Function to turn dict into query
            Parameters:
                parameter(dict): dict of columns to fetch with their query values
            
            return 
                QueryString(str): QueryString for query
        """

        cols = str(tuple(parameters.keys())).replace("'", "").replace("(", "").replace(")", "")

        
        searchQuery = f"select {cols} from cultures where "

        for name, parameter in parameters.items():

            if parameter != None:

                if type(parameter) == list and len(parameter) != 0:

                    parameter = json.dumps(parameter)

                    
                    searchQuery += """json_contains({}, '{}')""".format(name, parameter)

                    searchQuery += " and "


                elif type(parameter) == str:

                   
                    searchQuery += "{} = '{}'".format(name, parameter)

                    searchQuery += " and "

                elif type(parameter) == int or type(parameter) == float:

                   
                    searchQuery += "{} = {}".format(name, parameter)

                    searchQuery += " and "

        searchQuery = searchQuery[:-5] + ";"

        return searchQuery
        
        