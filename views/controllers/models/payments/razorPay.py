from dotenv import load_dotenv
from requests import request


import os, logging as log, __init__ #to get things work locally and to import core
from core.db import db
import razorpay


class razorPay( object ):

    """ 
        Module intended for creating and storing razorpay payments
    """

    def __init__(self) -> None:
        
        load_dotenv()
        self.db = db()
        self.key = os.getenv("razorPayKey")
        self.secret = os.getenv("razorPaySecret")
        self.client = razorpay.Client(auth=(self.key, self.secret))



    def __update(self, paymentId:str, signature:str, status:str, orderId:str):

        storeQuery = self.db.query("update payments set paymentId = '{}', signatureId = '{}', status = '{}' where orderId = '{}';".format(paymentId, signature, status, orderId))

        if storeQuery["result"]:

            result = {"result":True, "data":"Successful"}
            log.info(f'{{"Razorpay_Order_update_Successful":{{"orderId":{orderId}, "status":{status}}}}}')

        else:

            result = storeQuery

            log.error(f'{{"Razorpay_Order_update_Error":{{"orderId":{orderId}, "status":{status}}}}}')

        return result


    def __store(self, name:str, amount:str, orderId:str, status:str="Pending"):

        storeQuery = self.db.query("insert into payments (name, amount, status, orderId) values ('{}', {}, '{}', '{}')".format(name, amount, status, orderId))

        if storeQuery["result"]:

            result = {"result":True, "data":"Successful"}
            log.info(f'{{"Razorpay_Order_Store_Successful":{{"name":{name}, "amount":{amount}, "orderId":{orderId}}}}}')

        else:

            result = storeQuery

            log.error(f'{{"Razorpay_Order_Store_Error":{{"name":{name}, "amount":{amount}, "orderId":{orderId}}}}}')

        return result


    def checkOrder(self, responseObj:dict ):

        """
            POST converted dict should be passed
        """


        
        if "razorpay_signature" in responseObj:
            paymentId = responseObj["razorpay_payment_id"]
            orderId = responseObj["razorpay_order_id"]


            signature = responseObj["razorpay_signature"]
            verified = self.client.utility.verify_payment_signature(responseObj)
            status = "Successful" if verified else "Failed"
            result = {"result":verified, "data":status}

        else:

            result = {"result":True, "data":"Failed"}

            #TODO:Check and update
            pass


        self.__update(paymentId=paymentId, signature=signature, orderId=orderId)

        return result





        




        


    
    def createOrder(self, name:str, amount:int, currency:str="INR"):

        result = {"result":False, "data":"Razorpay_Order_Create_Error"}

        try:

            order = self.client.order.create({"amount":int(amount)*100, "currency":currency, "payment_capture":"1"})

            self.__store(name = name, amount = amount, orderId = order["id"])

            result = {"result":True, "data":{"key":self.key, "order":order}}

            log.info(f'{{"Razorpay_Order_Store_Successful":{{"name":{name}, "amount":{amount}, "currency":{currency}, "orderId":{order["id"]}}}}}')

        except Exception as e:

            log.error(f'{{"Razorpay_Order_Store_Error":{{"name":{name}, "amount":{amount}, "currency":{currency}, "error":{e}}}}}')


        return result



#print(razorPay().createOrder(name="shivam", amount=9))