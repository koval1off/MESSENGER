import tkinter as tk
import tkinter.messagebox
import customtkinter as ctk
from tkinter import ttk, StringVar
from user import User
from user_manager import UserManager
from mail_manager import MailManager
from main import print_mails

    
ctk.set_appearance_mode('System')
ctk.set_default_color_theme('dark-blue')

class App(ctk.CTk):

    WIDTH = 570
    HEIGTH = 400

    def __init__(self, *args, **kwargs):
        ctk.CTk.__init__(self, *args, **kwargs)

        self.title("Messenger")
        self.geometry(f"{App.WIDTH}x{App.HEIGTH}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        container = ctk.CTkFrame(self)
        container.grid(row=0, column=1)
        container.grid_columnconfigure(1, weight=1)
        container.grid_rowconfigure(0, weight=1)

        self.frames = {}

        for F in (LoginPage, SignUpPage, MenuPage):
            frame = F(container, self)    
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame(LoginPage)
        
    def on_closing(self, event = 0):
        self.destroy()

    def show_frame(self, cont, param=None):
        frame = self.frames[cont]
        if param:
            frame.update(param)  
        frame.tkraise()  
    
    # def get_page(self, page_class):
        # return self.frames[page_class]

class LoginPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller
        self.user_manager = UserManager()
        self.user = ctk.StringVar()
        self.login_success = False
        self.count_attempts = 1

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(7, weight=1)

        capital_label = ctk.CTkLabel(self, text="Welcome!", text_color='default_theme')
        capital_label.grid(row=0, column=0, pady=10, padx=10)

        login_label = ctk.CTkLabel(self, text="Enter login")
        login_label.grid(row=1, column=0, pady=10, padx=10)

        password_label = ctk.CTkLabel(self, text="Enter password")
        password_label.grid(row=3, column=0, pady=10, padx=10)
        
        self.login_entry = ctk.CTkEntry(self)
        self.login_entry.grid(row=2, column=0)
        
        password_entry = ctk.CTkEntry(self)
        password_entry.grid(row=4, column=0)

        button1 = ctk.CTkButton(self, text='Sign up', command=lambda: controller.show_frame(SignUpPage))
        button1.grid(row=5, column=0, pady=10, padx=10)

        button2 = ctk.CTkButton(self, text='Login', command=lambda: self.login(self.login_entry.get(), password_entry.get()))
        button2.grid(row=6, column=0, pady=10, padx=10)

    def login(self, login, password):
        print("you r in login")
        user = self.user_manager.get_user(login)
        if user:
            self.login_success = self.user_manager.check_pin(user, password)
            print("here is the user")
            
        if self.login_success:
            print('pin is ok')
            self.user.set(self.login_entry.get())
            self.controller.show_frame(MenuPage, login)
        else:
            self.controller.show_frame(LoginPage)


class SignUpPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(11, weight=1)

        label = ctk.CTkLabel(self, text="Welcome New User!", text_color='default_theme')
        label.grid(row=0, column=0, pady=10, padx=10)

        login_label = ctk.CTkLabel(self, text="Enter login")
        login_label.grid(row=1, column=0, pady=5, padx=10)

        email_label = ctk.CTkLabel(self, text="Enter email")
        email_label.grid(row=3, column=0, pady=5, padx=10)

        password_label = ctk.CTkLabel(self, text="Enter password")
        password_label.grid(row=5, column=0, pady=5, padx=10)

        repeat_password_label = ctk.CTkLabel(self, text="Repeat password")
        repeat_password_label.grid(row=7, column=0, pady=5, padx=10)

        login_entry = ctk.CTkEntry(self)
        login_entry.grid(row=2, column=0)

        email_entry = ctk.CTkEntry(self)
        email_entry.grid(row=4, column=0)

        password_entry = ctk.CTkEntry(self)
        password_entry.grid(row=6, column=0)

        repeat_password_entry = ctk.CTkEntry(self)
        repeat_password_entry.grid(row=8, column=0)

        button1 = ctk.CTkButton(self, text='back to login page', command=lambda: controller.show_frame(LoginPage))
        button1.grid(row=9, column=0, pady=10, padx=10)

        button2 = ctk.CTkButton(self, text='Sign Up', command=lambda: controller.show_frame(self.sign_up(login_entry.get(), password_entry.get(), repeat_password_entry.get(), email_entry.get())))
        button2.grid(row=10, column=0, pady=10, padx=10)

    def sign_up(self, login, passwd, repeat_passwd, email):
        print("you r in sign up")
        if passwd == repeat_passwd:
            print("passes r the same")
            user_manager = UserManager()
            user_manager.create_user(login, passwd, email)
            return MenuPage
        else:
            print("passes r not the same")
            return SignUpPage

class MenuPage(LoginPage):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)

        self.controller = controller

    def create(self):
        self.mail_manager = MailManager()
        self.user = UserManager().get_user(self.user_id)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.left_frame = ctk.CTkFrame(master=self, 
                                                width=180,
                                                bg='grey',
                                                corner_radius=0)
        self.left_frame.grid(row=0, column=0, sticky="nswe")

        self.right_frame = ctk.CTkFrame(master=self,
                                                width=380, 
                                                height=250, 
                                                border_width=2, 
                                                border_color='black')
        self.right_frame.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        self.left_frame.grid_rowconfigure(7, weight=1)

        label = ctk.CTkLabel(self.left_frame, text="Menu Page", text_color='default_theme')
        label.grid(row=0, column=0)

        back_to_login_button = ctk.CTkButton(self.left_frame, text='back to login page', command=lambda: self.controller.show_frame(LoginPage))
        back_to_login_button.grid(row=1, column=0, pady=5, padx=5) 

        button2 = ctk.CTkButton(self.left_frame, text="all mails", command=lambda: (self.clean_frame(self.right_frame), self.all_mails_button(self.user)))
        button2.grid(row=2, column=0, pady=5, padx=5)

        button3 = ctk.CTkButton(self.left_frame, text='incoming mails', command=lambda: (self.clean_frame(self.right_frame), self.incoming_mails_button(self.user)))
        button3.grid(row=3, column=0, pady=5, padx=5)

        button4 = ctk.CTkButton(self.left_frame, text='outgoing mails', command=lambda: (self.clean_frame(self.right_frame), self.outgoing_mails_button(self.user)))
        button4.grid(row=4, column=0, pady=5, padx=5)

        button5 = ctk.CTkButton(self.left_frame, text='new mail', command=lambda: (self.clean_frame(self.right_frame), self.new_mail_button(self.user.user_id)))
        button5.grid(row=5, column=0, pady=5, padx=5)

        button6 = ctk.CTkButton(self.left_frame, text='clear', command=lambda: self.clean_frame(self.right_frame))
        button6.grid(row=6, column=0, pady=5, padx=5)

    def update(self, param):
        self.user_id = param
        self.create()

    def print_table_users(self, frame, data):
        self.clean_frame(frame)
        my_tree = ttk.Treeview(self.right_frame)

        my_tree['columns'] = ('Direction', 'ID', 'Body', 'Status')

        my_tree.column('#0', width=0, stretch="no")
        my_tree.column('Direction', anchor='w', width=120)
        my_tree.column('ID', anchor='center', width=80)
        my_tree.column('Body', anchor='center', width=120)
        my_tree.column('Status', anchor='w', width=80)

        my_tree.heading('#0', text='', anchor='w')
        my_tree.heading('Direction', text='Direction', anchor='w')
        my_tree.heading('ID', text="ID", anchor='center')
        my_tree.heading('Body', text='Body', anchor='w')
        my_tree.heading('Status', text='Status', anchor='w')

        count = 0
        for mail in data:
            my_tree.insert(parent='', index='end', iid=count, text='', values=(mail[0], mail[1], mail[2], mail[3]))
            count += 1
        
        my_tree.pack(pady=20)

    def print_mails_button(self, mails):
        """prints mails using buttons with checkbox"""
        current_row = 0

        for mail in mails:
            mail_btn = ctk.CTkButton(self.right_frame, text=f"{mail[0]}  {mail[1]}  {mail[2]}  {mail[3]}", 
                                    width=330, 
                                    command=print(f"{mail[0]}  {mail[1]}  {mail[2]}  {mail[3]}"))
            mail_btn.grid(row=current_row, column=0, pady=5, padx=5)
            check_box = ctk.CTkCheckBox(self.right_frame, text="")
            check_box.grid(row=current_row, column=1, pady=5, padx=5)
            current_row += 1
    
    def all_mails_button(self, user):
        mails = self.mail_manager.get_all_mails(user.user_id)
        # edited_mails = print_mails(str(user.user_id), mails)
        self.print_mails_button(mails)

    def incoming_mails_button(self, user):
        mails = self.mail_manager.get_incoming(user.user_id)
        self.print_mails_button(mails)

    def outgoing_mails_button(self, user):
        mails = self.mail_manager.get_outgoing(user.user_id)
        self.print_mails_button(mails)
    
    def clean_frame(self, frame):
        for item in frame.winfo_children():
            item.destroy()

    def new_mail_button(self, user_id_from):
        label1 = ctk.CTkLabel(self.right_frame, 
                              width=365,
                              text="email you send to")
        label1.grid(row=1, column=0, pady=5, padx=5)

        last_senders = MailManager().get_last_senders(user_id_from)

        self.combox = ctk.CTkComboBox(self.right_frame,
                                 width=250, 
                                 values=[last_senders[0][0], last_senders[1][0], last_senders[2][0]])
        self.combox.set('')
        self.combox.grid(row=2, column=0, pady=5, padx=5)

        mail_entry = tk.Text(self.right_frame, height=3, width=30, bg="#5A5A5A", fg="#FFFFFF")
        mail_entry.grid(row=3, column=0, pady=5, padx=5)

        send_button = ctk.CTkButton(self.right_frame, text="Send", width=150, command=lambda: self.send_mail(self.combox, mail_entry, user_id_from))
        send_button.grid(row=4, column=0, pady=5, padx=5)
    
    def send_mail(self, combox_entry, mail_entry, user_id_from):
        user_choice = combox_entry.get()
        if "@" in user_choice:
            email = user_choice
            user_id_to = UserManager().get_user_id(email)
            body = mail_entry.get("1.0",'end-1c')
            MailManager().create_mail(user_id_from, user_id_to, body)
    


app = App()
app.mainloop()