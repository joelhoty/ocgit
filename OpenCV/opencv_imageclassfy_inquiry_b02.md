<!-- Path: General_python/openCV/影像辨識-傳統方法 | Timestamp: 2025-10-06 14:30:00 | Version: b02 -->
# OpenCV 影像辨識實作題目（詳細版）

本文件包含三個實作題目，讓學習者能夠運用 `opencv_imageclassfy_b05.md` 教學文件中的程式範例，完成指定的作業任務。這些題目專為 Python 初學者設計，提供詳細的需求說明與程式碼提示範例。

---

## 題目一：人臉計數與框選應用

### 📋 任務說明

請撰寫一個 Python 程式，能夠自動偵測照片中的人臉數量，並在每張人臉上方顯示編號標籤（例如：「人臉 1」、「人臉 2」...）。

---

### ✅ 詳細需求列表

#### 需求 1：環境準備與檔案下載
**說明**：在 Google Colab 環境中下載所需的模型檔案和測試圖片。

**程式碼提示**：
```python
# 在 Colab 第一個儲存格執行
import urllib.request
import os

# 下載必要檔案
files = {
    'haarcascade_frontalface_default.xml': 'https://raw.githubusercontent.com/opencv/opencv/4.x/data/haarcascades/haarcascade_frontalface_default.xml',
    'mona.jpg': 'https://steam.oxxostudio.tw/down/python/ai/mona.jpg',
    'girl.jpg': 'https://steam.oxxostudio.tw/down/python/ai/girl.jpg'
}

for filename, url in files.items():
    if not os.path.exists(filename):
        print(f"下載 {filename}...")
        urllib.request.urlretrieve(url, filename)
        print(f"✓ {filename} 下載完成")
    else:
        print(f"✓ {filename} 已存在")
```

---

#### 需求 2：匯入必要套件
**說明**：匯入 OpenCV、NumPy 和 Colab 顯示工具。

**程式碼提示**：
```python
# 匯入必要的套件
import cv2
import numpy as np
from google.colab.patches import cv2_imshow
```

---

#### 需求 3：讀取並檢查圖片
**說明**：讀取圖片檔案，並檢查是否成功讀取。

**程式碼提示**：
```python
# 讀取圖片
img = cv2.imread('girl.jpg')  # 或使用其他包含人臉的圖片

# 檢查圖片是否成功讀取
if img is None:
    print("錯誤: 無法讀取圖片，請確認檔案已正確下載")
    # 若失敗，程式應該停止執行
else:
    print("✓ 圖片讀取成功")
    # 可選：顯示圖片尺寸
    height, width, channels = img.shape
    print(f"圖片尺寸: {width} x {height} 像素")
```

---

#### 需求 4：轉換為灰階影像
**說明**：將彩色圖片轉換為灰階，以提高偵測效率。

**程式碼提示**：
```python
# 將圖片轉換為灰階
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
print("✓ 圖片已轉換為灰階")
```

---

#### 需求 5：載入 Haar Cascade 人臉偵測模型
**說明**：載入預訓練的人臉偵測模型。

**程式碼提示**：
```python
# 載入人臉偵測模型
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# 檢查模型是否成功載入
if face_cascade.empty():
    print("錯誤: 無法載入人臉偵測模型")
else:
    print("✓ 人臉偵測模型載入成功")
```

---

#### 需求 6：執行人臉偵測
**說明**：使用 `detectMultiScale()` 方法偵測圖片中的所有人臉。

**程式碼提示**：
```python
# 偵測人臉
# scaleFactor: 影像縮放比例，1.1 表示每次縮小 10%
# minNeighbors: 構成有效偵測所需的最少鄰居數量
faces = face_cascade.detectMultiScale(
    gray,                # 輸入的灰階圖片
    scaleFactor=1.1,     # 建議值：1.05-1.3
    minNeighbors=5,      # 建議值：3-8
    minSize=(30, 30)     # 最小人臉尺寸，避免偵測過小的區域
)

# 顯示偵測結果
print(f"✓ 偵測到 {len(faces)} 張人臉")
```

---

#### 需求 7：在每張人臉上繪製矩形框與編號
**說明**：遍歷所有偵測到的人臉，繪製框線並加上編號標籤。

**程式碼提示**：
```python
# 遍歷所有偵測到的人臉
for i, (x, y, w, h) in enumerate(faces, start=1):
    # 繪製矩形框
    # 參數：圖片, 左上角座標, 右下角座標, 顏色 (BGR), 線條粗細
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # 準備文字標籤
    label = f"人臉 {i}"

    # 在矩形框上方顯示編號
    # 文字位置設定在矩形框上方約 10 像素處
    text_x = x
    text_y = y - 10 if y - 10 > 10 else y + h + 20  # 避免超出圖片範圍

    # 繪製文字
    # 參數：圖片, 文字內容, 位置, 字體, 字體大小, 顏色, 粗細
    cv2.putText(
        img,                              # 目標圖片
        label,                            # 文字內容
        (text_x, text_y),                # 文字位置（左下角）
        cv2.FONT_HERSHEY_SIMPLEX,        # 字體類型
        0.9,                              # 字體大小
        (0, 255, 0),                      # 文字顏色（綠色）
        2                                 # 文字粗細
    )

    # 可選：輸出每張人臉的座標資訊
    print(f"人臉 {i}: 位置({x}, {y}), 大小({w}x{h})")
```

