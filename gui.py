# gui.py

import customtkinter as ctk
from main_function import process_data  # นำเข้า function จากไฟล์ main_function.py
import pandas as pd

# ฟังก์ชั่นสำหรับบันทึกข้อมูลลงในไฟล์ CSV
def save_data():
    # ดึงข้อมูลจากช่อง input
    user_input = input_entry.get("1.0", "end-1c").strip()
    if user_input:
        inputs = user_input.splitlines()  # แยกข้อมูลแต่ละบรรทัดเป็น list
        message = process_data(inputs)  # ส่งข้อมูลไปยังฟังก์ชันใน main_function.py
        display_box.configure(state='normal')  # เปิดการแก้ไขในกล่องแสดงข้อมูล
        display_box.delete("1.0", "end")  # ลบข้อมูลเดิม
        display_box.insert("1.0", message)  # ใส่ข้อความแสดงสถานะการบันทึกข้อมูล
        display_box.configure(state='disabled')  # ปิดการแก้ไขในกล่องแสดงข้อมูล
        input_entry.delete("1.0", "end")  # ล้างข้อมูลในช่อง input

# กำหนดธีมและสร้างหน้าต่างหลัก
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

app = ctk.CTk()  # สร้างหน้าต่างหลัก
app.title("Data Entry GUI")
app.geometry("600x400")

# สร้าง Label สำหรับช่องกรอกข้อมูล
input_label = ctk.CTkLabel(app, text="กรอกข้อมูลของคุณที่นี่:", font=("Arial", 16))
input_label.pack(pady=10)

# สร้างช่องกรอกข้อมูลที่กว้าง
input_entry = ctk.CTkTextbox(app, height=100, width=500)
input_entry.pack(pady=10)

# สร้างปุ่มสำหรับบันทึกข้อมูล
save_button = ctk.CTkButton(app, text="บันทึกข้อมูล", command=save_data)
save_button.pack(pady=10)

# สร้างกล่องแสดงข้อมูลล่าสุด
display_label = ctk.CTkLabel(app, text="สถานะการบันทึกข้อมูล:", font=("Arial", 16))
display_label.pack(pady=10)

display_box = ctk.CTkTextbox(app, height=50, width=500, state='disabled')  # ตั้งค่า state เป็น 'disabled' เพื่อไม่ให้แก้ไขได้
display_box.pack(pady=10)

# เริ่มการทำงานของหน้าต่างหลัก
app.mainloop()
