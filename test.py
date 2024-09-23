import csv
from collections import Counter

# ฟังก์ชั่นในการหาค่า Mode
def find_mode(data):
    if not data:
        return None
    count = Counter(data)
    mode_data = count.most_common(1)
    return mode_data[0][0]

# ฟังก์ชั่นหลักของโปรแกรม
def main():
    # สร้างไฟล์ CSV ขึ้นมาใหม่ และเขียน Header
    filename = "R24080016.csv"
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Time-Start", "Time-End", "RSSI"])

    # รับข้อมูลจากผู้ใช้
    rssi_list = []
    start_time = None

    print("ใส่ข้อมูล (แต่ละบรรทัด ตามด้วย Enter) และกด Enter 2 ครั้งเพื่อจบการ input:")

    while True:
        user_input = input()
        if user_input == "":
            # ถ้ากด Enter สองครั้ง
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

        except (IndexError, ValueError):
            print("ข้อมูลไม่ถูกต้อง กรุณาใส่ข้อมูลในรูปแบบ: 13:48:30.873 -> R24080016,-71")
            continue

    # คำนวณ Mode ของค่า RSSI ที่เก็บได้
    mode_rssi = find_mode(rssi_list)

    # เขียนข้อมูลลงไฟล์ CSV
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([start_time, time_part, mode_rssi])

    print(f"ข้อมูลถูกเขียนลงไฟล์ {filename} แล้ว")
    print("จบการทำงานของโปรแกรม")

# เรียกใช้ฟังก์ชั่นหลัก
if __name__ == "__main__":
    main()
