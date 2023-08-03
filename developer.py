from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import os


class Developer:

    def __init__(self, root):
        self.root = root
        self.root.geometry("890x600+350+50")
        self.root.title("FAMS - Vishal Saraiwal")
        # root.overrideredirect(1)

        # Background Image
        background_img = Image.open("./img/Developer2.png")
        background_img = background_img.resize(
            (890, 600), Image.Resampling.LANCZOS)
        self.photoimg1 = ImageTk.PhotoImage(background_img)

        background_img = Label(self.root, image=self.photoimg1)
        background_img.place(x=0, y=0, width=900, height=600)


if __name__ == "__main__":
    root = Tk()
    obj = Developer(root)
    root.mainloop()
