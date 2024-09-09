from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
import pymysql

def connect_db():
    return pymysql.connect(host="localhost", user="root", password="Dhanush9944708021", database="doctor")

# ---------------------------------------------------------------Login Function --------------------------------------
def clear():
    userentry.delete(0, END)
    passentry.delete(0, END)

def close():
    win.destroy()

def login():
    if user_name.get() == "" or password.get() == "":
        messagebox.showerror("Error", "Please enter both username and password", parent=win)
    else:
        try:
            con = connect_db()
            cur = con.cursor()

            # Check if Admin checkbox is checked
            if is_admin.get():
                cur.execute("select * from admin where username=%s and password = %s", (user_name.get(), password.get()))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Invalid Admin username or password", parent=win)
                else:
                    messagebox.showinfo("Success", "Admin Successfully Logged In", parent=win)
                    close()
                    admin_dashboard()  # Call Admin dashboard
            else:
                cur.execute("select * from appointment where username=%s and password = %s", (user_name.get(), password.get()))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Invalid username or password", parent=win)
                else:
                    messagebox.showinfo("Success", "Successfully Logged In", parent=win)
                    close()
                    deshboard()  # Call User dashboard

            con.close()
        except Exception as es:
            messagebox.showerror("Error", f"Error due to: {str(es)}", parent=win)


# ---------------------------------------------------- Dashboard Panel -----------------------------------------
def deshboard():
    def book():
        if docter_var.get() == "" or day.get() == "" or month.get() == "" or year.get() == "":
            messagebox.showerror("Error", "All fields are required to book an appointment", parent=des)
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
                messagebox.showinfo("Success", "Appointment booked", parent=des)
            except Exception as es:
                messagebox.showerror("Error", f"Error due to: {str(es)}", parent=des)

    des = Tk()
    des.title("Doctor Appointment Details ")
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
            messagebox.showerror("Error", "All fields are required", parent=winsignup)
        elif password.get() != very_pass.get():
            messagebox.showerror("Error", "Passwords do not match", parent=winsignup)
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
                messagebox.showerror("Error", f"Error due to: {str(es)}", parent=winsignup)

    def switch_to_login():
        winsignup.destroy()

    # clear data function
    def clear():
        first_name.delete(0, END)
        last_name.delete(0, END)
        age.delete(0, END)
        city.delete(0, END)
        add.delete(0, END)
        user_name.delete(0, END)
        password.delete(0, END)
        very_pass.delete(0, END)

    # signup window
    winsignup = Tk()
    winsignup.title("Signup System")
    winsignup.maxsize(width=500, height=600)
    winsignup.minsize(width=500, height=600)

    # heading label
    heading = Label(winsignup, text="Signup", font='Verdana 20 bold')
    heading.place(x=80, y=60)

    # form data label
    first_name_label = Label(winsignup, text="First Name:", font='Verdana 10 bold')
    first_name_label.place(x=80, y=130)

    last_name_label = Label(winsignup, text="Last Name:", font='Verdana 10 bold')
    last_name_label.place(x=80, y=160)

    age_label = Label(winsignup, text="Age:", font='Verdana 10 bold')
    age_label.place(x=80, y=190)

    gender_label = Label(winsignup, text="Gender:", font='Verdana 10 bold')
    gender_label.place(x=80, y=220)

    city_label = Label(winsignup, text="City:", font='Verdana 10 bold')
    city_label.place(x=80, y=260)

    add_label = Label(winsignup, text="Address:", font='Verdana 10 bold')
    add_label.place(x=80, y=290)

    user_name_label = Label(winsignup, text="User Name:", font='Verdana 10 bold')
    user_name_label.place(x=80, y=320)

    password_label = Label(winsignup, text="Password:", font='Verdana 10 bold')
    password_label.place(x=80, y=350)

    very_pass_label = Label(winsignup, text="Verify Password:", font='Verdana 10 bold')
    very_pass_label.place(x=80, y=380)

    # Entry box ------------------------------------------------------------------
    first_name = Entry(winsignup, width=40)
    first_name.place(x=200, y=133)

    last_name = Entry(winsignup, width=40)
    last_name.place(x=200, y=163)

    age = Entry(winsignup, width=40)
    age.place(x=200, y=193)

    var = StringVar()
    # gender
    male_rb = ttk.Radiobutton(winsignup, text='Male', value='Male', variable=var)
    male_rb.place(x=200, y=220)
    female_rb = ttk.Radiobutton(winsignup, text='Female', value='Female', variable=var)
    female_rb.place(x=200, y=238)

    city = Entry(winsignup, width=40)
    city.place(x=200, y=263)

    add = Entry(winsignup, width=40)
    add.place(x=200, y=293)

    user_name = Entry(winsignup, width=40)
    user_name.place(x=200, y=323)

    password = Entry(winsignup, width=40, show="*")
    password.place(x=200, y=353)

    very_pass = Entry(winsignup, width=40, show="*")
    very_pass.place(x=200, y=383)

    # button login and clear
    btn_signup = Button(winsignup, text="Signup", font='Verdana 10 bold', command=action)
    btn_signup.place(x=200, y=413)

    btn_login = Button(winsignup, text="Switch to Login", command=switch_to_login)
    btn_login.place(x=330, y=450)

    winsignup.mainloop()