---

#### 需求 8：統計並顯示總人數
**說明**：在終端機輸出總人數，並在圖片左上角顯示統計資訊。

**程式碼提示**：
```python
# 在終端機輸出總人數
total_faces = len(faces)
print(f"\n========== 偵測結果 ==========")
print(f"總共偵測到 {total_faces} 張人臉")
print(f"==============================\n")

# 可選：在圖片左上角顯示總人數
summary_text = f"Total: {total_faces} faces"
cv2.putText(
    img,
    summary_text,
    (10, 30),                        # 左上角位置
    cv2.FONT_HERSHEY_SIMPLEX,
    1.0,                              # 較大的字體
    (255, 0, 0),                      # 藍色
    2
)
```

---

#### 需求 9：顯示處理後的結果
**說明**：使用 `cv2_imshow()` 顯示標記後的圖片。

**程式碼提示**：
```python
# 顯示處理後的圖片
print("處理後的圖片：")
cv2_imshow(img)

# 可選：儲存結果圖片
# cv2.imwrite('result_faces.jpg', img)
# print("✓ 結果已儲存為 result_faces.jpg")
```

---

### 📝 完整程式碼框架

```python
# ========== 題目一：人臉計數與框選應用 ==========

import cv2
import numpy as np
from google.colab.patches import cv2_imshow

# 1. 讀取圖片
img = cv2.imread('girl.jpg')

if img is None:
    print("錯誤: 無法讀取圖片")
else:
    # 2. 轉換為灰階
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 3. 載入人臉偵測模型
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    # 4. 偵測人臉
    faces = face_cascade.detectMultiScale(gray, 1.1, 5, minSize=(30, 30))

    # 5. 繪製矩形框與編號
    for i, (x, y, w, h) in enumerate(faces, start=1):
        # TODO: 繪製矩形框
        # TODO: 加上編號標籤
        pass

    # 6. 顯示總人數
    print(f"偵測到 {len(faces)} 張人臉")

    # 7. 顯示結果
    cv2_imshow(img)
```

---

### 🎯 測試建議

1. **基本測試**：使用單人照片（如 `girl.jpg`）進行測試
2. **進階測試**：使用多人照片（團體照、全家福）測試
3. **參數調整**：
   - 若有漏偵測：降低 `scaleFactor`（如 1.05）或 `minNeighbors`（如 3）
   - 若有誤判：提高 `minNeighbors`（如 7-8）

---

### 🚀 延伸挑戰（選做）

#### 挑戰 1：使用不同顏色標示不同人臉
```python
# 定義顏色列表（BGR 格式）
colors = [
    (0, 255, 0),    # 綠色
    (255, 0, 0),    # 藍色
    (0, 0, 255),    # 紅色
    (255, 255, 0),  # 青色
    (255, 0, 255),  # 洋紅色
]

for i, (x, y, w, h) in enumerate(faces):
    color = colors[i % len(colors)]  # 循環使用顏色
    cv2.rectangle(img, (x, y), (x+w, y+h), color, 2)
```

#### 挑戰 2：顯示人臉大小資訊
```python
for i, (x, y, w, h) in enumerate(faces, start=1):
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # 計算面積
    area = w * h
    label = f"Face {i}: {w}x{h} ({area}px)"

    cv2.putText(img, label, (x, y-10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
```

---

## 題目二：彩色物體定位器

### 📋 任務說明

請撰寫一個 Python 程式，能夠追蹤並標記圖片中的特定顏色物體，並在畫面上顯示該顏色物體的位置與數量。

---

### ✅ 詳細需求列表

#### 需求 1：匯入套件與建立測試圖片
**說明**：匯入必要套件，並建立包含多種顏色物體的測試圖片。

**程式碼提示**：
```python
import cv2
import numpy as np
from google.colab.patches import cv2_imshow

# 建立一個 400x500 的黑色畫布
img = np.zeros((400, 500, 3), dtype=np.uint8)

# 在畫布上繪製不同顏色的物體（BGR 格式）
# 紅色矩形
cv2.rectangle(img, (50, 50), (150, 150), (0, 0, 255), -1)
# 藍色矩形
cv2.rectangle(img, (200, 50), (300, 150), (255, 0, 0), -1)
# 綠色圓形
cv2.circle(img, (100, 250), 50, (0, 255, 0), -1)
# 黃色圓形
cv2.circle(img, (250, 250), 50, (0, 255, 255), -1)
# 紅色圓形
cv2.circle(img, (400, 300), 40, (0, 0, 255), -1)

# 顯示原始測試圖片
print("原始測試圖片：")
cv2_imshow(img)

# 保存原圖副本（用於後續標記）
img_result = img.copy()
```

---

#### 需求 2：設定要追蹤的顏色 HSV 範圍
**說明**：定義至少兩種顏色的 HSV 範圍。

