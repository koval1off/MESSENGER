class USER:
    def __init__(self, user_id, login, user_pin, email):
        self.user_id = user_id
        self.login = login
        self.user_pin = user_pin
        self.email = email

    def check_pin(self, user_pin) -> bool:
        return user_pin == self.user_pin
