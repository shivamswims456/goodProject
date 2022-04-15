import base, logging as log, json
from uty import uty
from pincodes import pincodes
from conditions import conditions
from organs import organs


class cultures( uty ):

    def __init__(self):

        uty.__init__(self)

        self.db = self.db()

        self.pin = pincodes()

        self.cod = conditions()
        self.org = organs()



    def update(self, id:int, name:str = None, deliveryTime:str = None, discountPrice:list = None, price:float = None,\
                pincodesAvailable:list = None, organs:list = [], assoicatedNames:list = [], numberOfParameters = None,\
                components:list = [], conditions:list = [], listed:int = None, homePage:int = None, preTest:str = None):


        """

            Function updates cultures based on id of culture

            Parameters:
                *id(int)            :id of Culture
                name(str)          :Name of the test
                deliveryTime(str)  :Time it would require to get Delivered
                price(float)       :cost of test
                discount(float)    :discount given of test
                pincodesAvailable(list) :list of pincodes for which the services are available
                numberOfParameters :total numner of parametrs under test

                components(list)   :list of components included in tests
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

        try:


            for pin in pincodesAvailable:

                self.pin.create(pincode = pin)

            
            for condition in conditions:

                self.cod.create(cond = condition)


            for organ in organs:

                self.org.create(name = organ)


            numberOfParameters = len(components)
            pincodesAvailable = json.dumps(pincodesAvailable)
            conditions        = json.dumps(conditions)
            organs            = json.dumps(organs)
            assoicatedNames   = json.dumps(assoicatedNames)
            components        = json.dumps(components)

            parameters = {"name":name,
                        "deliveryTime":deliveryTime,
                        "components":components,
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


            updateQuery = self.updateQuery(parameters=parameters, table="cultures") + " where id = {}".format(id)

            if updateQuery["result"]:

                result = updateQuery
                log.info(f'culture(s)_updated ->  {updateQuery}')

            else:

                log.error(f'cultures - 107 ->  {{name:{str(name)}, deliveryTime:{str(deliveryTime)}, components:{str(components)}, assoicatedNames:{str(assoicatedNames)}, numberOfParameters:{str(numberOfParameters)}, preTest:{str(preTest)}, price:{str(price)}, discountPrice:{str(discountPrice)}, pincodesAvailable:{str(pincodesAvailable)}, organs:{str(organs)}, conditions:{str(conditions)}, listed:{str(listed)}, homePage:{str(homePage)}}}')


        except Exception as e:

            log.error(f'cultures - 108 ->  {{name:{str(name)}, deliveryTime:{str(deliveryTime)}, components:{str(components)}, assoicatedNames:{str(assoicatedNames)}, numberOfParameters:{str(numberOfParameters)}, preTest:{str(preTest)}, price:{str(price)}, discountPrice:{str(discountPrice)}, pincodesAvailable:{str(pincodesAvailable)}, organs:{str(organs)}, conditions:{str(conditions)}, listed:{str(listed)}, homePage:{str(homePage)}}}')




    def read(self, id:int=None, name:str = None, deliveryTime:str = None, discountPrice:list = None, price:float = None,\
             pincodesAvailable:list = None, organs:list = [], assoicatedNames:list = [], numberOfParameters = None,\
             components:list = [], conditions:list = [], listed:int = None, homePage:int = None, preTest:str = None):



        """
            Function reads out cultures based on intersections of parameters passed

            Parameters:
                id(int)            :id of Culture
                name(str)          :Name of the test
                deliveryTime(str)  :Time it would require to get Delivered
                price(float)       :cost of test
                discount(float)    :discount given of test
                pincodesAvailable(list) :list of pincodes for which the services are available
                numberOfParameters :total numner of parametrs under test

                components(list)   :list of components included in tests
                preTest(str)       :this is a description of what you should be like before test
                organs(list)       :list of organs related to tests
                conditions(list)   :list of disease or conditions for which test is required
                listed(int)        :is this test listed for indenpent booking - default 1
                homePage(int)      :will this test show on homePage - default 0
                associatedNames(list)   :list of names that resonate with the tests
                

            Results:
                result(dict):      {"result":True/False, "data":"Successful/Error Code"}

            

        """

        try:

    
            parameters = {"name":name,
                        "deliveryTime":deliveryTime,
                        "components":components,
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

            

            searchQuery = self.makeQuery(parameters=parameters, table="cultures")

            
            queryResult = self.db.query(searchQuery)

            if queryResult["result"]:

                result = queryResult
                log.info(f'culture(s)_queried ->  {queryResult}')

            else:

                log.error(f'cultures - 103 ->  {{name:{str(name)}, deliveryTime:{str(deliveryTime)}, components:{str(components)}, assoicatedNames:{str(assoicatedNames)}, numberOfParameters:{str(numberOfParameters)}, preTest:{str(preTest)}, price:{str(price)}, discountPrice:{str(discountPrice)}, pincodesAvailable:{str(pincodesAvailable)}, organs:{str(organs)}, conditions:{str(conditions)}, listed:{str(listed)}, homePage:{str(homePage)}}}')


        except Exception as e:

            log.error(f'cultures - 104 ->  {{name:{str(name)}, deliveryTime:{str(deliveryTime)}, components:{str(components)}, assoicatedNames:{str(assoicatedNames)}, numberOfParameters:{str(numberOfParameters)}, preTest:{str(preTest)}, price:{str(price)}, discountPrice:{str(discountPrice)}, pincodesAvailable:{str(pincodesAvailable)}, organs:{str(organs)}, conditions:{str(conditions)}, listed:{str(listed)}, homePage:{str(homePage)}}}')




        return result



        

    def create(self, name:str, deliveryTime:str, discountPrice:float, price:float,\
               pincodesAvailable:list, organs:list = [], assoicatedNames:list = [],\
               components:list = [], conditions:list = [], listed:int = 1,\
               homePage:int = 0, preTest:str = "") -> dict:

        """
            Function for creating tests, these tests can be the test that are
            individual and also those that are going to be placed in packages
            as test valirants, if provided sub info dosn'e exists in there relative 
            tables values are inserted

            Parameters:
                *name(str)          :Name of the test
                *deliveryTime(str)  :Time it would require to get Delivered
                *price(float)       :cost of test
                *discount(float)    :discount given of test
                *pincodesAvailable(list) :list of pincodes for which the services are available

                components(list)   :list of components included in tests
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


        result = {"result":False, "data":"Cultures - 101"}

        try:


            for pin in pincodesAvailable:

                self.pin.create(pincode = pin)

            
            for condition in conditions:

                self.cod.create(cond = condition)


            for organ in organs:

                self.org.create(name = organ)


            numberOfParameters = len(components)
            pincodesAvailable = json.dumps(pincodesAvailable)
            conditions        = json.dumps(conditions)
            organs            = json.dumps(organs)
            assoicatedNames   = json.dumps(assoicatedNames)
            components        = json.dumps(components)


            cultureCreate = self.db.query("insert into cultures (name, deliveryTime, components, assoicatedNames, numberOfParameters, preTest, price,\
                                           discountPrice, pincodesAvailable, organs, conditions,  listed, homePage) values \
                                          ('{}', '{}', '{}', '{}', {}, '{}', {}, {}, '{}', '{}', '{}', {}, {})".format(
                                           name, deliveryTime, components, assoicatedNames, numberOfParameters, preTest, price,
                                           discountPrice, pincodesAvailable, organs, conditions, listed, homePage))

            if cultureCreate["result"]:

                cultureCreate["data"] = "Successful"
                log.info(f'culture_created ->  {{name:{str(name)}, deliveryTime:{str(deliveryTime)}, components:{str(components)}, assoicatedNames:{str(assoicatedNames)}, numberOfParameters:{str(numberOfParameters)}, preTest:{str(preTest)}, price:{str(price)}, discountPrice:{str(discountPrice)}, pincodesAvailable:{str(pincodesAvailable)}, organs:{str(organs)}, conditions:{str(conditions)}, listed:{str(listed)}, homePage:{str(homePage)}}}')

            else:

                log.error(f'cultures 101 ->  {{name:{str(name)}, deliveryTime:{str(deliveryTime)}, components:{str(components)}, assoicatedNames:{str(assoicatedNames)}, numberOfParameters:{str(numberOfParameters)}, preTest:{str(preTest)}, price:{str(price)}, discountPrice:{str(discountPrice)}, pincodesAvailable:{str(pincodesAvailable)}, organs:{str(organs)}, conditions:{str(conditions)}, listed:{str(listed)}, homePage:{str(homePage)}}}')


        except Exception as e:

            log.error(f'cultures - 102 ->  {{name:{str(name)}, deliveryTime:{str(deliveryTime)}, components:{str(components)}, assoicatedNames:{str(assoicatedNames)}, numberOfParameters:{str(numberOfParameters)}, preTest:{str(preTest)}, price:{str(price)}, discountPrice:{str(discountPrice)}, pincodesAvailable:{str(pincodesAvailable)}, organs:{str(organs)}, conditions:{str(conditions)}, listed:{str(listed)}, homePage:{str(homePage)}}}')




        return cultureCreate




    



"""
cultures().create( name="K.F.T", deliveryTime="1 Day", discountPrice=200, price = 800, pincodesAvailable = ["834001", "834002", "834003"], organs = ["kidney"],\
                assoicatedNames = ["Kidney Function Test"], preTest="Empty Stomach",\
               components=["CBC", "RBC"], conditions=["Dibetise"], listed = 1,\
               homePage = 0
)        
"""

cultures().update(id=1, name="K.F.T", deliveryTime="1 Day", discountPrice=200, price = 800, pincodesAvailable = ["834001", "834002", "834003"], organs = ["kidney"],\
                assoicatedNames = ["Kidney Function Test"], preTest="Empty Stomach",\
               components=["CBC", "RBC"], conditions=["Dibetise"], listed = 1,\
               homePage = 0
)

#cultures().read(name="K.F.T", pincodesAvailable=["834001"])









