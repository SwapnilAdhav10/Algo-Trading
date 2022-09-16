from tkinter import *
from tkinter import ttk,messagebox
from PIL import Image,ImageTk
import re # for validation
import psycopg2
from Registration import *


class Userlogin_page:
    def __init__(self, root):
        self.root = root
        self.root.geometry('1920x1080')
        self.root.title("User login page")

        # title frame

        title_frame = Frame(self.root, bd=1, relief=RAISED, bg='lightgreen')
        title_frame.place(x=400, y=0, width=500, height=82)  ## unit of x & y is pixel

        title_label = Label(title_frame, text="User Login", font=('Times New Roman', 30, 'bold'), fg='black',
                            bg='lightgreen')
        title_label.place(x=125, y=10)

        # variables
        self.user_id = StringVar()
        self.password = StringVar()

        # User Id
        # ID frame

        ID_frame = Frame(self.root, bd=1, relief=RAISED, bg='lightgreen')
        ID_frame.place(x=425, y=150, width=450, height=60)  ## unit of x & y is pixel

        l1 = Label(ID_frame, text="User ID : ", font=('Times New Roman', 18, 'bold'), fg='darkblue')
        l1.grid(row=0, column=0, padx=10, pady=10, sticky=W)

        e1 = ttk.Entry(ID_frame, textvariable=self.user_id, font=('Times New Roman', 17, 'bold'), width=20)
        e1.grid(row=0, column=1, padx=20, pady=10, sticky=W)

        # password frame

        password_frame = Frame(self.root, bd=1, relief=RAISED, bg='lightgreen')
        password_frame.place(x=425, y=250, width=450, height=60)  ## unit of x & y is pixel

        l2 = Label(password_frame, text="Password :", font=('Times New Roman', 18, 'bold'), fg='darkblue')
        l2.grid(row=0, column=0, padx=10, pady=10, sticky=W)

        e2 = ttk.Entry(password_frame, textvariable=self.password, show='*', font=('Times New Roman', 17, 'bold'),
                       width=20)
        e2.grid(row=0, column=1, padx=10, pady=10, sticky=W)

        # login button frame
        login_frame = Frame(self.root, bd=1, relief=RAISED, bg='skyblue')
        login_frame.place(x=425, y=400, width=200, height=55)

        # login Button
        User_login = Button(login_frame, text='Login', command=self.validate, width=15, bg='brown', fg='white',
                            font=('bold', 15), cursor='hand2')
        User_login.grid(row=0, column=0, padx=10, pady=5)

        # sign up button frame
        signup_frame = Frame(self.root, bd=1, relief=RAISED, bg='skyblue')
        signup_frame.place(x=675, y=400, width=200, height=55)

        # sign up Button
        Sign_Up = Button(signup_frame, text='Sign Up', command=self.User_reg, width=15, bg='brown', fg='white',
                         font=('bold', 15), cursor='hand2')
        Sign_Up.grid(row=0, column=0, padx=10, pady=5)

    def User_reg(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = UserRegister(self.new_win)

    def validate(self):
        conn = psycopg2.connect(database="AlgoTrading", user="postgres", password="Swapnil10@", host="127.0.0.1",
                                port="5432")
        cur = conn.cursor()
        cur.execute("select * from registration")
        rows = cur.fetchall()
        flag = False
        for row in rows:
            if row[2] == self.user_id.get() and row[4] == self.password.get():
                flag = True
                break
            else:
                flag = False
        if flag == True:
            self.user_page()
        else:
            messagebox.showerror('ERROR', 'Invali User-Id or Password')

    def user_page(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = Window(self.new_win)


if __name__ == '__main__':
    root = Tk()
    obj = Userlogin_page(root)
    root.mainloop()
