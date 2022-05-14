import json, logging as log
from models.core.server import baseHandler
from models.pincodes import pincodes

pin = pincodes()

class areaPrice( baseHandler ):

    def post(self):

        pincode = self.get_argument("pincode")

        self.write(json.dumps(pin.read(pincode = pincode)));
