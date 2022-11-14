from db_menager import DBManager
from user_menager import UserManager


class MailManager(DBManager):
    def __init__(self) -> None:
        self.connection = self.get_connection()
        
    def create_mail(self, user_id_from: int) -> None:
        email = input("Enter email recipient: ")
        user_id_to = UserManager().get_user_id(email)
        body = input("Your message: ")
        
        mycursor = self.connection.cursor()
        mycursor.execute("INSERT INTO emails (user_id_from, user_id_to, body) VALUES (%s, %s, %s)", (user_id_from, user_id_to, body)) 
        self.connection.commit()

    def get_unread(self, user_id_to: int) -> list:
        mycursor = self.connection.cursor()
        mycursor.execute("SELECT text FROM emails WHERE user_id_to = %s AND is_read = 1", ([user_id_to]))
        unread_mails = mycursor.fetchall()
        return unread_mails

    def get_outgoing(self, user_id_from: int) -> list:
        mycursor = self.connection.cursor()
        mycursor.execute("SELECT mail_id, body FROM emails WHERE user_id_from = %s", ([user_id_from]))
        outgoing_mails = mycursor.fetchall()
        return outgoing_mails

    def get_incoming(self, user_id_to: int) -> list:
        mycursor = self.connection.cursor()
        mycursor.execute("SELECT mail_id, body FROM emails WHERE user_id_to = %s", ([user_id_to]))
        incoming_mails = mycursor.fetchall()
        return incoming_mails

    def get_all_mails(self, user_id: int) -> list:
        all_mails = self.get_incoming(user_id)
        for mail in self.get_outgoing(user_id):
            all_mails.append(mail)
        return all_mails
    
    def print_mails(self, mails):
        if not mails:
            print("Seems like you don't have any mails yet\nTry >>5)New mail<<\n")  
        for mail in sorted(mails):
            print(f"--{mail[0]}-- {mail[1]}\n")
        return None
   
    def delete_mail(self, mail_id: int) -> None:
        mycursor = self.connection.cursor()
        mycursor.execute("DELETE FROM emails WHERE mail_id = %s", ([mail_id]))
        self.connection.commit()
        