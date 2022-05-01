from core.db import db
from core.search import Trie
import json, re

class uty( object ):

    def __init__(self) -> None:
        self.db = db
        self.Trie = Trie


    def removeSpecial(self, string:str, subs:str = "") -> str:
        """
        Fuction intended for removing special string and substituting them with subs

        Parameters
            string(str):string to be parsed
            subs(str):sub string

        result:
            parsed string
        """

        return re.sub('[^A-Za-z0-9 ]+', subs, string)

        

    def updateQuery(self, parameters:dict, table:str) -> str:

        """
        Function to turn dict into update query it does not where statement support
            Parameters:
                parameter(dict): dict of columns to fetch with their query values
                table(str):For which query has to be made
            
            return 
                QueryString(str): QueryString for query
        """

        
        
        searchQuery = f"update {table} set "

        for name, parameter in parameters.items():

            if parameter != None:

                if type(parameter) == list and len(parameter) != 0:

                    parameter = json.dumps(parameter)

                    
                    searchQuery += """{} = '{}'""".format(name, json.dumps(parameter))

                    searchQuery += ", "


                elif type(parameter) == str:

                   
                    searchQuery += "{} = '{}'".format(name, parameter)

                    searchQuery += ", "

                elif type(parameter) == int or type(parameter) == float:

                   
                    searchQuery += "{} = {}".format(name, parameter)

                    searchQuery += ", "

        searchQuery = searchQuery[:-2]

        return searchQuery
      

    def makeQuery(self, parameters:dict, table:str) -> str:

        """
        Function to turn dict into query
            Parameters:
                parameter(dict): dict of columns to fetch with their query values
                table(str):name of table for which query has to be made
            
            return 
                QueryString(str): QueryString for query
        """

        cols = str(tuple(parameters.keys())).replace("'", "").replace("(", "").replace(")", "")

        
        searchQuery = ""

        for name, parameter in parameters.items():

            if parameter != None:

                if type(parameter) == tuple and len(parameter) != 0:

                    if len(parameter) == 1:

                        parameter = str(parameter).replace(",", "")

                    searchQuery += """{} in {}""".format(name, parameter)
                    searchQuery += " and "


                elif type(parameter) == list and len(parameter) != 0:

                    parameter = json.dumps(parameter)

                    
                    searchQuery += """json_contains({}, '{}')""".format(name, parameter)

                    searchQuery += " and "


                elif type(parameter) == str:

                   
                    searchQuery += "{} = '{}'".format(name, parameter)

                    searchQuery += " and "

                elif type(parameter) == int or type(parameter) == float:

                   
                    searchQuery += "{} = {}".format(name, parameter)

                    searchQuery += " and "


        if searchQuery == "":

            searchQuery = f"select {cols} from {table};"

        else:


            searchQuery = f"select {cols} from {table}; where " + searchQuery[:-5] + ";"
            

        return searchQuery
        
        