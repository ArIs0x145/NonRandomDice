import win32gui, win32ui, win32con, win32api
import numpy as np
import cv2

def win32_sct(hwnd, grap_rect=None):
    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()
    saveBitMap = win32ui.CreateBitmap()

    if grap_rect:
        x, y, w, h = grap_rect
    else:
        left, top, right, bot = win32gui.GetWindowRect(hwnd)
        x, y = 0, 0
        w = int((right - left) * 1.25)
        h = int((bot - top) * 1.25)

    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
    saveDC.SelectObject(saveBitMap)
    saveDC.BitBlt((0, 0), (w, h), mfcDC, (x, y), win32con.SRCCOPY)

    signed_ints_array = saveBitMap.GetBitmapBits(True)
    img = np.frombuffer(signed_ints_array, dtype="uint8")
    img.shape = (h, w, 4)
    img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)

    return img

if __name__ == '__main__':
    while True:
        img = win32_sct()
        cv2.namedWindow("a", cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)
        cv2.imshow('a', img)
        cv2.waitKey(1)