# ----------------------------------------------------------- End Signup Window --------------------------------------


# ------------------------------------------------------ Admin Dashboard Function --------------------------------------
def admin_dashboard():
    admin_win = Tk()
    admin_win.title("Admin Dashboard")
    admin_win.geometry("800x600")

    heading = Label(admin_win, text="Admin Dashboard", font=('Verdana', 20, 'bold'))
    heading.pack(pady=20)

    # Create Treeview to display user details
    tree = ttk.Treeview(admin_win, columns=("Username", "Doctor", "Day", "Month", "Year"), show="headings")


    tree.heading("Username", text="Username")
    tree.heading("Doctor", text="Doctor")
    tree.heading("Day", text="Day")
    tree.heading("Month", text="Month")
    tree.heading("Year", text="Year")

    # Set column width for better display

    tree.column("Username", width=100)
    tree.column("Doctor", width=100)
    tree.column("Day", width=50)
    tree.column("Month", width=100)
    tree.column("Year", width=60)

    tree.pack(pady=20, fill=tk.BOTH, expand=True)

    # Fetch user data from the database
    try:
        con = connect_db()
        cur = con.cursor()
        cur.execute("SELECT Username,Doctor,Day,Month,Year from appointment")
        rows = cur.fetchall()

        for row in rows:
            tree.insert('', 'end', values=row)

        con.close()

    except Exception as e:
        messagebox.showerror("Error", f"Error fetching data: {str(e)}", parent=admin_win)

    admin_win.mainloop()


# ---------------------------------------------------- User Dashboard Function -----------------------------------------
def deshboard():
    def book():
        if docter_var.get() == "" or day.get() == "" or month.get() == "" or year.get() == "":
            messagebox.showerror("Error", "All fields are required to book an appointment", parent=des)
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
                messagebox.showinfo("Success", "Appointment booked", parent=des)
            except Exception as es:
                messagebox.showerror("Error", f"Error due to: {str(es)}", parent=des)

    des = Tk()
    des.title("User Dashboard")
    des.maxsize(width=800, height=500)
    des.minsize(width=800, height=500)

    heading = Label(des, text=f"User Name : {user_name.get()}", font='Verdana 20 bold', bg='white')
    heading.place(x=220, y=50)

    f = Frame(des, height=1, width=800, bg="black")
    f.place(x=0, y=95)

    con = connect_db()
    cur = con.cursor()
    cur.execute("select * from appointment where username = %s", (user_name.get(),))
    row = cur.fetchall()

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

    heading = Label(des, text="Book Appointment", font='Verdana 20 bold')
    heading.place(x=470, y=100)

    doctor_label = Label(des, text="Doctor:", font='Verdana 10 bold')
    doctor_label.place(x=480, y=145)
    day_label = Label(des, text="Day:", font='Verdana 10 bold')
    day_label.place(x=480, y=165)
    month_label = Label(des, text="Month:", font='Verdana 10 bold')
    month_label.place(x=480, y=185)
    year_label = Label(des, text="Year:", font='Verdana 10 bold')
    year_label.place(x=480, y=205)

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
    month_box['values'] = ('January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December')
    month_box.current(0)
    month_box.place(x=550, y=188)
    year_entry = Entry(des, width=33, textvariable=year)
    year_entry.place(x=550, y=208)

    btn = Button(des, text="Book", font='Verdana 10 bold', width=20, command=book)
    btn.place(x=553, y=230)

    cur.execute("select * from appointment where username = %s", (user_name.get(),))
    rows = cur.fetchall()

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

    des.mainloop()


win = Tk()

# app title
win.title("Doctor Appointment")

# window size
win.maxsize(width=500, height=500)
win.minsize(width=500, height=500)

# heading label
heading = Label(win, text="Login", font='Verdana 20 bold')
heading.place(x=80, y=150)

username_label = Label(win, text="User Name :", font='Verdana 10 bold')
username_label.place(x=80, y=220)

userpass_label = Label(win, text="Password :", font='Verdana 10 bold')
userpass_label.place(x=80, y=260)

# Entry box
user_name = StringVar()
password = StringVar()
is_admin = BooleanVar()

userentry = Entry(win, width=40, textvariable=user_name)
userentry.focus()
userentry.place(x=200, y=223)

passentry = Entry(win, width=40, show="*", textvariable=password)
passentry.place(x=200, y=260)

# Admin checkbox
admin_check = Checkbutton(win, text="Login as Admin", variable=is_admin)
admin_check.place(x=200, y=290)

# button login and clear
btn_login = Button(win, text="Login", font='Verdana 10 bold', command=login)
btn_login.place(x=200, y=323)

btn_signup = Button(win, text="Signup", font='Verdana 10 bold', command=signup)
btn_signup.place(x=300, y=323)

win.mainloop()

