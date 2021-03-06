import logging as log
from core.uty import uty
from core.db import db

class pincodes( uty ):

    def __init__(self):

        uty.__init__(self)

        self.db = db()


    def delete(self, pincode:str = None)-> dict:

        
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
                log.info(f'{{Pincodes_Delete_Successful: {{"pincode":{pincode}}}}}')

            else:

                result = delPin
                log.error(f'{{Pincodes_Delete_Fail: {{"pincode":{pincode}}}}}')


        return result


            


    def read(self, pincode:str = None, status:int = None)-> dict:

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


        
        #if both are None

        if pincode != None or status != None:

            if pincode != None and status != None:

                result = {"result":False, "data":"Please provide any of the two( pincode or status ) only"}
                #if both are given
        
            elif pincode != None:

                statusQuery = self.db.query("select (listed) from pincodes where pincodes = '{}'".format(pincode))
                
                if statusQuery["result"]:

                    log.info(f'{{Pincode_Read_Listed_Successful: {statusQuery}')

                else:

                    log.error(f'{{Pincode_Read_Listed_Error: {{"pincode":{pincode}, "status":{status}}}}}')

                
                result = statusQuery



            elif status != None:

                pinQuery = self.db.query("select (pincodes) from pincodes where listed = {}".format(status))

                if pinQuery["result"]:

                    log.info(f'{{Pincode_Read_Pincodes_Successful: {pinQuery}')

                else:

                    log.error(f'{{Pincode_Read_Pincodes_Error: {{"pincode":{pincode}, "status":{status}}}}}')

                result = pinQuery


        else:

            pinQuery = self.db.query("select pincodes, listed from pincodes;")

            if pinQuery["result"]:

                log.info(f'{{Pincode_Read_Pincodes_Successful: {pinQuery}')

            else:

                log.error(f'{{Pincode_Read_Pincodes_Error: {{"pincode":{pincode}, "status":{status}}}}}')

            result = pinQuery

        
        return result

        

            




    def update(self, pincode:str = None, status:int = 0)-> dict:


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

            checkPresent = self.db.query("select (pincodes) from pincodes where pincodes = '{}'".format(pincode))

            if checkPresent["result"] and len(checkPresent["data"]) != 0:
                    
                queryResult = self.db.query( "update pincodes set pincodes='{}', listed={} where pincodes = '{}';".format(pincode, status, pincode) )


                if queryResult["result"]:

                    result = {"result":True, "data":"Successful"}
                    log.info(f'{{Pincode_Successful_Update: {{"pincode":{pincode}, "status":{status}}}}}')

                else:


                    result = queryResult
                    log.error(f'{{Pincode_Update_Error: {{"pincode":{pincode}, "status":{status}}}}}')


            elif checkPresent["result"] == False:

                result = checkPresent
                log.error(f'{{Pincode_Update_Search_Error: {{"pincode":{pincode}, "status":{status}}}}}')

            
            elif checkPresent["result"] and len(checkPresent) == 0:

                result = {"result":False, "data":"Pincode not Present"}
                log.warning(f'{{Pincode_Not_Present: {{"pincode":{pincode}, "status":{status}}}}}')



        return result





    def create(self, pincode:str = None, price:int = 1)-> dict:

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

            checkPresent = self.read(pincode=pincode)

            if checkPresent["result"] and len(checkPresent["data"]) == 0:
                    
                queryResult = self.db.query( "insert into pincodes (pincodes, listed) values ('{}', {});".format(pincode, price) )

                if queryResult["result"]:

                    result = {"result":True, "data":"Successful"}
                    log.info(f'{{Pincode_Successful_Insert: {{"pincode":{pincode}, "status":{price}}}}}')

                else:

                    result = queryResult
                    log.error(f'{{Pincode_Insert_Error: {{"pincode":{pincode}, "status":{price}}}}}')

            
            elif checkPresent["result"] == False:

                result = checkPresent
                log.error(f'{{Pincode_Create_Search_Error: {{"pincode":{pincode}, "status":{price}}}}}')

                

            else:

                result = {"result":False, "data":"Pincode Already Present"}
                log.warning(f'{{Pincode_Already_Present: {{"pincode":{pincode}, "status":{price}}}}}')



        return result
        

        

        

        

#print( pincodes().create(pincode="834004", price=1) )
#print( pincodes().update(pincode="834001", price=1) )
#print(pincodes().read(price=1))
#print(pincodes().delete(pincode="834003"))