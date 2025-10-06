<!-- Path: General_python/openCV/影像辨識-傳統方法 | Timestamp: 2025-10-06 16:00:00 | Version: b01 -->
# 題目一：人臉計數與框選應用

## 📋 任務說明

請撰寫一個 Python 程式，能夠自動偵測照片中的人臉數量，並在每張人臉上方顯示編號標籤（例如：「人臉 1」、「人臉 2」...）。

---

## 🖼️ 影像選擇指引

### 適合的影像類型

#### ✅ 推薦使用的影像
1. **正面人臉照片**
   - 特徵：臉部完整朝向鏡頭，五官清晰可見
   - 範例：證件照、自拍照、團體照
   - 偵測成功率：★★★★★（95%+）

2. **光線充足的照片**
   - 特徵：明亮均勻的光線，無強烈陰影
   - 拍攝環境：白天室內、戶外陰影處、柔和燈光下
   - 偵測成功率：★★★★★（90%+）

3. **中近距離拍攝**
   - 特徵：人臉在畫面中佔比適中（至少 50×50 像素）
   - 距離：1-3 公尺內拍攝
   - 偵測成功率：★★★★☆（85%+）

4. **單一或多人清晰照片**
   - 特徵：每張臉都清晰、不重疊
   - 範例：全家福、畢業照、會議合照
   - 偵測成功率：★★★★☆（80%+）

#### ⚠️ 效果較差的影像
1. **側臉或低頭照片**
   - 問題：Haar Cascade 主要訓練於正面人臉
   - 偵測成功率：★★☆☆☆（30-50%）
   - 改善方法：使用深度學習模型（如 MTCNN）

2. **逆光或過暗照片**
   - 問題：臉部特徵不清晰
   - 偵測成功率：★★☆☆☆（40-60%）
   - 改善方法：調整圖片亮度或對比度

3. **人臉過小的照片**
   - 問題：人臉像素少於 30×30
   - 偵測成功率：★☆☆☆☆（10-30%）
   - 改善方法：降低 `minSize` 參數或裁切放大

4. **模糊或動態照片**
   - 問題：五官輪廓不清晰
   - 偵測成功率：★★☆☆☆（30-50%）
   - 改善方法：使用清晰的靜態照片

#### ❌ 不適合的影像
- 純側面照（臉部角度 > 45°）
- 戴口罩、墨鏡等大面積遮擋
- 卡通或繪畫人臉（非真實人臉）
- 極端光線（全黑、強光過曝）

### 測試影像建議

#### 初學者測試（難度：★☆☆☆☆）
```
建議影像：
- girl.jpg（教學範例）
- mona.jpg（蒙娜麗莎）
- 自己的證件照或自拍照

特點：單人、正面、光線良好
預期結果：100% 偵測成功
```

#### 中級測試（難度：★★★☆☆）
```
建議影像：
- 2-4 人的團體照
- 全家福照片
- 朋友聚會照片

特點：多人、正面為主、部分側臉
預期結果：80-90% 偵測成功
```

#### 進階測試（難度：★★★★☆）
```
建議影像：
- 大型團體照（10 人以上）
- 包含不同角度的人臉
- 有部分遮擋或光線不均

特點：複雜場景、多種角度
預期結果：60-80% 偵測成功
```

### 影像準備檢查清單

在測試前，請確認你的影像：
- [ ] 格式為 JPG、PNG 等常見圖片格式
- [ ] 解析度至少 640×480（建議 1024×768 以上）
- [ ] 檔案大小不超過 5MB（避免記憶體問題）
- [ ] 人臉清晰可見，無嚴重模糊
- [ ] 光線適中，非極端明暗
- [ ] 人臉大小至少 50×50 像素

---

## ✅ 詳細需求列表

### 需求 1：環境準備與檔案下載

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

print("\n所有檔案準備完成！")
```

---

### 需求 2：匯入必要套件

**說明**：匯入 OpenCV、NumPy 和 Colab 顯示工具。

**程式碼提示**：
```python
# 匯入必要的套件
import cv2
import numpy as np
from google.colab.patches import cv2_imshow

