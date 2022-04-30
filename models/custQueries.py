from inspect import Parameter

from requests import delete
import base, logging as log, json
from uty import uty



class custQueries( uty ):

    def __init__(self) -> None:
        uty.__init__(self)
        self.db = self.db()


    def delete(self, id:int):

        """
        Function for deleteing Queries

        Parameters:
            id(int):id of Queries

        Results:
            result(dict):      {"result":True/False, "data":"Successful/Error Code"}
        
        """
            
        deleteQuery = self.db.query("delete from custQueries where id = {}".format(id))

        if deleteQuery["result"]:

            deleteQuery["data"] = "Successful"
            log.info(f'{{Query_Delete_Successful:{{id:{id}}}}}')


        else:
            
            log.error(f'{{Query_Delete_Error:{{id:{id}}}}}')

        
        return deleteQuery



    def update(self, id:int = None, custName:str = None, custEmail:str = None, phoneNumber:str = None,\
              particularName:str = None, particularId:str = None, particularSec:float = None,\
              payment:str = None, status:str = None, reportLink:str = None) -> dict:

        """
            Function for reading booked queries
        Parameters:
            *id:int = id of the query
            *custName:str = Name of the customer,
            *custEmail:str = Email of the customer,
            *phoneNumber:str = Mobile number of the customer,
            *particularName:str = Name of the Test/Package,
            *particularId:str = Id of the Test/Packages,
            *particularSec:float = sec of the Service test:0/Package:1,
            *payment:str = payment Status of the query,
            *status:str = "INITIALIZED" status of the query,
            *reportLink:str = "Link of the report" 
        
        Returns:
            {"result":True/False, "data:"Successful"/"Error"}
        
        *mandatory
        
        """


        try:

            result = {"result":False, "data":"Please Provide Id"}

            queryCheck = self.read(id = id)

            if queryCheck["result"] and len(queryCheck["data"]) != 0:

                parameters = {"id":id,
                              "custName":custName,
                              "custEmail":custEmail,
                              "phoneNumber":phoneNumber,
                              "particularName":particularName,
                              "particularId":particularId,
                              "particularSec":particularSec,
                              "payment":payment,
                              "status":status,
                              "reportLink":reportLink}
             
                
                updateQuery = self.updateQuery(parameters=parameters, table="custQueries") + " where id = {}".format(id)

                print(updateQuery)

                updateQuery = self.db.query(updateQuery)

                if updateQuery["result"]:

                    updateQuery["data"] = "Successful"

                    log.info(f'{{custQuery_Successful:  {updateQuery}}}')

                else:
                    log.error(f'{{"custQuery_Query_Error":{{id:{id}, custName:{custName}, custEmail:{custEmail}, phoneNumber:{phoneNumber}, particularName:{particularName}, particularId:{particularId}, particularSec:{particularSec}, payment:{payment}, status:{status}, reportLink:{reportLink}}}}}')

                
                result = updateQuery

            elif queryCheck["result"] == False:

                result = queryCheck
                log.error(f'{{"custQuery_Query_Error":{{id:{id}, custName:{custName}, custEmail:{custEmail}, phoneNumber:{phoneNumber}, particularName:{particularName}, particularId:{particularId}, particularSec:{particularSec}, payment:{payment}, status:{status}, reportLink:{reportLink}}}}}')

                

            else:

                result = {"result":False, "data":"Culture Not Present"}
                log.warning(f'{{"custQuery_Not_Presnt":{{id:{id}, custName:{custName}, custEmail:{custEmail}, phoneNumber:{phoneNumber}, particularName:{particularName}, particularId:{particularId}, particularSec:{particularSec}, payment:{payment}, status:{status}, reportLink:{reportLink}}}}}')

        
        
        except Exception as e:

            log.warning(f'{{"custQuery_Update_function_Error_103":{{id:{id}, custName:{custName}, custEmail:{custEmail}, phoneNumber:{phoneNumber}, particularName:{particularName}, particularId:{particularId}, particularSec:{particularSec}, payment:{payment}, status:{status}, reportLink:{reportLink}}}}}')

            




        return result




    def read(self, id:int = None, custName:str = None, custEmail:str = None, phoneNumber:str = None,\
             particularName:str = None, particularId:str = None, particularSec:float = None,\
             payment:str = None, status:str = None, reportLink:str = None, bookedTime:str = None) -> dict:



        """
            Function for reading booked queries
        Parameters:
            id:int = id of the query
            custName:str = Name of the customer,
            custEmail:str = Email of the customer,
            phoneNumber:str = Mobile number of the customer,
            particularName:str = Name of the Test/Package,
            particularId:str = Id of the Test/Packages,
            particularSec:float = sec of the Service test:0/Package:1,
            payment:str = payment Status of the query,
            status:str = "INITIALIZED" status of the query,
            reportLink:str = "Link of the report" 
            bookedTime:time = "Time of booking"
        Returns:
            {"result":True/False, "data:"Successful"/"Error"}
            

        """

        result = {"result":False, "data":"Packages - 102"}

        try:

            parameters = {"id":id,
             "custName":custName,
             "custEmail":custEmail,
             "phoneNumber":phoneNumber,
             "particularName":particularName,
             "particularId":particularId,
             "particularSec":particularSec,
             "payment":payment,
             "status":status,
             "reportLink":reportLink,
             "bookedTime":bookedTime}

    
            searchQuery = self.makeQuery(parameters=parameters, table="custQueries")[:-1] + " order by bookedTime DESC"

                            #removing ; and adding arrangement parameter

            
            queryResult = self.db.query(searchQuery)

            if queryResult["result"]:

                log.info(f'{{custQueries_Read_Successful:  {queryResult}}}')

            else:

                log.error(f'{{"custQueries_Read_Error":{{id:{id}, bookedTime:{bookedTime}, custName:{custName}, custEmail:{custEmail}, phoneNumber:{phoneNumber}, particularName:{particularName}, particularId:{particularId}, particularSec:{particularSec}, payment:{payment}, status:{status}, reportLink:{reportLink}}}}}')


            result = queryResult


        except Exception as e:

            
            log.error(f'{{"custQueries_Function_Error_102":{{id:{id}, bookedTime:{bookedTime}, custName:{custName}, custEmail:{custEmail}, phoneNumber:{phoneNumber}, particularName:{particularName}, particularId:{particularId}, particularSec:{particularSec}, payment:{payment}, status:{status}, reportLink:{reportLink}}}}}')




        return result


    def create(self, custName:str, custEmail:str, phoneNumber:str, particularName:str, particularId:str,\
               particularSec:float,  payment:str, status:str = "INITIALIZED", reportLink:str = "") -> dict:

        """
        
        Function for creating booking queries
        Parameters:
            custName:str = Name of the customer,
            custEmail:str = Email of the customer,
            phoneNumber:str = Mobile number of the customer,
            particularName:str = Name of the Test/Package,
            particularId:str = Id of the Test/Packages,
            particularSec:float = sec of the Service test:0/Package:1,
            payment:str = payment Status of the query,
            status:str = "INITIALIZED" status of the query,
            reportLink:str = "Link of the report" 
        Returns:
            {"result":True/False, "data:"Successful"/"Error"}



        """

        result = {"result":False, "data":"custQueries - 101"}

        try:

            custQuery = self.db.query("insert into custQueries (custName, custEmail, phoneNumber, particularName,\
                                            particularId, particularSec, payment, status, reportLink) values \
                                        ('{}', '{}', '{}', '{}', {}, {}, '{}', '{}', '{}');".format(
                                            custName, custEmail, phoneNumber, particularName,\
                                            particularId, particularSec, payment, status, reportLink))

            if custQuery["result"]:

                custQuery["data"] = "Successful"
                log.info(f'{{"custQueries_Create_Error":{{custName:{custName}, custEmail:{custEmail}, phoneNumber:{phoneNumber}, particularName:{particularName}, particularId:{particularId}, particularSec:{particularSec}, payment:{payment}, status:{status}, reportLink:{reportLink}}}}}')

            else:

                log.error(f'{{"custQueries_Create_Error":{{custName:{custName}, custEmail:{custEmail}, phoneNumber:{phoneNumber}, particularName:{particularName}, particularId:{particularId}, particularSec:{particularSec}, payment:{payment}, status:{status}, reportLink:{reportLink}}}}}')

            result = custQuery 


        except Exception as e:

            log.error(f'{{"custQueries_Create_Function_Error_101":{{custName:{custName}, custEmail:{custEmail}, phoneNumber:{phoneNumber}, particularName:{particularName}, particularId:{particularId}, particularSec:{particularSec}, payment:{payment}, status:{status}, reportLink:{reportLink}}}}}')


        return result



        #insertQuery = self.db.query()


        #print(insertQuery)



"""

print(custQueries().create(custName = "shivam", custEmail="shivamswims456@gmail.com", phoneNumber="9693432136",
                     particularName = "K.F.T_1", particularId = 1, particularSec = 1, payment = "C.O.D",
                     status = "INTIALIZED", reportLink = ""))
    

print(custQueries().update(id = 1, custName = "shivam1", custEmail="shivamswims456@gmail.com", phoneNumber="9693432136",
                     particularName = "K.F.T_1", particularId = 1, particularSec = 1, payment = "C.O.D",
                     status = "INTIALIZED", reportLink = ""))



print(custQueries().read(id=1))
print(custQueries().delete(id=1))
print(custQueries().read(id=1))

"""