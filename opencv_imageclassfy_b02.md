<!-- Path: General_python/openCV/影像辨識-傳統方法 | Timestamp: 2025-09-29 12:20:00 | Version: b02 -->
# OpenCV 影像辨識學習總彙

本篇教學統整了多個 OpenCV 影像辨識的應用，並將所有範例程式碼修改為可直接在 Google Colab 環境中執行。每個章節都增加了更詳細的程式邏輯解說，幫助你更深入地理解背後的原理。

## 1. Google Colab 環境設定

在 Colab 中，我們無法直接存取本機檔案或開啟攝影機。因此，我們需要先下載所需的模型檔案和範例圖片，並使用 `google.colab.patches` 中的 `cv2_imshow` 來顯示圖片。

請在 Colab 的程式碼儲存格中執行以下指令來下載所有必要的檔案：

```python
# 下載所有需要的模型和圖片
# 這些 .xml 檔案是 OpenCV 提供的預訓練 Haar Cascade 模型，用於物件偵測。
# Haar Cascade 是一種基於機器學習的物件偵測方法，它透過大量的正負樣本訓練，學習到特定物件（如人臉、眼睛）的特徵。
!wget https://raw.githubusercontent.com/opencv/opencv/4.x/data/haarcascades/haarcascade_frontalface_default.xml
!wget https://raw.githubusercontent.com/opencv/opencv/4.x/data/haarcascades/haarcascade_eye.xml
!wget https://raw.githubusercontent.com/atduskgreg/opencv-processing/master/lib/cascade-files/haarcascade_mcs_mouth.xml
!wget https://raw.githubusercontent.com/atduskgreg/opencv-processing/master/lib/cascade-files/haarcascade_mcs_nose.xml
!wget https://raw.githubusercontent.com/opencv/opencv/4.x/data/haarcascades/haarcascade_fullbody.xml
!wget https://raw.githubusercontent.com/andrewssobral/vehicle_detection_haarcascades/master/cars.xml

# 下載範例圖片
!wget https://steam.oxxostudio.tw/down/python/ai/mona.jpg
!wget https://steam.oxxostudio.tw/down/python/ai/cars.jpg
!wget https://steam.oxxostudio.tw/down/python/ai/girl.jpg
```

---

## 2. 追蹤並標記特定顏色

我們可以透過設定顏色的 HSV 範圍來追蹤畫面中的特定顏色。

### 處理邏輯說明

1.  **色彩空間轉換 (BGR to HSV)**: 相比於電腦螢幕使用的 BGR (藍綠紅) 色彩模型，HSV (色相、飽和度、亮度) 更符合人類對顏色的感知。在 HSV 模型中，顏色 (色相 Hue) 是獨立於飽和度 (Saturation) 和亮度 (Value) 的，這使得在不同光照條件下辨識特定顏色變得更加穩定和準確。
2.  **建立顏色遮罩 (Mask)**: 使用 `cv2.inRange()` 函數，我們可以定義一個顏色的上下限範圍。所有在 BGR 圖像轉換後的 HSV 圖像中，落在這個顏色範圍內的像素會被設定為白色 (255)，其餘的則為黑色 (0)。這樣就產生了一個二值化的「遮罩」，只突顯出我們感興趣的顏色區域。
3.  **尋找輪廓 (Contours)**: `cv2.findContours()` 函數會分析這個遮罩，找出所有連續的白色區域，並將這些區域的邊界點記錄下來，形成「輪廓」。
4.  **繪製邊界框 (Bounding Box)**: 遍歷所有找到的輪廓，我們可以計算每個輪廓的面積 (`cv2.contourArea`) 來過濾掉過小的雜訊。對於足夠大的輪-廓，使用 `cv2.boundingRect()` 計算出能剛好包圍它的最小矩形，並將這個矩形繪製回原始圖像上，從而標記出目標物體。

### 範例：追蹤單一顏色 (紅色)

