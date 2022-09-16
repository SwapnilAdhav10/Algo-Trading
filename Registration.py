from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import re  # for validation
import psycopg2


class UserRegister:
    def __init__(self, root):
        self.root = root
        self.root.geometry('1920x1080')
        self.root.title("User Registration")
        self.root.config(bg="white")
        self.root.focus_force()

        # variable
        self.f_name = StringVar()
        self.l_name = StringVar()
        self.email = StringVar()
        self.contact = StringVar()
        self.password = StringVar()
        self.c_password = StringVar()

        # title frame

        title_frame = Frame(self.root, bd=1, relief=RAISED, bg='skyblue')
        title_frame.place(x=400, y=0, width=550, height=82)  ## unit of x & y is pixel

        title_label = Label(title_frame, text="User  Register", font=('Times New Roman', 30, 'bold'), fg='black',
                            bg='skyblue')
        title_label.place(x=120, y=10)

        # information frame
        main_frame = Frame(self.root, bd=1, relief=RIDGE)
        main_frame.place(x=400, y=80, width=550, height=600)

        # First Name
        l1 = Label(main_frame, text="First Name:", font=('Times New Roman', 16, 'bold'), fg='darkblue')
        l1.grid(row=0, column=0, padx=10, pady=10, sticky=W)

        e1 = ttk.Entry(main_frame, textvariable=self.f_name, font=('Times New Roman', 15, 'bold'), width=17)
        e1.grid(row=0, column=1, padx=10, pady=10, sticky=W)

        # callback & Validation f_name
        validate_fname = self.root.register(self.checkf_name)
        e1.config(validate='key', validatecommand=(validate_fname, '%P'))

        # Last Name
        l2 = Label(main_frame, text="Last Name:", font=('Times New Roman', 16, 'bold'), fg='darkblue')
        l2.grid(row=1, column=0, padx=10, pady=10, sticky=W)

        e2 = ttk.Entry(main_frame, textvariable=self.l_name, font=('Times New Roman', 15, 'bold'), width=17)
        e2.grid(row=1, column=1, padx=10, pady=10, sticky=W)

        # callback & Validation l_name
        validate_lname = self.root.register(self.checkl_name)
        e2.config(validate='key', validatecommand=(validate_lname, '%P'))

        # email
        l3 = Label(main_frame, text="Email:", font=('Times New Roman', 16, 'bold'), fg='darkblue')
        l3.grid(row=2, column=0, padx=10, pady=10, sticky=W)

        e3 = ttk.Entry(main_frame, textvariable=self.email, font=('Times New Roman', 15, 'bold'), width=30)
        e3.grid(row=2, column=1, padx=10, pady=10, sticky=W)

        # callback & Validation email
        validate_email = self.root.register(self.check_email)
        e3.config(validate='key', validatecommand=(validate_email, '%P'))

        # contact
        l4 = Label(main_frame, text="Contact:", font=('Times New Roman', 16, 'bold'), fg='darkblue')
        l4.grid(row=3, column=0, padx=10, pady=10, sticky=W)

        e4 = ttk.Entry(main_frame, textvariable=self.contact, font=('Times New Roman', 15, 'bold'), width=25)
        e4.grid(row=3, column=1, padx=10, pady=10, sticky=W)

        # callback & Validation contact
        validate_contact = self.root.register(self.check_contact)
        e4.config(validate='key', validatecommand=(validate_contact, '%P'))

        # password
        l8 = Label(main_frame, text="Password:", font=('Times New Roman', 16, 'bold'), fg='darkblue')
        l8.grid(row=7, column=0, padx=10, pady=10, sticky=W)

        e8 = ttk.Entry(main_frame, textvariable=self.password, font=('Times New Roman', 15, 'bold'), width=17)
        e8.grid(row=7, column=1, padx=10, pady=10, sticky=W)

        # callback & Validation password
        validate_password = self.root.register(self.check_password)
        e8.config(validate='key', validatecommand=(validate_password, '%P'))

        # confirm password
        l9 = Label(main_frame, text=" Confirm \nPassword:", font=('Times New Roman', 16, 'bold'), fg='darkblue')
        l9.grid(row=8, column=0, padx=10, pady=10, sticky=W)

        e9 = ttk.Entry(main_frame, textvariable=self.c_password, font=('Times New Roman', 15, 'bold'), width=17)
        e9.grid(row=8, column=1, padx=10, pady=10, sticky=W)

        # submit frame
        submit_frame = Frame(main_frame)
        submit_frame.place(x=150, y=400, width=250, height=55)

        # Submit
        r3 = Button(submit_frame, text='Submit', command=self.validation, width=20, bg='green', fg='white',
                    font=('bold', 15), cursor='hand2')
        r3.grid(row=0, column=0, padx=0, pady=0)

    #######check firstname#########
    def checkf_name(self, f_name):
        if f_name.isalpha():
            return True
        if f_name == '':
            return True
        else:
            messagebox.showerror('Invalid', 'Not Allowed' + f_name[-1])

    # check Lastname
    def checkl_name(self, l_name):
        if l_name.isalpha():
            return True
        if l_name == '':
            return True
        else:
            messagebox.showerror('Invalid', 'Not Allowed' + l_name[-1])

    # check emailaddress
    def check_email(self, email):
        if len(email) < 7:
            if re.match("^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.)[a-zA-Z]{2,5})$", email):
                return True
            else:
                messagebox.showwarning('Alert', 'Not Allowed')
                return False
        else:
            messagebox.showinfo('Invalid', 'email length is too small')
            # return False

    # check contact name
    def check_contact(self, contact):
        if contact.isdigit():
            return True
        if len(str(contact)) == 0:
            return True
        else:
            messagebox.showerror('Invalid', 'Not Allowed')
            return False

    # check password
    def check_password(self, password):
        if len(self.password) <= 21:
            if re.match("/^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$/", self.password):
                return True
            else:
                messagebox.showinfo('Invalid', 'Not Allowed')
                return False
        else:
            messagebox.showerror('Invalid', 'Password is too small')
            return False

    ######################Validation####################################

    # validation f_name
    def validation(self):
        if self.f_name.get() == '':
            messagebox.showerror('error', 'Please enter your first name', parent=self.root)
        elif self.l_name.get() == '':
            messagebox.showerror('error', 'Please enter your last name', parent=self.root)
        elif self.email.get() == '':
            messagebox.showerror('error', 'Please enter your email', parent=self.root)
        elif self.contact.get() == '' or len(self.contact.get()) != 10:
            messagebox.showerror('error', 'Please enter your contact', parent=self.root)
        elif self.password.get() == '':
            messagebox.showerror('error', 'Please enter your password', parent=self.root)
        elif self.c_password.get() == '':
            messagebox.showerror('error', 'Please enter your Confirm Password', parent=self.root)
        elif self.password.get() != self.c_password.get():
            messagebox.showerror('error', 'Password and Confirm Password must be Same', parent=self.root)

        else:

            try:
                conn = psycopg2.connect(database="AlgoTrading", user="postgres", password="Swapnil10@",
                                        host="127.0.0.1", port="5432")
                my_cursor = conn.cursor()
                my_cursor.execute('insert into registration values(%s,%s,%s,%s,%s)', (
                    self.f_name.get(),
                    self.l_name.get(),
                    self.email.get(),
                    self.contact.get(),
                    self.password.get()

                ))
                conn.commit()
                conn.close()

                messagebox.showinfo('Succesfully',
                                    f'Your registration is succesfully completed\nUser ID: {self.email.get()}\nPassword: {self.password.get()}')
            except Exception as es:
                messagebox.showerror('error', f'Due to:{str(es)}', parent=self.root)


if __name__ == '__main__':
    root = Tk()
    obj = UserRegister(root)
    root.mainloop()
