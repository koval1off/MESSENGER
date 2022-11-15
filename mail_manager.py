from db_manager import DBManager
from user_manager import UserManager
from typing import List

class MailManager(DBManager):
    def create_mail(self, user_id_from: int) -> None:
        """constructing new mail and send it to database"""
        email = input("Enter email recipient: ")
        user_id_to = UserManager().get_user_id(email)
        body = input("Your message: ")
        
        self.mycursor.execute("INSERT INTO emails (user_id_from, user_id_to, body) VALUES (%s, %s, %s)", (user_id_from, user_id_to, body)) 
        self.connection.commit()

    def get_unread(self, user_id_to: int) -> List[tuple]:
        """returns list of unreaded mails of current user"""
        self.mycursor.execute("SELECT mail_id, body FROM emails WHERE user_id_to = %s AND is_read = 1", ([user_id_to]))
        unread_mails = self.mycursor.fetchall()
        return unread_mails

    def get_outgoing(self, user_id_from: int) -> List[tuple]:
        """returns list of outgoing mails from current user"""
        self.mycursor.execute("SELECT mail_id, body FROM emails WHERE user_id_from = %s", ([user_id_from]))
        outgoing_mails = self.mycursor.fetchall()
        return outgoing_mails

    def get_incoming(self, user_id_to: int) -> List[tuple]:
        """returns list of mails to current user"""
        self.mycursor.execute("SELECT mail_id, body FROM emails WHERE user_id_to = %s", ([user_id_to]))
        incoming_mails = self.mycursor.fetchall()
        return incoming_mails

    def get_all_mails(self, user_id: int) -> List[tuple]:
        """returns all mails that current user has"""
        all_mails = self.get_incoming(user_id)
        for mail in self.get_outgoing(user_id):
            all_mails.append(mail)
        return all_mails
    
    def print_mails(self, mails: List[tuple]) -> None:
        """prints all given mails"""
        if not mails:
            print("Seems like you don't have any mails yet\nTry >>5)New mail<<\n")  
        for mail in sorted(mails):
            print(f"--{mail[0]}-- {mail[1]}\n")
        return None
   
    def delete_mail(self, mail_id: int) -> None:
        """deletes mail by its id"""
        self.mycursor.execute("DELETE FROM emails WHERE mail_id = %s", ([mail_id]))
        self.connection.commit()
        