```python
# 在 Colab 中執行
import cv2
import numpy as np
from google.colab.patches import cv2_imshow

# 建立一個 300x300 的黑色畫布
img = np.zeros((300, 300, 3), dtype=np.uint8)
# 在畫布上畫一個紅色的矩形
cv2.rectangle(img, (100, 100), (200, 200), (0, 0, 255), -1)

# 設定紅色的 HSV 顏色範圍
# 注意：紅色的 Hue 值在 HSV 色彩空間中橫跨 0 和 180，所以有時需要設定兩個範圍
lower = np.array([0, 40, 40])
upper = np.array([10, 255, 255])

# 轉換到 HSV 色彩空間
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
# 根據顏色範圍進行過濾，產生遮罩
mask = cv2.inRange(hsv, lower, upper)

# 從遮罩中尋找輪廓
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 繪製輪廓
for contour in contours:
    area = cv2.contourArea(contour)
    if area > 100: # 避免標記到微小的雜訊
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

print("偵測到紅色物體並標記：")
cv2_imshow(img)
```

---

## 3. 人臉偵測

使用 OpenCV 提供的預訓練 Haar Cascade 模型，可以輕鬆偵測出影像中的人臉。

### 處理邏輯說明

1.  **載入模型**: `cv2.CascadeClassifier` 會載入預先訓練好的 `.xml` 模型檔案。
2.  **灰階轉換**: 人臉偵測主要依賴於明暗度的變化而非顏色，因此將圖片轉為灰階可以減少計算量並提高偵測效率。
3.  **多尺度偵測**: `detectMultiScale()` 是核心函數。它會在圖像上滑動一個偵測窗口，檢查窗口內的區域是否為人臉。
    *   `scaleFactor`: 由於圖片中的人臉大小不一，這個參數定義了每次掃描時，偵測窗口要縮小多少比例。例如 `1.1` 表示每次縮小 10%。值越小，偵測越慢但可能越精準。
    *   `minNeighbors`: 這個參數定義了構成一個有效偵測需要多少個重疊的候選框。一個較高的值可以過濾掉許多假陽性 (false positives)，使得偵測結果更為可靠。
4.  **繪製結果**: 函數會返回所有偵測到的人臉位置 `(x, y, w, h)` 列表。我們遍歷這個列表，並在原始彩色圖片上對應的位置繪製矩形框。

### 範例：偵測圖片中的人臉

```python
# 在 Colab 中執行
import cv2
import numpy as np
from google.colab.patches import cv2_imshow

# 讀取圖片並轉為灰階
img = cv2.imread('mona.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 載入人臉模型
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
# 偵測人臉
faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

# 繪製人臉方框
for (x, y, w, h) in faces:
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

print("蒙娜麗莎的人臉偵測結果：")
cv2_imshow(img)
```

---

## 4. 人臉馬賽克

偵測到人臉後，可以對該區域進行馬賽克處理，保護隱私。

### 處理邏輯說明

馬賽克的原理是「先縮小再放大」。

1.  **擷取人臉區域**: 根據人臉偵測返回的 `(x, y, w, h)`，從原圖中將人臉部分的影像擷取出來。
2.  **縮小影像**: 使用 `cv2.resize()` 將擷取的人臉影像縮小到一個非常小的尺寸，例如 `15x15` 像素。`interpolation=cv2.INTER_LINEAR` 會在縮小時對像素進行線性插值，平滑地合併顏色。
3.  **放大影像**: 接著，再使用 `cv2.resize()` 將這個縮小的影像放大回原來的人臉尺寸。關鍵在於使用 `interpolation=cv2.INTER_NEAREST` (最近鄰插值法)。這種方法在放大時，不會去平滑顏色或創造新的顏色，而是直接用最近的像素點顏色來填充，因此會產生明顯的色塊效果，也就是馬賽克。
4.  **替換原圖區域**: 最後，將處理好的馬賽克影像放回原圖中的人臉位置。

### 範例：將偵測到的人臉打上馬賽克

```python
# 在 Colab 中執行
import cv2
from google.colab.patches import cv2_imshow

img = cv2.imread('mona.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
faces = face_cascade.detectMultiScale(gray, 1.2, 3)

for (x, y, w, h) in faces:
    # 擷取人臉區域
    mosaic = img[y:y+h, x:x+w]
    level = 15 # 馬賽克程度，數值越高越模糊
    mh = int(h/level)
    mw = int(w/level)
    # 先縮小再放大，產生馬賽克效果
    mosaic = cv2.resize(mosaic, (mw,mh), interpolation=cv2.INTER_LINEAR)
    mosaic = cv2.resize(mosaic, (w,h), interpolation=cv2.INTER_NEAREST)
    # 將馬賽克放回原圖
    img[y:y+h, x:x+w] = mosaic

print("人臉馬賽克結果：")
cv2_imshow(img)
```

