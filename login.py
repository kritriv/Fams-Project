from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector
# --------------------------
from home import Face_Recognition_system
import os
import time
import sqlite3


class Login:
    def __init__(self, login_root):

        self.login_root = login_root
        self.login_root.title(
            "FAMS - Facial Recognition Attendance Management System")
        self.login_root.wm_iconbitmap("logo.ico")
        self.login_root.geometry("1280x700+0+0")

        self.var_ssq = StringVar()
        self.var_sa = StringVar()
        self.var_pwd = StringVar()

        background_img = Image.open("./img/login.png")
        background_img = background_img.resize(
            (1250, 680), Image.Resampling.LANCZOS)
        self.photoimg1 = ImageTk.PhotoImage(background_img)

        background_img = Label(self.login_root, image=self.photoimg1)
        background_img.place(x=10, y=0, width=1250, height=680)

        # label1
        username = lb1 = Label(background_img, text="Username:", font=(
            "times new roman", 15, "bold"), fg="#4A5B5E", bg="white")
        username.place(x=835, y=330)

        # entry1
        self.txtuser = ttk.Entry(
            background_img, font=("times new roman", 15, "bold"))
        self.txtuser.place(x=940, y=330, width=180)

        # label2
        pwd = lb1 = Label(background_img, text="Password:", font=(
            "times new roman", 15, "bold"), fg="#023137", bg="white")
        pwd.place(x=835, y=390)

        # entry2
        self.txtpwd = ttk.Entry(background_img, show="*", font=(
            "times new roman", 15, "bold"))
        self.txtpwd.place(x=940, y=390, width=180)

        Login_btn = Button(background_img, command=self.login, text="LOGIN NOW", width=15, font=(
            "verdana", 10, "bold"), bg="#2DC6DB", fg="#023137")
        Login_btn.place(x=920, y=450, width=120, height=35)

    def login(self):
        if (self.txtuser.get() == "" or self.txtpwd.get() == ""):
            messagebox.showerror("Error", "All Field Required!")
        else:
            conn = sqlite3.connect("database/attendence_management.db")

            mycursor = conn.cursor()
            mycursor.execute("select * from login_tbl where Username=? and Password=?", (
                self.txtuser.get(),
                self.txtpwd.get()
            ))
            row = mycursor.fetchone()
            if row == None:
                messagebox.showerror("Error", "Invalid Username and Password!")
            else:
                open_min = messagebox.askyesno("YesNo", "You want to Enter?")
                if open_min > 0:
                    self.new_window = Toplevel(self.login_root)
                    self.app = Face_Recognition_system(self.new_window)
                    if app == True:
                        self.login_root.destroy()
                else:
                    if not open_min:
                        return
            conn.commit()
            conn.close()


if __name__ == "__main__":
    login_root = Tk()
    login_root.resizable(0, 0)
    app = Login(login_root)
    login_root.mainloop()
