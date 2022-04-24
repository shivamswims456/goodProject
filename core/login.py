import logging as log, os, time
from db import db
from hashlib import sha256
from decimal import Decimal
from uuid import uuid4

class login( object ):


    """
        Programme assumes that users are loacted in table users
        with fields as follows
        +-------------+---------------+------+-----+---------+----------------+
        | Field       | Type          | Null | Key | Default | Extra          |
        +-------------+---------------+------+-----+---------+----------------+
        | id          | int           | NO   | PRI | NULL    | auto_increment |
        | userName    | varchar(50)   | YES  |     | NULL    |                |
        | password    | varchar(70)   | YES  |     | NULL    |                |
        | reset       | varchar(70)   | YES  |     | NULL    |                |
        | attempts    | int           | YES  |     | 0       |                |
        | lastAttempt | decimal(10,0) | YES  |     | 0       |                |
        +-------------+---------------+------+-----+---------+----------------+
        A database query function is generate via self.db

        A salt has been supplied via os.getenv with passwordSalt key

    """

    def __init__(self) -> None:
        
        self.db = db()


    def stringToPassword(self, password:str) -> dict:

        """
        Function for encrypting string to password
        Parameters
            1. password:plain string Password

        returns
            result = {"result":True/False, "data":"encString"/"ErrorCode"}

        """

        result = {"resulf":False, "data":"Func Error login 101"}

        try:

            password += os.getenv("passwordSalt")
            password = password.encode()

            result = {"result":True, "data":sha256(password).hexdigest()}



        except Exception as e:


            log.error(f'{{"login_matchPassword_Failed":{{"password":{password}}}}}')


        return result


    def resetCheck(self, reset:str, password:str, repeat:str)->dict:

        """
        Function for reseting password
        Parameters:
            usrName: naof the user whose password has to be resets
            reset: reset token extracted from truted source
            password: newPassword which has to be inserted
            repeat: newPassword which has to be inserted in repeat
        """

        if password == repeat:

            userSearch = self.db.query("select userName, reset from users where reset = '{}'".format(reset))

            if userSearch["result"]:

                if len(userSearch["data"]) != 0:

                    if reset == userSearch["data"][0][1]:

                        encPassword = self.stringToPassword(password)

                        if encPassword["result"]:

                            passwordUpdate = self.db.query("update users set reset = null, password = '{}' where userName = '{}';".format(encPassword["data"], userSearch["data"][0][0]))

                            if passwordUpdate["result"]:

                                passwordUpdate["data"] = "Successful"

                            else:

                                log.error(f'{{"login_query_Error":{{"reset":{reset}}}}}')

                            result = passwordUpdate



                        else:

                            result = encPassword

                            log.error(f'{{"login_enc_Error":{{"reset":{reset}}}}}')


                    else:

                        result = {"result":True, "data":"invalid Token"}




                else:

                    result = {"result":False, "data":"Invalid Request"}

                    log.warning(f'{{"login_reset_invalidToken":{{"reset":{reset}}}}}')


            else:

                result = userSearch
                log.error(f'{{"login_reset_queryFail":{{"reset":{reset}}}}}')

            

        else:

            result = {"result":False, "data":"Password and Repeat Passwords don't match"}


        return result




    def resetTrigger(self, userName:str)->dict:

        """
        Function for creating reset token
        Parameters:
            userName: name of the user whose trigger has to be reset

        Returns:
            reset: {"result":True/False, "data":"Successful"/"ErrorCode"}
        """

        getUsers = self.getUsers(userName=userName)

        if getUsers["result"]:
            
            qString = self.stringToPassword(str(uuid4()))

            if qString["result"]:



                updateQuery = self.db.query("update users set reset = '{}' where userName = '{}'".format(qString["data"], userName ))

                
                if updateQuery["result"]:

                    result = {"result":True, "data":qString}
                    log.error(f'{{"login_reset_trigger_successful":{{"userName":{userName}}}}}')

                else:

                    result = updateQuery
                    log.error(f'{{"login_resetTrigger_update_Error":{{"userName":{userName}}}}}')

            else:

                result = qString


        else:

            result = getUsers
            
            log.error(f'{{"login_resetTrigger_getUser_Error":{{"userName":{userName}}}}}')


        return result






    def matchPassword(self, userName:str, password:str) -> dict:

        """
        Function for matching userName and Passwords
        Deals with 3 scenerio
            1.  user-password match
            2.  user-password mismatch
            3.  user-not present
            
        Parameters:
            userName(str):userName of user whose password has to be Matched

        """

        userPresent = self.getUsers(userName=userName)

        if userPresent["result"]:

            #queryCorrect
            userPresent["data"] = userPresent["data"][0]

            if len(userPresent["data"]) != 0:

                #userPresent

                attemptsToLog = userPresent["data"][2] + 1
                timeToLog = time.time()

                if userPresent["data"][2] < 3:
                    #if attempt < 3

                    encPass = self.stringToPassword(password=password)
                    
                    if encPass["result"]:
                        #queryError Check

                        if userPresent["data"][1] == encPass["data"]:
                            #if password Match

                            result = {"result":True, "data":userName}

                            attemptsToLog = 0
                            log.error(f'{{"login_matchPassword_Successful":{{"userName":{userName}}}}}')

                        else:
                            #passwordMismatch

                            result = {"result":False, "data":"Userid-Password Mismatch"}
                            log.error(f'{{"login_matchPassword_passwordFailed":{{"userName":{userName}}}}}')

                    else:

                        result = encPass
                        log.error(f'{{"login_matchPassword_stringToPassword_Failed":{{"userName":{userName}}}}}')

                else:
                    #more match > 3

                    timeToLog = userPresent["data"][3]

                    if Decimal(time.time()) - userPresent["data"][3] < 1800:
                        #1800 time for which account will remian locked in sec
                        #userPresnt password Correct but locked 

                        result = {"result":False, "data":"Account Locked for 1/2 hour Please Contact Admin"}
                        log.warning(f'{{"login_matchPassword_AccountLock":{{"userName":{userName}}}}}')

                    else:
                        #unlockingAccount

                        attemptsToLog = 0

                        self.db.query("update users set attempts = {}, lastAttempt = {} where userName = '{}';".format(attemptsToLog, timeToLog, userName))
                        log.info(f'{{"login_matchPassword_AccountUnlocked":{{"userName":{userName}}}}}')

                        result = self.matchPassword(userName=userName, password=password)

                
                self.db.query("update users set attempts = {}, lastAttempt = {} where userName = '{}';".format(attemptsToLog, timeToLog, userName))

            else:

                #userNotPresent
                result = {"result":False, "data":"Userid-Password Mismatch"}

        else:

            userPresent["data"] = ""

            result = userPresent

            log.error(f'{{"login_matchPassword_funcFailed":{{"userName":{userName}}}}}')


        return result



    def getUsers(self, userName:str) -> dict:

        """
        Function for getting userData from table
        Parameters:
            userName(str): userName of user whose data has to be fetched
        
        Returns:
            result(dict): {"result":True/False, "data":"userData"/"errorCode"}
        """

        userSearch = self.db.query("select userName, password, attempts, lastAttempt, reset from users where userName = '{}'".format(userName))

        if userSearch["result"]:

            log.info(f'{{"login_getUser_Successful":{{"userName":{userName}}}}}')
            

        else:

            userSearch["data"] = "Successful"
            log.error(f'{{"login_getUser_Failed":{{"userName":{userName}}}}}')

        result = userSearch

        return result

        



#print(login().stringToPassword("Hello"))
#print(login().matchPassword(userName="shivam", password="password1"))

#print(login().resetTrigger(userName="shivam"))
#print(login().resetCheck(reset = "fdfb32cc3d0521d2f1a0e35cb1941c2d74f3832a716f2cdac923d000b2f4f1d6", password = "password1", repeat = "password1"))


