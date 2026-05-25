from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
import time

# ===== DATABASE CONNECTION =====
conn = mysql.connector.connect(
    host="localhost",
    username="root",
    password="Maanya@2005",
    database="pharmacy"
)

cursor = conn.cursor()

# ===== MAIN WINDOW =====
root = Tk()

selected_id = StringVar()

root.title("Pharmacy Management System")

root.geometry("1450x780+0+0")

root.config(bg="#f0f2f5")

# ===== CLOCK FUNCTION =====
def clock():

    current_time = time.strftime("%I:%M:%S %p")

    current_date = time.strftime("%d-%m-%Y")

    lbl_clock.config(
        text=f" Date: {current_date}        Time: {current_time}"
    )

    lbl_clock.after(1000, clock)

# ===== FETCH DATA =====
def fetch_data():

    cursor.execute("SELECT * FROM medicine")

    rows = cursor.fetchall()

    medicine_table.delete(*medicine_table.get_children())

    for row in rows:
        medicine_table.insert('', END, values=row)

# ===== SEARCH DATA =====
def search_data():

    search_value = txt_search.get()

    query = "SELECT * FROM medicine WHERE name LIKE %s"

    value = ("%" + search_value + "%",)

    cursor.execute(query, value)

    rows = cursor.fetchall()

    medicine_table.delete(*medicine_table.get_children())

    for row in rows:
        medicine_table.insert('', END, values=row)

# ===== CLEAR DATA =====
def clear_data():

    selected_id.set("")

    txt_name.delete(0, END)
    txt_company.delete(0, END)
    txt_price.delete(0, END)
    txt_quantity.delete(0, END)
    txt_expiry.delete(0, END)

# ===== SAVE DATA =====
def save_data():

    medicine_name = txt_name.get()
    company = txt_company.get()
    price = txt_price.get()
    quantity = txt_quantity.get()
    expiry = txt_expiry.get()

    if medicine_name == "" or company == "" or price == "" or quantity == "" or expiry == "":
        messagebox.showerror("Error", "All Fields Are Required")
        return

    query = """
    INSERT INTO medicine(name, company, price, quantity, expiry_date)
    VALUES(%s,%s,%s,%s,%s)
    """

    values = (
        medicine_name,
        company,
        price,
        quantity,
        expiry
    )

    cursor.execute(query, values)

    conn.commit()

    fetch_data()

    clear_data()

    messagebox.showinfo("Success", "Medicine Added Successfully")

# ===== GET CURSOR =====
def get_cursor(event):

    cursor_row = medicine_table.focus()

    contents = medicine_table.item(cursor_row)

    row = contents['values']

    if len(row) == 0:
        return

    selected_id.set(row[0])

    txt_name.delete(0, END)
    txt_name.insert(END, row[1])

    txt_company.delete(0, END)
    txt_company.insert(END, row[2])

    txt_price.delete(0, END)
    txt_price.insert(END, row[3])

    txt_quantity.delete(0, END)
    txt_quantity.insert(END, row[4])

    txt_expiry.delete(0, END)
    txt_expiry.insert(END, row[5])

# ===== UPDATE DATA =====
def update_data():

    if selected_id.get() == "":
        messagebox.showerror("Error", "Please Select Medicine")
        return

    query = """
    UPDATE medicine
    SET name=%s,
        company=%s,
        price=%s,
        quantity=%s,
        expiry_date=%s
    WHERE med_id=%s
    """

    values = (
        txt_name.get(),
        txt_company.get(),
        txt_price.get(),
        txt_quantity.get(),
        txt_expiry.get(),
        selected_id.get()
    )

    cursor.execute(query, values)

    conn.commit()

    fetch_data()

    clear_data()

    messagebox.showinfo("Success", "Medicine Updated Successfully")

# ===== DELETE DATA =====
def delete_data():

    if selected_id.get() == "":
        messagebox.showerror("Error", "Please Select Medicine")
        return

    query = "DELETE FROM medicine WHERE med_id=%s"

    cursor.execute(query, (selected_id.get(),))

    conn.commit()

    fetch_data()

    clear_data()

    messagebox.showinfo("Success", "Medicine Deleted Successfully")

# ===== TITLE =====
title = Label(
    root,
    text="PHARMACY MANAGEMENT SYSTEM",
    bg="#009688",
    fg="white",
    font=("Helvetica", 28, "bold"),
    pady=15
)

title.pack(fill=X)

# ===== CLOCK =====
lbl_clock = Label(
    root,
    bg="#4CAF50",
    fg="white",
    font=("Helvetica", 12, "bold"),
    pady=8
)

lbl_clock.pack(fill=X)

clock()

# ===== LEFT FRAME =====
left_frame = Frame(root, bg="white", bd=3, relief=RIDGE)

left_frame.place(x=30, y=120, width=520, height=600)

heading = Label(
    left_frame,
    text="Medicine Details",
    bg="white",
    fg="#009688",
    font=("Helvetica", 20, "bold")
)

heading.pack(pady=20)

