import base, logging as log
from uty import uty

class pincodes( uty ):

    def __init__(self):

        uty.__init__(self)

        self.db = self.db()


    def delete(self, pincode:str = None):

        
        """
        Function for deleting pincodes

        parameters 
            pincode(str): pincode of 6 digit in str

        Returns
            result(dict): result(dict)= {"result":True/False, "data":"Successful/ErrorCode"}

        """

        result = {"result":False, "data":"Please provide pincode to delete"}


        if pincode != None:

            delPin = self.db.query("delete from pincodes where pincodes = '{}'".format(pincode))

            if delPin["result"]:

                result = {"result":True, "data":"Successful"}

            else:

                result = delPin
                log.error(f'{{additionalInfo: {{"pincode":{pincode}}}}}')


        return result


            


    def read(self, pincode:str = None, status:int = None):

        """
        Function for reading list pincodes with same state
        and state of a particular pincode function only accepts
        either pincode or status

        parameters:
            pincodes(str): pincodes of 6 digit in str
            status(int):0/1;

        Returns:

            if status:


                result(dict)= {"result":True/False, "data":"listOfPincodes/ErrorCode"}

            if pincode

                result(dict)= {"result":True/False, "data":"satusOfPincode/ErrorCode"}
        

        """


        result = {"result":False, "data":"Please provide any of the two( pincode or status )"}
        #if both are None

        if pincode != None or status != None:

            if pincode != None and status != None:

                result = {"result":False, "data":"Please provide any of the two( pincode or status ) only"}
                #if both are given
        
            elif pincode != None:

                statusQuery = self.db.query("select (listed) from pincodes where pincodes = '{}'".format(pincode))
                
                if statusQuery["result"]:

                    result = {"result":True, "data":statusQuery["data"]}

                else:

                    result = statusQuery
                    log.error(f'{{additionalInfo: {{"pincode":{pincode}, "status":{status}}}}}')



            elif status != None:

                pinQuery = self.db.query("select (pincodes) from pincodes where listed = {}".format(status))
                
                if pinQuery["result"]:

                    result = {"result":True, "data":pinQuery["data"]}

                else:

                    result = pinQuery
                    log.error(f'{{additionalInfo: {{"pincode":{pincode}, "status":{status}}}}}')

        
        return result

        

            




    def update(self, pincode:str = None, status:int = 0):


        """
        Function for updateing pincodes and its state

        parameters:
            pincodes(str): pincodes of 6 digit in str
            status(int):0/1; default 0

        Returns:

            result(dict)= {"result":True/False, "data":"output/ErrorCode"}
        

        """

        result = {"result":False, "data":"please provide pincode"}

        if pincode != None:

            result = {"result":False, "data":"Func202"}


            checkPresent = self.db.query("select (pincodes) from pincodes where pincodes = '{}'".format(pincode))


            if checkPresent["result"] and len(checkPresent["data"]) != 0:
                    
                queryResult = self.db.query( "update pincodes set pincodes='{}', listed={} where pincodes = '{}';".format(pincode, status, pincode) )

                

                if queryResult["result"]:

                    result = {"result":True, "data":"Successful"}

                else:


                    result = queryResult
                    log.error(f'{{additionalInfo: {{"pincode":{pincode}, "status":{status}}}}}')


            elif checkPresent["result"] == False:

                result = checkPresent
                log.error(f'{{additionalInfo: {{"pincode":{pincode}, "status":{status}}}}}')

            else:

                result = {"result":False, "data":"Pincode Already Present"}



        return result





    def create(self, pincode:str = None, status:int = 0):

        """
        Function for inserting pincodes and its status

        parameters:
            pincodes(str): pincodes of 6 digit in str
            status(int):0/1; default 0

        Returns:

            result(dict)= {"result":True/False, "data":"output/ErrorCode"}

        """

        result = {"result":False, "data":"please provide pincode"}

        if pincode != None:

            result = {"result":False, "data":"Func201"}

            checkPresent = self.db.query("select (pincodes) from pincodes where pincodes = '{}'".format(pincode))

            if checkPresent["result"] and len(checkPresent["data"]) == 0:
                    
                queryResult = self.db.query( "insert into pincodes (pincodes, listed) values ('{}', {});".format(pincode, status) )

                if queryResult["result"]:

                    result = {"result":True, "data":"Successful"}

                else:

                    result = queryResult
                    log.error(f'{{additionalInfo: {{"pincode":{pincode}, "status":{status}}}}}')

            elif checkPresent["result"] == False:

                result = checkPresent
                log.error(f'{{additionalInfo: {{"pincode":{pincode}, "status":{status}}}}}')

            else:

                result = {"result":False, "data":"Pincode Already Present"}



        return result
        

        

        

        

#print( pincodes().create(pincode="834003", status=1) )
#print( pincodes().update(pincode="834003", status=0) )
#print(pincodes().read(status=1))
print(pincodes().delete(pincode="834003"))