**程式碼提示**：
```python
# 定義顏色追蹤字典
# 格式：'顏色名稱': (HSV下限, HSV上限, BGR顯示顏色)
color_ranges = {
    '紅色': {
        'lower': np.array([0, 40, 40]),      # HSV 下限
        'upper': np.array([10, 255, 255]),   # HSV 上限
        'display_color': (0, 0, 255)         # BGR 格式（用於繪製）
    },
    '藍色': {
        'lower': np.array([100, 40, 40]),
        'upper': np.array([130, 255, 255]),
        'display_color': (255, 0, 0)
    },
    '綠色': {
        'lower': np.array([40, 40, 40]),
        'upper': np.array([80, 255, 255]),
        'display_color': (0, 255, 0)
    },
    '黃色': {
        'lower': np.array([20, 40, 40]),
        'upper': np.array([40, 255, 255]),
        'display_color': (0, 255, 255)
    }
}

print("顏色範圍設定完成，將追蹤以下顏色：")
for color_name in color_ranges.keys():
    print(f"  - {color_name}")
```

**常見顏色 HSV 範圍參考**：
| 顏色 | H (色相) | S (飽和度) | V (亮度) |
|------|---------|-----------|---------|
| 紅色 | 0-10 或 170-180 | 40-255 | 40-255 |
| 橙色 | 11-25 | 40-255 | 40-255 |
| 黃色 | 26-40 | 40-255 | 40-255 |
| 綠色 | 41-80 | 40-255 | 40-255 |
| 青色 | 81-100 | 40-255 | 40-255 |
| 藍色 | 101-130 | 40-255 | 40-255 |
| 紫色 | 131-160 | 40-255 | 40-255 |

---

#### 需求 3：轉換色彩空間為 HSV
**說明**：將 BGR 圖片轉換為 HSV 格式，以便進行顏色追蹤。

**程式碼提示**：
```python
# 將圖片從 BGR 轉換為 HSV 色彩空間
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
print("✓ 圖片已轉換為 HSV 色彩空間")
```

---

#### 需求 4：為每種顏色建立遮罩並偵測物體
**說明**：遍歷每種顏色，建立遮罩、尋找輪廓、並標記物體。

**程式碼提示**：
```python
# 建立統計字典
color_statistics = {}

# 遍歷每種顏色
for color_name, color_info in color_ranges.items():
    print(f"\n處理顏色：{color_name}")

    # 步驟 4-1：建立顏色遮罩
    mask = cv2.inRange(
        hsv,                      # HSV 圖片
        color_info['lower'],      # 顏色下限
        color_info['upper']       # 顏色上限
    )

    # 可選：顯示遮罩（用於除錯）
    print(f"  {color_name} 遮罩：")
    cv2_imshow(mask)

    # 步驟 4-2：尋找輪廓
    contours, _ = cv2.findContours(
        mask,                          # 輸入遮罩
        cv2.RETR_EXTERNAL,             # 只偵測外部輪廓
        cv2.CHAIN_APPROX_SIMPLE        # 壓縮輪廓點數
    )

    print(f"  找到 {len(contours)} 個輪廓")

    # 步驟 4-3：過濾並標記有效輪廓
    valid_count = 0
    for contour in contours:
        # 計算輪廓面積
        area = cv2.contourArea(contour)

        # 過濾太小的輪廓（雜訊）
        if area > 100:  # 面積閾值，可調整
            valid_count += 1

            # 取得邊界矩形
            x, y, w, h = cv2.boundingRect(contour)

            # 繪製矩形框
            cv2.rectangle(
                img_result,
                (x, y),
                (x+w, y+h),
                color_info['display_color'],  # 使用對應顏色
                2                              # 線條粗細
            )

            # 加上標籤
            label = f"{color_name} ({area}px)"
            cv2.putText(
                img_result,
                label,
                (x, y-10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                color_info['display_color'],
                2
            )

            print(f"  - 物體 {valid_count}: 位置({x},{y}), 大小({w}x{h}), 面積{area}px")

    # 記錄統計資訊
    color_statistics[color_name] = valid_count
    print(f"  ✓ {color_name}物體總數: {valid_count}")
```

---

#### 需求 5：顯示統計結果
**說明**：在終端機和圖片上顯示每種顏色的物體數量。

**程式碼提示**：
```python
# 在終端機顯示統計結果
print("\n" + "="*40)
print("偵測結果統計")
print("="*40)
for color_name, count in color_statistics.items():
    print(f"{color_name}: {count} 個物體")
print("="*40 + "\n")

# 在圖片上顯示總統計
y_offset = 30
for i, (color_name, count) in enumerate(color_statistics.items()):
    text = f"{color_name}: {count}"
    cv2.putText(
        img_result,
        text,
        (10, y_offset + i*30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        color_ranges[color_name]['display_color'],
        2
    )
```

---

#### 需求 6：顯示處理結果
**說明**：並排顯示原圖和標記後的結果。

**程式碼提示**：
```python
# 顯示原圖
print("原始圖片：")
cv2_imshow(img)

# 顯示標記後的結果
print("\n標記後的結果：")
cv2_imshow(img_result)

# 可選：儲存結果
# cv2.imwrite('color_detection_result.jpg', img_result)
```

---

### 📝 完整程式碼框架

```python
# ========== 題目二：彩色物體定位器 ==========

import cv2
import numpy as np
from google.colab.patches import cv2_imshow

# 1. 建立測試圖片
img = np.zeros((400, 500, 3), dtype=np.uint8)
# TODO: 繪製不同顏色的物體

img_result = img.copy()

# 2. 設定顏色範圍
color_ranges = {
    '紅色': {
        'lower': np.array([0, 40, 40]),
        'upper': np.array([10, 255, 255]),
        'display_color': (0, 0, 255)
    },
    # TODO: 新增其他顏色
}

# 3. 轉換色彩空間
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# 4. 處理每種顏色
color_statistics = {}
for color_name, color_info in color_ranges.items():
    # TODO: 建立遮罩
    # TODO: 尋找輪廓
    # TODO: 標記物體
    pass

# 5. 顯示結果
print("統計結果：", color_statistics)
cv2_imshow(img_result)
```

