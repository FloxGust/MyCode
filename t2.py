import csv
import os
from collections import Counter

# ฟังก์ชั่นในการหาค่า Mode
def find_mode(data):
    if not data:
        return None
    count = Counter(data)
    mode_data = count.most_common(1)
    return mode_data[0][0]

# ฟังก์ชั่นในการตรวจสอบขนาดของไฟล์และจำนวนแถวในไฟล์
def check_csv_file(filename):
    # ตรวจสอบว่าไฟล์มีข้อมูลหรือไม่
    if not os.path.exists(filename):
        return 0

    with open(filename, mode='r', newline='') as file:
        reader = csv.reader(file)
        row_count = sum(1 for _ in reader)
        return row_count

# ฟังก์ชั่นหลักของโปรแกรม
def main():
    # ชื่อไฟล์ CSV ที่จะบันทึกข้อมูล
    filename = "R24080016.csv"
    # ตรวจสอบจำนวนแถวในไฟล์
    row_count = check_csv_file(filename)

    # ถ้าไฟล์ไม่มีข้อมูล ให้สร้างไฟล์ใหม่และเขียน Header
    if row_count == 0:
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Time-Start", "Time-End", "RSSI"])

    # รับข้อมูลจากผู้ใช้
    while True:
        rssi_list = []
        time_list = []
        start_time = None

        print("ใส่ข้อมูล (แต่ละบรรทัด ตามด้วย Enter) หรือพิมพ์ 'end' เพื่อจบโปรแกรม:")

        while True:
            user_input = input()
            if user_input.lower() == "end":
                print("จบการทำงานของโปรแกรมทั้งหมด")
                return

            if user_input == "":
                # กด Enter สองครั้งเพื่อหยุดรับข้อมูลชุดนี้และไปประมวลผล
                if start_time is not None:
                    break
                continue

            # แยกข้อมูลเวลาและค่า RSSI ออกจากข้อมูลที่รับเข้ามา
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
                print("ข้อมูลไม่ถูกต้อง กรุณาใส่ข้อมูลในรูปแบบ: 13:48:30.873 -> R24080016,-71")
                continue

        # คำนวณ Mode ของค่า RSSI ที่เก็บได้
        mode_rssi = find_mode(rssi_list)

        # นำเครื่องหมาย '-' ออกจาก RSSI ก่อนเขียนลงไฟล์
        mode_rssi = abs(mode_rssi)

        # หาเวลาที่น้อยที่สุดในชุดข้อมูลสำหรับ Time-End
        time_end = min(time_list)

        # เขียนข้อมูลลงไฟล์ CSV
        with open(filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([start_time, time_end, mode_rssi])

        print(f"ข้อมูลถูกเขียนลงไฟล์ {filename} แล้ว")

# เรียกใช้ฟังก์ชั่นหลัก
if __name__ == "__main__":
    main()
