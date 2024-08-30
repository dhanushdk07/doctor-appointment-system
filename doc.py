from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
import pymysql

# ---------------------------------------------------------------Login Function --------------------------------------
def clear():
    userentry.delete(0, END)
    passentry.delete(0, END)

def close():
    win.destroy()

def connect_db():
    return pymysql.connect(host="localhost", user="root", password="Dhanush9944708021", database="doctor")

def login():
    if user_name.get() == "" or password.get() == "":
        messagebox.showerror("Error", "Enter User Name And Password", parent=win)
    else:
        try:
            con = connect_db()
            cur = con.cursor()

            cur.execute("select * from appointment where username=%s and password = %s", (user_name.get(), password.get()))
            row = cur.fetchone()

            if row is None:
                messagebox.showerror("Error", "Invalid User Name And Password", parent=win)
            else:
                messagebox.showinfo("Success", "Successfully Logged In", parent=win)
                close()
                deshboard()
            con.close()
        except Exception as es:
            messagebox.showerror("Error", f"Error Due to: {str(es)}", parent=win)

# ---------------------------------------------------------------End Login Function ---------------------------------

# ---------------------------------------------------- Dashboard Panel -----------------------------------------
def deshboard():
    def book():
        if docter_var.get() == "" or day.get() == "" or month.get() == "" or year.get() == "":
            messagebox.showerror("Error", "All Fields Are Required", parent=des)
        else:
            try:
                con = connect_db()
                cur = con.cursor()

                cur.execute(
                    "update appointment set doctor = %s, day = %s, month = %s, year = %s where username = %s",
                    (docter_var.get(), day.get(), month.get(), year.get(), user_name.get())
                )
                con.commit()
                con.close()
                messagebox.showinfo("Success", "Appointment Booked", parent=des)
            except Exception as es:
                messagebox.showerror("Error", f"Error Due to: {str(es)}", parent=des)

    des = Tk()
    des.title("Admin Panel Doctor App")
    des.maxsize(width=800, height=500)
    des.minsize(width=800, height=500)

    # heading label
    heading = Label(des, text=f"User Name : {user_name.get()}", font='Verdana 20 bold', bg='white')
    heading.place(x=220, y=50)

    f = Frame(des, height=1, width=800, bg="black")
    f.place(x=0, y=95)

    con = connect_db()
    cur = con.cursor()

    cur.execute("select * from appointment where username = %s", (user_name.get(),))
    row = cur.fetchall()

    a = Frame(des, height=1, width=400, bg="black")
    a.place(x=0, y=195)

    b = Frame(des, height=100, width=1, bg="black")
    b.place(x=400, y=97)

    for data in row:
        first_name_label = Label(des, text=f"First Name : {data[6]}", font='Verdana 10 bold')
        first_name_label.place(x=20, y=100)

        last_name_label = Label(des, text=f"Last Name : {data[1]}", font='Verdana 10 bold')
        last_name_label.place(x=20, y=130)

        age_label = Label(des, text=f"Age : {data[2]}", font='Verdana 10 bold')
        age_label.place(x=20, y=160)

        gender_label = Label(des, text=f"Gender : {data[3]}", font='Verdana 10 bold')
        gender_label.place(x=250, y=100)

        city_label = Label(des, text=f"City : {data[4]}", font='Verdana 10 bold')
        city_label.place(x=250, y=130)

        add_label = Label(des, text=f"Address : {data[5]}", font='Verdana 10 bold')
        add_label.place(x=250, y=160)

    # Book Doctor Appointment
    heading = Label(des, text="Book Appointment", font='Verdana 20 bold')
    heading.place(x=470, y=100)

    # Book Doctor Label
    doctor_label = Label(des, text="Doctor:", font='Verdana 10 bold')
    doctor_label.place(x=480, y=145)

    day_label = Label(des, text="Day:", font='Verdana 10 bold')
    day_label.place(x=480, y=165)

    month_label = Label(des, text="Month:", font='Verdana 10 bold')
    month_label.place(x=480, y=185)

    year_label = Label(des, text="Year:", font='Verdana 10 bold')
    year_label.place(x=480, y=205)

    # Book Doctor Entry Box
    docter_var = tk.StringVar()
    day = StringVar()
    month = tk.StringVar()
    year = StringVar()

    doctor_box = ttk.Combobox(des, width=30, textvariable=docter_var, state='readonly')
    doctor_box['values'] = ('Andy', 'Charlie', 'Shetal', 'Danish', 'Sunil')
    doctor_box.current(0)
    doctor_box.place(x=550, y=145)

    day_entry = Entry(des, width=33, textvariable=day)
    day_entry.place(x=550, y=168)

    month_box = ttk.Combobox(des, width=30, textvariable=month, state='readonly')
    month_box['values'] = (
        'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November',
        'December')
    month_box.current(0)
    month_box.place(x=550, y=188)

    year_entry = Entry(des, width=33, textvariable=year)
    year_entry.place(x=550, y=208)

    # button
    btn = Button(des, text="Book", font='Verdana 10 bold', width=20, command=book)
    btn.place(x=553, y=230)

    cur.execute("select * from appointment where username = %s", (user_name.get(),))
    rows = cur.fetchall()

    # Book Appointment Details
    heading = Label(des, text=f"{user_name.get()} Appointments", font='Verdana 15 bold')
    heading.place(x=20, y=250)

    for book in rows:
        d1 = Label(des, text=f"Doctor: {book[9]}", font='Verdana 10 bold')
        d1.place(x=20, y=300)

        d2 = Label(des, text=f"Day: {book[10]}", font='Verdana 10 bold')
        d2.place(x=20, y=320)

        d3 = Label(des, text=f"Month: {book[11]}", font='Verdana 10 bold')
        d3.place(x=20, y=340)

        d4 = Label(des, text=f"Year: {book[12]}", font='Verdana 10 bold')
        d4.place(x=20, y=360)

