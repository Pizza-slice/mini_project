import tkinter

import client

WINDOW_SIZE = "400x450+0+0"


class Gui:
    def __init__(self):
        self.main_window = tkinter.Tk()
        self.main_window.geometry(WINDOW_SIZE)
        self.main_window.configure(background="#3c3b40")
        self.main_window.resizable(width=False, height=False)
        self.client = client.Client()
        self.username = tkinter.StringVar()
        self.password = tkinter.StringVar()

    def log_in_window(self, massage):
        self.password.set('')
        self.username.set('')
        login_window = tkinter.Frame(self.main_window)
        tkinter.Label(login_window.place(), text="LOG-IN", bg="#3c3b40", font=("impact", 55), padx=10).place(x=95, y=50)
        if massage:
            tkinter.Label(login_window.place(), text=massage, bg="#3c3b40", font=("impact", 10), padx=10).place(x=90,
                                                                                                                y=150)
        tkinter.Label(login_window.place(), text="username:", bg="#3c3b40", font=("impact", 15)).place(x=10, y=200)
        tkinter.Entry(login_window.place(), textvariable=self.username, width=35).place(x=105, y=207)
        tkinter.Label(login_window.place(), text="password:", bg="#3c3b40", font=("impact", 15)).place(x=10, y=230)
        tkinter.Entry(login_window.place(), textvariable=self.password, width=35, show="*").place(x=105, y=237)
        tkinter.Button(login_window.place(), text="log-in", width=10, bg="black", fg="white",
                       font=("impact", 10), command=(lambda: (login_window.place_forget(), self.login()))).place(
            x=170,
            y=300)
        tkinter.Button(login_window.place(), text="sign-up", width=10, bg="white", fg="black",
                       font=("impact", 10),
                       command=(lambda: (login_window.place_forget(), self.sign_in_window("")))).place(
            x=170,
            y=350)

    def sign_in_window(self, massage):
        self.password.set('')
        self.username.set('')
        sign_window = tkinter.Frame(self.main_window)
        tkinter.Label(sign_window.place(), text="SIGN IN", bg="#3c3b40", font=("impact", 55)).place(x=90, y=50)
        if massage:
            tkinter.Label(sign_window.place(), text=massage, bg="#3c3b40", font=("impact", 10), padx=10).place(x=90,
                                                                                                               y=150)
        tkinter.Label(sign_window.place(), text="username:", bg="#3c3b40", font=("impact", 15)).place(x=10, y=200)
        tkinter.Entry(sign_window.place(), textvariable=self.username, width=35).place(x=105, y=207)
        tkinter.Label(sign_window.place(), text="password:", bg="#3c3b40", font=("impact", 15)).place(x=10, y=230)
        tkinter.Entry(sign_window.place(), textvariable=self.password, width=35, show="*").place(x=105, y=237)
        tkinter.Button(sign_window.place(), text="sign-up", width=10, bg="black", fg="white",
                       font=("impact", 10),
                       command=(lambda: (sign_window.place_forget(), self.sign_in()))).place(x=170,
                                                                                             y=300)
        tkinter.Button(sign_window.place(), text="log-in", width=10, bg="white", fg="black",
                       font=("impact", 10),
                       command=(lambda: (sign_window.place_forget(), self.log_in_window("")))).place(x=170,
                                                                                                     y=350)

    def login(self):
        success, massage = self.client.log_in(self.username.get(), self.password.get())
        if not success:
            self.log_in_window(massage)
        else:
            print("log in successfully")

    def sign_in(self):
        success, massage = self.client.create_user(self.username.get(), self.password.get())
        if not success:
            self.sign_in_window(massage)
        else:
            print("created a user")




g = Gui()
g.log_in_window("")
g.main_window.mainloop()