print("✓ 套件匯入完成")
```

---

### 需求 3：讀取並檢查圖片

**說明**：讀取圖片檔案，並檢查是否成功讀取。

**程式碼提示**：
```python
# 讀取圖片
img = cv2.imread('girl.jpg')  # 或使用其他包含人臉的圖片

# 檢查圖片是否成功讀取
if img is None:
    print("錯誤: 無法讀取圖片，請確認檔案已正確下載")
    print("請檢查：")
    print("1. 檔案是否存在於當前目錄")
    print("2. 檔案名稱是否正確")
else:
    print("✓ 圖片讀取成功")
    # 顯示圖片尺寸
    height, width, channels = img.shape
    print(f"圖片尺寸: {width} x {height} 像素")
    print(f"色彩通道: {channels}")
```

---

### 需求 4：轉換為灰階影像

**說明**：將彩色圖片轉換為灰階，以提高偵測效率。

**程式碼提示**：
```python
# 將圖片轉換為灰階
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
print("✓ 圖片已轉換為灰階")
```

---

### 需求 5：載入 Haar Cascade 人臉偵測模型

**說明**：載入預訓練的人臉偵測模型。

**程式碼提示**：
```python
# 載入人臉偵測模型
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# 檢查模型是否成功載入
if face_cascade.empty():
    print("錯誤: 無法載入人臉偵測模型")
    print("請確認 haarcascade_frontalface_default.xml 檔案存在")
else:
    print("✓ 人臉偵測模型載入成功")
```

---

### 需求 6：執行人臉偵測

**說明**：使用 `detectMultiScale()` 方法偵測圖片中的所有人臉。

**程式碼提示**：
```python
# 偵測人臉
# scaleFactor: 影像縮放比例，1.1 表示每次縮小 10%
# minNeighbors: 構成有效偵測所需的最少鄰居數量
# minSize: 最小人臉尺寸
faces = face_cascade.detectMultiScale(
    gray,                # 輸入的灰階圖片
    scaleFactor=1.1,     # 建議值：1.05-1.3
    minNeighbors=5,      # 建議值：3-8
    minSize=(30, 30)     # 最小人臉尺寸，避免偵測過小的區域
)

# 顯示偵測結果
print(f"✓ 偵測完成")
print(f"找到 {len(faces)} 張人臉")

# 若沒有偵測到人臉
if len(faces) == 0:
    print("\n⚠️ 未偵測到人臉，可能原因：")
    print("1. 圖片中沒有正面人臉")
    print("2. 人臉過小或過大")
    print("3. 光線條件不佳")
    print("4. 建議調整 scaleFactor 或 minNeighbors 參數")
```

---

### 需求 7：在每張人臉上繪製矩形框與編號

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

    # 計算文字位置（矩形框上方）
    text_x = x
    text_y = y - 10 if y - 10 > 10 else y + h + 20  # 避免超出圖片範圍

    # 繪製文字
    cv2.putText(
        img,                              # 目標圖片
        label,                            # 文字內容
        (text_x, text_y),                # 文字位置（左下角）
        cv2.FONT_HERSHEY_SIMPLEX,        # 字體類型
        0.9,                              # 字體大小
        (0, 255, 0),                      # 文字顏色（綠色）
        2                                 # 文字粗細
    )

    # 輸出每張人臉的座標資訊
    print(f"人臉 {i}: 位置({x}, {y}), 大小({w}x{h})")
```

---

### 需求 8：統計並顯示總人數

**說明**：在終端機輸出總人數，並在圖片左上角顯示統計資訊。

**程式碼提示**：
```python
# 在終端機輸出總人數
total_faces = len(faces)
print(f"\n{'='*40}")
print(f"偵測結果統計")
print(f"{'='*40}")
print(f"總共偵測到 {total_faces} 張人臉")
print(f"{'='*40}\n")

# 可選：在圖片左上角顯示總人數
summary_text = f"Total: {total_faces} face(s)"
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

### 需求 9：顯示處理後的結果

**說明**：使用 `cv2_imshow()` 顯示標記後的圖片。

**程式碼提示**：
```python
# 顯示處理後的圖片
print("處理後的圖片：")
cv2_imshow(img)

