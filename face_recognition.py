from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import os
import mysql.connector
import cv2
import numpy as np
from time import strftime
from datetime import datetime
import time
import re
import csv
import sqlite3


class Face_Recognition:
    def __init__(self, root):
        self.root = root
        self.root.geometry("890x600+350+50")
        self.root.title("FAMS - Recognition Students")
        # root.overrideredirect(1)

        # Background Image
        background_img = Image.open("./img/recognition_train.png")
        background_img = background_img.resize(
            (890, 600), Image.Resampling.LANCZOS)
        self.photoimg1 = ImageTk.PhotoImage(background_img)

        background_img = Label(self.root, image=self.photoimg1)
        background_img.place(x=0, y=0, width=900, height=600)

        train_btn = Button(background_img, command=self.train_classifier, text="Train DataSet", width=15, font=(
            "verdana", 10, "bold"), cursor="hand2", bg="#2DC6DB", fg="#ffffff")
        train_btn.place(x=95, y=240, width=120, height=35)

        recogn_btn = Button(background_img, command=self.face_recog, text="Recognition", width=15, font=(
            "verdana", 10, "bold"), cursor="hand2", bg="#30FFC1", fg="#ffffff")
        recogn_btn.place(x=430, y=500, width=120, height=35)

    # =====================Training Datasets===================

    def train_classifier(self):
        data_dir = ("data-img")
        path = [os.path.join(data_dir, file) for file in os.listdir(data_dir)]

        faces = []
        ids = []

        for image in path:
            img = Image.open(image).convert('L')  # Gray scale
            imageNp = np.array(img, 'uint8')
            id = int(os.path.split(image)[1].split('.')[1])

            faces.append(imageNp)
            ids.append(id)
            cv2.imshow("Training", imageNp)
            cv2.waitKey(1) == 13
        ids = np.array(ids)

        # ===== Train the classifier

        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.train(faces, ids)
        clf.write("algorithms/clf.xml")
        cv2.destroyAllWindows()

    # =====================Mark Attendance Function : ===================

    def mark_attendance(self, i, r, n, d, al):
        now = datetime.now()
        date_1 = now.strftime("%d-%m-%Y")

        f = open("attendance_record/" + date_1 + ".csv", "a+")

        myDatalist = []
        f.seek(0)
        while True:
            a = f.readline().strip().split(",")
            # print('a',a)
            if a == ['']:
                break
            myDatalist.append(a)
        name_list = []
        for line in myDatalist:
            name_list.append(line[1].strip())
        if r not in name_list:

            now = datetime.now()
            d1 = now.strftime("%d/%m/%Y")
            dtString = now.strftime("%H:%M:%S")
            f.write(i + "," + r + "," + n + "," +
                    dtString + "," + d1 + "," + "Present")

 # ================face recognition==================

    def face_recog(self):

        def draw_boundray(img, classifier, scaleFactor, minNeighbors, color, text, clf):
            gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            featuers = classifier.detectMultiScale(
                gray_image, scaleFactor, minNeighbors)

            coord = []

            for (x, y, w, h) in featuers:
                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
                id, predict = clf.predict(gray_image[y:y+h, x:x+w])

                confidence = int((100*(1-predict/300)))

                conn = sqlite3.connect("database/attendence_management.db")
                cursor = conn.cursor()

                cursor.execute(
                    "select * from student where Student_ID="+str(id))
                al = cursor.fetchall()

                cursor.execute(
                    "select Name from student where Student_ID="+str(id))
                n = cursor.fetchone()
                n = str(n)[2:-3]

                # n="+".join(n)

                cursor.execute(
                    "select Roll from student where Student_ID="+str(id))
                r = cursor.fetchone()
                r = str(r)[2:-3]
                # print(r)
                # r="+".join(r)

                cursor.execute(
                    "select Course from student where Student_ID="+str(id))
                d = cursor.fetchone()
                d = str(d)[2:-3]

                # d="+".join(d)

                cursor.execute(
                    "select Student_ID from student where Student_ID="+str(id))
                i = cursor.fetchone()
                i = str(i)[1:-2]
                # print(i)

                if confidence > 82:
                    cv2.putText(
                        img, f"ID:{i}", (x, y-80), cv2.FONT_HERSHEY_COMPLEX, 0.8, (64, 15, 223), 1)
                    cv2.putText(
                        img, f"Name:{n}", (x, y-55), cv2.FONT_HERSHEY_COMPLEX, 0.8, (64, 15, 223), 1)
                    cv2.putText(
                        img, f"Roll No:{r}", (x, y-30), cv2.FONT_HERSHEY_COMPLEX, 0.8, (64, 15, 223), 1)
                    cv2.putText(
                        img, f"Course:{d}", (x, y-10), cv2.FONT_HERSHEY_COMPLEX, 0.8, (64, 15, 223), 1)
                    self.mark_attendance(i, r, n, d, al)

                else:
                    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 3)
                    cv2.putText(img, "Unknown Face", (x, y-8),
                                cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 0), 1)

                coord = [x, y, w, y]

            return coord

        # ========== Recognize Function
        def recognize(img, clf, faceCascade):
            coord = draw_boundray(img, faceCascade, 1.1,
                                  10, (255, 25, 255), "Face", clf)
            return img

        faceCascade = cv2.CascadeClassifier(
            "algorithms/haarcascade_frontalface_default.xml")
        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.read("algorithms/clf.xml")

        videoCap = cv2.VideoCapture(0)

        while True:
            ret, img = videoCap.read()
            img = recognize(img, clf, faceCascade)
            cv2.imshow("Face Detector", img)

            if cv2.waitKey(1) == 13:
                break
        videoCap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    root = Tk()
    obj = Face_Recognition(root)
    root.mainloop()
