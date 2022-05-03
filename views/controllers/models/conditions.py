import logging as log
from core.uty import uty
from core.db import db

class conditions( uty ):

    def __init__(self) -> None:
        uty.__init__(self)
        self.db = db()



    def delete(self, cond:str) -> dict:

        """
        Function for deleteing condition

        Parameter:

            cond(str):cond of condition

        Returns:

            result(dict):{"result":True/False data:"SuccessFul/ErrorCode"}

        """

        result = {"result":False, "data":"Please provide conditions cond"}

        if cond != None:

            conditionDelte = self.db.query("delete from conditions where cond = '{}';".format(cond))

            if not conditionDelte["result"]:

                log.error(f'{{Conditions_Delete_Error: {{"condition":{cond}}}}}')

            else:

                conditionDelte["data"] = "Successful"
                log.info(f'{{Conditions_Delete_Successful: {{"condition":{cond}}}}}')

            result = conditionDelte

        
        return result





    def update(self, cond:str = None, listed:int = 0) -> dict:

        """
        Function for updateing state of a condition

        Parameters:
            cond(str): cond of the condition
            listed(int):0/1 default 0 

        Returns:
            result(dict):{"result":True/False, "data":"successful/errorCode"}

        """


        result = {"result":False, "data":"please provide condition's cond"}


        if cond != None:

            checkcondition = self.db.query("select (cond) from conditions where cond = '{}'".format(cond))

            if checkcondition["result"] and checkcondition["data"] != 0:

                updatecondition = self.db.query("update conditions set listed = {} where cond = '{}'".format(listed, cond))

                if not updatecondition["result"]:
                    
                    log.error(f'{{Condition_Update_Error: {{"condition":{cond}, "listed":{listed}}}}}')

                else:

                    updatecondition["data"] = "Successful"

                    log.info(f'{{Condition_Update_Successful: {{"condition":{cond}, "listed":{listed}}}}}')

                    

                result = updatecondition




            elif checkcondition["result"] == False:

                result = checkcondition

                log.error(f'{{Condition_Update_Search_Error: {{"condition":{cond}, "listed":{listed}}}}}')

            
            elif checkcondition["result"] and len(checkcondition["data"]) == 0:

                result = {"result":False, "data":"Condition Not Present"}
                log.warning(f'{{Condition_Not_Present: {{"condition":{cond}, "listed":{listed}}}}}')



        return result














    def read(self, cond:str = None, listed:int = None) -> dict:

        """"
        Function for Reading out list conds based on their listed state and 
        to get listed staet of a condition function only accepts either of (cond or
        listed)

        Parameters:
            cond(str): cond of the condition
            listed(int): state of the condition

        Returns:
            result(dict): {"result":True/False, "data":"successful/errorCode"}

        """

        result = {"result":False, "data":"Please Provide either of (cond, listed)"}
        #both parameters are given

        if cond != None or listed != None:


            if cond != None and listed != None:

                result = {"result":False, "data":"Please Provide either of (cond, listed) only"}
                #both parameters are None

            elif cond != None:

                getconditions = self.db.query("select (listed) from conditions where cond = '{}'".format(cond))

                if not getconditions["result"]:
                    
                    log.error(f'{{additionalInfo: {{"condition":{cond}, "listed":{listed}}}}}')

                    
                result = getconditions
                

            elif listed != None:

                getListed = self.db.query("select (cond) from conditions where listed = {}".format(listed))

                if not getListed["result"]:

                    log.error(f'{{additionalInfo: {{"condition":{cond}, "listed":{listed}}}}}')

                result = getListed

        
        return result

                    
            


    def create(self, cond:str = None, listed:int = 1)-> dict:

        """
        Function For addition of conditions 
        
        Parameters:
            cond(str): cond of condition to be added
            listed(int):0/1 default 1

        Returns
            result(dict) = {"result":True/False, "data":"SuccessFul/ErrorCode"}

        
        """

        result = {"result":False, "data":"Please Provide condition cond"}

        if cond != None:

            conditionCheck = self.read(cond=cond)

            if conditionCheck["result"] and len(conditionCheck["data"]) == 0:

                conditionAdd = self.db.query("insert into conditions (cond, listed) values ('{}', {})".format(cond, listed))

                if conditionAdd["result"]:

                    result = {"result":True, "data":"Successful"}
                    log.info(f'{{Condition_Added_Successfully: {{"condition":{cond}, "listed":{listed}}}}}')


                else:

                    result = conditionAdd


            elif conditionCheck["result"] == False:

                result = conditionCheck

                log.error(f'{{Condition_Query_Error: {{"condition":{cond}, "listed":{listed}}}}}')


            else:

                result = {"result":False, "data":"condition Already Present"}
                log.warning(f'{{Condition_Already_Present: {{"condition":{cond}, "listed":{listed}}}}}')

        
        return result

            

#print(conditions().create(cond="Dengue"))
#print(conditions().create(cond="Heart"))

#print(conditions().read(listed=1))
#print(conditions().update(cond="Dengue", listed=0))
#print(conditions().delete(cond="Dengue"))


    
