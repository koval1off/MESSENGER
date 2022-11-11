import mysql.connector
import os


class DB_Menager():
    def __init__(self) -> None:
        self.connection = self.get_connection()

    def get_connection(self):
        connection = mysql.connector.connect(
            host="localhost",
            user=f"{os.getenv('USER_DB')}",
            password=f"{os.getenv('PASS_DB')}",
            database="messenger"
        )
        return connection
        