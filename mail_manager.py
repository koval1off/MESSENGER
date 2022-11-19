from db_manager import DBManager
from user_manager import UserManager
from typing import List

class MailManager(DBManager):
    def create_new_mail(self, user_id_from: int) -> None:
        """creates new mail and send it to database"""
        unique_senders = []
        i = 1
        self.mycursor.execute("""SELECT users.email 
                                FROM emails, users 
                                WHERE emails.user_id_from = %s 
                                AND users.user_id = emails.user_id_to limit 0,5""", ([user_id_from]))
        last_senders = self.mycursor.fetchall()
        
        for sender in last_senders:
            if sender[0] not in unique_senders:
                unique_senders.append(sender[0])
        for sender in unique_senders:
            print(f"--{i}-- {sender}")
            i += 1

        user_choice = input("Enter № of last sender or email you wanna send: ")
        if "@" in user_choice:
            email = user_choice
        elif user_choice.isnumeric():
            if int(user_choice) > 0 and int(user_choice) <= 5:
                email = unique_senders[int(user_choice) - 1]
        else:
            print("Wrong command. Try again")
            return
        
        user_id_to = UserManager().get_user_id(email)
        body = input("Your message: ")
        self.mycursor.execute("INSERT INTO emails (user_id_from, user_id_to, body) VALUES (%s, %s, %s)", (user_id_from, user_id_to, body)) 
        self.connection.commit()

    def get_unread(self, user_id_to: int) -> List[tuple]:
        """returns list of unreaded mails of current user"""
        self.mycursor.execute("SELECT mail_id, body FROM emails WHERE user_id_to = %s AND is_read = 0", ([user_id_to]))
        unread_mails = self.mycursor.fetchall()
        return unread_mails

    def mark_as_read(self, mails: List[tuple]) -> None:
        """updates data in db to read mails"""
        for mail in mails:    
            self.mycursor.execute("UPDATE emails SET is_read = 1 WHERE mail_id = %s", ([mail[0]]))
        self.connection.commit()

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
        return self.get_outgoing(user_id), self.get_incoming(user_id)
    
    def print_outgoing_mails(self, mails: List[tuple]) -> None:
        """prints outgoing mails"""
        if not mails:
            print("Seems like you don't have any mails\n")  
        for mail in mails:
            print(f"--{mail[0]}>> {mail[1]}\n")
        return None

    def print_incoming_mails(self, mails: List[tuple]) -> None:
        """prints incoming mails"""
        if not mails:
            print("Seems like you don't have any mails\n")  
        for mail in mails:
            print(f"<<{mail[0]}-- {mail[1]}\n")
        return None

    def print_all_mails(self, mails: List[tuple]) -> None:
        """prints all mails"""
        self.print_outgoing_mails(mails[0])
        self.print_incoming_mails(mails[1])
        return None

    def delete_mail(self, mail_id: int) -> None:
        """deletes mail by its id"""
        self.mycursor.execute("DELETE FROM emails WHERE mail_id = %s", ([mail_id]))
        self.connection.commit()
        