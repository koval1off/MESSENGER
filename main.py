import os
from datetime import datetime
from typing import Optional, List
from user import User
from user_manager import UserManager
from mail_manager import MailManager


def create_mail():
    pass


def print_mails(client_id: str, mails: List[tuple]):
    """prints incoming mails"""
    if not mails:
        print("Seems like you don't have any mails\n")  

    for mail in mails:
        mail_from = mail[3]
        direction = "<<--" if mail_from == client_id else "-->>"
        read_status = "[v]" if mail[2] else "[0]"
        print(f"{direction} ID: {mail[0]} Body: {mail[1]} {read_status}")
      

def sign_up() -> Optional[User]:
    """
    creates new user
    :return: user if sign up success or None
    """
    while True:
        login = input("Enter Login(q to quit): ")

        if login == "q":
            return None

        email = input("Enter E-mail: ")
        user_pin = input("Create Password: ")
        repeat_pin = input("Repeat Password: ")
        if user_pin == repeat_pin:
            user_manager = UserManager()
            user = User(login, user_pin, email)
            user_manager.write_new_user(user)
            return user_manager.get_user(login)
        else:
            print("Your passwords aren't the same. Please, try again")
            

def menu(user: User, user_manager: UserManager) -> None:
    if user is None:
        return
    
    if user_manager is None:
        return 
    
    mail_manager = MailManager()

    while True:
        time = datetime.now().strftime('%H:%M')
        print(time.center(14, '*'))

        title = "Messenger"
        print(title.center(15, '*'))

        print("Menu:\n\t"
              "1) All mails\n\t"
              "2) Mark as read mails\n\t"
              "3) Incoming mails\n\t"
              "4) Outgoing mails\n\t"
              "5) New mail\n\t"
              "6) Delete mail\n\t"
              "7) Exit\n\t")

        menu_choice = int(input("Enter the number of operation: "))
        if menu_choice == 1:
            print("You choice the All mails\n")
            mails = mail_manager.get_all_mails(user.user_id)
            print_mails(str(user.user_id), mails)
        elif menu_choice == 2:
            print("You choice the Unread mails\n")
            mails = mail_manager.get_unread(user.user_id)
            if mails:
                do_read = input("Mark this mails as read?(y/any): ")
                if do_read.lower() == "y":
                    mail_manager.mark_as_read(mails)
        elif menu_choice == 3:
            print("You choice Incoming mails\n")
            mails = mail_manager.get_incoming(user.user_id)
            print_mails(str(user.user_id), mails)
        elif menu_choice == 4:
            print("You choice Outgoing mails\n")
            mails = mail_manager.get_outgoing(user.user_id)
            print_mails(str(user.user_id), mails)
        elif menu_choice == 5:
            print("You choice the New mail\n")
            mail_manager.create_new_mail(user.user_id)
        elif menu_choice == 6:
            print("You choice Delete mail\n")
            mails = mail_manager.get_all_mails(user.user_id)
            print_mails(user.user_id, mails)
            mail_id = input("Which mail you wanna delete: ")
            mail_manager.delete_mail(mail_id)
        elif menu_choice == 7:
            return
        else:
            print("Wrong command. Please try again")


def main():
    user_manager = UserManager()
    user = None
    login_success = False
    count_attempts = 1

    print("1)Login in\n"
          "2)Sign up\n"
          "3)Exit\n")
    start_choise = int(input("Select: "))
    if start_choise == 1:
        while count_attempts <= 3:
            login = input("Enter Login: ")
            user_pin = input("Enter Password: ")
            user = user_manager.get_user(login)
            if user:
                login_success = user_manager.check_pin(user, user_pin)
            if not login_success:
                error_text = f"Wrong ID or PASS. {count_attempts}/3."
                print(error_text + ' Try again') if count_attempts < 3 else print(error_text)
                count_attempts += 1
            else:
                break
    elif start_choise == 2:
        print("Hello, new user!")
        user = sign_up()
        login_success = True if user else False
    else:   # if 3 were selected
        return

    if login_success:
        menu(user, user_manager)
    else:
        print("Error. Too much fails while entering")


if __name__ == "__main__":
    debug = True
    if debug:
        user_manager = UserManager()
        user = user_manager.get_user("login1")
        menu(user, user_manager)
    else:
        main()
