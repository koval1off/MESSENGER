class User:
    def __init__(self, login, user_pin, email, user_id=None):
        self.user_id = user_id
        self.login = login
        self.user_pin = user_pin
        self.email = email

    def check_pin(self, user_pin) -> bool:
        return user_pin == self.user_pin