# 可選：儲存結果圖片
output_filename = 'result_face_count.jpg'
cv2.imwrite(output_filename, img)
print(f"\n✓ 結果已儲存為 {output_filename}")
```

---

## 📝 完整可執行程式碼

```python
# ========================================
# 題目一：人臉計數與框選應用
# ========================================

import cv2
import numpy as np
from google.colab.patches import cv2_imshow

# 1. 讀取圖片
img = cv2.imread('girl.jpg')

if img is None:
    print("錯誤: 無法讀取圖片")
else:
    print("✓ 圖片讀取成功")
    height, width, channels = img.shape
    print(f"圖片尺寸: {width} x {height} 像素")

    # 2. 轉換為灰階
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    print("✓ 圖片已轉換為灰階")

    # 3. 載入人臉偵測模型
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    if face_cascade.empty():
        print("錯誤: 無法載入人臉偵測模型")
    else:
        print("✓ 人臉偵測模型載入成功")

        # 4. 偵測人臉
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )

        print(f"✓ 偵測完成，找到 {len(faces)} 張人臉")

        # 5. 繪製矩形框與編號
        for i, (x, y, w, h) in enumerate(faces, start=1):
            # 繪製矩形框
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

            # 準備標籤
            label = f"人臉 {i}"

            # 計算文字位置
            text_x = x
            text_y = y - 10 if y - 10 > 10 else y + h + 20

            # 繪製文字
            cv2.putText(
                img,
                label,
                (text_x, text_y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (0, 255, 0),
                2
            )

            print(f"人臉 {i}: 位置({x}, {y}), 大小({w}x{h})")

        # 6. 顯示總人數統計
        total_faces = len(faces)
        print(f"\n{'='*40}")
        print(f"總共偵測到 {total_faces} 張人臉")
        print(f"{'='*40}\n")

        # 在圖片上顯示統計
        summary_text = f"Total: {total_faces} face(s)"
        cv2.putText(
            img,
            summary_text,
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.0,
            (255, 0, 0),
            2
        )

        # 7. 顯示結果
        print("處理後的圖片：")
        cv2_imshow(img)

        # 儲存結果
        cv2.imwrite('result_face_count.jpg', img)
        print("\n✓ 結果已儲存為 result_face_count.jpg")
```

---

## 🎯 測試建議

### 基本測試流程

1. **單人照片測試**
   ```python
   img = cv2.imread('girl.jpg')  # 使用教學範例
   ```
   - 預期結果：偵測到 1 張人臉
   - 檢查：框線是否準確、標籤是否顯示

2. **多人照片測試**
   ```python
   # 上傳你自己的團體照
   from google.colab import files
   uploaded = files.upload()
   img = cv2.imread('your_photo.jpg')
   ```
   - 預期結果：偵測到大部分正面人臉
   - 檢查：是否有漏偵測或誤判

### 參數調整實驗

**實驗 1：調整 scaleFactor**
```python
# 測試不同的 scaleFactor 值
scale_factors = [1.05, 1.1, 1.2, 1.3]

for sf in scale_factors:
    faces = face_cascade.detectMultiScale(gray, scaleFactor=sf, minNeighbors=5)
    print(f"scaleFactor={sf}: 偵測到 {len(faces)} 張人臉")
```

**實驗 2：調整 minNeighbors**
```python
# 測試不同的 minNeighbors 值
min_neighbors = [3, 5, 7, 10]

for mn in min_neighbors:
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=mn)
    print(f"minNeighbors={mn}: 偵測到 {len(faces)} 張人臉")
```

### 效果評估

記錄測試結果：
- 使用圖片：__________
- 實際人臉數量：__________
- 偵測到的數量：__________
- 準確率：__________ %
- 最佳參數組合：scaleFactor=______, minNeighbors=______

---

## 🚀 延伸挑戰（選做）

### 挑戰 1：使用不同顏色標示不同人臉

```python
# 定義顏色列表（BGR 格式）
colors = [
    (0, 255, 0),    # 綠色
    (255, 0, 0),    # 藍色
    (0, 0, 255),    # 紅色
    (255, 255, 0),  # 青色
    (255, 0, 255),  # 洋紅色
    (0, 255, 255),  # 黃色
]