---

### 🎯 測試建議

1. **調整面積閾值**：嘗試不同的 `area` 閾值（50, 100, 500）觀察結果
2. **調整 HSV 範圍**：若偵測效果不佳，微調上下限值
3. **測試真實照片**：使用包含實際物體的照片測試

---

### 🚀 延伸挑戰（選做）

#### 挑戰 1：計算物體中心點
```python
# 在標記物體時加入中心點計算
for contour in contours:
    if cv2.contourArea(contour) > 100:
        x, y, w, h = cv2.boundingRect(contour)

        # 計算中心點
        center_x = x + w // 2
        center_y = y + h // 2

        # 繪製中心點
        cv2.circle(img_result, (center_x, center_y), 5, (255, 255, 255), -1)

        # 標註座標
        cv2.putText(img_result, f"({center_x},{center_y})",
                    (center_x+10, center_y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
```

#### 挑戰 2：排序並標示最大/最小物體
```python
# 將所有輪廓與面積配對並排序
contour_areas = [(contour, cv2.contourArea(contour)) for contour in contours]
contour_areas.sort(key=lambda x: x[1], reverse=True)  # 由大到小排序

# 標示最大物體
if contour_areas:
    largest_contour, largest_area = contour_areas[0]
    x, y, w, h = cv2.boundingRect(largest_contour)
    cv2.putText(img_result, "LARGEST", (x, y-30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
```

---

## 題目三：智慧型隱私保護系統

### 📋 任務說明

請撰寫一個 Python 程式，能夠偵測人臉並「選擇性」地對特定五官進行馬賽克處理，實現更精細的隱私保護功能。

---

### ✅ 詳細需求列表

#### 需求 1：環境準備
**說明**：下載所需的模型檔案和測試圖片。

**程式碼提示**：
```python
import urllib.request
import os

# 下載所需檔案
files = {
    'haarcascade_frontalface_default.xml': 'https://raw.githubusercontent.com/opencv/opencv/4.x/data/haarcascades/haarcascade_frontalface_default.xml',
    'haarcascade_eye.xml': 'https://raw.githubusercontent.com/opencv/opencv/4.x/data/haarcascades/haarcascade_eye.xml',
    'haarcascade_mcs_mouth.xml': 'https://raw.githubusercontent.com/atduskgreg/opencv-processing/master/lib/cascade-files/haarcascade_mcs_mouth.xml',
    'girl.jpg': 'https://steam.oxxostudio.tw/down/python/ai/girl.jpg'
}

for filename, url in files.items():
    if not os.path.exists(filename):
        print(f"下載 {filename}...")
        urllib.request.urlretrieve(url, filename)
        print(f"✓ {filename} 下載完成")
```

---

#### 需求 2：匯入套件與設定模式
**說明**：匯入必要套件，並定義隱私保護模式。

**程式碼提示**：
```python
import cv2
import numpy as np
from google.colab.patches import cv2_imshow

# 設定隱私保護模式
# 選項："eyes", "mouth", "eyes_mouth", "none"
PRIVACY_MODE = "eyes"  # 可修改此變數來改變模式

print(f"隱私保護模式: {PRIVACY_MODE}")
```

---

#### 需求 3：讀取圖片與載入模型
**說明**：讀取測試圖片並載入所需的 Haar Cascade 模型。

**程式碼提示**：
```python
# 讀取圖片
img = cv2.imread('girl.jpg')

if img is None:
    print("錯誤: 無法讀取圖片")
else:
    print("✓ 圖片讀取成功")

    # 保存原圖副本（用於對比）
    img_original = img.copy()

    # 轉換為灰階
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 載入模型
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
    mouth_cascade = cv2.CascadeClassifier('haarcascade_mcs_mouth.xml')

    # 檢查模型是否載入成功
    if face_cascade.empty():
        print("錯誤: 人臉模型載入失敗")
    if eye_cascade.empty():
        print("錯誤: 眼睛模型載入失敗")
    if mouth_cascade.empty():
        print("錯誤: 嘴巴模型載入失敗")

    print("✓ 所有模型載入完成")
```

---

#### 需求 4：定義馬賽克處理函數
**說明**：建立一個可重複使用的馬賽克處理函數。

**程式碼提示**：
```python
def apply_mosaic(image, x, y, w, h, level=15):
    """
    對圖片的指定區域進行馬賽克處理

    參數:
        image: 輸入圖片（會直接修改）
        x, y: 區域左上角座標
        w, h: 區域寬度和高度
        level: 馬賽克程度（數值越小越模糊，建議 5-30）

    返回:
        無（直接修改 image）
    """
    # 確保座標在圖片範圍內
    x = max(0, x)
    y = max(0, y)
    w = min(w, image.shape[1] - x)
    h = min(h, image.shape[0] - y)

    # 擷取區域
    region = image[y:y+h, x:x+w]

    # 計算縮小後的尺寸（至少為 1）
    small_h = max(1, h // level)
    small_w = max(1, w // level)

    # 縮小圖片（產生模糊效果）
    region_small = cv2.resize(region, (small_w, small_h),
                              interpolation=cv2.INTER_LINEAR)

    # 放大回原尺寸（產生馬賽克效果）
    region_mosaic = cv2.resize(region_small, (w, h),
                               interpolation=cv2.INTER_NEAREST)

    # 將馬賽克區域放回原圖
    image[y:y+h, x:x+w] = region_mosaic

    return image

# 測試函數
print("✓ 馬賽克函數定義完成")
```