---

## 5. 五官偵測 (眼睛、鼻子、嘴巴)

除了人臉，也可以使用對應的模型來偵測眼睛、鼻子和嘴巴。

### 處理邏輯說明

原理與人臉偵測完全相同，只是分別載入了針對眼睛 (`haarcascade_eye.xml`)、嘴巴 (`haarcascade_mcs_mouth.xml`) 和鼻子 (`haarcascade_mcs_nose.xml`) 的 Haar Cascade 模型。

一個常見的優化技巧是：先偵測人臉，然後只在人臉的區域內偵測五官。這樣可以大幅減少搜尋範圍，降低運算量並減少誤判。不過，為了簡化範例，這裡我們仍然在整張圖片上進行偵測。

### 範例：偵測圖片中的五官

```python
# 在 Colab 中執行
import cv2
from google.colab.patches import cv2_imshow

img = cv2.imread('girl.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 載入不同部位的模型
eye_cascade = cv2.CascadeClassifier("haarcascade_eye.xml")
mouth_cascade = cv2.CascadeClassifier("haarcascade_mcs_mouth.xml")
nose_cascade = cv2.CascadeClassifier("haarcascade_mcs_nose.xml")

# 分別偵測五官
eyes = eye_cascade.detectMultiScale(gray)
mouths = mouth_cascade.detectMultiScale(gray)
noses = nose_cascade.detectMultiScale(gray)

# 繪製方框
for (x, y, w, h) in eyes:
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2) # 綠色
for (x, y, w, h) in mouths:
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2) # 紅色
for (x, y, w, h) in noses:
    cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2) # 藍色

print("五官偵測結果 (綠:眼, 藍:鼻, 紅:嘴):")
cv2_imshow(img)
```

---

## 6. 行人與汽車偵測

同樣的原理可以應用於偵測行人或車輛。

### 處理邏輯說明

此範例與人臉/五官偵測的邏輯完全一致，只是更換了模型檔案。我們使用 `haarcascade_fullbody.xml` 來偵測完整的行人身體，並使用 `cars.xml` 來偵測汽車。這展示了 Haar Cascade 方法的通用性，只要有對應的訓練模型，就可以用來偵測各種剛性物體。

### 範例：偵測圖片中的行人與汽車

```python
# 在 Colab 中執行
import cv2
from google.colab.patches import cv2_imshow

img = cv2.imread('cars.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 載入模型
pedestrian_cascade = cv2.CascadeClassifier("haarcascade_fullbody.xml")
car_cascade = cv2.CascadeClassifier("cars.xml")

# 偵測
pedestrians = pedestrian_cascade.detectMultiScale(gray, 1.1, 1)
cars = car_cascade.detectMultiScale(gray, 1.1, 1)

# 繪製方框
for (x, y, w, h) in pedestrians:
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2) # 綠色
for (x, y, w, h) in cars:
    cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2) # 藍色

print("行人(綠)與汽車(藍)偵測結果：")
cv2_imshow(img)
```

---

## 7. 單物件追蹤

在 Colab 中，我們無法使用 `cv2.selectROI` 進行互動式選取。因此，我們需要手動指定要追蹤的物件初始位置 (Bounding Box)。

### 處理邏輯說明

物件追蹤與物件偵測不同。偵測是在每一幀都重新尋找物件，而追蹤則是在第一幀指定物件後，試圖在後續的每一幀中「跟隨」這個物件。

