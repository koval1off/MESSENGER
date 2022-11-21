from user import User
from typing import List, Optional
from db_manager import DBManager


class UserManager(DBManager):
    def __init__(self) -> None:
        super(UserManager, self).__init__()
        self.users = self._read_users()

    def _read_users(self) -> List[User]:
        """
        reads users from database

        :return: list of users
        """
        users = []
        self.mycursor.execute("SELECT * FROM users")
        data_users = self.mycursor.fetchall()

        for data in data_users:
            user = User(data[1], data[2], data[3], data[0])
            users.append(user)

        return users

    def get_user(self, login: str) -> Optional[User]:
        """
        checks if user exists

        :param login: The login of user
        :return: user if exists or None
        """
        for user in self.users:
            if user.login == login:
                return user
        return None

    def check_pin(self, user, user_pin: str) -> bool:
        """
        checks user password

        :param user: Current user
        :param user_pin: passwd we need to check
        :return: True if user_pin is correct or False
        """
        return user.check_pin(user_pin)

    def _print_users(self):
        for user in self.users:
            print(f"user_id: {user.user_id}, login: {user.login}, user pin: {user.user_pin}, email: {user.email}\n")
            print(type(user))

    def get_user_id(self, email: str) -> int:
        """returns user_id by email"""
        self.mycursor.execute("SELECT user_id FROM users WHERE email = %s", ([email])) 
        user_id = self.mycursor.fetchone()
        return user_id[0]

    def write_new_user(self, user: User) -> None:
        """writes new user to DB"""
        self.mycursor.execute("INSERT INTO users (login, pass, email) VALUES (%s, %s, %s)", (user.login, user.user_pin, user.email))
        self.connection.commit()
    