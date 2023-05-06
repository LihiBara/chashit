from PIL import Image, ImageTk
import base64
from CashitClient import CashitClient
import binascii
from tkinter import filedialog
from io import BytesIO
import datetime
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import Entry
from tkinter import messagebox
from tkinter import Label
import config
from tkinter import Toplevel

from CashitDB import CashitDB


class MainApp:
    def __init__(self, username):
        self.username = username
        self.client = CashitClient()
        self.root = tk.Tk()
        self.root.title("cashit Main App")
        self.root.geometry("400x400")
        self.root.configure(bg='light green')

        self.second_user = ""
        self.amount = 0

        self.create_widgets()

    def create_widgets(self):
        self.menu_frame = ttk.Frame(self.root)
        self.menu_frame.pack(pady=10)

        self.passmoney_button = ttk.Button(self.menu_frame, text="pass money", command=self.open_passmoney)
        self.passmoney_button.grid(row=0, column=0, padx=5)

        self.recieve_button = ttk.Button(self.menu_frame, text="recieve money", command=self.open_recieve)
        self.recieve_button.grid(row=0, column=1, padx=5)

        self.mymoney_button = ttk.Button(self.menu_frame, text="my money", command=self.open_mymoney)
        self.mymoney_button.grid(row=0, column=2, padx=5)

    def open_passmoney(self):
        recieve_window = Toplevel(self.root)
        recieve_app = CashitRecieve(recieve_window)

        self.on_click(self.username, recieve_window, "Enter user to pass money :")

        self.submit_button = Button(recieve_window, text="Submit", command=self.submit_pass)
        self.submit_button.pack(pady=5)

        recieve_window.grab_set()




    def open_recieve(self):
        self.recieve_window = Toplevel(self.root)
        recieve_app = CashitRecieve(self.recieve_window)

        self.on_click(self.username, self.recieve_window, "Enter user to receive money :")

        self.submit_button = Button(self.recieve_window, text="Submit", command=self.submit_receive)
        self.submit_button.pack(pady=5)

        self.recieve_window.grab_set()

    def open_mymoney(self):
        mymoney_window = Toplevel(self.root)
        mymoney_app = CashitMymoney(mymoney_window)
        money = get_my_money(self.username)

        label = Label(mymoney_window, text=f" You have {money} money in your account")

        label.pack()
        mymoney_window.grab_set()

    def submit_receive(self):
        self.second_user = self.username_entry.get()
        self.amount = self.money_entry.get()
        #if CashitClient.get_permission(self.CashitClient, self.username, self.amount, self.second_user):
        set_money(self.username, int(self.amount))
        set_money(self.second_user, -1 * int(self.amount))
        #else:
        #לכתןב הודעה שלא אושר
        #    pass
        self.recieve_window.destroy()

    def submit_pass(self):
        self.second_user = self.username_entry.get()
        self.amount = self.money_entry.get()

        set_money(self.second_user, int(self.amount))
        set_money(self.username, -1 * int(self.amount))

        self.recieve_window.destroy()

    def on_click(self, username, root, txt):
        self.username_label = Label(root, text=txt)
        self.username_label.pack()
        self.username_entry = Entry(root)
        self.username_entry.pack()

        self.money_label = Label(root, text="Enter money amount")
        self.money_label.pack()
        self.money_entry = Entry(root)
        self.money_entry.pack()


class CashitPassmoney:
    def __init__(self, root, client, username):
        self.root = root
        self.client = client
        self.username = username
        self.create_widgets()

    def create_widgets(self):
        self.root.title("Profile")
        self.root.geometry("400x400")

        self.username_label = Label(self.root, text=f"Username: {self.username}")
        self.username_label.pack()

        user_data = self.client.send_command("ReadSignup", self.username)


class CashitRecieve:
    def __init__(self, root):
        self.root = root
        # Add the code for the explore window here


class CashitMymoney:
    def __init__(self, root):
        self.root = root
        # Add the code for the post image window here


def get_my_money(username):
    conn = CashitDB().create_connection()

    with conn:
        query = "SELECT * FROM users WHERE username = ?"
        result = conn.execute(query, (username,)).fetchone()
        sum = result[4]
        # return result

    conn.close()
    return sum


def set_money(username, amount):
    # print(username)

    current_money = int(get_my_money(username))
    updated_money = current_money + amount

    # Validate that user is existed in DB

    if updated_money < 0:
        raise Exception(f"Sorry, you have {current_money} money, you cant pass {amount} :(")

    conn = CashitDB().create_connection()

    with conn:
        query = "UPDATE users SET sum = ? WHERE username = ?"
        result = conn.execute(query, (updated_money, username))
        conn.commit()
        # return result

    conn.close()
    return sum
