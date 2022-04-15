import base, logging as log
from uty import uty

class organs( uty ):

    def __init__(self) -> None:
        uty.__init__(self)
        self.db = self.db()



    def delete(self, name:str) -> dict:

        """
        Function for deleteing organ

        Parameter:

            name(str):name of organ

        Returns:

            result(dict):{"result":True/False data:"SuccessFul/ErrorCode"}

        """

        result = {"result":False, "data":"Please provide organs name"}

        if name != None:

            organDelte = self.db.query("delete from organs where name = '{}';".format(name))

            if not organDelte["result"]:

                log.error(f'{{Organs_Delete_Error: {{"organ":{name}}}}}')

            else:

                log.info(f'{{Organs_Delete_Successful: {{"organ":{name}}}}}')

                organDelte["data"] = "Successful"

            result = organDelte

        
        return result





    def update(self, name:str = None, listed:int = 0) -> dict:

        """
        Function for updateing state of a organ

        Parameters:
            name(str): Name of the organ
            listed(int):0/1 default 0 

        Returns:
            result(dict):{"result":True/False, "data":"successful/errorCode"}

        """


        result = {"result":False, "data":"please provide organ's Name"}


        if name != None:

            checkOrgan = self.read(name=name)

            if checkOrgan["result"] and checkOrgan["data"] != 0:

                updateOrgan = self.db.query("update organs set listed = {} where name = '{}'".format(listed, name))

                if updateOrgan["result"]:

                    updateOrgan["data"] = "Successful"
                    
                    log.info(f'{{Organs_Update_Successful: {{"organ":{name}, "listed":{listed}}}}}')

                else:
                    
                    log.error(f'{{Organs_Update_Error: {{"organ":{name}, "listed":{listed}}}}}')

                result = updateOrgan




            elif checkOrgan["result"] == False:

                result = checkOrgan

                log.error(f'{{Organs_Update_Search_NotFound: {{"organ":{name}, "listed":{listed}}}}}')

            
            elif checkOrgan["result"] and len(checkOrgan["data"]) == 0:

                result = {"result":False, "data":"Organ Not Present"}

                log.info(f'{{Organs_Update_Notfound: {{"organ":{name}, "listed":{listed}}}}}')



        return result














    def read(self, name:str = None, listed:int = None) -> dict:

        """"
        Function for Reading out list names based on their listed state and 
        to get listed staet of a organ function only accepts either of (name or
        listed)

        Parameters:
            name(str): Name of the organ
            listed(int): state of the organ

        Returns:
            result(dict): {"result":True/False, "data":"successful/errorCode"}

        """

        result = {"result":False, "data":"Please Provide either of (name, listed)"}
        #both parameters are given

        if name != None or listed != None:


            if name != None and listed != None:

                result = {"result":False, "data":"Please Provide either of (name, listed) only"}
                #both parameters are None

            elif name != None:

                getOrgans = self.db.query("select (listed) from organs where name = '{}'".format(name))

                if getOrgans["result"]:

                    log.info(f'{{Organs_Read_Organ_Successful: {{"organ":{name}, "listed":{listed}}}}}')

                else:
                    
                    log.info(f'{{Organs_Read_Organ_Error: {{"organ":{name}, "listed":{listed}}}}}')

                    
                result = getOrgans
                

            elif listed != None:

                getListed = self.db.query("select (name) from organs where listed = {}".format(listed))

                if getListed["result"]:

                    log.info(f'{{Organs_Read_Listed_Successful: {{"organ":{name}, "listed":{listed}}}}}')

                else:

                    log.error(f'{{Organs_Read_Listed_Error: {{"organ":{name}, "listed":{listed}}}}}')

                result = getListed

        
        return result

                    
            


    def create(self, name:str = None, listed:int = 0)-> dict:

        """
        Function For addition of organs 
        
        Parameters:
            name(str): Name of organ to be added
            listed(int):0/1 default 0

        Returns
            result(dict) = {"result":True/False, "data":"SuccessFul/ErrorCode"}

        
        """

        result = {"result":False, "data":"Please Provide Organ Name"}

        if name != None:

            organCheck = self.read(name = name)

            if organCheck["result"] and len(organCheck["data"]) == 0:

                organAdd = self.db.query("insert into organs (name, listed) values ('{}', {})".format(name, listed))

                if organAdd["result"]:

                    result = {"result":True, "data":"Successful"}
                    log.info(f'{{Organ_Created: {{"organ":{name}, "listed":{listed}}}}}')


                else:

                    result = organAdd
                    log.error(f'{{Organ_Create_Error: {{"organ":{name}, "listed":{listed}}}}}')


            elif organCheck["result"] == False:

                result = organCheck
                log.error(f'{{Organ_Create_Search_Error: {{"organ":{name}, "listed":{listed}}}}}')


            else:

                result = {"result":False, "data":"Organ Already Present"}
                log.warning(f'{{Organ_Already_Present: {{"organ":{name}, "listed":{listed}}}}}')

        
        return result

            

#print(organs().create(name="kidney"))
#print(organs().create(name="Heart"))

#print(organs().read(listed=1))
#print(organs().update(name="kidney", listed=1))
#print(organs().delete(name="Heart"))


    