---

#### 需求 5：偵測人臉
**說明**：偵測圖片中的所有人臉。

**程式碼提示**：
```python
# 偵測人臉
faces = face_cascade.detectMultiScale(
    gray,
    scaleFactor=1.1,
    minNeighbors=5,
    minSize=(50, 50)
)

print(f"✓ 偵測到 {len(faces)} 張人臉")

# 若沒有偵測到人臉，顯示警告
if len(faces) == 0:
    print("⚠ 警告: 未偵測到人臉，請檢查圖片或調整參數")
```

---

#### 需求 6：在人臉區域內偵測五官並進行馬賽克處理
**說明**：針對每張人臉，偵測五官並根據模式進行處理。

**程式碼提示**：
```python
# 遍歷每張偵測到的人臉
for face_idx, (fx, fy, fw, fh) in enumerate(faces, start=1):
    print(f"\n處理人臉 {face_idx}:")

    # 擷取人臉區域（ROI: Region of Interest）
    face_roi_gray = gray[fy:fy+fh, fx:fx+fw]
    face_roi_color = img[fy:fy+fh, fx:fx+fw]

    # 選項 1: 處理眼睛
    if PRIVACY_MODE in ["eyes", "eyes_mouth"]:
        print("  偵測眼睛...")

        # 在人臉區域內偵測眼睛
        eyes = eye_cascade.detectMultiScale(
            face_roi_gray,
            scaleFactor=1.1,
            minNeighbors=10,  # 較高的值以減少誤判
            minSize=(20, 20)
        )

        print(f"  找到 {len(eyes)} 個眼睛區域")

        # 對每個眼睛區域進行馬賽克處理
        for (ex, ey, ew, eh) in eyes:
            # 重要：轉換為原圖的絕對座標
            abs_x = fx + ex
            abs_y = fy + ey

            # 進行馬賽克處理
            apply_mosaic(img, abs_x, abs_y, ew, eh, level=10)
            print(f"  ✓ 眼睛已馬賽克: ({abs_x}, {abs_y})")

    # 選項 2: 處理嘴巴
    if PRIVACY_MODE in ["mouth", "eyes_mouth"]:
        print("  偵測嘴巴...")

        # 在人臉區域的下半部偵測嘴巴（提高準確度）
        # 嘴巴通常位於人臉下半部
        mouth_roi_gray = face_roi_gray[fh//2:, :]

        mouths = mouth_cascade.detectMultiScale(
            mouth_roi_gray,
            scaleFactor=1.1,
            minNeighbors=20,  # 嘴巴偵測需要更高的閾值
            minSize=(30, 20)
        )

        print(f"  找到 {len(mouths)} 個嘴巴區域")

        # 對每個嘴巴區域進行馬賽克處理
        for (mx, my, mw, mh) in mouths:
            # 重要：轉換為原圖的絕對座標
            # 注意：my 需要加上 fh//2（因為是在下半部偵測）
            abs_x = fx + mx
            abs_y = fy + (fh//2) + my

            # 進行馬賽克處理
            apply_mosaic(img, abs_x, abs_y, mw, mh, level=12)
            print(f"  ✓ 嘴巴已馬賽克: ({abs_x}, {abs_y})")

    print(f"✓ 人臉 {face_idx} 處理完成")
```

**重要說明**：
- 五官偵測返回的座標是**相對於人臉 ROI** 的座標
- 需要加上人臉的 `(fx, fy)` 才能得到在原圖中的絕對座標
- 公式：`絕對座標 = 人臉座標 + ROI 內的相對座標`

---

#### 需求 7：顯示處理結果
**說明**：並排顯示原圖和處理後的圖片。

**程式碼提示**：
```python
# 顯示處理前後對比
print("\n" + "="*50)
print(f"隱私保護處理完成 (模式: {PRIVACY_MODE})")
print("="*50)

print("\n原始圖片：")
cv2_imshow(img_original)

print(f"\n處理後圖片 ({PRIVACY_MODE} 已馬賽克)：")
cv2_imshow(img)

# 可選：儲存結果
# output_filename = f'privacy_result_{PRIVACY_MODE}.jpg'
# cv2.imwrite(output_filename, img)
# print(f"\n✓ 結果已儲存為 {output_filename}")
```

---

### 📝 完整程式碼框架

```python
# ========== 題目三：智慧型隱私保護系統 ==========

import cv2
import numpy as np
from google.colab.patches import cv2_imshow

# 設定模式
PRIVACY_MODE = "eyes"  # "eyes", "mouth", "eyes_mouth"

# 讀取圖片
img = cv2.imread('girl.jpg')
img_original = img.copy()
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 載入模型
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
mouth_cascade = cv2.CascadeClassifier('haarcascade_mcs_mouth.xml')

# 定義馬賽克函數
def apply_mosaic(image, x, y, w, h, level=15):
    # TODO: 實作馬賽克處理
    pass

# 偵測人臉
faces = face_cascade.detectMultiScale(gray, 1.1, 5)

# 處理每張人臉
for (fx, fy, fw, fh) in faces:
    face_roi_gray = gray[fy:fy+fh, fx:fx+fw]

    # 根據模式處理五官
    if PRIVACY_MODE in ["eyes", "eyes_mouth"]:
        # TODO: 偵測並處理眼睛
        pass

    if PRIVACY_MODE in ["mouth", "eyes_mouth"]:
        # TODO: 偵測並處理嘴巴
        pass

# 顯示結果
cv2_imshow(img_original)
cv2_imshow(img)
```

