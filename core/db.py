from dotenv import load_dotenv
import mysql.connector as connector, os, logging as log
log.basicConfig(filename="logs.log", level=log.INFO, format='%(levelname)s[%(filename)s:%(funcName)s:%(lineno)d]:%(message)s')


class db( object ):

    """
    Class for executing raw queries
    """

    def __init__(self) -> None:

        load_dotenv()
        
        try:
            
            self.cnx = connector.connect(user=os.getenv('dbUser'), password=os.getenv('dbPassword'), host=os.getenv("dbHost"), database=os.getenv("dbBase"))

        except Exception as e:

            log.info(f"loggingError -> {str(e)}")



    def __clean__(self, cursor):

        """
        Function running query and cleaning results from cursor

        Parameters
            cursor (mysqlCursor):cursor of executed query

        Returns
            result (list):[output data]

        """

        result = [each for each in cursor]

        if len(result) != 0 and len(result[0]) > 1:

            result = [ [_ for _ in each] for each in result]

        elif len(result) != 0 and len(result[0]) == 1:

            result = [ each[0] for each in result]

        

        
        return result


    def query(self, query:str):

        """
        High class function for getting result of a query

        Parameters
            query (str):query string

        Returns
            result (dict):{"result":True/False, "data":"output/errorCode"}

        """

        result = {"result":False, "data":"Func102"}

        try:

            result = self.__query__(query)

            self.cnx.commit()


        except Exception as e:

            log.error(f'funcError -> {str(e)}, additionalInfo -> {"query":{str(query)}}')


        return result





    def __query__(self, query:str):

        """
        Function running query and cleaning results from cursor

        Parameters
            query (str):query string

        Returns
            result (dict):{"result":True/False, "data":"output/errorCode"}

        """

        result = {"result":False, "data":"Func101"}

        try:

            cursor = self.cnx.cursor()


            try:
                
                cursor.execute(query)

                result["result"] = True

                result["data"] = self.__clean__(cursor)

                cursor.close()

            except Exception as e:

                result["data"] = "Error101"

                log.error(f"queryError -> {str(e)}")

        
        except Exception as e:

            log.error(f'funcError -> {str(e)}, additionalInfo -> {"query":{str(query)}}')

        
        return result


    



        


#print( db().query(query = "show tables;") )


