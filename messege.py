import mysql.connector
import os
from user import USER
from typing import List


class MAIL:
    def __init__(self) -> None:
        self.users = self._read_users()

    def get_connection(self):
        connection = mysql.connector.connect(
            host="localhost",
            user=f"{os.getenv('USER_DB')}",
            password=f"{os.getenv('PASS_DB')}",
            database="messenger"
        )
        return connection

    def _read_users(self) -> List[USER]:
        users = []
        mydb = self.get_connection()
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM users")
        data_users = mycursor.fetchall()

        for data in data_users:
            user = USER(data[0], data[1], data[2], data[3])
            users.append(user)

        return users

    def get_user(self, login):
        """
        checks if user exists

        :param login: The login of user
        :return: user if exists or None
        """
        for user in self.users:
            if user.login == login:
                return user
        return None

    def check_pin(self, user, user_pin) -> bool:
        return user.check_pin(user_pin)

