from tkinter import *
from tkinter import messagebox
import mysql.connector

# ===== DATABASE CONNECTION =====
conn = mysql.connector.connect(
    host="localhost",
    username="root",
    password="Maanya@2005",
    database="pharmacy"
)

cursor = conn.cursor(buffered=True)

# ===== LOGIN FUNCTION =====
def login():

    username = user_var.get()

    password = pass_var.get()

    if username == "" or password == "":

        messagebox.showerror(
            "Error",
            "All Fields Are Required"
        )

        return

    query = """
    SELECT *
    FROM admin_login
    WHERE username=%s
    AND password=%s
    """

    values = (username, password)

    cursor.execute(query, values)

    row = cursor.fetchone()

    if row is not None:

        messagebox.showinfo(
            "Success",
            "Login Successful"
        )

        root.destroy()

        import dashboard

    else:

        messagebox.showerror(
            "Error",
            "Invalid Username or Password"
        )

# ===== MAIN WINDOW =====
root = Tk()

root.title("Pharmacy Login System")

root.geometry("600x400+350+120")

root.config(bg="#f0f2f5")

root.resizable(False, False)

# ===== VARIABLES =====
user_var = StringVar()
pass_var = StringVar()

# ===== TITLE =====
title = Label(
    root,
    text="PHARMACY LOGIN SYSTEM",
    bg="#673AB7",
    fg="white",
    font=("Helvetica", 26, "bold"),
    pady=15
)

title.pack(fill=X)

# ===== LOGIN FRAME =====
frame = Frame(
    root,
    bg="white",
    bd=4,
    relief=RIDGE
)

frame.place(
    x=90,
    y=90,
    width=420,
    height=240
)

# ===== USERNAME LABEL =====
lbl_user = Label(
    frame,
    text="Username",
    font=("Helvetica", 14, "bold"),
    bg="white"
)

lbl_user.place(x=30, y=50)

# ===== USERNAME ENTRY =====
txt_user = Entry(
    frame,
    textvariable=user_var,
    font=("Helvetica", 13),
    width=24
)

txt_user.place(x=150, y=50)

# ===== PASSWORD LABEL =====
lbl_pass = Label(
    frame,
    text="Password",
    font=("Helvetica", 14, "bold"),
    bg="white"
)

lbl_pass.place(x=30, y=110)

# ===== PASSWORD ENTRY =====
txt_pass = Entry(
    frame,
    textvariable=pass_var,
    font=("Helvetica", 13),
    width=24,
    show="*"
)

txt_pass.place(x=150, y=110)

# ===== LOGIN BUTTON =====
btn_login = Button(
    frame,
    text="LOGIN",
    font=("Helvetica", 14, "bold"),
    bg="#009688",
    fg="white",
    width=15,
    cursor="hand2",
    command=login
)

btn_login.place(x=110, y=170)

# ===== FOOTER =====
footer = Label(
    root,
    text="Secure Pharmacy Management System",
    bg="#673AB7",
    fg="white",
    font=("Helvetica", 11, "bold"),
    pady=8
)

footer.pack(side=BOTTOM, fill=X)

root.mainloop()