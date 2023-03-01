import argparse
import math
import os
import platform
import sys
from pathlib import Path

import numpy as np
import torch
import time

from utils.augmentations import letterbox

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # YOLOv5 root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative

from models.common import DetectMultiBackend
from utils.dataloaders import IMG_FORMATS, VID_FORMATS, LoadImages, LoadScreenshots, LoadStreams
from utils.general import (LOGGER, Profile, check_file, check_img_size, check_imshow, check_requirements, colorstr, cv2,
                           increment_path, non_max_suppression, print_args, scale_boxes, strip_optimizer, xyxy2xywh)
from utils.plots import Annotator, colors, save_one_box
from utils.torch_utils import select_device, smart_inference_mode

from multiprocessing import set_start_method, Queue, Process
from win32_screenshot import win32_sct
from mss_screenshot import mss_sct
from landmine_control import landmine_ctrl
from get_hwnd import get_hwnd
from mouse_control import input_listener
from handle import handle_data


# def global value
start_yolo, flag_yolo = False, True

# Get hwnd
hwnd, hwndTool = get_hwnd('夜神模擬器')


@smart_inference_mode()
def detect_img(obj_data, start):
    # Load model
    # device = torch.device('cuda:0')
    device = select_device()
    model = DetectMultiBackend(weights='../../runs/train/exp13/weights/best.pt', device=device, dnn=False, data=False, fp16=True)

    # start yolo
    while start.empty():
        print('按home鍵開啟腳本雷')
        time.sleep(5)

    while True:
        # Read img
        # im = mss_screenshot(grap_rect=(1361, 32, 543, 966))
        # im = cv2.imread(r"C:\Users\Abc\OneDrive\圖片\螢幕擷取畫面\螢幕擷取畫面_20230212_052514.png")
        # im = win32_sct(0, grap_rect=(1280, 358, 640, 640))

        im = win32_sct(hwnd, grap_rect=(0, 335, 640, 640))
        im0 = im

        # Transform img
        im = letterbox(im, (640, 640), stride=32, auto=True)[0]  # padded resize
        im = im.transpose((2, 0, 1))[::-1]  # HWC to CHW, BGR to RGB
        im = np.ascontiguousarray(im)  # contiguous

        # Run inference
        im = torch.from_numpy(im).to(model.device)
        im = im.half() if model.fp16 else im.float()  # uint8 to fp16/32
        im /= 255  # 0 - 255 to 0.0 - 1.0
        if len(im.shape) == 3:
            im = im[None]  # expand for batch dim

        # Inference
        # start = time.time()
        pred = model(im, augment=False, visualize=False)

        # NMS
        pred = non_max_suppression(pred, conf_thres=0.65, iou_thres=0.45, classes=None, max_det=300)

        # Second-stage classifier (optional)
        # pred = utils.general.apply_classifier(pred, classifier_model, im, im0s)

        # Process predictions
        for i, det in enumerate(pred):  # per image
            annotator = Annotator(im0, line_width=1)
            if len(det):
                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_boxes(im.shape[2:], det[:, :4], im0.shape).round()

                # Write results
                for *xyxy, conf, cls in reversed(det):
                    xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4))).view(-1).tolist()  # normalized xywh
                    # line = cls, *xywh, conf # label format
                    annotator.box_label(xyxy, label=f'[{int(cls)}, {round(float(conf), 2)}]', color=(34, 139, 34), txt_color=(0, 191, 255))

                    # save obj data
                    obj_list = [int(cls), xywh]
                    obj_data.put(obj_list)

        obj_data.put(777)

        # cv2 result
        im0 = annotator.result()
        cv2.namedWindow("screenshot", cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)
        cv2.imshow("screenshot", im0)
        cv2.waitKey(1)


def main():
    # run
    set_start_method('spawn')
    q = Queue()
    s = Queue()
    f = Queue()
    p_d = Process(target=detect_img, args=(q, s, ))
    p_d.start()
    p_m = Process(target=handle_data, args=(q, f, hwndTool, ))
    p_m.start()
    p_m = Process(target=input_listener, args=(s, f, ))
    p_m.start()


if __name__ == "__main__":
    main()
