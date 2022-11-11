from db_menager import DB_Menager
from user_menager import User_Menager

class Mail_Menager(DB_Menager):
    def __init__(self) -> None:
        DB_Menager.__init__(self)
        
    def create_mail(self, user_id_from) -> None:
        email = input("Enter email recipient: ")
        user_id_to = User_Menager().get_user_id(email)
        body = input("Your message: ")
        
        mycursor = self.connection.cursor()
        mycursor.execute("INSERT INTO emails (user_id_from, user_id_to, body) VALUES (%s, %s, %s)", (user_id_from, user_id_to, body)) 
        self.connection.commit()

    def get_unread(self, user_id_to):
        pass

    def get_outgoing(self, user_id_from):
        pass

    def get_incoming(self, user_id_to):
        pass

    def get_all_mails(self, user_id):
        self.get_outgoing()
        self.get_incoming()