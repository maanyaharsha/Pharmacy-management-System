from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
from datetime import date

# ===== DATABASE CONNECTION =====
conn = mysql.connector.connect(
    host="localhost",
    username="root",
    password="Maanya@2005",
    database="pharmacy"
)

# ===== BUFFERED CURSOR =====
cursor = conn.cursor(buffered=True)

# ===== MAIN WINDOW =====
root = Tk()

root.title("Pharmacy Billing System")

root.geometry("1000x650+150+50")

root.config(bg="#f0f2f5")

# ===== VARIABLES =====
medicine_var = StringVar()
price_var = StringVar()
quantity_var = StringVar()

bill_total = 0

# ===== TITLE =====
title = Label(
    root,
    text="PHARMACY BILLING SYSTEM",
    bg="#1976D2",
    fg="white",
    font=("Helvetica", 26, "bold"),
    pady=15
)

title.pack(fill=X)

# ===== MAIN FRAME =====
main_frame = Frame(
    root,
    bg="white",
    bd=3,
    relief=RIDGE
)

main_frame.place(x=30, y=100, width=940, height=500)

# ===== LEFT FRAME =====
left_frame = Frame(
    main_frame,
    bg="white"
)

left_frame.place(x=20, y=20, width=400, height=440)

# ===== MEDICINE NAME =====
Label(
    left_frame,
    text="Medicine Name",
    font=("Helvetica", 14, "bold"),
    bg="white"
).pack(anchor="w", pady=10)

medicine_combo = ttk.Combobox(
    left_frame,
    textvariable=medicine_var,
    font=("Helvetica", 13),
    width=28,
    state="readonly"
)

medicine_combo.pack()

# ===== LOAD MEDICINES =====
cursor.execute("SELECT name FROM medicine")

medicines = cursor.fetchall()

medicine_list = []

for med in medicines:
    medicine_list.append(med[0])

medicine_combo["values"] = medicine_list

# ===== FETCH PRICE =====
def fetch_price(event):

    selected_medicine = medicine_var.get()

    query = "SELECT price FROM medicine WHERE name=%s"

    cursor.execute(query, (selected_medicine,))

    result = cursor.fetchone()

    if result:
        price_var.set(result[0])

medicine_combo.bind(
    "<<ComboboxSelected>>",
    fetch_price
)

# ===== PRICE =====
Label(
    left_frame,
    text="Price",
    font=("Helvetica", 14, "bold"),
    bg="white"
).pack(anchor="w", pady=10)

txt_price = Entry(
    left_frame,
    textvariable=price_var,
    font=("Helvetica", 13),
    width=30
)

txt_price.pack()

# ===== QUANTITY =====
Label(
    left_frame,
    text="Quantity",
    font=("Helvetica", 14, "bold"),
    bg="white"
).pack(anchor="w", pady=10)

txt_quantity = Entry(
    left_frame,
    textvariable=quantity_var,
    font=("Helvetica", 13),
    width=30
)

txt_quantity.pack()

# ===== BILL AREA =====
right_frame = Frame(
    main_frame,
    bg="white",
    bd=2,
    relief=RIDGE
)

right_frame.place(x=450, y=20, width=450, height=440)

bill_title = Label(
    right_frame,
    text="CUSTOMER BILL",
    font=("Helvetica", 18, "bold"),
    bg="#009688",
    fg="white",
    pady=10
)

bill_title.pack(fill=X)

bill_text = Text(
    right_frame,
    font=("Courier New", 12),
    width=50,
    height=20
)

bill_text.pack(padx=10, pady=10)

bill_text.insert(END, "Medicine\tQty\tTotal\n")
bill_text.insert(END, "--------------------------------------\n")

# ===== ADD TO BILL =====
def add_to_bill():

    global bill_total

    medicine_name = medicine_var.get()

    price = price_var.get()

    quantity = quantity_var.get()

    if medicine_name == "" or price == "" or quantity == "":

        messagebox.showerror(
            "Error",
            "All Fields Required"
        )

        return

    price = float(price)

    quantity = int(quantity)

    total = price * quantity

    # ===== CHECK STOCK =====
    cursor.execute(
        "SELECT quantity FROM medicine WHERE name=%s",
        (medicine_name,)
    )

    stock = cursor.fetchone()[0]

    if quantity > stock:

        messagebox.showerror(
            "Error",
            f"Only {stock} items available"
        )

        return

    # ===== ADD TO BILL =====
    bill_text.insert(
        END,
        f"{medicine_name}\t{quantity}\t₹{total}\n"
    )

    bill_total += total

    # ===== UPDATE STOCK =====
    new_quantity = stock - quantity

    update_query = """
    UPDATE medicine
    SET quantity=%s
    WHERE name=%s
    """

    cursor.execute(
        update_query,
        (new_quantity, medicine_name)
    )

    # ===== SAVE SALES =====
    today = date.today()

    sale_query = """
    INSERT INTO sales(
        medicine_name,
        quantity,
        total_price,
        sale_date
    )
    VALUES(%s,%s,%s,%s)
    """

    sale_values = (
        medicine_name,
        quantity,
        total,
        today
    )

    cursor.execute(
        sale_query,
        sale_values
    )

    conn.commit()

    # ===== CLEAR FIELDS =====
    medicine_var.set("")
    price_var.set("")
    quantity_var.set("")

# ===== GENERATE BILL =====
def generate_bill():

    bill_text.insert(
        END,
        "\n--------------------------------------\n"
    )

    bill_text.insert(
        END,
        f"TOTAL BILL = ₹ {bill_total}"
    )

    messagebox.showinfo(
        "Success",
        "Bill Generated Successfully"
    )

# ===== BUTTON FRAME =====
btn_frame = Frame(
    left_frame,
    bg="white"
)

btn_frame.pack(pady=40)

# ===== ADD TO BILL BUTTON =====
Button(
    btn_frame,
    text="Add To Bill",
    font=("Helvetica", 12, "bold"),
    bg="#009688",
    fg="white",
    width=15,
    height=2,
    command=add_to_bill
).grid(row=0, column=0, padx=10)

# ===== GENERATE BILL BUTTON =====
Button(
    btn_frame,
    text="Generate Bill",
    font=("Helvetica", 12, "bold"),
    bg="#1976D2",
    fg="white",
    width=15,
    height=2,
    command=generate_bill
).grid(row=0, column=1, padx=10)

# ===== FOOTER =====
footer = Label(
    root,
    text="Developed Using Python + Tkinter + MySQL",
    bg="#1976D2",
    fg="white",
    font=("Helvetica", 11, "bold"),
    pady=8
)

footer.pack(side=BOTTOM, fill=X)

root.mainloop()