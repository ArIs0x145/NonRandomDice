import cv2
import numpy as np
from mss import mss



def mss_sct(grap_rect):
    x, y, w, h = grap_rect
    window_size = (
        int(x),
        int(y),
        int(x + w),
        int(y + h)
    )
    img = mss().grab(window_size)
    img = np.array(img)
    img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
    return img
