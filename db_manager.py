import mysql.connector
import os


class DBManager():
    def __init__(self) -> None:
        self.connection = self.get_connection()
        self.mycursor = self.connection.cursor()

    def get_connection(self):
        """returns conection to database"""
        connection = mysql.connector.connect(
            host="localhost",
            user=f"{os.getenv('USER_DB')}",
            password=f"{os.getenv('PASS_DB')}",
            database="messenger"
        )
        return connection
        