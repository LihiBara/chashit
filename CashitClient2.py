 #file name CashitClient.py
import os.path
import socket
import json
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import CashitMainApp
import threading
import time
from tkinter import filedialog
import base64
import config

"""
to do : 
1. encrypt  password  in connection amd in data base
2. ake encrypt connection 
3. asserts 
4 fix bug , mtdetails after update 
"""


class CashitClient:
    def __init__(self, host="127.0.0.1", port=8080):
        self.host = host
        self.port = port
        self.special = []
        self.regular = []
        self.lock = threading.Lock()
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.event = threading.Event()
        self.thread5sec = threading.Thread(target=listen_server,
                                           args=(self.client, self.event, self.special, self.regular, self.lock))

    def connect(self):
        self.client.connect((self.host, self.port))

    def send_command(self, command, *args):
        self.lock.acquire()
        response = "lihi"
        try:
            print("Sending JSON data:", json.dumps((command, args)))
            self.client.send(json.dumps((command, args)).encode('utf-8'))
            response = json.loads(self.client.recv(20000).decode('utf-8'))
            #response = self.special
            #self.special.pop
            print(response)
        except socket.error as err:
            print(str(err))
        finally:
            self.lock.release()
            return response

    def get_permission(self, username, amount, second_user):
        per = self.send_command("permission", username, amount, second_user)
        return per

    def start1(self):
        self.thread5sec.start()

    def close(self):
        self.event.set()
        self.thread5sec.join()
        self.client.close()


def listen_server(client, event, special, regular, lock):


        while not event.is_set():
            #lock.acquire()
            try:
                #
#                solamit = ''
#               plen = ''
 #               while solamit != '#':
 #                   solamit = json.loads(client.recv(1).decode('utf-8'))
  #                  if solamit != '#':
   #                     plen += solamit
    #                plen = int(plen)
                    data = json.loads(client.recv(20000).decode('utf-8'))
            finally:
                #lock.release()
                #לעשות טיפול של ההודעה ולשים אותה בGUI במקרה ואכן התקבלה הודעה
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

        self.create_widgets()

    def create_widgets(self):
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
        username = self.username_entry.get()
        password = self.password_entry.get()

        if self.client.send_command("validate", username, password):
            messagebox.showinfo("Success", "Logged in successfully.")
            self.root.destroy()
            self.client.start1()
            main_app_window = CashitMainApp.MainApp(username, self.client)
            main_app_window.root.mainloop()
        else:
            messagebox.showerror("Error", "Invalid username or password.")


    def open_sign_up(self):
        self.sign_up_window = Toplevel(self.root)
        sign_up_app = CashitSignUp(self.sign_up_window, self.client,self.root)
        self.sign_up_window.grab_set()

    def run(self):
        self.root.mainloop()


class CashitSignUp:
    def __init__(self, root, client,login ):
        self.root = root
        self.client = client

        self.root.title("cashit Sign Up")
        self.root.geometry("400x400")
        self.login=login

        self.create_widgets()

    def create_widgets(self):
        self.username_label = Label(self.root, text="Username:")
        self.username_label.pack()
        self.username_entry= Entry(self.root)
        self.username_entry.pack()

        self.password_label = Label(self.root, text="Password:")
        self.password_label.pack()
        self.password_entry = Entry(self.root, show="*")
        self.password_entry.pack()

        self. email_label = Label(self.root, text="email:")
        self. email_label.pack()
        self. email_entry = Entry(self.root)
        self. email_entry.pack()

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
        username = self.username_entry.get()
        password = self.password_entry.get()
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