# ===== FORM =====
form_inner = Frame(left_frame, bg="white")

form_inner.pack(pady=10)

# ===== LABELS =====
labels = [
    "Medicine Name",
    "Company",
    "Price",
    "Quantity",
    "Expiry Date"
]

entries = []

for i, text in enumerate(labels):

    Label(
        form_inner,
        text=text,
        font=("Helvetica", 14),
        bg="white"
    ).grid(row=i, column=0, padx=20, pady=18, sticky="w")

    entry = Entry(
        form_inner,
        font=("Helvetica", 14),
        bd=2,
        relief=GROOVE,
        width=25
    )

    entry.grid(row=i, column=1, padx=20)

    entries.append(entry)

txt_name = entries[0]
txt_company = entries[1]
txt_price = entries[2]
txt_quantity = entries[3]
txt_expiry = entries[4]

# ===== EXPIRY FORMAT LABEL =====
Label(
    left_frame,
    text="Expiry Format: YYYY-MM-DD",
    font=("Helvetica", 11),
    bg="white",
    fg="gray"
).pack()

# ===== BUTTON FRAME =====
btn_frame = Frame(left_frame, bg="white")

btn_frame.pack(pady=30)

Button(
    btn_frame,
    text="Save",
    bg="#009688",
    fg="white",
    font=("Helvetica", 12, "bold"),
    width=10,
    command=save_data
).grid(row=0, column=0, padx=10, pady=10)

Button(
    btn_frame,
    text="Update",
    bg="#1976D2",
    fg="white",
    font=("Helvetica", 12, "bold"),
    width=10,
    command=update_data
).grid(row=0, column=1, padx=10, pady=10)

Button(
    btn_frame,
    text="Delete",
    bg="#D32F2F",
    fg="white",
    font=("Helvetica", 12, "bold"),
    width=10,
    command=delete_data
).grid(row=1, column=0, padx=10, pady=10)

Button(
    btn_frame,
    text="Clear",
    bg="#616161",
    fg="white",
    font=("Helvetica", 12, "bold"),
    width=10,
    command=clear_data
).grid(row=1, column=1, padx=10, pady=10)

# ===== RIGHT FRAME =====
right_frame = Frame(root, bg="white", bd=3, relief=RIDGE)

right_frame.place(x=580, y=120, width=830, height=600)

# ===== SEARCH FRAME =====
search_frame = Frame(right_frame, bg="white")

search_frame.pack(fill=X, pady=15)

Label(
    search_frame,
    text="Search Medicine",
    font=("Helvetica", 14, "bold"),
    bg="white"
).pack(side=LEFT, padx=15)

txt_search = Entry(
    search_frame,
    font=("Helvetica", 13),
    bd=2,
    relief=GROOVE,
    width=30
)

txt_search.pack(side=LEFT, padx=10)

Button(
    search_frame,
    text="Search",
    bg="#009688",
    fg="white",
    font=("Helvetica", 11, "bold"),
    width=10,
    command=search_data
).pack(side=LEFT, padx=10)

Button(
    search_frame,
    text="Show All",
    bg="#616161",
    fg="white",
    font=("Helvetica", 11, "bold"),
    width=10,
    command=fetch_data
).pack(side=LEFT, padx=10)

# ===== TABLE FRAME =====
table_frame = Frame(right_frame, bg="white")

table_frame.pack(fill=BOTH, expand=1, padx=10, pady=10)

scroll_x = Scrollbar(table_frame, orient=HORIZONTAL)

scroll_y = Scrollbar(table_frame, orient=VERTICAL)

medicine_table = ttk.Treeview(
    table_frame,
    columns=("id", "name", "company", "price", "quantity", "expiry"),
    xscrollcommand=scroll_x.set,
    yscrollcommand=scroll_y.set
)

scroll_x.pack(side=BOTTOM, fill=X)

scroll_y.pack(side=RIGHT, fill=Y)

scroll_x.config(command=medicine_table.xview)

scroll_y.config(command=medicine_table.yview)

medicine_table.heading("id", text="ID")
medicine_table.heading("name", text="Medicine Name")
medicine_table.heading("company", text="Company")
medicine_table.heading("price", text="Price")
medicine_table.heading("quantity", text="Quantity")
medicine_table.heading("expiry", text="Expiry Date")

medicine_table["show"] = "headings"

medicine_table.column("id", width=60)
medicine_table.column("name", width=160)
medicine_table.column("company", width=160)
medicine_table.column("price", width=100)
medicine_table.column("quantity", width=100)
medicine_table.column("expiry", width=140)

medicine_table.pack(fill=BOTH, expand=1)

medicine_table.bind("<ButtonRelease-1>", get_cursor)

# ===== FOOTER =====
footer = Label(
    root,
    text="Developed Using Python + Tkinter + MySQL",
    bg="#009688",
    fg="white",
    font=("Helvetica", 11, "bold"),
    pady=8
)

footer.pack(side=BOTTOM, fill=X)

fetch_data()

root.mainloop()