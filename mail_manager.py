from db_manager import DBManager
from user_manager import UserManager
from typing import List

class MailManager(DBManager):
    def get_last_senders(self, user_id_from: int):
        """returns list of unique last senders' emails"""
        self.mycursor.execute("""SELECT DISTINCT users.email 
                                FROM emails, users 
                                WHERE emails.user_id_from = %s 
                                AND users.user_id = emails.user_id_to limit 0,5""", ([user_id_from]))
        last_senders = self.mycursor.fetchall()
        return last_senders

    def create_mail(self, user_id_from: int, user_id_to: int, body: str):
        """writes new mail to database"""
        self.mycursor.execute("INSERT INTO emails (user_id_from, user_id_to, body) VALUES (%s, %s, %s)", (user_id_from, user_id_to, body)) 
        self.connection.commit()

    def get_unread(self, user_id_to: int) -> List[tuple]:
        """returns list of unreaded mails of current user"""
        self.mycursor.execute("SELECT mail_id, body, is_read, user_id_from, user_id_to FROM emails WHERE user_id_to = %s AND is_read = 0", ([user_id_to]))
        unread_mails = self.mycursor.fetchall()
        return unread_mails

    def mark_as_read(self, mails: List[tuple]) -> None:
        """updates data in db to read mails"""
        for mail in mails:    
            self.mycursor.execute("UPDATE emails SET is_read = 1 WHERE mail_id = %s", ([mail[0]]))
        self.connection.commit()

    def get_outgoing(self, user_id_from: int) -> List[tuple]:
        """returns list of outgoing mails from current user"""
        self.mycursor.execute("SELECT mail_id, body, is_read, user_id_from, user_id_to FROM emails WHERE user_id_from = %s", ([user_id_from]))
        outgoing_mails = self.mycursor.fetchall()
        return outgoing_mails

    def get_incoming(self, user_id_to: int) -> List[tuple]:
        """returns list of mails to current user"""
        self.mycursor.execute("SELECT mail_id, body, is_read, user_id_from, user_id_to FROM emails WHERE user_id_to = %s", ([user_id_to]))
        incoming_mails = self.mycursor.fetchall()
        return incoming_mails

    def get_all_mails(self, user_id: int) -> List[tuple]:
        """returns all mails that current user has"""
        self.mycursor.execute("SELECT mail_id, body, is_read, user_id_from, user_id_to FROM emails WHERE user_id_to = %s or user_id_from = %s", (user_id, user_id))
        all_mails = self.mycursor.fetchall()
        return all_mails
    
    def delete_mail(self, mail_id: int) -> None:
        """deletes mail by its id"""
        self.mycursor.execute("DELETE FROM emails WHERE mail_id = %s", ([mail_id]))
        self.connection.commit()
        