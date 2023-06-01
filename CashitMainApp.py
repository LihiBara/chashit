"""
author - lihi
date   - 29 / 05 / 23
main_app
"""
from PIL import Image, ImageTk
import base64

import CreditBank
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
    def __init__(self, username, client):
        self.submitmoney_button = None
        self.username = username
        #self.client = CashitClient()
        self.client = client
        self.root = tk.Tk()
        self.root.title("cashit Main App")
        self.root.geometry("400x400")
        self.root.configure(bg='light green')

        self.second_user = ""
        self.amount = 0

        self.create_widgets()

    def create_widgets(self):
        """
         a function that opens the window of the main page of the function
        :return:
        """
        self.menu_frame = ttk.Frame(self.root)
        self.menu_frame.pack(pady=10)

        self.passmoney_button = ttk.Button(self.menu_frame, text="pass money", command=self.open_passmoney)
        self.passmoney_button.grid(row=0, column=0, padx=5)

        self.recieve_button = ttk.Button(self.menu_frame, text="recieve money", command=self.open_recieve)
        self.recieve_button.grid(row=0, column=1, padx=5)

        self.mymoney_button = ttk.Button(self.menu_frame, text="my money", command=self.open_mymoney)
        self.mymoney_button.grid(row=0, column=2, padx=5)

        self.chargemoney_button = ttk.Button(self.menu_frame, text="charge money", command=self.open_chargemoney)
        self.chargemoney_button.grid(row=0, column=3, padx=5)

    def open_chargemoney(self):
        """
        a function that opening a window who is responsibale of charging
        money to the account from the bank
        :return:
        """
        chargemoney_window = Toplevel(self.root)
        chargemoney_app = CashitRecieve(chargemoney_window)

        self.moneycharge_label = Label(chargemoney_window, text="Enter money amount to charge")
        self.moneycharge_label.pack()
        self.moneycharge_entry = Entry(chargemoney_window)
        self.moneycharge_entry.pack()

        self.cardnumber_label = Label(chargemoney_window, text="Enter card number")
        self.cardnumber_label.pack()
        self.cardnumber_entry = Entry(chargemoney_window)
        self.cardnumber_entry.pack()

        self.valid_label = Label(chargemoney_window, text="Enter validation date")
        self.valid_label.pack()
        self.valid_entry = Entry(chargemoney_window)
        self.valid_entry.pack()

        self.cvv_label = Label(chargemoney_window, text="Enter CVV")
        self.cvv_label.pack()
        self.cvv_entry = Entry(chargemoney_window)
        self.cvv_entry.pack()

        current_money = int(get_my_money(self.username))

        self.submitmoney_button = Button(chargemoney_window, text="Submit",
                                         command=lambda: CreditBank.charging(self.username, self.moneycharge_entry.get(), current_money))
        self.submitmoney_button.pack(pady=5)

        chargemoney_window.grab_set()

    def open_passmoney(self):
        """
        a function that opening a window who is responsibale of passing money to another account
        :return:
        """
        self.passmoney_window = Toplevel(self.root)
        passmoney_app = CashitRecieve(self.passmoney_window)

        self.on_click(self.username, self.passmoney_window, "Enter user to pass money :")

        self.submit_button = Button(self.passmoney_window, text="Submit", command=self.submit_pass)
        self.submit_button.pack(pady=5)

        self.passmoney_window.grab_set()

    def open_recieve(self):
        """
        a function that opening a window who is responsibale of recieving money to another account
        :return:
        """
        self.recieve_window = Toplevel(self.root)
        recieve_app = CashitRecieve(self.recieve_window)

        self.on_click(self.username, self.recieve_window, "Enter user to receive money :")

        self.submit_button = Button(self.recieve_window, text="Submit", command=self.submit_receive)
        self.submit_button.pack(pady=5)

        self.recieve_window.grab_set()

    def open_mymoney(self):
        """
        a function that opening a window who is responsibale of showing the money in the account
        :return:
        """
        mymoney_window = Toplevel(self.root)
        mymoney_app = CashitMymoney(mymoney_window)
        money = get_my_money(self.username)

        label = Label(mymoney_window, text=f" You have {money} money in your account")

        label.pack()
        mymoney_window.grab_set()

    def submit_receive(self):
        """
        a function who is responsibale of the money transfer
        :return:
        """
        self.second_user = self.username_entry.get()
        self.amount = self.money_entry.get()
        if self.client.get_permission(self.username, self.amount, self.second_user) == 1:
            set_money(self.username, int(self.amount))
            set_money(self.second_user, -1 * int(self.amount))
        else:
            #לכתןב הודעה שלא אושר
            pass
        self.recieve_window.destroy()

    def submit_pass(self):
        """
        a function who is responsibale of the money transfer
        :return:
        """
        self.second_user = self.username_entry.get()
        self.amount = self.money_entry.get()

        set_money(self.second_user, int(self.amount))
        set_money(self.username, -1 * int(self.amount))

        self.passmoney_window.destroy()

    def on_click(self, username, root, txt):
        """
        a function who is responsible for the GUI of the money transfer
        :param username:
        :param root:
        :param txt:
        :return:
        """
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
        self.root.title("Cashit")
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
    """
    a function who gets the money amount from the database by the username
    :param username:
    :return:
    """
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
    """
    a function who sets the new money amount of each user
    in the database by the username
    """
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
