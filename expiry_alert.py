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

root.title("Expiry Alert System")

root.geometry("1000x600+120+50")

root.config(bg="#f0f2f5")

# ===== TITLE =====
title = Label(
    root,
    text="MEDICINE EXPIRY ALERT SYSTEM",
    bg="#E91E63",
    fg="white",
    font=("Helvetica", 26, "bold"),
    pady=15
)

title.pack(fill=X)

# ===== TABLE FRAME =====
table_frame = Frame(
    root,
    bg="white",
    bd=4,
    relief=RIDGE
)

table_frame.place(
    x=30,
    y=100,
    width=930,
    height=420
)

# ===== SCROLLBARS =====
scroll_x = Scrollbar(
    table_frame,
    orient=HORIZONTAL
)

scroll_y = Scrollbar(
    table_frame,
    orient=VERTICAL
)

medicine_table = ttk.Treeview(
    table_frame,
    columns=(
        "id",
        "name",
        "company",
        "price",
        "quantity",
        "expiry"
    ),
    xscrollcommand=scroll_x.set,
    yscrollcommand=scroll_y.set
)

scroll_x.pack(side=BOTTOM, fill=X)

scroll_y.pack(side=RIGHT, fill=Y)

scroll_x.config(command=medicine_table.xview)

scroll_y.config(command=medicine_table.yview)

# ===== HEADINGS =====
medicine_table.heading("id", text="ID")
medicine_table.heading("name", text="Medicine")
medicine_table.heading("company", text="Company")
medicine_table.heading("price", text="Price")
medicine_table.heading("quantity", text="Quantity")
medicine_table.heading("expiry", text="Expiry Date")

medicine_table["show"] = "headings"

# ===== COLUMN WIDTH =====
medicine_table.column("id", width=70)
medicine_table.column("name", width=200)
medicine_table.column("company", width=200)
medicine_table.column("price", width=120)
medicine_table.column("quantity", width=120)
medicine_table.column("expiry", width=150)

medicine_table.pack(fill=BOTH, expand=1)

# ===== FETCH EXPIRING MEDICINES =====
query = """
SELECT *
FROM medicine
WHERE expiry_date <= CURDATE() + INTERVAL 30 DAY
"""

cursor.execute(query)

rows = cursor.fetchall()

for row in rows:

    medicine_table.insert(
        "",
        END,
        values=row
    )

# ===== ALERT TEXT =====
Label(
    root,
    text="Medicines expiring within 30 days are shown above",
    bg="#f0f2f5",
    fg="red",
    font=("Helvetica", 14, "bold")
).place(x=220, y=540)

# ===== FOOTER =====
footer = Label(
    root,
    text="Expiry Monitoring System",
    bg="#E91E63",
    fg="white",
    font=("Helvetica", 11, "bold"),
    pady=8
)

footer.pack(side=BOTTOM, fill=X)

root.mainloop()