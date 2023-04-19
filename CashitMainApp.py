from PIL import Image, ImageTk
import base64
from CashitClient import CashitClient
import binascii
from tkinter import filedialog
from io import BytesIO
import datetime
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import Label
import config
from tkinter import Toplevel


class MainApp:
    def __init__(self, username):
        self.username = username
        self.client = CashitClient()
        self.root = tk.Tk()
        self.root.title("cashit Main App")
        self.root.geometry("400x400")
        self.root.configure(bg='light green')

        self.create_widgets()

    def create_widgets(self):
        self.menu_frame = ttk.Frame(self.root)
        self.menu_frame.pack(pady=10)

        self.passmoney_button = ttk.Button(self.menu_frame, text="pass money", command=self.open_passmoney)
        self.passmoney_button.grid(row=0, column=0, padx=5)

        self.recieve_button = ttk.Button(self.menu_frame, text="recieve money", command=self.open_recieve)
        self.recieve_button.grid(row=0, column=1, padx=5)

        self.mymoney_button = ttk.Button(self.menu_frame, text="my money", command=self.open_post_mymoney)
        self.mymoney_button.grid(row=0, column=2, padx=5)

    def open_passmoney(self):
        self.passmoney_window = Toplevel(self.root)
        profile_app = CashitPassmoney(self.profile_window, self.client, self.username)
        self.passmoney_window.grab_set()

    def open_recieve(self):
        recieve_window = Toplevel(self.root)
        recieve_app = CashitRecieve(recieve_window)
        recieve_window.grab_set()

    def open_mymoney(self):
        mymoney_window = Toplevel(self.root)
        mymoney_app = CashitMymoney(mymoney_window)
        mymoney_window.grab_set()


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