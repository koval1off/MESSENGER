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
        mycursor = self.connection.cursor()
        mycursor.execute("SELECT text FROM emails WHERE user_id_to = %s AND is_read = 1", ([user_id_to]))
        unread_mails = mycursor.fetchall()
        return unread_mails

    def print_outgoing(self, user_id_from):
        mycursor = self.connection.cursor()
        mycursor.execute("SELECT mail_id, body FROM emails WHERE user_id_from = %s", ([user_id_from]))
        outgoing_mails = mycursor.fetchall()
        for mail in outgoing_mails:
            print(f"--{mail[0]}-- {mail[1]}\n")
        return None

    def print_incoming(self, user_id_to):
        mycursor = self.connection.cursor()
        mycursor.execute("SELECT mail_id, body FROM emails WHERE user_id_to = %s", ([user_id_to]))
        incoming_mails = mycursor.fetchall()
        for mail in incoming_mails:
            print(f"--{mail[0]}-- {mail[1]}\n")
        return None

    def print_all_mails(self, user_id):
        return self.print_outgoing(user_id), self.print_incoming(user_id)
        
    def delete_mail(self, mail_id):
        mycursor = self.connection.cursor()
        mycursor.execute("DELETE FROM emails WHERE mail_id = %s", ([mail_id]))
        self.connection.commit()
        