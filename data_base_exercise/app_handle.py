import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox
import data_base_exercise.db_handle as db
from pyperclip import copy


link = db.DataBase()
APP_COLOR = '#383061'
APP_ALT_COLOR = '#BB8FCE'
LABEL_FONT = ('Courier', 10)
BUTTON_FONT = ('Courier', 10)

class SampleApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title_font = tkfont.Font(family='Verdana', size=14,
                                      weight="bold", slant="italic")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight = 1)
        container.columnconfigure(0, weight=1)
        self.id= tk.StringVar()

        self.frames = {}
        for F in (LoginPage, StartPage, NewEntry, CheckEntry, EditPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky = "nsew")

        self.show_frame("LoginPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

class LoginPage(tk.Frame):
    """
    Log in + take the ID as a variable for the account for the data base
    Create an account, error message if wrong infos
    """
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg= APP_COLOR)

        label1 = tk.Label(self, text="Welcome to Pass Manager",
                          font=controller.title_font,
                          bg = APP_COLOR, foreground="white")
        label2 = tk.Label(self, text="Login : ",
                          font='courier',
                          bg = APP_COLOR, foreground="white")
        label3 = tk.Label(self, text="Pasword : ",
                          font='courier',
                          bg=APP_COLOR, foreground="white")

        label1.grid(row=0, column=0, sticky='n', pady=30, padx=20, columnspan=2)
        label2.grid(row=1, column=0, padx=20)
        label3.grid(row=2, column=0, padx=20)

        result_name = tk.StringVar()
        result_pass =tk.StringVar()
        new_account = tk.IntVar()

        name_entry = tk.Entry(self, bg='white', textvariable= result_name, width = 22)
        pass_entry = tk.Entry(self, bg='white', textvariable = result_pass, width = 22)
        new_account_radio = tk.Checkbutton(self, bg=APP_COLOR, bd=5,
                                           text='Create an account ? ', variable = new_account,
                                           fg='white', indicatoron=0, selectcolor=APP_ALT_COLOR,
                                           command=lambda: print(result_name.get()))

        name_entry.grid(row=1, column  =1, pady=5, padx=5)
        pass_entry.grid(row=2, column = 1, pady=5, padx=5)
        new_account_radio.grid(row=3, column=0, pady=5, padx=5)

        def unlock_page():
            id_entry = result_name.get()
            password = result_pass.get()
            user_list=link.users_list()

            if new_account.get() and id_entry not in user_list :
                if password != '' and id_entry != '':
                    #Add account in main table then create their secondary table
                    link.add_account(id_entry, password)
                    link.create_secondary(id_entry)
                    link.save_query()
                    controller.id.set(id_entry)
                    controller.show_frame('StartPage')

                else:
                    wrong_password_label['text'] = "Identification couldn't proceed \n" \
                                               "entry missing"

            if new_account.get() and id_entry in user_list:
                wrong_password_label['text'] = "Identification couldn't proceed \n" \
                                       "this account may already exist"

            if not new_account.get():
                connexion = link.check_table()
                if password != '' and id_entry != '':
                    try:
                        m = connexion[id_entry]
                        if m == password:
                            controller.id.set(id_entry)
                            controller.show_frame('StartPage')

                        else:
                            wrong_password_label['text'] = 'Identification failed \n' \
                                                           'login or password is wrong'
                    except:
                        wrong_password_label['text'] = 'Identification failed \n' \
                                                       'please try again'
                else:
                    wrong_password_label['text'] = 'Identification failed \n' \
                                                   'field(s) missing an entry'

        validation = tk.Button(self, text="OK", command= unlock_page,
                               relief ='raised', font= BUTTON_FONT)
        wrong_password_label = tk.Label(self, text="", fg="white",
                                        bg=APP_COLOR, foreground="red",
                                        font=('Courier', 12))

        validation.grid(row=3, column = 1, columnspan=2,pady=5, padx= 5)
        wrong_password_label.grid(row=4, column=0, columnspan=3, pady=5, padx=5)

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=APP_COLOR)
        self.controller = controller
        self.controller.title('PassManager')
        # self.controller.state('zoomed')
        self.controller.iconphoto(False, tk.PhotoImage(file="lock.png"))
        label = tk.Label(self, text=f"Hello,"
                                    f"\n what do you want to do ? ",
                         font=controller.title_font, bg=APP_COLOR, fg='white')
        label.pack(side="top", fill="x", pady=20, padx=15)

        button1 = tk.Button(self, text="Add a new entry",
                            command=lambda : controller.show_frame("NewEntry"),
                            font=BUTTON_FONT)
        button2 = tk.Button(self, text="Get a password",
                            command=lambda: controller.show_frame("CheckEntry"),
                            font=BUTTON_FONT)
        button3 = tk.Button(self, text="Update an entry",
                            command=lambda: controller.show_frame("EditPage"),
                            font=BUTTON_FONT)

        button1.pack(pady=5)
        button2.pack(pady=5)
        button3.pack(pady=5)

