import pandas as pd
import customtkinter as ctk
from tkinter import messagebox
from tkinter import ttk  # ใช้ ttk สำหรับ Treeview

# ฟังก์ชั่นสำหรับการอัพเดทข้อมูลใน Treeview
def update_treeview():
    # Clear existing data in the treeview
    tree.delete(*tree.get_children())
    
    # ใส่ข้อมูลใหม่จาก DataFrame ลงใน treeview
    for _, row in df.iterrows():
        values = [str(item) if not pd.isna(item) else "" for item in row]
        tree.insert("", "end", values=values)

# ฟังก์ชั่นสำหรับการเพิ่มคอลัมน์ใหม่
def add_new_columns():
    global df, columns_per_entry
    # คำนวณจำนวนคอลัมน์ใหม่ที่ต้องเพิ่ม
    new_col_start_index = len(df.columns)
    new_column_names = [
        f"Time-Start-{(new_col_start_index // columns_per_entry) + 1}",
        f"Time-End-{(new_col_start_index // columns_per_entry) + 1}",
        f"RSSI-{(new_col_start_index // columns_per_entry) + 1}"
    ]

    # เพิ่มคอลัมน์ใหม่ใน DataFrame
    for col_name in new_column_names:
        df[col_name] = None
    
    # อัพเดท treeview columns
    tree["columns"] = df.columns.tolist()
    tree["displaycolumns"] = df.columns.tolist()

    # กำหนดหัว column ใหม่
    for col in tree["columns"]:
        tree.heading(col, text=col)

    # อัพเดทข้อมูลใน treeview
    update_treeview()

# ฟังก์ชั่นสำหรับการเพิ่มข้อมูลใหม่
def add_data():
    # ค่าตัวอย่างสำหรับข้อมูลใหม่
    new_data = ["14:09:00", "14:09:01", 50]
    # หา column index ที่จะใส่ข้อมูลใหม่
    col_index = 0
    while col_index < len(df.columns):
        col_subset = df.iloc[:, col_index:col_index + columns_per_entry]
        if col_subset.isnull().all().all():
            break
        col_index += columns_per_entry

    # ตรวจสอบว่ามีพื้นที่พอสำหรับใส่ข้อมูลไหม
    if col_index < len(df.columns):
        df.iloc[len(df), col_index:col_index + columns_per_entry] = new_data
        update_treeview()
    else:
        messagebox.showerror("Error", "ไม่มีพื้นที่พอสำหรับใส่ข้อมูลใหม่ กรุณาเพิ่มคอลัมน์ใหม่ก่อน")

# กำหนดจำนวนคอลัมน์ต่อชุดข้อมูล
columns_per_entry = 3

# สร้าง DataFrame ว่างสำหรับเก็บข้อมูล
df = pd.DataFrame(columns=["Time-Start", "Time-End", "RSSI"])

# สร้างหน้าต่างหลักของ customtkinter
root = ctk.CTk()
root.title("Dynamic Column Addition")

# กำหนดขนาดหน้าต่าง
root.geometry("800x600")

# สร้าง Treeview จาก tkinter
tree_frame = ctk.CTkFrame(root)
tree_frame.pack(expand=True, fill='both')

# เพิ่ม scroll bar สำหรับ treeview
tree_scroll = ctk.CTkScrollbar(tree_frame, orientation="horizontal")
tree_scroll.pack(side="bottom", fill="x")

# สร้าง Treeview สำหรับแสดงข้อมูล
tree = ttk.Treeview(tree_frame, xscrollcommand=tree_scroll.set)
tree_scroll.configure(command=tree.xview)

tree.pack(expand=True, fill='both')

# กำหนด columns ให้กับ treeview
tree["columns"] = df.columns.tolist()
tree["displaycolumns"] = df.columns.tolist()

# กำหนดหัว column ให้กับ treeview
for col in tree["columns"]:
    tree.heading(col, text=col)

# ปุ่มสำหรับการเพิ่มคอลัมน์ใหม่
add_column_btn = ctk.CTkButton(root, text="เพิ่มคอลัมน์ใหม่", command=add_new_columns)
add_column_btn.pack(pady=10)

# ปุ่มสำหรับการเพิ่มข้อมูลใหม่
add_data_btn = ctk.CTkButton(root, text="เพิ่มข้อมูลใหม่", command=add_data)
add_data_btn.pack(pady=10)

# เริ่มต้นโปรแกรม GUI
root.mainloop()