# -----------------------------------------------------End Dashboard Panel -------------------------------------
# ----------------------------------------------------------- Signup Window --------------------------------------------------

def signup():
    # signup database connect
    def action():
        if (first_name.get() == "" or last_name.get() == "" or age.get() == "" or city.get() == "" or
            add.get() == "" or user_name.get() == "" or password.get() == "" or very_pass.get() == ""):
            messagebox.showerror("Error", "All Fields Are Required", parent=winsignup)
        elif password.get() != very_pass.get():
            messagebox.showerror("Error", "Password & Confirm Password Should Be Same", parent=winsignup)
        else:
            try:
                con = connect_db()
                cur = con.cursor()
                cur.execute("select * from appointment where username=%s", (user_name.get(),))
                row = cur.fetchone()
                if row is not None:
                    messagebox.showerror("Error", "User Name Already Exists", parent=winsignup)
                else:
                    cur.execute(
                        "insert into appointment(first_name, last_name, age, gender, city, address, username, password) values(%s, %s, %s, %s, %s, %s, %s, %s)",
                        (
                            first_name.get(),
                            last_name.get(),
                            age.get(),
                            var.get(),
                            city.get(),
                            add.get(),
                            user_name.get(),
                            password.get()
                        ))
                    con.commit()
                    con.close()
                    messagebox.showinfo("Success", "Registration Successful", parent=winsignup)
                    clear()
                    switch_to_login()
            except Exception as es:
                messagebox.showerror("Error", f"Error Due to: {str(es)}", parent=winsignup)

    def clear():
        first_name_entry.delete(0, END)
        last_name_entry.delete(0, END)
        age_entry.delete(0, END)
        user_entry.delete(0, END)
        pass_entry.delete(0, END)
        verify_entry.delete(0, END)
        city_entry.delete(0, END)
        add_entry.delete(0, END)

    def switch_to_login():
        winsignup.destroy()

    # signup window
    winsignup = Tk()
    winsignup.title("Signup")
    winsignup.maxsize(width=500, height=600)
    winsignup.minsize(width=500, height=600)

    # heading label
    heading = Label(winsignup, text="Signup", font='Verdana 20 bold')
    heading.place(x=80, y=60)

    # form data label
    first_name_label = Label(winsignup, text="First Name :", font='Verdana 10 bold')
    first_name_label.place(x=80, y=130)

    last_name_label = Label(winsignup, text="Last Name :", font='Verdana 10 bold')
    last_name_label.place(x=80, y=160)

    age_label = Label(winsignup, text="Age :", font='Verdana 10 bold')
    age_label.place(x=80, y=190)

    gender_label = Label(winsignup, text="Gender :", font='Verdana 10 bold')
    gender_label.place(x=80, y=220)

    city_label = Label(winsignup, text="City :", font='Verdana 10 bold')
    city_label.place(x=80, y=260)

    add_label = Label(winsignup, text="Address :", font='Verdana 10 bold')
    add_label.place(x=80, y=290)

    user_label = Label(winsignup, text="User Name :", font='Verdana 10 bold')
    user_label.place(x=80, y=320)

    pass_label = Label(winsignup, text="Password :", font='Verdana 10 bold')
    pass_label.place(x=80, y=350)

    verify_label = Label(winsignup, text="Verify Password:", font='Verdana 10 bold')
    verify_label.place(x=80, y=380)

    # Entry Box
    first_name = StringVar()
    last_name = StringVar()
    age = IntVar()
    var = StringVar()
    city = StringVar()
    add = StringVar()
    user_name = StringVar()
    password = StringVar()
    very_pass = StringVar()

    first_name_entry = Entry(winsignup, width=40, textvariable=first_name)
    first_name_entry.place(x=200, y=133)

    last_name_entry = Entry(winsignup, width=40, textvariable=last_name)
    last_name_entry.place(x=200, y=163)

    age_entry = Entry(winsignup, width=40, textvariable=age)
    age_entry.place(x=200, y=193)

    # gender radio button
    radio_frame = Frame(winsignup)
    radio_frame.place(x=200, y=220)

    male_rb = Radiobutton(radio_frame, text='Male', variable=var, value="male")
    male_rb.pack(side=LEFT)

    female_rb = Radiobutton(radio_frame, text='Female', variable=var, value="female")
    female_rb.pack(side=LEFT)

    city_entry = Entry(winsignup, width=40, textvariable=city)
    city_entry.place(x=200, y=263)

    add_entry = Entry(winsignup, width=40, textvariable=add)
    add_entry.place(x=200, y=293)

    user_entry = Entry(winsignup, width=40, textvariable=user_name)
    user_entry.place(x=200, y=323)

    pass_entry = Entry(winsignup, width=40, show="*", textvariable=password)
    pass_entry.place(x=200, y=353)

    verify_entry = Entry(winsignup, width=40, show="*", textvariable=very_pass)
    verify_entry.place(x=200, y=383)

    # button
    btn_signup = Button(winsignup, text="Signup", font='Verdana 10 bold', command=action)
    btn_signup.place(x=200, y=413)

    winsignup.mainloop()

# -----------------------------------------------------------End Signup Window -----------------------------------------

# ----------------------------------------------------------- Login Window -----------------------------------------

win = Tk()
win.title("Doctor Appointment")
win.maxsize(width=500, height=500)
win.minsize(width=500, height=500)

# heading label
heading = Label(win, text="Login", font='Verdana 25 bold')
heading.place(x=80, y=150)

user_name = StringVar()
password = StringVar()

# username label and text entry box
user_label = Label(win, text="User Name :", font='Verdana 10 bold')
user_label.place(x=80, y=220)

userentry = Entry(win, width=40, textvariable=user_name)
userentry.focus()
userentry.place(x=200, y=223)

# password label and password entry box
pass_label = Label(win, text="Password :", font='Verdana 10 bold')
pass_label.place(x=80, y=260)

passentry = Entry(win, width=40, show="*", textvariable=password)
passentry.place(x=200, y=260)

# login button
btn_login = Button(win, text="Login", font='Verdana 10 bold', command=login)
btn_login.place(x=200, y=293)

# signup button
sign_up_btn = Button(win, text="Register New Account?", command=signup)
sign_up_btn.place(x=200, y=320)

win.mainloop()
