import logging as log
from core.uty import uty
from core.search import Trie
from cultures import cultures
from pincodes import pincodes
from collections import defaultdict



class pinSearch( uty ):


    def __init__(self):

        uty.__init__(self)
        self.search = Trie()
        self.pincodes = pincodes()
        self.__getPincodes()


    
    def pincodeSearch(self, term:str)->list:
        """
        Function intended for searching cultures
        parameters:
            term:search Term
        result:
            [termParentName, dbIndex]/ErrorCode


        """

        return self.__conciseResult(self.search.query(term.upper()))



    def __conciseResult(self, resultList):

        """
            Function intended for concising found result

            parameters:
                resultList(list of list) = result queried from tries

            Return
                list of list [[termParentName dbIndex], [termParentName dbIndex]]

        """

        result = []

        for each in resultList:
            #('1100920', 1, ['110092  Kalyan Vas', 10.0])
            result.append(each[2])

        return result







    def __breakStrings(self, string, index):

        """
            Function intended for breaking string and cleaning it from special characters
            Parameters:
                string:strin to be treated
            index:
                additional info that has to be adjoined with index
        """

        data  = [[self.removeSpecial(_.upper()), index] for _ in string.split(" ")]

        return data


    def __buildTrie(self, queryTerms):

        """ 
            Function for buildin out trie for suplied queryTerms

            querTerms(list of list)
        """

        queryInserted = {}

        for each in queryTerms:

            query = each[0]

            queryInserted[query] = queryInserted.get(query, -1) + 1
            #checks if value has been inserted or not by mainataining a key value pair 
            #if already associated with another key a incremental index is added 
            #and is inserted in key

            query += str(queryInserted[query])

            self.search.insert(query, each[1])
            



    

    def __getPincodes(self):

        """ 
            Function for fetching pincodes from database and making tree out of it

        """

        pincodeSearch = self.pincodes.read();

        pincodes = []

        if pincodeSearch["result"]:

            for pincode in pincodeSearch["data"]:

                pincodes += self.__breakStrings(pincode[0], pincode)

        self.__buildTrie(pincodes)

        

                
        
    



""" t = pinSearch()
while True:

    k = input()

    if k == "duck":

        break

    else:

        print(t.pincodeSearch(k))


 """



class testSearch( uty ):

    def __init__(self) -> None:
        
        uty.__init__(self)
        self.search = Trie()
        self.cultures = cultures()
        self.__getCultureParameters()


    def cultureSearch(self, term:str)->list:
        """
        Function intended for searching cultures
        parameters:
            term:search Term
        result:
            [termParentName, dbIndex]/ErrorCode


        """

        return self.__conciseResult(self.search.query(term.upper()))


    def __conciseResult(self, resultList):

        """
            Function intended for concising found result

            parameters:
                resultList(list of list) = result queried from tries

            Return
                list of list [[termParentName dbIndex], [termParentName dbIndex]]

        """

        result = {}

        output = defaultdict(list)

        sortedList = []

        for each in resultList:

            #('KINASE0', 1, ['CARDIAC PROFILE', 47, 2])
            #indexedSearchTerm, wordCounter, associatedData

            each = each[2]

            #['CARDIAC PROFILE', 47, 2]

            result[each[1]] = [each[0], each[2]]

        for id, vals in result.items():

            name = vals[0].upper()
            prio = vals[1]

            output[prio].append([name, id])

        for key in sorted(list(output.keys())):

            sortedList += output[key]


        return sortedList




    def __breakStrings(self, string, index):

        """
            Function intended for breaking string and cleaning it from special characters
            Parameters:
                string:strin to be treated
            index:
                additional info that has to be adjoined with index
        """

        data  = [[self.removeSpecial(_.upper()), index] for _ in string.split(" ")]

        return data



    def __buildTrie(self, queryTerms):

        """ 
            Function for buildin out trie for suplied queryTerms

            querTerms(list of list)
        """

        queryInserted = {}

        for each in queryTerms:

            query = each[0]

            queryInserted[query] = queryInserted.get(query, -1) + 1
            #checks if value has been inserted or not by mainataining a key value pair 
            #if already associated with another key a incremental index is added 
            #and is inserted in key

            query += str(queryInserted[query])

            self.search.insert(query, each[1])

        



    def __getCultureParameters(self):

        """ 
            Function for deriving out values from culture module and 
            assigning priority to each key
            column              prio
            name[0]                1
            components[2]          2
            associatedNames[3]     3
            conditions[4]          4

        """

        queryTerms = []

        cultureRead = self.cultures.read()

        if cultureRead["result"]:

            cultureRead = cultureRead["data"]

            for row in cultureRead:

                id = row[17]
                name = row[0]

                if row[11] == 1:

                    queryTerms += self.__breakStrings(name, [name, id, 1])

                
                for stringPrio in [[row[2], 2], [row[3], 3], [row[10], 4]]:

                    stringList = stringPrio[0]
                    priority = stringPrio[1]

                    for string in stringList:

                        queryTerms += self.__breakStrings(string, [name, id, priority])

            self.__buildTrie(queryTerms=queryTerms)

""" 

t = testSearch()
while True:        
    print("param")
    param = input()
    if param == "duck":
        break
    else:
        print(t.cultureSearch(param.upper()))
"""