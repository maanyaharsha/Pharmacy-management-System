from tkinter import *
from tkinter import ttk
import mysql.connector

# ===== DATABASE CONNECTION =====
conn = mysql.connector.connect(
    host="localhost",
    username="root",
    password="Maanya@2005",
    database="pharmacy"
)

cursor = conn.cursor(buffered=True)

# ===== MAIN WINDOW =====
root = Tk()

root.title("Sales Report Dashboard")

root.geometry("1200x700+100+30")

root.config(bg="#f0f2f5")

# ===== FUNCTIONS =====

# TOTAL REVENUE
def total_revenue():

    cursor.execute(
        "SELECT SUM(total_price) FROM sales"
    )

    result = cursor.fetchone()

    if result[0] is None:
        return 0

    return result[0]

# TOTAL SALES
def total_sales():

    cursor.execute(
        "SELECT COUNT(*) FROM sales"
    )

    result = cursor.fetchone()

    return result[0]

# TOTAL MEDICINES SOLD
def medicines_sold():

    cursor.execute(
        "SELECT SUM(quantity) FROM sales"
    )

    result = cursor.fetchone()

    if result[0] is None:
        return 0

    return result[0]

# TODAY REVENUE
def today_revenue():

    cursor.execute(
        """
        SELECT SUM(total_price)
        FROM sales
        WHERE sale_date = CURDATE()
        """
    )

    result = cursor.fetchone()

    if result[0] is None:
        return 0

    return result[0]

# ===== TITLE =====
title = Label(
    root,
    text="SALES REPORT DASHBOARD",
    bg="#673AB7",
    fg="white",
    font=("Helvetica", 28, "bold"),
    pady=15
)

title.pack(fill=X)

# ===== CARD FRAME =====
card_frame = Frame(root, bg="#f0f2f5")

card_frame.pack(pady=30)

# ===== CARD FUNCTION =====
def create_card(text, value, row, col, color):

    frame = Frame(
        card_frame,
        bg=color,
        width=250,
        height=140,
        bd=4,
        relief=RIDGE
    )

    frame.grid(
        row=row,
        column=col,
        padx=25,
        pady=20
    )

    frame.grid_propagate(False)

    Label(
        frame,
        text=text,
        font=("Helvetica", 16, "bold"),
        bg=color,
        fg="white"
    ).place(relx=0.5, rely=0.3, anchor=CENTER)

    Label(
        frame,
        text=value,
        font=("Helvetica", 24, "bold"),
        bg=color,
        fg="white"
    ).place(relx=0.5, rely=0.65, anchor=CENTER)

# ===== CARDS =====
create_card(
    "Total Revenue",
    f"₹ {total_revenue()}",
    0,
    0,
    "#009688"
)

create_card(
    "Total Sales",
    total_sales(),
    0,
    1,
    "#1976D2"
)

create_card(
    "Medicines Sold",
    medicines_sold(),
    1,
    0,
    "#FF9800"
)

create_card(
    "Today's Revenue",
    f"₹ {today_revenue()}",
    1,
    1,
    "#D32F2F"
)

# ===== SALES TABLE FRAME =====
table_frame = Frame(
    root,
    bg="white",
    bd=3,
    relief=RIDGE
)

table_frame.pack(
    fill=BOTH,
    expand=1,
    padx=40,
    pady=20
)

scroll_x = Scrollbar(
    table_frame,
    orient=HORIZONTAL
)

scroll_y = Scrollbar(
    table_frame,
    orient=VERTICAL
)

sales_table = ttk.Treeview(
    table_frame,
    columns=(
        "id",
        "medicine",
        "quantity",
        "price",
        "date"
    ),
    xscrollcommand=scroll_x.set,
    yscrollcommand=scroll_y.set
)

scroll_x.pack(side=BOTTOM, fill=X)

scroll_y.pack(side=RIGHT, fill=Y)

scroll_x.config(command=sales_table.xview)

scroll_y.config(command=sales_table.yview)

sales_table.heading("id", text="Sale ID")
sales_table.heading("medicine", text="Medicine")
sales_table.heading("quantity", text="Quantity")
sales_table.heading("price", text="Total Price")
sales_table.heading("date", text="Sale Date")

sales_table["show"] = "headings"

sales_table.column("id", width=80)
sales_table.column("medicine", width=220)
sales_table.column("quantity", width=120)
sales_table.column("price", width=150)
sales_table.column("date", width=150)

sales_table.pack(fill=BOTH, expand=1)

# ===== FETCH SALES DATA =====
cursor.execute(
    "SELECT * FROM sales"
)

rows = cursor.fetchall()

for row in rows:

    sales_table.insert(
        "",
        END,
        values=row
    )

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