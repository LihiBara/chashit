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
        self.port = port
        self.special = []
        self.regular = []
        with io.open("key.key", mode='r') as file:
            # Write content to the file
            key = file.read()
        self.fernet = Fernet(key)
        self.lock = threading.Lock()
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.event = threading.Event()
        self.thread5sec = threading.Thread(target=listen_server,
                                           args=(
                                           self.fernet, self.client, self.event, self.special, self.regular, self.lock))

    def connect(self):
        """
        a function that connects to the server
        :return:
        """
        self.client.connect((self.host, self.port))

    # def encrypt_json_file(file_path, key):
    #     with open(file_path, 'r') as file:
    #         data = json.load(file)
    #
    #     serialized_data = json.dumps(data).encode('utf-8')
    #     cipher_suite = Fernet(key)
    #     encrypted_data = cipher_suite.encrypt(serialized_data)
    #
    #     encrypted_file_path = f"{file_path}.encrypted"
    #     with open(encrypted_file_path, 'wb') as encrypted_file:
    #         encrypted_file.write(encrypted_data)
    #
    #     print(f"JSON file encrypted successfully. Encrypted file saved as {encrypted_file_path}.")
    # def decrypt_json_file(json, key):
    #     encrypted_data = json
    #
    #     cipher_suite = Fernet(key)
    #     decrypted_data = cipher_suite.decrypt(encrypted_data)
    #
    #     serialized_data = decrypted_data.decode('utf-8')
    #     data = json.loads(serialized_data)
    #
    #     decrypted_file_path = f"{file_path[:-10]}.decrypted.json"  # Remove the '.encrypted' extension
    #     with open(decrypted_file_path, 'w') as decrypted_file:
    #         json.dump(data, decrypted_file, indent=4)
    #
    #     print(f"JSON file decrypted successfully. Decrypted file saved as {decrypted_file_path}.")

    def send_command(self, command, *args):
        """
        a function that is responsible for sending an encrepted command to the server
        and recieving the answer from him
        :param command:
        :param args:
        :return:
        """
        self.lock.acquire()
        response = "lihi"
        try:
            print("Sending JSON data :) :", json.dumps((command, args)))
            command = config.COMMANDPRO + command
            encryped = self.fernet.encrypt((json.dumps((command, args))).encode('utf-8'))
            self.client.send(encryped)

            response = json.loads(self.fernet.decrypt(self.client.recv(20000)).decode('utf-8'))
            # response = self.special
            # self.special.pop
            print(response)
            solamit = ''
            plen = ''
            # while solamit:
            #    while solamit != '#':
            #        solamit = json.loads(self.client.recv(1).decode('utf-8'))
            #        plen += solamit
            #    if json.loads(self.client.recv(1).decode('utf-8'))=="#":
            #        response = json.loads(self.client.recv(2000).decode('utf-8'))
            # plen = int(plen)
            # print(response)
        except socket.error as err:
            print(str(err))
        finally:
            self.lock.release()
            return response

    def get_permission(self, username, amount, second_user):
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


def listen_server(fernet, client, event, special, regular, lock):
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

            data = json.loads(fernet.decrypt(client.recv(20000)).decode('utf-8'))

            print("1 data: ", data)
            if data:
                permission_window = Toplevel(client.root)

                client.permission_label = Label(permission_window, text=data + "yes/no")
                client.permission_label.pack()
                client.permission_entry = Entry(permission_window)
                client.permission_entry.pack()
                if client.permission_entry.get == "yes":
                    return True
                elif client.permission_entry.get == "no":
                    return False
                else:
                    print("answer with yes/no")
        finally:
            # lock.release()
            # לעשות טיפול של ההודעה ולשים אותה בGUI במקרה ואכן התקבלה הודעה
            time.sleep(5)


class CashitLogin:
    def __init__(self):
        self.client = CashitClient()
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

        if self.client.send_command("validate", username, password):
            messagebox.showinfo("Success", "Logged in successfully.")
            self.root.destroy()
            self.client.start1()
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
