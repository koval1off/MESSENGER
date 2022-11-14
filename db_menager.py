import mysql.connector
import os


class DBManager():
    def get_connection(self):
        connection = mysql.connector.connect(
            host="localhost",
            user=f"{os.getenv('USER_DB')}",
            password=f"{os.getenv('PASS_DB')}",
            database="messenger"
        )
        return connection
        