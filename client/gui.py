import threading
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
        self.text_couner = 1.0

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
        self.main_window.mainloop()

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
        self.main_window.mainloop()

    def login(self):
        success, massage = self.client.log_in(self.username.get(), self.password.get())
        if not success:
            self.log_in_window(massage)
        else:
            self.main_chat_window()

    def sign_in(self):
        success, massage = self.client.create_user(self.username.get(), self.password.get())
        if not success:
            self.sign_in_window(massage)
        else:
            self.log_in_window(massage)

    def get_new_massages(self, text):
        data, client_socket = self.client.get_massages_from_server()
        text.insert(str(self.text_couner),
                    self.client.get_username_from_id(data["user_id"]) + ": " + data["massage"] + "\n")
        self.text_couner += 1.0
        while True:
            data = self.client.get_massages_from_server(client_socket)[0]
            text.insert(str(self.text_couner),
                        self.client.get_username_from_id(data["user_id"]) + ": " + data["massage"] + "\n")
            self.text_couner += 1.0

    def send_massage(self, text, massage):
        self.client.send_massage(massage)
        text.insert(str(self.text_couner), "me: " + massage + "\n")
        text.tag_configure("right", justify='right')
        text.tag_add("right", str(self.text_couner), str(self.text_couner + 1.0))
        self.text_couner += 1.0

    def main_chat_window(self):
        self.main_window.destroy()
        self.main_window = tkinter.Tk()
        self.main_window.configure(background="#3c3b40")
        self.main_window.resizable(width=False, height=False)
        self.main_window.geometry("700x600")
        self.main_window.grid_columnconfigure((1, 2), weight=1)
        user_input = tkinter.StringVar()
        user_id_list = self.client.get_user_id_list()
        counter = 2
        tkinter.Button(self.main_window, text="all", width=20, height=1, bg="#503c5c", font=("impact", 10),
                       fg="black", bd=1).grid(row=1, column=0)
        for user_id in user_id_list:
            tkinter.Button(self.main_window, text=self.client.get_username_from_id(user_id), width=20, height=1,
                           bg="#503c5c", font=("impact", 10),
                           fg="black", bd=1).grid(row=counter, column=0)
            counter += 1
        text = tkinter.Text(self.main_window, bg="#201f24", wrap="word", fg="#ffffff")
        text.grid(column=1)
        entry_input = tkinter.Entry(self.main_window, width=80, textvariable=user_input)
        entry_input.grid(column=1, sticky="w", pady=22)
        enter_button = tkinter.Button(width=10, height=1, text="send",
                                      command=lambda: (self.send_massage(text, user_input.get())))
        enter_button.grid(row=counter + 1, column=1, sticky="e")
        threading.Thread(target=self.get_new_massages, args=(text,)).start()

        self.main_window.mainloop()


g = Gui()
g.log_in_window("")
