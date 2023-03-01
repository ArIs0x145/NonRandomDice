from pynput import keyboard
import win32gui, win32con
import time


# def v
start_yolo, flag_yolo = False, False


# ctrl
def keyboard_press(hwndTool, key):
    win32gui.SendMessage(hwndTool, win32con.WM_CHAR, ord(key), 0)


# listen
def on_press(key):
    global start_yolo, flag_yolo
    try:
        if key == keyboard.Key.home:
            start_yolo = True
        if key == keyboard.Key.f1:
            flag_yolo = True
    except AttributeError:
        print('special key {0} pressed'.format(key))


def input_listener(start, f_start):
    global start_yolo, flag_yolo, count
    # ...or, in a non-blocking fashion:
    listener_keyboard = keyboard.Listener(on_press=on_press)
    listener_keyboard.start()

    while not start_yolo:
        pass
    start.put(1)
    print('腳本雷已開啟')
    while True:
        if flag_yolo:
            f_start.put(1)
            flag_yolo = False
        else:
            continue


if __name__ == '__main__':
        win32gui.SendMessage(460734, win32con.WM_CHAR, ord('A'), 0)