class NewEntry(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=APP_COLOR)
        self.id = ""
        self.controller = controller

        label = tk.Label(self, text="Add an entry",
                         font=controller.title_font, bg=APP_COLOR, fg='white')
        label_name = tk.Label(self, text="Platform name ",
                              bg=APP_COLOR, fg='white', font=LABEL_FONT)
        label_login = tk.Label(self, text="Login ",
                               bg=APP_COLOR, fg='white', font=LABEL_FONT)
        label_pass = tk.Label(self, text="Password ",
                              bg=APP_COLOR, fg='white', font=LABEL_FONT)

        label.grid(row=0, column=0, columnspan=4, sticky='ew', pady=20)
        label_name.grid(row=1, column=0, padx=5, pady=5)
        label_login.grid(row=2, column=0, padx=5, pady=5)
        label_pass.grid(row=3, column=0, padx=5, pady=5)

        entry_name = tk.StringVar()
        password_name = tk.StringVar()
        login_name = tk.StringVar()

        name_entry = tk.Entry(self, bg='white',
                              textvariable=entry_name, width=22)
        password_entry = tk.Entry(self, bg='white',
                                  textvariable=password_name, width=22)
        login_entry = tk.Entry(self, bg='white',
                               textvariable=login_name, width=22)
        name_entry.grid(row=1, column=1)
        password_entry.grid(row=3, column=1)
        login_entry.grid(row=2, column=1)

        def check_name_entry():
            lock = password_name.get()
            appli = entry_name.get().lower()
            login = login_name.get()
            user = controller.id.get()


            if lock !='' and appli != '' and login != '':
                check_box = tk.messagebox.askyesno(title='Are those informations correct ?',
                                                   message= f"Save {lock} \n "
                                                            f"for account {login}, "
                                                            f"on platform {appli} ?")
                if check_box:
                    link.add_in_secondary(user, appli, login, lock)
            else:
                tk.messagebox.showerror(title='Error', message = "A value is missing, please try again")


        return_button = tk.Button(self, text="BACK",
                           command=lambda: controller.show_frame("StartPage"),
                                  font= BUTTON_FONT)
        validation = tk.Button(self, text="OK", command = check_name_entry,
                               font= BUTTON_FONT)

        return_button.grid(row=4, column = 1, padx = 5, pady=5)
        validation.grid(row=2, column = 2, pady=5, padx= 5)

class CheckEntry(tk.Frame):
    def __init__(self, parent, controller):
        # Rappel : we imported pyperclip to copy data in clipboard
        tk.Frame.__init__(self, parent, bg=APP_COLOR)

        account_entry = tk.StringVar()

        labeltitle = tk.Label(self, text="Get a password ", font=controller.title_font,
                              bg=APP_COLOR, foreground='white')
        enteraccount = tk.Entry(self, bg='light grey', fg=APP_COLOR,
                                textvariable=account_entry, bd=5, width=30)
        labelresult = tk.Label(self, text="Password : ",
                               font=BUTTON_FONT, bg=APP_COLOR, fg='white')
        buttonback = tk.Button(self, text="BACK",
                               command=lambda: controller.show_frame("StartPage"),
                               font=BUTTON_FONT)
        def check_account():
            application = account_entry.get().lower()
            user = controller.id.get()
            data_tuple = link.check_pass(user, application)
            labelresult.configure(text= "Account = " + data_tuple[0] +
                                        '\n Password = ' +
                                        data_tuple[1])

        def ctrl_c():
            application = account_entry.get()
            user = controller.id.get()
            data_tuple = link.check_pass(user, application)
            copy(data_tuple[1])

        clipboard = tk.Button(self, text="Copy",
                                  font=BUTTON_FONT, command=ctrl_c)
        validation = tk.Button(self, text="OK", command=check_account,
                               font=BUTTON_FONT)

        labeltitle.grid(row=0, column = 0, columnspan=2, pady=20, padx=20, sticky='n')
        enteraccount.grid(row=1, column=0, padx=15, sticky='w')
        validation.grid(row=1, column=2, pady=5, padx=5)
        labelresult.grid(row=2, column=0, columnspan=2, padx=20, pady=20, sticky='w')
        clipboard.grid(row=2, column=2, padx=20, pady=20)
        buttonback.grid(row=3, column=0, padx=25, sticky='w')

class EditPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=APP_COLOR)

        app_entry = tk.StringVar()
        pass_entry = tk.StringVar()

        def confirm_change():
            app_name = app_entry.get().lower()
            pass_change = pass_entry.get()
            login = controller.id.get()

            check_box = tk.messagebox.askyesno(title="Validation",
                                               message=f"Update the password for {app_name}, "
                                                       f"with {pass_change} ?")
            if check_box:
                if app_name !=''and pass_change!= '':
                    link.update_entry(login, app_name, pass_change)

                else:
                    tk.messagebox.showerror(title='Error', message='Data is missing')




        label_title = tk.Label(self, text="Update password ", font=controller.title_font,
                         bg= APP_COLOR, foreground = 'white')
        label_change_appli = tk.Label(self, text = "What account do you want to update ?",
                                    bg= APP_COLOR, fg='white')
        label_change_mdp = tk.Label(self, text="New password ",
                                    bg=APP_COLOR, fg='white')
        entry_appli = tk.Entry(self, bg='light grey', fg=APP_COLOR,
                               textvariable= app_entry, bd=5, width= 20)
        entry_mdp = tk.Entry(self, bg='light grey', fg=APP_COLOR,
                               textvariable= pass_entry, bd=5, width= 20)
        button_back = tk.Button(self, text="BACK",
                           command=lambda: controller.show_frame("StartPage"), font= BUTTON_FONT)
        button_valider = tk.Button(self, text="OK", font=BUTTON_FONT,
                                   command = lambda : confirm_change())


        label_title.grid(row=0, column = 0, columnspan=2, pady=20, padx=20, sticky='n')
        label_change_appli.grid(row=1, column=0, padx=15, sticky='w', pady=20)
        label_change_mdp.grid(row=2, column=0, padx=15, sticky='w', pady=20)
        entry_appli.grid(row=1, column=1, padx=5, pady=10, sticky = 'w')
        entry_mdp.grid(row=2, column=1, padx=5, pady=10, sticky = 'w')
        button_back.grid(row=3, column=0, padx=25, sticky='w', pady=20)
        button_valider.grid(row=3, column=1, padx=25, sticky='w', pady=20)


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