for i, (x, y, w, h) in enumerate(faces):
    # 循環使用顏色
    color = colors[i % len(colors)]

    # 繪製彩色框線
    cv2.rectangle(img, (x, y), (x+w, y+h), color, 2)

    # 使用相同顏色繪製文字
    label = f"人臉 {i+1}"
    cv2.putText(img, label, (x, y-10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
```

### 挑戰 2：顯示人臉大小資訊

```python
for i, (x, y, w, h) in enumerate(faces, start=1):
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # 計算面積
    area = w * h
    label = f"Face {i}: {w}x{h} ({area}px)"

    cv2.putText(img, label, (x, y-10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
```

### 挑戰 3：標示最大和最小的人臉

```python
if len(faces) > 0:
    # 計算每張人臉的面積
    face_areas = [(i, x, y, w, h, w*h) for i, (x, y, w, h) in enumerate(faces, start=1)]

    # 找出最大和最小
    largest = max(face_areas, key=lambda x: x[5])
    smallest = min(face_areas, key=lambda x: x[5])

    # 標示最大人臉
    i, x, y, w, h, area = largest
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 3)  # 紅色粗框
    cv2.putText(img, "LARGEST", (x, y-30),
                cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2)

    # 標示最小人臉
    i, x, y, w, h, area = smallest
    cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 3)  # 藍色粗框
    cv2.putText(img, "SMALLEST", (x, y-30),
                cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 0), 2)
```

---

## 🔧 除錯技巧

### 問題 1：無法讀取圖片

**症狀**：`img is None` 錯誤

**解決方法**：
```python
import os

# 檢查檔案是否存在
if os.path.exists('girl.jpg'):
    print("✓ 檔案存在")
else:
    print("✗ 檔案不存在")
    # 列出當前目錄的所有檔案
    print("當前目錄的檔案：")
    for f in os.listdir('.'):
        print(f"  - {f}")
```

### 問題 2：模型載入失敗

**症狀**：`face_cascade.empty()` 返回 `True`

**解決方法**：
```python
import os

# 檢查模型檔案
model_file = 'haarcascade_frontalface_default.xml'

if not os.path.exists(model_file):
    print(f"模型檔案不存在，正在下載...")
    import urllib.request
    url = 'https://raw.githubusercontent.com/opencv/opencv/4.x/data/haarcascades/haarcascade_frontalface_default.xml'
    urllib.request.urlretrieve(url, model_file)
    print("✓ 下載完成")
```

### 問題 3：偵測不到人臉

**診斷工具**：
```python
# 顯示灰階圖片，檢查品質
print("灰階圖片：")
cv2_imshow(gray)

# 嘗試不同參數組合
param_combinations = [
    (1.05, 3),
    (1.1, 3),
    (1.1, 5),
    (1.2, 5),
]

print("\n參數測試：")
for sf, mn in param_combinations:
    faces = face_cascade.detectMultiScale(gray, scaleFactor=sf, minNeighbors=mn)
    print(f"scaleFactor={sf}, minNeighbors={mn}: {len(faces)} 張人臉")
```

### 問題 4：中文標籤顯示為亂碼或方框

**原因**：OpenCV 預設不支援中文字體

**解決方法**：
```python
# 方法 1：使用英文標籤
label = f"Face {i}"  # 不使用中文

# 方法 2：使用 PIL 繪製中文（進階）
from PIL import Image, ImageDraw, ImageFont

# 將 OpenCV 圖片轉為 PIL 格式
pil_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
draw = ImageDraw.Draw(pil_img)

# 載入中文字體（需要上傳字體檔）
# font = ImageFont.truetype("NotoSansTC-Regular.ttf", 30)
# draw.text((x, y-40), f"人臉 {i}", font=font, fill=(0, 255, 0))

# 轉回 OpenCV 格式
img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
```

---

## 💡 常見問題 FAQ

### Q1: 為什麼偵測到的人臉數量不正確？

**A:** 可能原因：
1. **人臉角度問題**：Haar Cascade 對正面臉效果最好
2. **光線問題**：太暗或過曝會影響偵測
3. **人臉大小**：過小（< 30×30px）會被忽略
4. **參數設定**：`minNeighbors` 過高會漏掉真實人臉

**建議調整**：
- 降低 `scaleFactor`：1.1 → 1.05
- 降低 `minNeighbors`：5 → 3
- 降低 `minSize`：(30,30) → (20,20)

### Q2: 如何上傳自己的照片到 Colab？

**A:** 使用以下程式碼：
```python
from google.colab import files

# 上傳檔案
print("請選擇要上傳的圖片：")
uploaded = files.upload()

# 列出上傳的檔案
for filename in uploaded.keys():
    print(f"已上傳: {filename}")

# 讀取上傳的圖片
img = cv2.imread(filename)
```

### Q3: 可以一次處理多張圖片嗎？

**A:** 可以，使用迴圈處理：
```python
# 圖片列表
image_files = ['photo1.jpg', 'photo2.jpg', 'photo3.jpg']

for img_file in image_files:
    print(f"\n處理圖片: {img_file}")
    img = cv2.imread(img_file)

    if img is None:
        print(f"  無法讀取 {img_file}")
        continue

    # 執行偵測（與原程式碼相同）
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)

    print(f"  偵測到 {len(faces)} 張人臉")

    # 繪製結果並儲存
    for i, (x, y, w, h) in enumerate(faces, start=1):
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

    output_file = f"result_{img_file}"
    cv2.imwrite(output_file, img)
    print(f"  結果已儲存為 {output_file}")
