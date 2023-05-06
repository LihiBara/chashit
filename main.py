from tkinter import *
from PIL import ImageTk, Image
import tkinter as tk
from tkinter import font as tkfont  # python 3
import re
from tkinter import messagebox, ttk


regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')


def email_check(email):
    if re.fullmatch(regex, email):
        return "emailtrue"
    else:
        return "emailwrong"


def cc_check(credit_card: str):
    if (len(credit_card) == 15 or len(credit_card) == 16) and credit_card.isnumeric():
        return "cctrue"
    else:
        return "ccwrong"


def cvv_check(cvv_number: str):
    if len(cvv_number) == 3 and cvv_number.isnumeric():
        return "cvvtrue"
    else:
        return "cvvwrong"


def iden_check(iden: str):
    if len(iden) == 9 and iden.isnumeric():
        return "identrue"
    else:
        return "idenwrong"


def verify(name, iden, email, password, cc, month, year, cvv):
    # name no check
    print(email_check)
    print(cc_check)
    print(cvv_check)
    print(iden_check)


class SampleApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, SignUpPage, LogInPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("StartPage")

    def show_frame(self, page_name):
        #Show a frame for the given page name
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background='#99ff99')
        self.canvas = Canvas(self, width=700, height=450)
        self.img = Image.open("original_image.jpg")
        self.resized_image = self.img.resize((700, 450), Image.ANTIALIAS)
        self.resized_image.save("fixed_image.jpg")
        self.new_image = ImageTk.PhotoImage(Image.open("fixed_image.jpg"))
        self.logo = Label(self, image=self.new_image)
        self.sign_up = Button(self, text="Sign Up", font=("Aharoni", 20), bg="#60ff60", borderwidth=1,
                              command=lambda: controller.show_frame("SignUpPage"))
        self.log_in = Button(self, text="Log In", bg="#60ff60", font=("Aharoni", 20), borderwidth=1,
                             command=lambda: controller.show_frame("LogInPage"))

        self.logo.place(x=250, y=-50, width=700, height=450)
        self.sign_up.place(x=475, y=400, width=100, height=100)
        self.log_in.place(x=625, y=400, width=100, height=100)

#    def startup(self):
#       self.win.geometry("1200x650")
#      self.win.configure(bg='#99ff99')
#     self.logo.place(x=250, y=-50, width=700, height=450)
#    self.sign_up.place(x=475, y=400, width=100, height=100)
#   self.log_in.place(x=625, y=400, width=100, height=100)
#  self.win.mainloop()


class SignUpPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background='#99ff99')
        self.controller = controller
        label = tk.Label(self, text="SIGN UP", font=controller.title_font, background='#99ff99')
        name_entry = Entry(self, font="Aharoni")
        email_entry = Entry(self, font="Aharoni")
        id_entry = Entry(self, font="Aharoni")
        password_entry = Entry(self, font="Aharoni")
        credit_entry = Entry(self, font="Aharoni")
        cvv_entry = Entry(self, font="Aharoni")
        name_label = Label(self, font="Aharoni", text="name:", background='#99ff99')
        email_label = Label(self, font="Aharoni", text="email:", background='#99ff99')
        id_label = Label(self, font="Aharoni", text="id:", background='#99ff99')
        password_label = Label(self, font="Aharoni", text="password:", background='#99ff99')
        credit_label = Label(self, font="Aharoni", text="credit card number:", background='#99ff99')
        cvv_label = Label(self, font="Aharoni", text="CVV:", background='#99ff99')
        date_label = Label(self, font="Aharoni", text="valid:", background='#99ff99')
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        check_button = Button(self, text="Submit", background="#60ff60", borderwidth=2, font=("Aharoni", 15),
                              command=lambda: verify(name_entry.get(), id_entry.get(), email_entry.get(),
                                                     password_entry.get(), credit_entry.get(), combo1.get(),
                                                     combo2.get(), cvv_entry.get()))
        combo1 = ttk.Combobox(self, state="readonly", values=[str(i) for i in range(1, 13)])
        combo2 = ttk.Combobox(self, state="readonly", values=[str(i) for i in range(2024, 2050)])

        button.pack()
        name_label.place(x=100, y=75)
        email_label.place(x=100, y=175)
        id_label.place(x=600, y=75)
        password_label.place(x=600, y=175)
        credit_label.place(x=100, y=355)
        cvv_label.place(x=700, y=428)
        date_label.place(x=100, y=428)
        name_entry.place(x=100, y=100, width=490, height=45)
        email_entry.place(x=100, y=200, width=490, height=45)
        id_entry.place(x=600, y=100, width=490, height=45)
        password_entry.place(x=600, y=200, width=490, height=45)
        credit_entry.place(x=100, y=380, width=1000, height=45)
        cvv_entry.place(x=700, y=450, width=400, height=45)
        check_button.place(x=550, y=550, width=100, height=50)
        combo1.place(x=100, y=450)
        combo2.place(x=300, y=450)

class LogInPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background='#99ff99')
        self.controller = controller
        label = tk.Label(self, text="LOG IN", font=controller.title_font, background='#99ff99')
        email_label = Label(self, font="Aharoni", text="email:", background='#99ff99')
        password_label = Label(self, font="Aharoni", text="password:", background='#99ff99')
        email_entry = Entry(self, font="Aharoni")
        password_entry = Entry(self, font="Aharoni")
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()
        email_label.place(x=350, y=260)
        password_label.place(x=350, y=160)
        email_entry.place(x=350, y=280, width=550, height=50)
        password_entry.place(x=350, y=180, width=550, height=50)


if __name__ == "__main__":
    app = SampleApp()
    app.geometry("1200x650")

app.mainloop()