1.  **建立追蹤器**: `cv2.legacy.TrackerCSRT_create()` 會建立一個 CSRT 追蹤器。CSRT (Channel and Spatial Reliability Tracker) 是一種較為精準但速度稍慢的追蹤演算法。OpenCV 還提供了其他追蹤器，如 KCF、MOSSE 等。
2.  **初始化追蹤器**: `tracker.init(frame, bbox)` 是關鍵步驟。我們提供第一幀影像和一個手動指定的 `bbox` (bounding box，格式為 `(x, y, w, h)`) 給追蹤器，告訴它「這就是你要追蹤的目標」。
3.  **更新追蹤器**: 在迴圈中，對影片的每一幀呼叫 `tracker.update(frame)`。追蹤器會在這新的一幀中尋找它認為是目標的物體，並返回兩個值：`success` (布林值，表示是否成功追蹤到) 和更新後的 `bbox`。
4.  **繪製結果**: 如果 `success` 為 `True`，我們就用新的 `bbox` 繪製方框，實現視覺上的追蹤效果。

### 範例：追蹤影片中的特定物件

**注意：** 此範例需要您先上傳一個名為 `test.mp4` 的影片檔到 Colab。

```python
# 在 Colab 中執行
import cv2
from google.colab.patches import cv2_imshow

# tracker = cv2.TrackerCSRT_create() # OpenCV 3.x
tracker = cv2.legacy.TrackerCSRT_create() # OpenCV 4.x

# 開啟影片檔案
cap = cv2.VideoCapture('test.mp4')

# 讀取第一幀
ret, frame = cap.read()

# 手動設定初始追蹤框 (x, y, w, h)
# 這裡的數值需要您根據您的影片內容手動調整
bbox = (200, 100, 50, 50)

# 初始化追蹤器
tracker.init(frame, bbox)

# 讀取影片並追蹤
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 更新追蹤器
    success, bbox = tracker.update(frame)

    # 如果追蹤成功，繪製方框
    if success:
        (x, y, w, h) = [int(v) for v in bbox]
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    else:
        cv2.putText(frame, "Tracking failure", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)

    # 顯示結果 (僅顯示部分幀以加快速度)
    # cv2_imshow(frame) # 如果想看每一幀的結果，可以取消註解此行

# 釋放資源
cap.release()
print("單物件追蹤完成。請注意，由於 Colab 的限制，只會顯示最終結果的其中一幀或不顯示過程。")
```

---

## 8. 辨識不同人臉

這是一個更進階的應用，包含兩個步驟：
1.  **訓練 (Training):** 使用多張已知人物的照片來訓練一個人臉辨識模型。
2.  **辨識 (Recognition):** 使用訓練好的模型來辨識新影像中的人臉。

我們這裡使用的是 LBPH (Local Binary Patterns Histograms) 演算法。

### 處理邏輯說明

1.  **LBPH 演算法簡介**: LBPH 是一種高效的人臉辨識演算法，對光線變化有很好的抵抗力。它的核心思想是分析每個像素與其周圍像素的關係，並將這些關係編碼成一個二進位數，最後統計整張臉的這些編碼的直方圖。這個「直方圖」就成為了代表這張臉的「特徵」。

2.  **步驟一：準備資料**:
    *   為每個不同的人建立一個資料夾，並賦予一個獨一無二的數字 ID (例如 Person 1 的 ID 是 1，Person 2 的 ID 是 2)。
    *   遍歷所有圖片，使用 Haar Cascade 偵測出人臉。
    *   建立兩個列表：一個 `faces` 列表，儲存所有偵測到的人臉區域 (影像本身)；一個 `ids` 列表，儲存每張人臉對應的數字 ID。

3.  **步驟二：訓練模型**:
    *   `recognizer.train(faces, np.array(ids))` 是訓練的核心。它會接收人臉影像列表和對應的 ID 列表。
    *   對於 `faces` 中的每一張人臉，演算法會計算其 LBPH 直方圖 (特徵)。
    *   然後，它會將計算出的特徵與對應的 `id` 關聯起來並儲存。簡單來說，就是建立一個「ID -> 人臉特徵」的對照表。
    *   `recognizer.save()` 會將這個學習到的對照表儲存成一個 `.yml` 檔案，方便未來直接載入使用，無需重新訓練。

4.  **步驟三：進行辨識**:
    *   `recognizer.read()` 載入訓練好的模型。
    *   在一張新的測試圖片上，同樣先用 Haar Cascade 偵測出人臉。
    *   對於偵測到的每張臉，呼叫 `recognizer.predict()`。這個函數會計算這張新臉的 LBPH 特徵，然後去模型裡比對，找出特徵最接近的那個已知 ID。
    *   `predict()` 會返回兩個值：預測的 `id_num` 和一個 `confidence` (信心指數)。
    *   **重要**: 對於 LBPH 演算法，`confidence` 代表的是「距離」，所以**數值越低，表示特徵越接近，可信度越高**。一個常見的門檻值是 50 或 100，低於這個值我們就認為辨識成功。

