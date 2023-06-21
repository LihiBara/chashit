"""
author - lihi
date   - 29 / 05 / 23
client
"""
# file name CashitClient.py
import os.path
import socket
import json
from tkinter import *
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import CashitMainApp
import threading
import time
import io
from tkinter import filedialog
import base64
import config
from cryptography.fernet import Fernet
import base64
import math
import hashlib

"""
to do : 
1. encrypt  password  in connection amd in data base
2. ake encrypt connection 
3. asserts 
4 fix bug , mtdetails after update 
"""


class CashitClient:

    def __init__(self, host="127.0.0.1", port=8080):
        """
        class function that is opening a user for each client
        :param host:
        :param port:
        """
        self.host = host
        self.host2 = host
        self.port = port
        self.port2 = 8082
        self.special = []
        self.regular = []
        with io.open("key.key", mode='r') as file:
            # Write content to the file
            key = file.read()
        self.fernet = Fernet(key)
        self.lock = threading.Lock()
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.event = threading.Event()
        #self.thread5sec = threading.Thread(target=listen_server,
        #                                   args=(
        #                                   self.fernet, self.client2, self.event, self.special, self.regular, self.lock))

    def connect(self):
        """
        Establishes a connection to the server using self.client socket.
        """
        try:
            self.client.connect((self.host, self.port))
            print("Connected to the server.")
        except socket.error as err:
            print("Error connecting to the server:", str(err))

    def connect_port2(self):
        """
        Establishes a connection to the server using self.client2 socket.
        """
        try:
            self.client2.connect((self.host, self.port2))
            print("Connected to the server (port2).")
        except socket.error as err:
            print("Error connecting to the server (port2):", str(err))

    def send_command_validate_port2(self, *args):
        self.connect_port2()
        self.send_validate_port2(*args)
        listen_server(self.fernet, self.client2, self.event, self.special, self.regular, self.lock)

    def send_command(self, command, *args):
        """
        a function that is responsible for sending the encrypted command to the server
        and recieving the answer from him
        :param command:
        :param args:
        :return:
        """
        self.lock.acquire()
        try:
            print("Sending JSON data :) :", json.dumps((command, args)))
            encryped = self.fernet.encrypt((json.dumps((command, args))).encode('utf-8'))
            self.client.send(encryped)

            response = json.loads(self.fernet.decrypt(self.client.recv(20000)).decode('utf-8'))
            # response = self.special
            # self.special.pop
            print(response)
            solamit = ''
            plen = ''
            t = response.split('#')
            print(t)
            print(len(t[1]))
            t[0]= int(t[0])
            if command == 'validate':
                self.thread5sec = threading.Thread(target=self.send_command_validate_port2,
                                                   args=('validate2', *args))
                self.thread5sec.start()
            if len(t[1]) == t[0]:
                return t[1]
            else:
                print("no")
        except socket.error as err:
            print(str(err))
        finally:
            self.lock.release()
            print("4")

    def send_validate_port2(self, command, *args):
            """
            a function that is responsible for sending a validate command to the server from the second port
            and recieving the answer from him
            :param command:
            :param args:
            :return:
            """
            self.lock.acquire()
            try:
                print("Sending JSON data :) :", json.dumps((command, args)))
                encryped = self.fernet.encrypt((json.dumps((command, args))).encode('utf-8'))
                self.client2.send(encryped)

                response = json.loads(self.fernet.decrypt(self.client2.recv(20000)).decode('utf-8'))
                # response = self.special
                # self.special.pop
                print(response)

                solamit = ''
                plen = ''
                t = response.split('#')
                print(t)
                print(len(t[1]))
                t[0] = int(t[0])
                if len(t[1]) == t[0]:
                    print(t[1])
                    return t[1]
                else:
                    print("no")
            except socket.error as err:
                print(str(err))
            finally:
                self.lock.release()

    def permission_exepted(self):
        encryped = self.fernet.encrypt((json.dumps(True)).encode('utf-8'))
        self.client2.send(encryped)
        print(encryped)

    def permission_declined(self):
        encryped = self.fernet.encrypt((json.dumps(False)).encode('utf-8'))
        self.client2.send(encryped)
        print(encryped)

    def get_permission(self, username, amount, second_user, transfor_name):
        """
        a function that gets a permission for a recieving or passing money from the other client
        throgh the server
        :param username:
        :param amount:
        :param second_user:
        :return:
        """
        per = self.send_command("permission", username, amount, second_user)
        return per

    def start1(self):
        """
        a function that starts the threading for the listening to the server
        :return:
        """
        self.thread5sec.start()

    def close(self):
        """
        a function that close the connection between the client and the server and stop the threading
        when the window is closed
        :return:
        """
        self.event.set()
        self.thread5sec.join()
        self.client.close()


