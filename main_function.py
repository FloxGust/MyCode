# main_function.py

import pandas as pd
import os

# ฟังก์ชั่นสำหรับการจัดการข้อมูลในไฟล์ CSV
def process_data(user_inputs, filename="R24020016 - R24020016.csv"):
    columns_per_entry = 3  # จำนวนคอลัมน์ต่อหนึ่งชุดข้อมูล (Time-Start, Time-End, RSSI)

    # ตรวจสอบว่ามีไฟล์อยู่แล้วหรือไม่ ถ้าไม่มีสร้างไฟล์ใหม่
    if not os.path.exists(filename):
        # สร้าง DataFrame ว่างๆ ตามโครงสร้างคอลัมน์ที่ต้องการ
        df = pd.DataFrame(columns=["Time-Start", "Time-End", "RSSI"])
    else:
        # อ่านข้อมูลจากไฟล์ CSV ที่มีอยู่
        df = pd.read_csv(filename)

    rssi_list = []
    time_list = []
    start_time = None

    for user_input in user_inputs:
        try:
            parts = user_input.split(" -> ")
            time_part = parts[0]
            rssi_value = int(parts[1].split(",")[1])

            # เก็บค่าที่รับมาใน list
            if start_time is None:
                start_time = time_part

            rssi_list.append(rssi_value)
            time_list.append(time_part)

        except (IndexError, ValueError):
            continue  # ข้ามข้อมูลที่ไม่ถูกต้อง

    # ถ้าข้อมูลน้อยเกินไป ให้ข้ามการประมวลผล
    if not rssi_list or not time_list:
        return "ข้อมูลไม่เพียงพอในการประมวลผล"

    # คำนวณ Mode ของค่า RSSI ที่เก็บได้
    mode_rssi = abs(max(rssi_list, key=rssi_list.count))

    # หาเวลาที่น้อยที่สุดในชุดข้อมูลสำหรับ Time-End (ไม่รวมแถวแรก)
    if len(time_list) > 1:
        time_end = min(time_list[1:])
    else:
        time_end = time_list[0]

    # ค้นหาตำแหน่งว่างใน DataFrame เพื่อลงข้อมูลใหม่
    col_index = 0
    while col_index < len(df.columns):
        col_subset = df.iloc[:, col_index:col_index + columns_per_entry]
        if col_subset.isnull().all().all():  # เช็คว่าคอลัมน์ทั้งชุดว่างทั้งหมดหรือไม่
            break
        col_index += columns_per_entry

    # ถ้าตำแหน่งคอลัมน์ใหม่เกินจากที่มีอยู่ ให้สร้างคอลัมน์ใหม่
    if col_index >= len(df.columns):
        for i in range(columns_per_entry):
            df[f"Time-Start-{(col_index // columns_per_entry) + 1}"] = None
            df[f"Time-End-{(col_index // columns_per_entry) + 1}"] = None
            df[f"RSSI-{(col_index // columns_per_entry) + 1}"] = None

    # อัปเดตชื่อคอลัมน์เพื่อให้ตรงกับที่ต้องการ
    entry_columns = df.columns[col_index:col_index + columns_per_entry]

    # ใส่ข้อมูลใหม่ลงในแถวที่มีตำแหน่งว่าง (หรือสร้างแถวใหม่ถ้าตำแหน่งว่างหมด)
    new_data = pd.Series([start_time, time_end, mode_rssi], index=entry_columns)
    df = df.append(new_data, ignore_index=True)

    # เขียนข้อมูลกลับลงไฟล์ CSV
    df.to_csv(filename, index=False)
    return f"ข้อมูลถูกเขียนลงไฟล์ {filename} แล้ว"
