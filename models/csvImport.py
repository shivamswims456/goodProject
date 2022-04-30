import base, csv, os, logging as log
from cultures import cultures

class csvHelper( object ):

    """ 
        Excpected index of file
    """

    def __init__(self) -> None:
        self.insertObject = []
        self.cultures = cultures()


    def insert(self, filePath:str) -> dict:

        """
        Intended for inserting csv file to database (cultures) table
        expected index

        

        [0]Test Name(str) -> name      
        [1]Components(list) -> components 
        [2]MRP(float) -> price 
        [3]Specimen(str) -> speciment 
        [4]TurnAround Time(str) -> deliveryTime 
        [5]Run Days(str) -> runTime 
        [6]Section(str) -> section 
        [7]Pre Test Condition(list) -> preTest
        [8]illness/situations for which Test is prescribed(list) -> conditions 
        [9]Common name of Test(list) -> assocaitedNames
        [10]Organ/Body Part(list) -> organs   


        parameter:
            filePath(str) = path of file to be inserted

        result:

            result(dict) = {"result":True/False, "data":"successful/errorReason"}

        """

        result = {"result":False, "data":"File Not Exists"}

        if os.path.exists(filePath):

            log.info(f'{{"csvImport_FileRead_Success":{{"filePath":{filePath}}}}}')

            with open(filePath, "r") as f:

                csvList = list(csv.reader(f))

                counterRow = 6

                i = 10

                temp = []

                for row in csvList[1:]:
                    
                    if len(temp) != 0 and temp[0] != "" and row[counterRow] != "":

                        temp += [len(temp[1]), 0, [834001, 834002], 1, 0, ""]


                        self.cultures.create(name=temp[0], deliveryTime = temp[4], price = temp[2], pincodesAvailable = temp[13], assoicatedNames = temp[9],\
                                             preTest=temp[7], components = temp[1], conditions = temp[8], listed = temp[14], homePage = temp[15], specimen = temp[16],\
                                             runTime = temp[5], section = temp[6], discountPrice = 0)

                        

                    if row[counterRow] != "":

                        temp = ["", [], "", "", "", "", "", [], [], [], []] 
                        

                        for index, each in enumerate(row):

                     
                            if temp[index] == "":

                                temp[index] = each.replace("\n", "")

                            else:

                                temp[index].append(each.replace("\n", ""))



                    else:

                        for index, each in enumerate(row):

                            if type(temp[index]) == list and each != "":

                                temp[index].append(each.replace("\n", ""))


        else:

            log.error(f'{{"csvImport_FileRead_Failed":{{"filePath":{filePath}}}}}')

        

csvHelper().insert(filePath= r"C:\Users\Dell\Desktop\goodProject\goodProject\storage\admin\finalDatabaseDoc.csv")

"""
print(cultures().create( name="K.F.T", deliveryTime="1 Day", discountPrice=200, price = 800, pincodesAvailable = ["834001", "834002", "834003"], organs = ["kidney"],\
                         assoicatedNames = ["Kidney Function Test"], preTest="Empty Stomach",\
                         components=["CBC", "RBC"], conditions=["Dibetise"], listed = 1,\
                         homePage = 0, specimen = "blood", runTime="1day", section="hemotology"
))   

"""