---

### 🎯 測試建議

1. **測試不同模式**：
   ```python
   PRIVACY_MODE = "eyes"        # 只模糊眼睛
   PRIVACY_MODE = "mouth"       # 只模糊嘴巴
   PRIVACY_MODE = "eyes_mouth"  # 模糊眼睛和嘴巴
   ```

2. **調整馬賽克程度**：
   ```python
   apply_mosaic(img, x, y, w, h, level=10)  # 粗糙馬賽克
   apply_mosaic(img, x, y, w, h, level=20)  # 細緻馬賽克
   ```

3. **調整偵測參數**：
   - 若眼睛偵測過多：提高 `minNeighbors` 到 15-20
   - 若嘴巴偵測不到：降低 `minNeighbors` 到 10-15

---

### 🚀 延伸挑戰（選做）

#### 挑戰 1：加入使用者互動
```python
# 讓使用者選擇模式
print("請選擇隱私保護模式：")
print("1. 只模糊眼睛")
print("2. 只模糊嘴巴")
print("3. 模糊眼睛和嘴巴")

choice = input("請輸入選項 (1/2/3): ")

mode_map = {
    "1": "eyes",
    "2": "mouth",
    "3": "eyes_mouth"
}

PRIVACY_MODE = mode_map.get(choice, "eyes")
print(f"已選擇模式: {PRIVACY_MODE}")
```

#### 挑戰 2：支援高斯模糊效果
```python
def apply_blur(image, x, y, w, h, blur_level=21):
    """使用高斯模糊代替馬賽克"""
    region = image[y:y+h, x:x+w]

    # 確保 blur_level 為奇數
    if blur_level % 2 == 0:
        blur_level += 1

    # 套用高斯模糊
    blurred = cv2.GaussianBlur(region, (blur_level, blur_level), 0)
    image[y:y+h, x:x+w] = blurred

    return image
```

#### 挑戰 3：統計處理資訊
```python
# 在處理過程中統計
processed_count = {
    'eyes': 0,
    'mouths': 0
}

# 在處理眼睛時
for (ex, ey, ew, eh) in eyes:
    apply_mosaic(img, fx+ex, fy+ey, ew, eh)
    processed_count['eyes'] += 1

# 最後顯示統計
print(f"\n處理統計：")
print(f"  已保護 {processed_count['eyes']} 個眼睛")
print(f"  已保護 {processed_count['mouths']} 個嘴巴")
```

---

## 作業繳交建議

### 📄 程式碼規範

1. **檔案命名**：
   - 題目一：`task1_face_counter.py` 或 `task1_face_counter.ipynb`
   - 題目二：`task2_color_tracker.py` 或 `task2_color_tracker.ipynb`
   - 題目三：`task3_privacy_protector.py` 或 `task3_privacy_protector.ipynb`

2. **程式碼結構**：
```python
# ========================================
# 題目 X: XXXX
# 學生姓名: XXX
# 學號: XXXXXXXX
# 日期: YYYY-MM-DD
# ========================================

# 1. 匯入必要套件
import cv2
import numpy as np
from google.colab.patches import cv2_imshow

# 2. 設定參數
# ...

# 3. 主要功能實作
# ...

# 4. 執行與顯示結果
# ...

# 5. 測試報告
"""
【測試報告】
測試環境: Google Colab
測試圖片: girl.jpg
參數設定: scaleFactor=1.1, minNeighbors=5
執行結果: 成功偵測到 1 張人臉
心得反思: ...
"""
```

3. **註解撰寫**：
```python
# 好的註解範例
faces = face_cascade.detectMultiScale(gray, 1.1, 5)  # 偵測人臉，使用預設參數

# 不好的註解範例
faces = face_cascade.detectMultiScale(gray, 1.1, 5)  # 執行 detectMultiScale
```

---

### ✅ 檢查清單

提交作業前，請確認：

- [ ] 程式能夠正常執行，無錯誤
- [ ] 所有必要功能都已實作
- [ ] 程式碼有適當的註解
- [ ] 變數命名清楚易懂
- [ ] 有基本的錯誤處理（如檢查圖片是否讀取成功）
- [ ] 有輸出處理過程的訊息
- [ ] 附上測試報告
- [ ] （選做）完成至少一項延伸挑戰

---

### 📊 測試報告範本

