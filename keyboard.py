from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Controller, Key

keyboard = Controller()

def on_click(x, y, button, pressed):
    if pressed:
        if button.name == 'left':  # คลิกเม้าซ้าย
            # กด Ctrl + C
            with keyboard.pressed(Key.ctrl):
                keyboard.press('c')
                keyboard.release('c')
            print("Ctrl + C")

        elif button.name == 'middle':  # คลิกเม้ากลาง
            # กด Ctrl + V
            with keyboard.pressed(Key.ctrl):
                keyboard.press('v')
                keyboard.release('v')
            print("Ctrl + V")

# เริ่มต้นฟังการคลิกของเม้าส์
with MouseListener(on_click=on_click) as listener:
    listener.join()