def listen_server(fernet, client2, event, special, regular, lock):
    """
    a function that is listening every 5 seconds to the server and checking if a massage from him recieved
    :param fernet:
    :param client:
    :param event:
    :param special:
    :param regular:
    :param lock:
    :return:
    """
    while not event.is_set():
        # lock.acquire()
        try:

            data = json.loads(fernet.decrypt(client2.recv(20000)).decode('utf-8'))
            print("1 data: ", data)
            if data:
                permission_root = tk.Tk()
                permission_root.title("cashit permission")
                permission_root.geometry("300x300")
                permission_root.configure(bg='light green')
                permission_window = Toplevel(permission_root)
                permission_label = Label(permission_window, text=data)
                permission_label.pack()
                yes_button = Button(permission_window, text="yes", command=lambda: permission_exepted(client2, fernet))
                yes_button.pack(pady=5)
                no_button = Button(permission_window, text="no", command=lambda: permission_declined(client2, fernet))
                no_button.pack(pady=5)
                permission_root.mainloop()
        finally:
            # lock.release()
            # לעשות טיפול של ההודעה ולשים אותה בGUI במקרה ואכן התקבלה הודעה
            time.sleep(5)


def permission_exepted(client_socket, fernet):
    encryped = fernet.encrypt((json.dumps(True)).encode('utf-8'))
    client_socket.send(encryped)
    print(encryped)


def permission_declined(client_socket, fernet):
    encryped = fernet.encrypt((json.dumps(False)).encode('utf-8'))
    client_socket.send(encryped)
    print(encryped)

class CashitLogin:
    def __init__(self):
        self.client = CashitClient()
        self.client2 = CashitClient()
        self.client.connect()
        self.root = Tk()
        self.root.title("cashit Login")
        self.root.geometry("400x400")
        self.logo_img = Image.open(os.path.join(config.LOGO_FILE_PATH, "logo1.png"))
        self.logo_photo = ImageTk.PhotoImage(self.logo_img)
        self.root.configure(bg='light green')
        self.create_widgets()

    def create_widgets(self):
        """
        a function that opens the window of the log in to the system
        :return:
        """
        self.logo_label = Label(self.root, image=self.logo_photo)
        self.logo_label.pack(pady=10)

        self.username_label = Label(self.root, text="Username:")
        self.username_label.pack()
        self.username_entry = Entry(self.root)
        self.username_entry.pack()

        self.password_label = Label(self.root, text="Password:")
        self.password_label.pack()
        self.password_entry = Entry(self.root, show="*")
        self.password_entry.pack()

        self.sign_in_button = Button(self.root, text="Sign In", command=self.sign_in)
        self.sign_in_button.pack(pady=5)

        self.sign_up_button = Button(self.root, text="Sign Up", command=self.open_sign_up)
        self.sign_up_button.pack(pady=5)

    def sign_in(self):
        """
        a function that is checking if the user exist and return a massage according to that
        :return:
        """
        username = self.username_entry.get()
        password = self.password_entry.get()
        # hashed_password = hashlib.sha256(password.encode()).hexdigest

        if self.client.send_command("validate", username, password) == "True":
            #if self.client2.send_validate_port2("validate2", username, password) == "True":
            messagebox.showinfo("Success", "Logged in successfully.")
            self.root.destroy()
            #self.client.start1()
            main_app_window = CashitMainApp.MainApp(username, self.client)
            main_app_window.root.mainloop()
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    def open_sign_up(self):
        """
        a function who open the window of the sing up
        :return:
        """
        self.sign_up_window = Toplevel(self.root)
        sign_up_app = CashitSignUp(self.sign_up_window, self.client, self.root)
        self.sign_up_window.grab_set()

    def run(self):
        self.root.mainloop()


class CashitSignUp:
    def __init__(self, root, client, login):
        self.root = root
        self.client = client

        self.root.title("cashit Sign Up")
        self.root.geometry("400x400")
        self.login = login
        self.root.configure(bg='light green')

        self.create_widgets()

    def create_widgets(self):
        """
        a function that opens the window of the sing up to the system
        :return:
        """
        self.username_label = Label(self.root, text="Username:")
        self.username_label.pack()
        self.username_entry = Entry(self.root)
        self.username_entry.pack()

        self.password_label = Label(self.root, text="Password:")
        self.password_label.pack()
        self.password_entry = Entry(self.root, show="*")
        self.password_entry.pack()

        self.email_label = Label(self.root, text="email:")
        self.email_label.pack()
        self.email_entry = Entry(self.root)
        self.email_entry.pack()

        self.id_label = Label(self.root, text="id:")
        self.id_label.pack()
        self.id_entry = Entry(self.root)
        self.id_entry.pack()

        self.sum_label = Label(self.root, text="sum:")
        self.sum_label.pack()
        self.sum_entry = Entry(self.root)
        self.sum_entry.pack()

        self.submit_button = Button(self.root, text="Submit", command=self.submit_sign_up)
        self.submit_button.pack(pady=5)

    def submit_sign_up(self):
        """
        a function who get the details from the entries and saves them in the database
        :return:
        """
        username = self.username_entry.get()
        password = self.password_entry.get()
        # hashed_password = hashlib.sha256(password.encode()).hexdigest
        email = self.email_entry.get()
        id = self.id_entry.get()
        sum = self.sum_entry.get()
        result = self.client.send_command("SaveSignupDetails", username, password, email, id, sum)

        if result:
            messagebox.showinfo("Success", "Sign up successful.")
        else:
            messagebox.showinfo("Error ", "Sign up failed.")

        self.root.destroy()


if __name__ == "__main__":
    login_app = CashitLogin()
    login_app.run()