```markdown
# OpenCV 影像辨識作業測試報告

## 學生資訊
- 姓名：XXX
- 學號：XXXXXXXX
- 日期：2025-XX-XX

---

## 題目一：人臉計數與框選應用

### 測試環境
- 平台：Google Colab
- Python 版本：3.10.x
- OpenCV 版本：4.8.0

### 測試圖片
1. girl.jpg（教學範例圖片）
2. 自行準備的全家福照片

### 參數設定
```python
scaleFactor = 1.1
minNeighbors = 5
minSize = (30, 30)
```

### 執行結果
| 測試圖片 | 偵測數量 | 備註 |
|---------|---------|------|
| girl.jpg | 1 張人臉 | 正確偵測 |
| 全家福 | 4 張人臉 | 有 1 張側臉未偵測 |

### 心得反思
1. **什麼情況下偵測效果較好？**
   - 正面照的偵測效果最佳
   - 光線充足、人臉清晰的照片準確度高

2. **參數調整的影響**
   - 降低 `minNeighbors` 可以偵測到更多人臉，但也增加誤判機率
   - 調整 `scaleFactor` 到 1.05 後，成功偵測到原本漏掉的側臉

3. **遇到的困難與解決方法**
   - 問題：文字標籤超出圖片範圍
   - 解決：加入座標檢查，若 y-10 < 0 則將文字放在矩形框下方

### 延伸挑戰完成情況
- [x] 使用不同顏色標示不同人臉
- [x] 顯示人臉大小資訊
- [ ] 顯示總人數統計（未完成）

---

## 題目二：彩色物體定位器

### 測試環境
（同上）

### 測試圖片
自行建立的測試圖片（包含紅、藍、綠、黃色物體）

### 參數設定
```python
顏色範圍：紅色、藍色、綠色、黃色
輪廓面積閾值：100 像素
```

### 執行結果
| 顏色 | 偵測數量 | 備註 |
|------|---------|------|
| 紅色 | 2 個 | 正確 |
| 藍色 | 1 個 | 正確 |
| 綠色 | 1 個 | 正確 |
| 黃色 | 1 個 | 正確 |

### 心得反思
（填寫你的心得）

---

## 題目三：智慧型隱私保護系統

### 測試環境
（同上）

### 測試模式
- [x] 只模糊眼睛
- [x] 只模糊嘴巴
- [x] 模糊眼睛和嘴巴

### 參數設定
```python
PRIVACY_MODE = "eyes_mouth"
馬賽克 level = 15
眼睛偵測 minNeighbors = 10
嘴巴偵測 minNeighbors = 20
```

### 執行結果
- 成功偵測到 1 張人臉
- 成功偵測到 2 個眼睛區域
- 成功偵測到 1 個嘴巴區域
- 馬賽克效果正常

### 心得反思
（填寫你的心得）

---

## 總結

### 學習收穫
1. 學會使用 Haar Cascade 進行物體偵測
2. 理解 HSV 色彩空間在顏色追蹤的應用
3. 掌握座標轉換的概念（ROI 相對座標 → 絕對座標）
4. 學會參數調整對偵測結果的影響

### 未來改進方向
1. 嘗試使用深度學習模型提高準確度
2. 優化程式執行效率
3. 加入更多使用者互動功能

---
```

---

## 學習資源

### 📚 參考文件

