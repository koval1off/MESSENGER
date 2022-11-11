from user import USER
from typing import List
from db_menager import DB_Menager


class User_Menager(DB_Menager):
    def __init__(self) -> None:
        DB_Menager.__init__(self)
        self.users = self._read_users()

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

    def print_users(self):
        for user in self.users:
            print(f"user_id: {user.user_id}, login: {user.login}, user pin: {user.user_pin}, email: {user.email}\n")
            print(type(user))

    def get_user_id(self, email):
        """returns user id by email"""
        check_mail = [email]
        mycursor = self.connection.cursor()
        mycursor.execute("SELECT user_id FROM users WHERE email = %s", (check_mail)) 
        user_id = mycursor.fetchone()
        return user_id[0]