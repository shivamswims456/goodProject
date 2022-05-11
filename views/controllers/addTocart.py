import json, logging as log
from models.core.server import baseHandler

class addToCart( baseHandler ):

    
    def post(self):

        try:
            
            id = self.get_argument("id", None)
            pack = self.get_argument("pack", None)
            nature = self.get_argument("nature", None)
            cart = self.get_secure_cookie("cart")


            if cart == None:

                cart = "[]"

            cart = set(json.loads(cart))

            if nature == "add":
            
                cart.add(id)

                result = {"result":True, "data":{"count":len(cart)}}

            elif nature == "remove":

                cart.remove(id)

                result = {"result":True, "data":{"count":cart}}

            elif nature == "count":

                result = {"result":True, "data":{"count":len(cart)}}


            cart = list(cart)

            self.set_secure_cookie("cart", json.dumps(cart))

            
            
            

        except Exception as e:

            result = {"result":False, "data":"cartCookieSetError"}

            log.error(f'{{CookieSetError:{{"id":{self.get_argument("id")}, "pack":{self.get_argument("pack")},  "nature":{self.get_argument("nature")} }}}}')


        self.write(json.dumps(result))