```

### Q4: 如何提高偵測準確率？

**A:** 實用技巧：
1. **影像預處理**：
   ```python
   # 調整對比度和亮度
   img = cv2.convertScaleAbs(img, alpha=1.2, beta=20)

   # 去除雜訊
   img = cv2.GaussianBlur(img, (5, 5), 0)
   ```

2. **多尺度偵測**：
   ```python
   # 使用更小的 scaleFactor
   faces = face_cascade.detectMultiScale(
       gray,
       scaleFactor=1.05,  # 更精細的掃描
       minNeighbors=3,
       minSize=(20, 20)
   )
   ```

3. **後處理過濾**：
   ```python
   # 過濾面積過小的偵測框
   valid_faces = []
   for (x, y, w, h) in faces:
       area = w * h
       if area > 1000:  # 只保留面積 > 1000 的人臉
           valid_faces.append((x, y, w, h))
   ```

### Q5: 程式執行很慢怎麼辦？

**A:** 優化技巧：
1. **縮小圖片**：
   ```python
   # 縮小到原來的 50%
   img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)
   ```

2. **提高 scaleFactor**：
   ```python
   # 使用較大的 scaleFactor 加快速度
   faces = face_cascade.detectMultiScale(gray, 1.3, 5)
   ```

3. **限制偵測區域**（如果知道人臉大概位置）：
   ```python
   # 只偵測圖片中央區域
   h, w = gray.shape
   roi = gray[h//4:3*h//4, w//4:3*w//4]
   faces = face_cascade.detectMultiScale(roi, 1.1, 5)

   # 記得將座標轉換回原圖
   for (x, y, w, h) in faces:
       actual_x = x + w//4
       actual_y = y + h//4
       # ...
   ```

---

## 📊 評分標準

| 項目 | 配分 | 評分重點 |
|------|------|----------|
| **功能完整性** | 40% | 所有 9 個需求都已實作並正常運作 |
| **程式碼品質** | 25% | 結構清晰、註解完整、變數命名規範 |
| **執行結果** | 20% | 能正確偵測人臉並顯示編號 |
| **測試報告** | 10% | 完整記錄測試過程與心得反思 |
| **延伸挑戰** | 5% | 完成至少一項延伸挑戰（加分項） |

---

## 📚 學習資源

### 參考文件
- 主要教學：`opencv_imageclassfy_b05.md`
- OpenCV 官方：[Cascade Classifier Tutorial](https://docs.opencv.org/4.x/db/d28/tutorial_cascade_classifier.html)

### 相關函數說明
- `cv2.imread()`：讀取圖片
- `cv2.cvtColor()`：轉換色彩空間
- `cv2.CascadeClassifier()`：載入分類器
- `detectMultiScale()`：多尺度偵測
- `cv2.rectangle()`：繪製矩形
- `cv2.putText()`：繪製文字

---

**祝學習順利！完成後記得測試不同的影像，觀察參數對結果的影響。** 🎓