### 步驟一：下載並準備訓練資料

```python
# 在 Colab 中執行
import os
import cv2
import numpy as np
from google.colab.patches import cv2_imshow

# 建立資料夾結構
!mkdir -p face_data/person1
!mkdir -p face_data/person2

# 下載範例圖片 (這裡以貓狗代替，您可以換成自己的人臉圖片)
# Person 1 (Cats)
!wget -O face_data/person1/1.jpg https://i.natgeofe.com/n/548467d8-c5f1-4551-9f58-6817a8d2c45e/NationalGeographic_2572187_square.jpg
!wget -O face_data/person1/2.jpg https://www.catster.com/wp-content/uploads/2023/11/white-fluffy-cat-in-a-garden_By-Kay-Altair_shutterstock.jpg
# Person 2 (Dogs)
!wget -O face_data/person2/1.jpg https://hips.hearstapps.com/hmg-prod/images/dog-puppy-on-garden-royalty-free-image-1586966191.jpg
!wget -O face_data/person2/2.jpg https://www.hartz.com/wp-content/uploads/2022/04/small-dog-breeds-1.jpg

print("資料下載完成！")
```

### 步驟二：訓練人臉辨識模型

```python
# 在 Colab 中執行
# recognizer = cv2.face.LBPHFaceRecognizer_create() # OpenCV 3.x
recognizer = cv2.legacy.LBPHFaceRecognizer_create() # OpenCV 4.x
detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

faces = []
ids = []
data_path = 'face_data'
# 取得 person1, person2 等資料夾路徑
person_folders = [os.path.join(data_path, f) for f in os.listdir(data_path)]

id_counter = 1
for person_folder in person_folders:
    if not os.path.isdir(person_folder):
        continue
    
    # 取得資料夾內所有圖片的路徑
    person_images = [os.path.join(person_folder, f) for f in os.listdir(person_folder)]
    
    for image_path in person_images:
        img = cv2.imread(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img_np = np.array(gray, 'uint8')
        
        # 偵測人臉 (在此範例中是貓臉/狗臉)
        # 注意：haarcascade_frontalface 對動物臉效果不佳，僅為示範流程
        face_rects = detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
        
        for (x, y, w, h) in face_rects:
            faces.append(img_np[y:y+h, x:x+w]) # 加入人臉 ROI
            ids.append(id_counter) # 加入對應的 ID
            
    id_counter += 1

print('開始訓練模型...')
recognizer.train(faces, np.array(ids))
recognizer.save('face_model.yml')
print('模型訓練完成並儲存為 face_model.yml！')
```

### 步驟三：進行人臉辨識

```python
# 在 Colab 中執行
# recognizer = cv2.face.LBPHFaceRecognizer_create() # OpenCV 3.x
recognizer = cv2.legacy.LBPHFaceRecognizer_create() # OpenCV 4.x
recognizer.read('face_model.yml')
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

# 建立 ID 和姓名的對照表
name_map = {
    1: 'Person 1 (Cat)',
    2: 'Person 2 (Dog)'
}

# 讀取一張新的圖片來測試
!wget -O test_image.jpg https://i.natgeofe.com/n/548467d8-c5f1-4551-9f58-6817a8d2c45e/NationalGeographic_2572187_square.jpg
img = cv2.imread('test_image.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

for (x, y, w, h) in faces:
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
    # 進行預測
    id_num, confidence = recognizer.predict(gray[y:y+h, x:x+w])
    
    # 信心指數越低，表示匹配度越高
    if confidence < 100:
        text = name_map.get(id_num, "Unknown")
        # 轉換為更容易理解的百分比
        confidence_text = f"  {round(100 - confidence)}%"
    else:
        text = "Unknown"
        confidence_text = ""
        
    cv2.putText(img, text + confidence_text, (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

print("辨識結果：")
cv2_imshow(img)
```
