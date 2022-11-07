from datetime import datetime
from user import USER
from messege import MAIL
from typing import Optional


def sign_up() -> Optional[USER]:
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
            user = USER(2, login, user_pin, email)
            return user
        else:
            print("Your passwords aren't the same. Please, try again")
            

def menu(user: USER, mail: MAIL):
    if user is None:
        return
    
    if mail is None:
        return 
    
    while True:
        time = datetime.now().strftime('%H:%M')
        print(time.center(14, '*'))

        title = "Messenger"
        print(title.center(15, '*'))

        print("Menu:\n\t"
              "1) All mails\n\t"
              "2) Unread mails\n\t"
              "3) New mail\n\t"
              "4) Exit\n\t")

        menu_choice = int(input("Enter the number of operation: "))
        if menu_choice == 1:
            print("You choice the All mails")
        elif menu_choice == 2:
            print("You choice the Unread mails")
        elif menu_choice == 3:
            print("You choice the New mail")
        elif menu_choice == 4:
            return
        else:
            print("Wrong command. Please try again")


def main():
    mail = MAIL()
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
            user = mail.get_user(login)
            if user:
                login_success = mail.check_pin(user, user_pin)
            if not login_success:
                error_text = f"Wrong ID or PASS. {count_attempts}/3."
                print(error_text + ' Try again') if count_attempts < 3 else print(error_text)
                count_attempts += 1
            else:
                break
    elif start_choise == 2:
        print("Hello, new user!")
        user = sign_up()
        login_success = True
    else:   # if 3 were selected
        return

    if login_success and user:
        menu(user, mail)
    else:
        print("Error. Too much fails while entering")


main()
