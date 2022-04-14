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

                log.error(f'{{additionalInfo: {{"organ":{name}}}}}')

            else:

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

            checkOrgan = self.db.query("select (name) from organs where name = '{}'".format(name))

            if checkOrgan["result"] and checkOrgan["data"] != 0:

                updateOrgan = self.db.query("update organs set listed = {} where name = '{}'".format(listed, name))

                if not updateOrgan["result"]:
                    
                    log.error(f'{{additionalInfo: {{"organ":{name}, "listed":{listed}}}}}')

                else:

                    updateOrgan["data"] = "Successful"

                result = updateOrgan




            elif checkOrgan["result"] == False:

                result = checkOrgan

                log.error(f'{{additionalInfo: {{"organ":{name}, "listed":{listed}}}}}')

            
            elif checkOrgan["result"] and len(checkOrgan["data"]) == 0:

                result = {"result":False, "data":"Organ Not Present"}



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

                if not getOrgans["result"]:
                    
                    log.error(f'{{additionalInfo: {{"organ":{name}, "listed":{listed}}}}}')

                    
                result = getOrgans
                

            elif listed != None:

                getListed = self.db.query("select (name) from organs where listed = {}".format(listed))

                if not getListed["result"]:

                    log.error(f'{{additionalInfo: {{"organ":{name}, "listed":{listed}}}}}')

                result = getListed

        
        return result

                    
            


    def create(self, name:str = None, listed:int = 1)-> dict:

        """
        Function For addition of organs 
        
        Parameters:
            name(str): Name of organ to be added
            listed(int):0/1 default 1

        Returns
            result(dict) = {"result":True/False, "data":"SuccessFul/ErrorCode"}

        
        """

        result = {"result":False, "data":"Please Provide Organ Name"}

        if name != None:

            organCheck = self.db.query("select (name) from organs where name = '{}'".format(name))

            if organCheck["result"] and len(organCheck["data"]) == 0:

                organAdd = self.db.query("insert into organs (name, listed) values ('{}', {})".format(name, listed))

                if organAdd["result"]:

                    result = {"result":True, "data":"Successful"}


                else:

                    result = organAdd


            elif organCheck["result"] == False:

                result = organCheck

                log.error(f'{{additionalInfo: {{"organ":{name}, "listed":{listed}}}}}')


            else:

                result = {"result":False, "data":"Organ Already Present"}

        
        return result

            

#print(organs().create(name="kidney"))
#print(organs().create(name="Heart"))

#print(organs().read(listed=1))
#print(organs().update(name="kidney", listed=1))
#print(organs().delete(name="Heart"))


    
