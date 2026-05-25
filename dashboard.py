from tkinter import *
from tkinter import messagebox
import os

# ===== FUNCTIONS =====

def open_management():

    os.system("python main.py")


def open_billing():

    os.system("python billing.py")


def open_sales():

    os.system("python sales_report.py")


def open_low_stock():

    os.system("python low_stock.py")


def logout():

    answer = messagebox.askyesno(
        "Logout",
        "Do you want to logout?"
    )

    if answer == True:

        root.destroy()

        os.system("python login.py")


# ===== MAIN WINDOW =====
root = Tk()

root.title("Pharmacy Dashboard")

root.geometry("1000x650+150+40")

root.config(bg="#f0f2f5")

root.resizable(False, False)

# ===== TITLE =====
title = Label(
    root,
    text="PHARMACY MANAGEMENT DASHBOARD",
    bg="#673AB7",
    fg="white",
    font=("Helvetica", 28, "bold"),
    pady=18
)

title.pack(fill=X)

# ===== WELCOME =====
welcome = Label(
    root,
    text="Welcome Admin",
    bg="#f0f2f5",
    fg="#333333",
    font=("Helvetica", 22, "bold")
)

welcome.pack(pady=30)

# ===== BUTTON FRAME =====
btn_frame = Frame(
    root,
    bg="#f0f2f5"
)

btn_frame.pack(pady=20)

# ===== MANAGEMENT BUTTON =====
btn_management = Button(
    btn_frame,
    text="Medicine\nManagement",
    font=("Helvetica", 18, "bold"),
    bg="#009688",
    fg="white",
    width=18,
    height=5,
    cursor="hand2",
    command=open_management
)

btn_management.grid(
    row=0,
    column=0,
    padx=25,
    pady=25
)

# ===== BILLING BUTTON =====
btn_billing = Button(
    btn_frame,
    text="Billing\nSystem",
    font=("Helvetica", 18, "bold"),
    bg="#1976D2",
    fg="white",
    width=18,
    height=5,
    cursor="hand2",
    command=open_billing
)

btn_billing.grid(
    row=0,
    column=1,
    padx=25,
    pady=25
)

# ===== SALES REPORT BUTTON =====
btn_sales = Button(
    btn_frame,
    text="Sales\nReport",
    font=("Helvetica", 18, "bold"),
    bg="#FF9800",
    fg="white",
    width=18,
    height=5,
    cursor="hand2",
    command=open_sales
)

btn_sales.grid(
    row=1,
    column=0,
    padx=25,
    pady=25
)

# ===== LOW STOCK BUTTON =====
btn_stock = Button(
    btn_frame,
    text="Low Stock\nAlert",
    font=("Helvetica", 18, "bold"),
    bg="#D32F2F",
    fg="white",
    width=18,
    height=5,
    cursor="hand2",
    command=open_low_stock
)

btn_stock.grid(
    row=1,
    column=1,
    padx=25,
    pady=25
)

# ===== LOGOUT BUTTON =====
btn_logout = Button(
    root,
    text="LOGOUT",
    font=("Helvetica", 16, "bold"),
    bg="black",
    fg="white",
    width=18,
    height=2,
    cursor="hand2",
    command=logout
)

btn_logout.pack(pady=25)

# ===== FOOTER =====
footer = Label(
    root,
    text="Developed Using Python + Tkinter + MySQL",
    bg="#673AB7",
    fg="white",
    font=("Helvetica", 11, "bold"),
    pady=8
)

footer.pack(side=BOTTOM, fill=X)

root.mainloop()