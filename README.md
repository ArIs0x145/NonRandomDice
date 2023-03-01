# Random Dice Plugin (隨機骰子插件) (歷史久遠純紀錄不保證能用)

![RD](./1EE8AF75-CA81-4B64-B49D-BD4CABE7CF9A.png)

基於YOLOv5的Random Dice遊戲自動化輔助工具，可以識別遊戲元素並執行自動操作。

## 專案簡介

這個專案使用計算機視覺技術自動識別Random Dice遊戲中的元素，並通過自動化腳本控制遊戲。主要功能包括：

- 即時螢幕截圖和遊戲元素識別（基於YOLOv5）
- 自動地雷骰子控制
- 根據遊戲波次自動調整策略
- 鍵盤快捷鍵控制腳本開關

## 專案結構

```
randomdice-plug/
├── dataset/               # 訓練資料集
│   ├── train/             # 訓練集圖像和標註
│   ├── valid/             # 驗證集圖像和標註
│   └── class-hit.yaml     # 類別定義檔案
├── model/                 # 模型檔案
│   ├── best.pt            # 訓練好的最佳模型
│   └── yolov5s.pt         # YOLOv5s預訓練模型
├── funtion/               # 功能模組
│   ├── detect.py          # 物件檢測主模組
│   ├── handle.py          # 資料處理模組
│   ├── landmine_control.py # 地雷控制模組
│   ├── mouse_control.py   # 滑鼠和鍵盤控制
│   ├── get_hwnd.py        # 獲取視窗控制代碼
│   ├── win32_screenshot.py # Win32螢幕截圖
│   └── mss_screenshot.py  # MSS螢幕截圖
└── old_dataset/           # 舊版資料集（備份）
```

## 安裝要求

確保你已安裝以下依賴：

```bash
# 基礎依賴
numpy>=1.18.5
opencv-python>=4.1.1
torch>=1.7.0
torchvision>=0.8.1
PyYAML>=5.3.1

# 隨機骰子插件特定依賴
pywin32>=305        # 用於Windows介面控制
pynput>=1.7.6       # 用於鍵盤輸入控制
mss>=7.0.0          # 用於螢幕擷取
PyQt5>=5.15.0       # 用於GUI介面
multiprocess>=0.70.14  # 用於行程管理
```

你可以通過以下命令安裝所有依賴：

```bash
pip install -r requirements.txt
```

## 使用方法

1. 確保遊戲視窗（夜神模擬器）已經打開
2. 執行檢測腳本：

```bash
python funtion/detect.py
```

3. 使用快捷鍵控制腳本：
   - `Home` 鍵：啟動腳本
   - `F1` 鍵：切換腳本開/關狀態

## 客製化

### 模型訓練

如果你想訓練自己的模型，可以使用以下命令：

```bash
# 從YOLOv5儲存庫執行訓練
python train.py --data randomdice-plug/dataset/class-hit.yaml --weights yolov5s.pt --img 640
```

### 調整檢測參數

在 `detect.py` 檔案中，你可以調整以下參數：
- 信心閾值 (`conf_thres`)
- IoU閾值 (`iou_thres`)
- 檢測類別

## 備註

- 該專案是為"Random Dice"遊戲開發的，針對夜神模擬器進行了最佳化
- 主要功能是自動控制地雷骰子的放置和觸發
- 使用YOLOv5進行即時物件檢測