1. **主要教學文件**：`opencv_imageclassfy_b05.md`
2. **OpenCV 官方文件**：
   - [Haar Cascade 教學](https://docs.opencv.org/4.x/db/d28/tutorial_cascade_classifier.html)
   - [輪廓偵測教學](https://docs.opencv.org/4.x/d4/d73/tutorial_py_contours_begin.html)
3. **Python 基礎**：
   - [enumerate() 用法](https://docs.python.org/3/library/functions.html#enumerate)
   - [字典 (dict) 操作](https://docs.python.org/3/tutorial/datastructures.html#dictionaries)

---

### 🔧 除錯技巧

#### 問題 1：圖片無法讀取
```python
# 除錯程式碼
img = cv2.imread('test.jpg')
if img is None:
    print("錯誤: 無法讀取圖片")
    print("請檢查：")
    print("1. 檔案是否存在於當前目錄")
    print("2. 檔案名稱是否正確（區分大小寫）")
    print("3. 在 Colab 中，檔案是否已上傳")

    # 列出當前目錄的檔案
    import os
    print("當前目錄的檔案：", os.listdir('.'))
```

#### 問題 2：模型載入失敗
```python
# 檢查模型檔案
cascade = cv2.CascadeClassifier('model.xml')
if cascade.empty():
    print("錯誤: 模型載入失敗")
    print("請確認 model.xml 是否已下載")

    # 嘗試重新下載
    import urllib.request
    url = "https://raw.githubusercontent.com/..."
    urllib.request.urlretrieve(url, 'model.xml')
    print("已重新下載模型")
```

#### 問題 3：座標超出範圍
```python
# 安全的座標擷取
def safe_crop(image, x, y, w, h):
    """安全地擷取圖片區域，自動處理超出範圍的情況"""
    height, width = image.shape[:2]

    # 限制座標範圍
    x = max(0, min(x, width))
    y = max(0, min(y, height))
    w = max(0, min(w, width - x))
    h = max(0, min(h, height - y))

    return image[y:y+h, x:x+w]
```

#### 問題 4：偵測效果不理想
```python
# 參數調校輔助工具
def test_parameters(image_path):
    """測試不同參數組合"""
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    # 測試不同參數組合
    test_cases = [
        (1.1, 3),
        (1.1, 5),
        (1.1, 8),
        (1.05, 5),
        (1.3, 5)
    ]

    for scale, neighbors in test_cases:
        faces = cascade.detectMultiScale(gray, scale, neighbors)
        print(f"scaleFactor={scale}, minNeighbors={neighbors}: {len(faces)} 張人臉")
```

---

### 💡 常見問題 FAQ

#### Q1: `cv2.putText()` 的字體太小或太大怎麼辦？

**A:** 調整 `fontScale` 參數：
```python
cv2.putText(img, "文字", (x, y), cv2.FONT_HERSHEY_SIMPLEX,
            0.5,  # 小字體
            (0, 255, 0), 2)

cv2.putText(img, "文字", (x, y), cv2.FONT_HERSHEY_SIMPLEX,
            1.5,  # 大字體
            (0, 255, 0), 2)
```

#### Q2: 如何在 Colab 中上傳自己的圖片？

**A:** 使用以下程式碼：
```python
from google.colab import files

# 上傳檔案
uploaded = files.upload()

# 列出上傳的檔案
for filename in uploaded.keys():
    print(f"已上傳: {filename}")
```

#### Q3: 為什麼紅色物體總是偵測不到？

**A:** 紅色在 HSV 色環中橫跨兩端，需要使用兩個範圍：
```python
# 紅色需要兩個範圍
lower_red1 = np.array([0, 40, 40])
upper_red1 = np.array([10, 255, 255])

lower_red2 = np.array([170, 40, 40])
upper_red2 = np.array([180, 255, 255])

# 建立兩個遮罩並合併
mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
mask = cv2.bitwise_or(mask1, mask2)
```

#### Q4: 如何加快程式執行速度？

**A:** 幾個優化技巧：
```python
# 1. 縮小圖片尺寸
img = cv2.imread('test.jpg')
img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)  # 縮小 50%

# 2. 提高 scaleFactor
faces = cascade.detectMultiScale(gray, 1.3, 5)  # 較快但較不精確

# 3. 限制偵測區域
# 只在圖片中央區域偵測
h, w = gray.shape
roi = gray[h//4:3*h//4, w//4:3*w//4]
```

#### Q5: `enumerate()` 是什麼？怎麼用？

**A:** `enumerate()` 可以同時取得元素和索引：
```python
# 傳統方式
for i in range(len(faces)):
    x, y, w, h = faces[i]
    print(f"人臉 {i+1}: ({x}, {y})")

# 使用 enumerate（更簡潔）
for i, (x, y, w, h) in enumerate(faces, start=1):
    print(f"人臉 {i}: ({x}, {y})")
```

---

## 評分標準參考

| 項目 | 題目一 | 題目二 | 題目三 | 評分重點 |
|------|-------|-------|-------|---------|
| **功能完整性 (40%)** | 16分 | 12分 | 12分 | 所有必要功能都已實作並正常運作 |
| **程式碼品質 (25%)** | 10分 | 7分 | 8分 | 結構清晰、註解完整、命名規範 |
| **執行結果 (20%)** | 8分 | 6分 | 6分 | 能正確執行並產生預期結果 |
| **測試報告 (10%)** | 4分 | 3分 | 3分 | 完整記錄測試過程與心得反思 |
| **延伸挑戰 (5%)** | 2分 | 2分 | 1分 | 額外功能實作（加分項） |

### 詳細評分準則

#### 功能完整性 (40%)
- ✅ **優秀 (90-100%)**：所有功能完整實作，執行無誤，有額外優化
- ✅ **良好 (75-89%)**：所有必要功能都已實作，執行正常
- ⚠️ **及格 (60-74%)**：大部分功能已實作，有少數功能缺漏或錯誤
- ❌ **不及格 (<60%)**：許多功能未實作或無法正常執行

#### 程式碼品質 (25%)
- ✅ **優秀**：結構清晰、註解完整、變數命名有意義、有錯誤處理
- ✅ **良好**：結構合理、有基本註解、變數命名尚可
- ⚠️ **及格**：程式可執行但結構較亂、註解不足
- ❌ **不及格**：程式結構混亂、完全沒有註解、變數命名不當

#### 執行結果 (20%)
- ✅ **優秀**：完全符合需求，結果正確且有良好的輸出格式
- ✅ **良好**：符合基本需求，結果正確
- ⚠️ **及格**：部分符合需求，有少數錯誤
- ❌ **不及格**：無法執行或結果錯誤

#### 測試報告 (10%)
- ✅ **優秀**：報告完整、分析深入、有具體的反思與改進建議
- ✅ **良好**：報告完整、有基本的測試記錄與心得
- ⚠️ **及格**：有簡單的測試記錄
- ❌ **不及格**：無測試報告或極度簡略

---

## 進階學習方向

完成這三個題目後，你可以嘗試以下進階主題：

### 🎥 影片處理
```python
# 將程式應用於影片
cap = cv2.VideoCapture('test.mp4')

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # 在此加入你的偵測程式碼
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    cv2_imshow(frame)

cap.release()
```

### 🤖 深度學習方法
- YOLO (You Only Look Once)
- SSD (Single Shot MultiBox Detector)
- Faster R-CNN
- RetinaFace

### 🎭 人臉辨識
- LBPH Face Recognizer
- FaceNet
- ArcFace

### 📱 嵌入式部署
- 樹莓派 (Raspberry Pi)
- NVIDIA Jetson Nano
- 手機應用 (Android/iOS)

---

**祝學習順利！有任何問題歡迎參考教學文件或尋求協助。**

**記得善用程式碼提示範例，一步步完成你的專案！** 🚀
