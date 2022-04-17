from turtle import update
import base
from uty import uty 
from cultures import cultures
import json, logging as log

class packages( uty ):

    def __init__(self):

        uty.__init__(self)
        self.cultures = cultures()
        self.pin = self.cultures.pin
        self.cod = self.cultures.cod
        self.org = self.cultures.org
        self.db = self.db()

    def delete(self, id:int):

        """
        Function for deleteing Packages

        Parameters:
            id(int):id of Packages

        Results:
            result(dict):      {"result":True/False, "data":"Successful/Error Code"}
        
        """
            
        deleteQuery = self.db.query("delete from packages where id = {}".format(id))

        if deleteQuery["result"]:

            deleteQuery["data"] = "Successful"
            log.info(f'{{Packages_Delete_Successful:{{id:{id}}}}}')


        else:
            
            log.error(f'{{Packages_Delete_Error:{{id:{id}}}}}')

        
        return deleteQuery

    
    
    def update(self, id:int, name:str = None, deliveryTime:str = None, discountPrice:list = None, price:float = None,\
                pincodesAvailable:list = None, organs:list = [], assoicatedNames:list = [], numberOfParameters = None,\
                cultures:list = [], conditions:list = [], listed:int = None, homePage:int = None, preTest:list = []) -> dict:


        """

            Function updates packages based on id of culture

            Parameters:
                *id(int)            :id of Culture
                *name(str)          :Name of the test
                *deliveryTime(str)  :Time it would require to get Delivered
                *price(float)       :cost of test
                *discount(float)    :discount given of test
                *pincodesAvailable(list) :list of pincodes for which the services are available
                *numberOfParameters :total numner of parametrs under test

                *cultures(list)     :list of cultures included in tests
                *preTest(list)      :list of this is a description of what you should be like before test
                *organs(list)       :list of organs related to tests
                *conditions(list)   :list of disease or conditions for which test is required
                *listed(int)        :is this test listed for indenpent booking - default 1
                *homePage(int)      :will this test show on homePage - default 0
                *associatedNames(list)   :list of names that resonate with the tests
                

            Results:
                result(dict):      {"result":True/False, "data":"Successful/Error Code"}

            *mandatory
        
        """

        try:

            result = {"result":False, "data":"Please Provide Id"}

            cultureCheck = self.read(id = id)

            if cultureCheck["result"] and len(cultureCheck["data"]) != 0:


                for pin in pincodesAvailable:

                    self.pin.create(pincode = pin)



                
                for condition in conditions:

                    self.cod.create(cond = condition)


                for organ in organs:

                    self.org.create(name = organ)



                numberOfParameters = len(cultures)
                pincodesAvailable = json.dumps(pincodesAvailable)
                conditions        = json.dumps(conditions)
                organs            = json.dumps(organs)
                assoicatedNames   = json.dumps(assoicatedNames)
                cultures          = json.dumps(cultures)
                preTest          = json.dumps(preTest)

                parameters = {"name":name,
                            "deliveryTime":deliveryTime,
                            "cultures":cultures,
                            "assoicatedNames":assoicatedNames,
                            "numberOfParameters":numberOfParameters,
                            "preTest":preTest,
                            "price":price,
                            "discountPrice":discountPrice,
                            "pincodesAvailable":pincodesAvailable,
                            "organs":organs,
                            "conditions":conditions,
                            "listed":listed,
                            "homePage":homePage,
                            "id":id}


                
                updateQuery = self.updateQuery(parameters=parameters, table="packages") + " where id = {}".format(id)

                print(updateQuery)

                updateQuery = self.db.query(updateQuery)

                if updateQuery["result"]:

                    updateQuery["data"] = "Successful"

                    log.info(f'{{Packages_Update_Successful:  {updateQuery}}}')

                else:

                    log.error(f'{{Packages_Update_Query_Error: {{name:{str(name)}, deliveryTime:{str(deliveryTime)}, cultures:{str(cultures)}, assoicatedNames:{str(assoicatedNames)}, numberOfParameters:{str(numberOfParameters)}, preTest:{str(preTest)}, price:{str(price)}, discountPrice:{str(discountPrice)}, pincodesAvailable:{str(pincodesAvailable)}, organs:{str(organs)}, conditions:{str(conditions)}, listed:{str(listed)}, homePage:{str(homePage)}}}}}')

                
                result = updateQuery

            elif cultureCheck["result"] == False:

                result = cultureCheck

                log.error(f'{{Packages_Update_Query_Error:  {{name:{str(name)}, deliveryTime:{str(deliveryTime)}, cultures:{str(cultures)}, assoicatedNames:{str(assoicatedNames)}, numberOfParameters:{str(numberOfParameters)}, preTest:{str(preTest)}, price:{str(price)}, discountPrice:{str(discountPrice)}, pincodesAvailable:{str(pincodesAvailable)}, organs:{str(organs)}, conditions:{str(conditions)}, listed:{str(listed)}, homePage:{str(homePage)}}}}}')

            else:

                result = {"result":False, "data":"Culture Not Present"}

                log.warning(f'{{Packages_Update_Not_Presnt:  {{name:{str(name)}, deliveryTime:{str(deliveryTime)}, cultures:{str(cultures)}, assoicatedNames:{str(assoicatedNames)}, numberOfParameters:{str(numberOfParameters)}, preTest:{str(preTest)}, price:{str(price)}, discountPrice:{str(discountPrice)}, pincodesAvailable:{str(pincodesAvailable)}, organs:{str(organs)}, conditions:{str(conditions)}, listed:{str(listed)}, homePage:{str(homePage)}}}}}')
        
        
        
        except Exception as e:

            log.error(f'{{Packages_Update_Function_Error_2:  {{name:{str(name)}, deliveryTime:{str(deliveryTime)}, cultures:{str(cultures)}, assoicatedNames:{str(assoicatedNames)}, numberOfParameters:{str(numberOfParameters)}, preTest:{str(preTest)}, price:{str(price)}, discountPrice:{str(discountPrice)}, pincodesAvailable:{str(pincodesAvailable)}, organs:{str(organs)}, conditions:{str(conditions)}, listed:{str(listed)}, homePage:{str(homePage)}}}}}')




        return result


    def read(self, id:int=None, name:str = None, deliveryTime:str = None, discountPrice:list = None, price:float = None,\
             pincodesAvailable:list = None, organs:list = [], assoicatedNames:list = [], numberOfParameters = None,\
             cultures:list = [], conditions:list = [], listed:int = None, homePage:int = None, preTest:str = None) -> dict:



        """
            Function reads out packages based on intersections of parameters passed

            Parameters:
                id(int)            :id of Culture
                name(str)          :Name of the test
                deliveryTime(str)  :Time it would require to get Delivered
                price(float)       :cost of test
                discount(float)    :discount given of test
                pincodesAvailable(list) :list of pincodes for which the services are available
                numberOfParameters :total numner of parametrs under test

                cultures(list)   :list of cultures included in tests
                preTest(str)       :this is a description of what you should be like before test
                organs(list)       :list of organs related to tests
                conditions(list)   :list of disease or conditions for which test is required
                listed(int)        :is this test listed for indenpent booking - default 1
                homePage(int)      :will this test show on homePage - default 0
                associatedNames(list)   :list of names that resonate with the tests
                

            Results:
                result(dict):      {"result":True/False, "data":"Successful/Error Code"}

            

        """

        result = {"result":False, "data":"Packages - 102"}

        try:

    
            parameters = {"name":name,
                          "deliveryTime":deliveryTime,
                          "cultures":cultures,
                          "assoicatedNames":assoicatedNames,
                          "numberOfParameters":numberOfParameters,
                          "preTest":preTest,
                          "price":price,
                          "discountPrice":discountPrice,
                          "pincodesAvailable":pincodesAvailable,
                          "organs":organs,
                          "conditions":conditions,
                          "listed":listed,
                          "homePage":homePage,
                          "id":id}

            

            searchQuery = self.makeQuery(parameters=parameters, table="packages")

            
            queryResult = self.db.query(searchQuery)

            if queryResult["result"]:

                #converting json to dataType

                for index, each in enumerate(queryResult["data"]):

                    queryResult["data"][index][2] = json.loads(queryResult["data"][index][2])
                    queryResult["data"][index][3] = json.loads(queryResult["data"][index][3])
                    queryResult["data"][index][8] = json.loads(queryResult["data"][index][8])
                    queryResult["data"][index][9] = json.loads(queryResult["data"][index][9])
                    queryResult["data"][index][10] = json.loads(queryResult["data"][index][10])
                    

                result = queryResult
                log.info(f'{{Packages_Read_Successful:  {queryResult}}}')

            else:

                log.error(f'{{Packages_Create_Query_Error:  {{name:{str(name)}, deliveryTime:{str(deliveryTime)}, cultures:{str(cultures)}, assoicatedNames:{str(assoicatedNames)}, numberOfParameters:{str(numberOfParameters)}, preTest:{str(preTest)}, price:{str(price)}, discountPrice:{str(discountPrice)}, pincodesAvailable:{str(pincodesAvailable)}, organs:{str(organs)}, conditions:{str(conditions)}, listed:{str(listed)}, homePage:{str(homePage)}}}}}')


        except Exception as e:

            
            log.error(f'{{Packages_Function_Error_101:  {{name:{str(name)}, deliveryTime:{str(deliveryTime)}, cultures:{str(cultures)}, assoicatedNames:{str(assoicatedNames)}, numberOfParameters:{str(numberOfParameters)}, preTest:{str(preTest)}, price:{str(price)}, discountPrice:{str(discountPrice)}, pincodesAvailable:{str(pincodesAvailable)}, organs:{str(organs)}, conditions:{str(conditions)}, listed:{str(listed)}, homePage:{str(homePage)}}}}}')




        return result

     
    def create(self, name:str, deliveryTime:str, price:float, discountPrice:float, pincodesAvailable:list, cultures:list = None,\
               assoicatedNames:list = None, preTest:str = None,  organs:list = None, conditions:list = None, listed:int = None,\
               homePage:int = None ):

        """
                Function for creating packages, these packages assume that tests passed 
                are already create in Packages modules

                Parameters:
                    *name(str)          :Name of the test
                    *deliveryTime(str)  :Time it would require to get Delivered
                    *price(float)       :cost of test
                    *discount(float)    :discount given of test
                    *pincodesAvailable(list) :list of pincodes for which the services are available

                    Packages(list)     :list of Packages included in tests
                    preTest(str)       :this is a description of what you should be like before test
                    organs(list)       :list of organs related to tests
                    conditions(list)   :list of disease or conditions for which test is required
                    listed(int)        :is this test listed for indenpent booking - default 1
                    homePage(int)      :will this test show on homePage - default 0
                    associatedNames(list)   :list of names that resonate with the tests
                    

                Results:
                    result(dict):      {"result":True/False, "data":"Successful/Error Code"}

                *mandatory

            """


        result = {"result":False, "data":"Packages - 101"}

       
        try:

            numberOfParameters = 0
            preTest = set([preTest])
            


            for pin in pincodesAvailable:

                self.pin.create(pincode = pin)

            
            for condition in conditions:

                self.cod.create(cond = condition)


            for organ in organs:

                self.org.create(name = organ)


            culture = self.cultures.read(id=tuple(cultures))
            #lazy hack passing list against convetion of float
            #because programme test for data type and coverts 
            #where argument from '{}={}' to {} in () query 

            
            if culture["result"]:
                
                for cult in culture["data"]:

                    numberOfParameters += cult[4] #4 is the index of numberOfParameteres in read query in cultures modules
                    preTest.add(cult[5])#5 same index reason


            else:

                
                log.error(f'{{Packages_Culture_Read_Error:  {{name:{str(name)}, deliveryTime:{str(deliveryTime)}, cultures:{str(cultures)}, assoicatedNames:{str(assoicatedNames)}, numberOfParameters:{str(numberOfParameters)}, preTest:{str(preTest)}, price:{str(price)}, discountPrice:{str(discountPrice)}, pincodesAvailable:{str(pincodesAvailable)}, organs:{str(organs)}, conditions:{str(conditions)}, listed:{str(listed)}, homePage:{str(homePage)}}}}}')

                
            

            preTest = list(preTest)
            
            
            pincodesAvailable = json.dumps(pincodesAvailable)
            conditions        = json.dumps(conditions)
            organs            = json.dumps(organs)
            assoicatedNames   = json.dumps(assoicatedNames)
            cultures          = json.dumps(cultures)
            preTest           = json.dumps(preTest)


            packageCreate = self.db.query("insert into packages (name, deliveryTime, cultures, assoicatedNames, numberOfParameters, preTest, price,\
                                           discountPrice, pincodesAvailable, organs, conditions,  listed, homePage) values \
                                          ('{}', '{}', '{}', '{}', {}, '{}', {}, {}, '{}', '{}', '{}', {}, {})".format(
                                           name, deliveryTime, cultures, assoicatedNames, numberOfParameters, preTest, price,
                                           discountPrice, pincodesAvailable, organs, conditions, listed, homePage))


            if packageCreate["result"]:

                packageCreate["data"] = "Successful"
                log.info(f'{{Packages_Create_Successful:  {{name:{str(name)}, deliveryTime:{str(deliveryTime)}, cultures:{str(cultures)}, assoicatedNames:{str(assoicatedNames)}, numberOfParameters:{str(numberOfParameters)}, preTest:{str(preTest)}, price:{str(price)}, discountPrice:{str(discountPrice)}, pincodesAvailable:{str(pincodesAvailable)}, organs:{str(organs)}, conditions:{str(conditions)}, listed:{str(listed)}, homePage:{str(homePage)}}}}}')

            else:

                log.error(f'{{Packages_Query_Error:  {{name:{str(name)}, deliveryTime:{str(deliveryTime)}, cultures:{str(cultures)}, assoicatedNames:{str(assoicatedNames)}, numberOfParameters:{str(numberOfParameters)}, preTest:{str(preTest)}, price:{str(price)}, discountPrice:{str(discountPrice)}, pincodesAvailable:{str(pincodesAvailable)}, organs:{str(organs)}, conditions:{str(conditions)}, listed:{str(listed)}, homePage:{str(homePage)}}}}}')

            
            result = packageCreate

        
        except Exception as e:

            log.error(f'{{Packages_Function_Error:  {{name:{str(name)}, deliveryTime:{str(deliveryTime)}, cultures:{str(cultures)}, assoicatedNames:{str(assoicatedNames)}, numberOfParameters:{str(numberOfParameters)}, preTest:{str(preTest)}, price:{str(price)}, discountPrice:{str(discountPrice)}, pincodesAvailable:{str(pincodesAvailable)}, organs:{str(organs)}, conditions:{str(conditions)}, listed:{str(listed)}, homePage:{str(homePage)}}}}}')

        return result
        

"""
print(packages().create(name = "Package1", deliveryTime="1_Day", price=300, discountPrice=150, pincodesAvailable=["834001", "834002"], cultures=[2],\
assoicatedNames = ["Package_test"], preTest="Empty Stomach",  organs=["Heart"],\
conditions=["Heart Failures"], listed=1, homePage=1))
"""

#packages().read(id=1)

"""
print(packages().update(id = 1, name = "Package_1", deliveryTime="1_Day", price=300, discountPrice=150, pincodesAvailable=["834001", "834002"], cultures=[2],\
assoicatedNames = ["Package_test"], preTest=["Empty Stomach"],  organs=["Heart"],\
conditions=["Heart Failures"], listed=1, homePage=1))
"""

#print(packages().delete(id=1))

