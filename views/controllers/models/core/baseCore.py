import os
from dotenv import load_dotenv

class base( object ):

    def __init__(self) -> None:

        load_dotenv()

        self.parseEnv()


    def getEnv(self, key):

        return self.env.get(key.upper(), None)



    def parseEnv(self):
        
        self.env = {}

        for each in os.environ:

            val = os.getenv(each)

            if val == "true":

                self.env[each] = True

            elif val == "false":

                self.env[each] = False

            else:

                self.env[each] = val


#print(os.listdir(base().getEnv("staticPath")), os.getcwd())