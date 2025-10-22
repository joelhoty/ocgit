<!-- Path: General_python/openCV/影像辨識-傳統方法 | Timestamp: 2025-10-06 16:00:00 | Version: b01 -->
# 題目三：智慧型隱私保護系統

## 📋 任務說明

請撰寫一個 Python 程式，能夠偵測人臉並「選擇性」地對特定五官進行馬賽克處理，實現更精細的隱私保護功能。

---

## 🖼️ 影像選擇指引

### 適合的影像類型

#### ✅ 推薦使用的影像

1. **清晰的正面人臉照片**
   - 特徵：臉部完全朝向鏡頭、五官清晰
   - 範例：證件照、自拍照、肖像照
   - 偵測成功率：★★★★★（95%+）
   - 最佳範例：
     - 證件照等級的清晰度
     - 眼睛完全張開、直視鏡頭
     - 嘴巴閉合或微笑（避免大笑張嘴）
     - 無瀏海遮擋眼睛

2. **光線充足且均勻的照片**
   - 特徵：臉部明亮、無強烈陰影
   - 拍攝環境：白天室內、柔和燈光、陰天戶外
   - 偵測成功率：★★★★★（90%+）
   - 光線建議：
     ```
     ✅ 前方或側前方光源（45° 角）
     ✅ 環境光均勻（如攝影棚打光）
     ✅ 陰天的自然光（無陰影）
     ⚠️ 避免正上方光源（眼窩陰影）
     ⚠️ 避免逆光（臉部過暗）
     ⚠️ 避免強烈側光（陰陽臉）
     ```

3. **單人特寫照片**
   - 特徵：臉部佔畫面 40% 以上
   - 距離：50cm - 1.5m
   - 偵測成功率：★★★★★（90%+）
   - 構圖建議：
     - 半身照或大頭照
     - 人臉在畫面中央
     - 背景簡單不雜亂

4. **五官無遮擋的照片**
   - 特徵：眼睛、鼻子、嘴巴完整可見
   - 偵測成功率：★★★★☆（85%+）
   - 注意事項：
     ```
     ✅ 無戴墨鏡（眼睛偵測需要）
     ✅ 無口罩（嘴巴偵測需要）
     ✅ 瀏海不遮眼（眼睛偵測需要）
     ✅ 頭髮不遮臉（臉部完整）
     ```

#### ⚠️ 效果較差的影像

1. **側臉或低頭照片**
   - 問題：五官偵測器主要訓練於正面角度
   - 影響：眼睛、嘴巴可能偵測不到
   - 偵測成功率：★★☆☆☆（30-50%）
   - 臉部角度建議：
     ```
     ✅ 正面（0°）      → 最佳
     ⚠️ 微側面（< 15°） → 尚可
     ❌ 側臉（> 30°）   → 效果差
     ❌ 低頭/抬頭       → 效果差
     ```

2. **五官部分遮擋**
   - 問題：遮擋物干擾特徵偵測
   - 常見情況：
     ```
     ⚠️ 戴一般眼鏡      → 尚可（可能誤判鏡框）
     ❌ 戴墨鏡          → 無法偵測眼睛
     ❌ 戴口罩          → 無法偵測嘴巴
     ⚠️ 瀏海遮眼        → 可能漏偵測
     ⚠️ 手遮臉          → 被遮擋部位無法偵測
     ```
   - 偵測成功率：★★☆☆☆（20-60%）

3. **解析度不足或模糊**
   - 問題：五官細節不清晰
   - 影響：眼睛等小特徵難以偵測
   - 偵測成功率：★★☆☆☆（40-60%）
   - 解析度需求：
     ```
     臉部像素建議：
     - 眼睛偵測：眼睛區域至少 20×20 px
     - 嘴巴偵測：嘴巴區域至少 30×20 px
     - 整體人臉：至少 100×100 px
     ```

4. **表情誇張或動態照片**
   - 問題：五官形狀變化大
   - 影響：
     - 閉眼 → 眼睛偵測失敗
     - 大笑張嘴 → 嘴巴形狀異常，可能偵測失敗或偵測多個區域
     - 鬼臉 → 五官變形，偵測率下降
   - 偵測成功率：★★☆☆☆（40-70%）

#### ❌ 完全不適合的影像

- 卡通或繪畫人像（非真實人臉）
- 純側面照（臉部角度 > 60°）
- 極度模糊或低解析度（< 200×200 px）
- 極端光線（全黑、強烈過曝）
- 多重曝光或特效照片

### 測試影像建議

#### 初學者測試（難度：★☆☆☆☆）

**推薦影像**：
```
1. girl.jpg（教學範例）
   - 特點：單人正面、光線良好、五官清晰
   - 預期：人臉 100%、眼睛 90%、嘴巴 80%

2. 自己的證件照或自拍照
   - 拍攝建議：
     * 正面直視鏡頭
     * 白色或淺色背景
     * 自然光或室內燈光
     * 無瀏海、無眼鏡
   - 預期：全部偵測成功

3. mona.jpg（蒙娜麗莎）
   - 特點：經典肖像畫（但 Haar Cascade 效果有限）
   - 預期：人臉可能偵測到，五官較難
```

#### 中級測試（難度：★★★☆☆）

**挑戰場景**：
```
1. 戴眼鏡的照片
   - 測試：眼睛偵測是否會誤判鏡框
   - 調整：可能需要提高 minNeighbors 參數

2. 不同表情的照片
   - 正常表情 vs 微笑 vs 大笑
   - 觀察：表情對嘴巴偵測的影響

3. 不同光線的照片
   - 明亮室內 vs 昏暗室內 vs 戶外陽光
   - 觀察：光線對五官偵測的影響

4. 輕微側臉（15° 內）
   - 測試：演算法對角度的容忍度
```

#### 進階測試（難度：★★★★☆）

**高難度場景**：
```
1. 團體照
   - 挑戰：多張人臉、不同大小、部分側臉
   - 目標：對所有偵測到的人臉都進行處理

2. 動態或表情誇張照片
   - 挑戰：五官形狀變化大
   - 觀察：哪些情況會導致偵測失敗

3. 複雜背景照片
   - 挑戰：背景雜亂可能影響偵測
   - 測試：演算法的抗干擾能力
```

### 不同偵測模式的影像需求

#### 模式 A：只模糊眼睛
```
影像需求：
✅ 眼睛完全張開
✅ 無瀏海遮擋
✅ 正面或微側面（< 15°）
✅ 眼睛區域光線充足

不適合：
❌ 閉眼照片
❌ 戴墨鏡
❌ 厚重瀏海遮眼
```

#### 模式 B：只模糊嘴巴
```
影像需求：
✅ 嘴巴清晰可見
✅ 正常閉合或微笑
✅ 無口罩或手遮擋
✅ 下半臉光線充足

不適合：
❌ 大笑張嘴（嘴巴形狀差異大）
❌ 戴口罩
❌ 低頭（下巴遮擋嘴巴）
```

#### 模式 C：模糊眼睛和嘴巴
```
影像需求：
綜合上述兩種模式的要求

最佳照片特徵：
✅ 證件照風格
✅ 正面、眼睛張開、嘴巴自然閉合
✅ 無遮擋、光線均勻
✅ 背景簡單
```

### 影像品質檢查清單

測試前請確認：
- [ ] 影像格式：JPG、PNG
- [ ] 解析度：至少 640×480（建議 1024×768）
- [ ] 人臉大小：至少 100×100 像素
- [ ] 臉部角度：正面或微側面（< 15°）
- [ ] 五官清晰：眼睛、鼻子、嘴巴可見
- [ ] 光線條件：明亮均勻、無強烈陰影
- [ ] 無遮擋：不戴墨鏡、口罩
- [ ] 表情自然：眼睛張開、嘴巴閉合或微笑

---

## ✅ 詳細需求列表

### 需求 1：環境準備

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

print("開始下載必要檔案...")
for filename, url in files.items():
    if not os.path.exists(filename):
        print(f"  下載 {filename}...")
        try:
            urllib.request.urlretrieve(url, filename)
            print(f"  ✓ {filename} 下載完成")
        except Exception as e:
            print(f"  ✗ {filename} 下載失敗: {e}")
    else:
        print(f"  ✓ {filename} 已存在")

print("\n所有檔案準備完成！")
```

---

### 需求 2：匯入套件與設定模式

**說明**：匯入必要套件，並定義隱私保護模式。

**程式碼提示**：
```python
import cv2
import numpy as np
from google.colab.patches import cv2_imshow

# 設定隱私保護模式
# 選項："eyes"（只模糊眼睛）
#       "mouth"（只模糊嘴巴）
#       "eyes_mouth"（模糊眼睛和嘴巴）
PRIVACY_MODE = "eyes"  # 可修改此變數來改變模式

print("="*50)
print(f"隱私保護系統")
print("="*50)
print(f"當前模式: {PRIVACY_MODE}")
print("="*50 + "\n")
```

---

### 需求 3：讀取圖片與載入模型

**說明**：讀取測試圖片並載入所需的 Haar Cascade 模型。

**程式碼提示**：
```python
# 讀取圖片
img = cv2.imread('girl.jpg')

if img is None:
    print("錯誤: 無法讀取圖片")
else:
    print("✓ 圖片讀取成功")
    height, width, channels = img.shape
    print(f"圖片尺寸: {width} x {height} 像素\n")

    # 保存原圖副本（用於對比）
    img_original = img.copy()

    # 轉換為灰階
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    print("✓ 圖片已轉換為灰階\n")

    # 載入模型
    print("載入 Haar Cascade 模型...")
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
    mouth_cascade = cv2.CascadeClassifier('haarcascade_mcs_mouth.xml')

    # 檢查模型是否載入成功
    models_ok = True
    if face_cascade.empty():
        print("  ✗ 人臉模型載入失敗")
        models_ok = False
    else:
        print("  ✓ 人臉模型載入成功")

    if eye_cascade.empty():
        print("  ✗ 眼睛模型載入失敗")
        models_ok = False
    else:
        print("  ✓ 眼睛模型載入成功")

    if mouth_cascade.empty():
        print("  ✗ 嘴巴模型載入失敗")
        models_ok = False
    else:
        print("  ✓ 嘴巴模型載入成功")

    if models_ok:
        print("\n✓ 所有模型載入完成\n")
```

---

### 需求 4：定義馬賽克處理函數

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
        image: 處理後的圖片
    """
    # 確保座標在圖片範圍內
    img_h, img_w = image.shape[:2]
    x = max(0, min(x, img_w - 1))
    y = max(0, min(y, img_h - 1))
    w = max(1, min(w, img_w - x))
    h = max(1, min(h, img_h - y))

    # 確保區域有效
    if w <= 0 or h <= 0:
        return image

    # 擷取區域
    region = image[y:y+h, x:x+w].copy()

    # 確保區域不為空
    if region.size == 0:
        return image

    # 計算縮小後的尺寸（至少為 1）
    small_h = max(1, h // level)
    small_w = max(1, w // level)

    try:
        # 縮小圖片（產生模糊效果）
        region_small = cv2.resize(region, (small_w, small_h),
                                  interpolation=cv2.INTER_LINEAR)

        # 放大回原尺寸（產生馬賽克效果）
        region_mosaic = cv2.resize(region_small, (w, h),
                                   interpolation=cv2.INTER_NEAREST)

        # 將馬賽克區域放回原圖
        image[y:y+h, x:x+w] = region_mosaic
    except Exception as e:
        print(f"  ⚠️ 馬賽克處理失敗 ({x},{y},{w},{h}): {e}")

    return image

# 測試函數定義
print("✓ 馬賽克處理函數定義完成\n")
```

---

### 需求 5：偵測人臉

**說明**：偵測圖片中的所有人臉。

**程式碼提示**：
```python
# 偵測人臉
print("="*50)
print("開始偵測人臉")
print("="*50)

faces = face_cascade.detectMultiScale(
    gray,
    scaleFactor=1.1,
    minNeighbors=5,
    minSize=(50, 50)
)

print(f"偵測結果: 找到 {len(faces)} 張人臉")

# 若沒有偵測到人臉，顯示警告
if len(faces) == 0:
    print("\n⚠️ 警告: 未偵測到人臉")
    print("可能原因:")
    print("  1. 圖片中沒有正面人臉")
    print("  2. 人臉過小或過大")
    print("  3. 光線條件不佳")
    print("  4. 請嘗試調整參數或更換圖片")
else:
    # 顯示每張人臉的位置
    for i, (x, y, w, h) in enumerate(faces, start=1):
        print(f"  人臉 {i}: 位置({x}, {y}), 大小({w}x{h})")

print("")
```

---

### 需求 6：在人臉區域內偵測五官並進行馬賽克處理

**說明**：針對每張人臉，偵測五官並根據模式進行處理。

**程式碼提示**：
```python
# 統計變數
total_eyes_detected = 0
total_mouths_detected = 0
total_eyes_mosaicked = 0
total_mouths_mosaicked = 0

# 遍歷每張偵測到的人臉
for face_idx, (fx, fy, fw, fh) in enumerate(faces, start=1):
    print("="*50)
    print(f"處理人臉 {face_idx}/{len(faces)}")
    print("="*50)

    # 擷取人臉區域（ROI: Region of Interest）
    face_roi_gray = gray[fy:fy+fh, fx:fx+fw]
    face_roi_color = img[fy:fy+fh, fx:fx+fw]

    # === 選項 1: 處理眼睛 ===
    if PRIVACY_MODE in ["eyes", "eyes_mouth"]:
        print("偵測眼睛...")

        # 在人臉區域內偵測眼睛
        eyes = eye_cascade.detectMultiScale(
            face_roi_gray,
            scaleFactor=1.1,
            minNeighbors=10,  # 較高的值以減少誤判
            minSize=(20, 20)
        )

        print(f"  找到 {len(eyes)} 個眼睛區域")
        total_eyes_detected += len(eyes)

        # 對每個眼睛區域進行馬賽克處理
        for eye_idx, (ex, ey, ew, eh) in enumerate(eyes, start=1):
            # 重要：轉換為原圖的絕對座標
            # 公式：絕對座標 = 人臉座標 + ROI 內相對座標
            abs_x = fx + ex
            abs_y = fy + ey

            # 進行馬賽克處理
            apply_mosaic(img, abs_x, abs_y, ew, eh, level=10)
            total_eyes_mosaicked += 1

            print(f"    眼睛 {eye_idx}: 位置({abs_x}, {abs_y}), 已馬賽克")

    # === 選項 2: 處理嘴巴 ===
    if PRIVACY_MODE in ["mouth", "eyes_mouth"]:
        print("偵測嘴巴...")

        # 在人臉區域的下半部偵測嘴巴（提高準確度）
        # 嘴巴通常位於人臉下半部
        mouth_roi_start = fh // 2  # 從人臉中間開始
        mouth_roi_gray = face_roi_gray[mouth_roi_start:, :]

        mouths = mouth_cascade.detectMultiScale(
            mouth_roi_gray,
            scaleFactor=1.1,
            minNeighbors=20,  # 嘴巴偵測需要更高的閾值
            minSize=(30, 20)
        )

        print(f"  找到 {len(mouths)} 個嘴巴區域")
        total_mouths_detected += len(mouths)

        # 對每個嘴巴區域進行馬賽克處理
        for mouth_idx, (mx, my, mw, mh) in enumerate(mouths, start=1):
            # 重要：轉換為原圖的絕對座標
            # 注意：my 需要加上 mouth_roi_start（因為是在下半部偵測）
            abs_x = fx + mx
            abs_y = fy + mouth_roi_start + my

            # 進行馬賽克處理
            apply_mosaic(img, abs_x, abs_y, mw, mh, level=12)
            total_mouths_mosaicked += 1

            print(f"    嘴巴 {mouth_idx}: 位置({abs_x}, {abs_y}), 已馬賽克")

    print(f"✓ 人臉 {face_idx} 處理完成\n")
```

**座標轉換說明**：
```
重要概念：ROI 相對座標 → 絕對座標

假設：
- 人臉位置：fx=100, fy=80, fw=200, fh=200
- 在人臉 ROI 內偵測到眼睛：ex=50, ey=40

則眼睛在原圖中的絕對座標為：
- abs_x = fx + ex = 100 + 50 = 150
- abs_y = fy + ey = 80 + 40 = 120

若是在人臉下半部偵測嘴巴：
- mouth_roi_start = fh // 2 = 100
- 偵測到嘴巴：mx=60, my=50
- abs_x = fx + mx = 100 + 60 = 160
- abs_y = fy + mouth_roi_start + my = 80 + 100 + 50 = 230
```

---

### 需求 7：顯示處理結果與統計

**說明**：顯示處理前後對比，並輸出統計資訊。

**程式碼提示**：
```python
# 顯示統計結果
print("="*50)
print("處理統計")
print("="*50)
print(f"偵測到的人臉數量: {len(faces)}")
if PRIVACY_MODE in ["eyes", "eyes_mouth"]:
    print(f"偵測到的眼睛數量: {total_eyes_detected}")
    print(f"已馬賽克的眼睛: {total_eyes_mosaicked}")
if PRIVACY_MODE in ["mouth", "eyes_mouth"]:
    print(f"偵測到的嘴巴數量: {total_mouths_detected}")
    print(f"已馬賽克的嘴巴: {total_mouths_mosaicked}")
print("="*50 + "\n")

# 顯示處理前後對比
print("原始圖片：")
cv2_imshow(img_original)

print(f"\n處理後圖片 (模式: {PRIVACY_MODE})：")
cv2_imshow(img)

# 儲存結果
output_filename = f'result_privacy_{PRIVACY_MODE}.jpg'
cv2.imwrite(output_filename, img)
print(f"\n✓ 結果已儲存為 {output_filename}")
```

---

## 📝 完整可執行程式碼

```python
# ========================================
# 題目三：智慧型隱私保護系統
# ========================================

import cv2
import numpy as np
from google.colab.patches import cv2_imshow

# === 1. 設定模式 ===
PRIVACY_MODE = "eyes"  # "eyes", "mouth", "eyes_mouth"

print("="*50)
print("智慧型隱私保護系統")
print("="*50)
print(f"當前模式: {PRIVACY_MODE}")
print("="*50 + "\n")

# === 2. 讀取圖片 ===
img = cv2.imread('girl.jpg')

if img is None:
    print("錯誤: 無法讀取圖片")
else:
    print("✓ 圖片讀取成功")
    height, width = img.shape[:2]
    print(f"圖片尺寸: {width} x {height} 像素\n")

    # 保存原圖副本
    img_original = img.copy()

    # 轉換為灰階
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    print("✓ 圖片已轉換為灰階\n")

    # === 3. 載入模型 ===
    print("載入 Haar Cascade 模型...")
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
    mouth_cascade = cv2.CascadeClassifier('haarcascade_mcs_mouth.xml')

    if not face_cascade.empty() and not eye_cascade.empty() and not mouth_cascade.empty():
        print("✓ 所有模型載入完成\n")
    else:
        print("✗ 部分模型載入失敗")

    # === 4. 定義馬賽克函數 ===
    def apply_mosaic(image, x, y, w, h, level=15):
        """對指定區域進行馬賽克處理"""
        img_h, img_w = image.shape[:2]
        x = max(0, min(x, img_w - 1))
        y = max(0, min(y, img_h - 1))
        w = max(1, min(w, img_w - x))
        h = max(1, min(h, img_h - y))

        if w <= 0 or h <= 0:
            return image

        region = image[y:y+h, x:x+w].copy()

        if region.size == 0:
            return image

        small_h = max(1, h // level)
        small_w = max(1, w // level)

        try:
            region_small = cv2.resize(region, (small_w, small_h),
                                      interpolation=cv2.INTER_LINEAR)
            region_mosaic = cv2.resize(region_small, (w, h),
                                       interpolation=cv2.INTER_NEAREST)
            image[y:y+h, x:x+w] = region_mosaic
        except Exception as e:
            print(f"  ⚠️ 馬賽克處理失敗: {e}")

        return image

    print("✓ 馬賽克處理函數定義完成\n")

    # === 5. 偵測人臉 ===
    print("="*50)
    print("開始偵測人臉")
    print("="*50)

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(50, 50)
    )

    print(f"偵測結果: 找到 {len(faces)} 張人臉\n")

    if len(faces) == 0:
        print("⚠️ 未偵測到人臉，請檢查圖片或調整參數\n")

    # === 6. 處理五官 ===
    total_eyes_mosaicked = 0
    total_mouths_mosaicked = 0

    for face_idx, (fx, fy, fw, fh) in enumerate(faces, start=1):
        print(f"處理人臉 {face_idx}/{len(faces)}")

        face_roi_gray = gray[fy:fy+fh, fx:fx+fw]

        # 處理眼睛
        if PRIVACY_MODE in ["eyes", "eyes_mouth"]:
            print("  偵測眼睛...")
            eyes = eye_cascade.detectMultiScale(
                face_roi_gray,
                scaleFactor=1.1,
                minNeighbors=10,
                minSize=(20, 20)
            )

            print(f"    找到 {len(eyes)} 個眼睛區域")

            for (ex, ey, ew, eh) in eyes:
                abs_x = fx + ex
                abs_y = fy + ey
                apply_mosaic(img, abs_x, abs_y, ew, eh, level=10)
                total_eyes_mosaicked += 1

        # 處理嘴巴
        if PRIVACY_MODE in ["mouth", "eyes_mouth"]:
            print("  偵測嘴巴...")
            mouth_roi_start = fh // 2
            mouth_roi_gray = face_roi_gray[mouth_roi_start:, :]

            mouths = mouth_cascade.detectMultiScale(
                mouth_roi_gray,
                scaleFactor=1.1,
                minNeighbors=20,
                minSize=(30, 20)
            )

            print(f"    找到 {len(mouths)} 個嘴巴區域")

            for (mx, my, mw, mh) in mouths:
                abs_x = fx + mx
                abs_y = fy + mouth_roi_start + my
                apply_mosaic(img, abs_x, abs_y, mw, mh, level=12)
                total_mouths_mosaicked += 1

        print(f"  ✓ 人臉 {face_idx} 處理完成\n")

    # === 7. 顯示結果 ===
    print("="*50)
    print("處理統計")
    print("="*50)
    print(f"偵測到的人臉數量: {len(faces)}")
    if PRIVACY_MODE in ["eyes", "eyes_mouth"]:
        print(f"已馬賽克的眼睛: {total_eyes_mosaicked}")
    if PRIVACY_MODE in ["mouth", "eyes_mouth"]:
        print(f"已馬賽克的嘴巴: {total_mouths_mosaicked}")
    print("="*50 + "\n")

    print("原始圖片：")
    cv2_imshow(img_original)

    print(f"\n處理後圖片 (模式: {PRIVACY_MODE})：")
    cv2_imshow(img)

    # 儲存結果
    output_filename = f'result_privacy_{PRIVACY_MODE}.jpg'
    cv2.imwrite(output_filename, img)
    print(f"\n✓ 結果已儲存為 {output_filename}")
```

---

## 🎯 測試建議

### 測試 1：不同模式測試

```python
# 分別測試三種模式
modes = ["eyes", "mouth", "eyes_mouth"]

for mode in modes:
    print(f"\n{'='*50}")
    print(f"測試模式: {mode}")
    print(f"{'='*50}")

    PRIVACY_MODE = mode
    img = cv2.imread('girl.jpg').copy()

    # ... 執行完整處理流程 ...

    cv2.imwrite(f'result_{mode}.jpg', img)
    print(f"✓ 模式 {mode} 測試完成")
```

### 測試 2：調整馬賽克程度

```python
# 測試不同的 level 值
levels = [5, 10, 15, 20, 30]

for level in levels:
    img = cv2.imread('girl.jpg').copy()

    # ... 偵測流程 ...

    # 使用不同的 level
    apply_mosaic(img, abs_x, abs_y, ew, eh, level=level)

    cv2.imwrite(f'result_level{level}.jpg', img)
    print(f"Level {level}: 馬賽克程度 {'粗' if level < 10 else '細'}")
```

### 測試 3：調整五官偵測參數

```python
# 測試眼睛偵測的不同 minNeighbors 值
min_neighbors_values = [5, 10, 15, 20]

for mn in min_neighbors_values:
    eyes = eye_cascade.detectMultiScale(
        face_roi_gray,
        scaleFactor=1.1,
        minNeighbors=mn,
        minSize=(20, 20)
    )

    print(f"minNeighbors={mn}: 偵測到 {len(eyes)} 個眼睛")
```

---

## 🚀 延伸挑戰（選做）

### 挑戰 1：加入使用者互動

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
print(f"\n已選擇模式: {PRIVACY_MODE}\n")
```

### 挑戰 2：支援高斯模糊效果

```python
def apply_blur(image, x, y, w, h, blur_level=21):
    """使用高斯模糊代替馬賽克"""
    img_h, img_w = image.shape[:2]
    x = max(0, min(x, img_w - 1))
    y = max(0, min(y, img_h - 1))
    w = max(1, min(w, img_w - x))
    h = max(1, min(h, img_h - y))

    if w <= 0 or h <= 0:
        return image

    region = image[y:y+h, x:x+w].copy()

    # 確保 blur_level 為奇數
    if blur_level % 2 == 0:
        blur_level += 1

    # 套用高斯模糊
    blurred = cv2.GaussianBlur(region, (blur_level, blur_level), 0)
    image[y:y+h, x:x+w] = blurred

    return image

# 使用方式
apply_blur(img, abs_x, abs_y, ew, eh, blur_level=25)
```

### 挑戰 3：加入黑色遮罩選項

```python
def apply_black_bar(image, x, y, w, h):
    """使用純黑矩形遮蓋（類似電視新聞效果）"""
    img_h, img_w = image.shape[:2]
    x = max(0, min(x, img_w - 1))
    y = max(0, min(y, img_h - 1))
    w = max(1, min(w, img_w - x))
    h = max(1, min(h, img_h - y))

    # 繪製黑色矩形
    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 0, 0), -1)

    return image

# 使用方式
apply_black_bar(img, abs_x, abs_y, ew, eh)
```

### 挑戰 4：處理多人照片並顯示統計

```python
# 在圖片上顯示處理資訊
info_text = [
    f"Mode: {PRIVACY_MODE}",
    f"Faces: {len(faces)}",
    f"Eyes blurred: {total_eyes_mosaicked}",
    f"Mouths blurred: {total_mouths_mosaicked}"
]

y_offset = 30
for i, text in enumerate(info_text):
    cv2.putText(
        img,
        text,
        (10, y_offset + i*30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 0),
        2
    )
```

---

## 🔧 除錯技巧

### 問題 1：眼睛或嘴巴偵測不到

**診斷工具**：
```python
# 視覺化人臉 ROI，檢查是否正確
face_roi_display = img[fy:fy+fh, fx:fx+fw].copy()
print("人臉區域：")
cv2_imshow(face_roi_display)

# 顯示偵測參數
print(f"人臉大小: {fw}x{fh}")
print(f"眼睛最小尺寸: 20x20")
print(f"嘴巴最小尺寸: 30x20")

# 如果人臉太小，五官可能也會太小
if fw < 100 or fh < 100:
    print("⚠️ 警告: 人臉過小，五官偵測可能失敗")
```

**解決方法**：
```python
# 方法 1：降低 minNeighbors
eyes = eye_cascade.detectMultiScale(
    face_roi_gray,
    scaleFactor=1.1,
    minNeighbors=5,  # 從 10 降低到 5
    minSize=(20, 20)
)

# 方法 2：降低最小尺寸
eyes = eye_cascade.detectMultiScale(
    face_roi_gray,
    scaleFactor=1.1,
    minNeighbors=10,
    minSize=(15, 15)  # 從 20x20 降低到 15x15
)

# 方法 3：調整 scaleFactor
eyes = eye_cascade.detectMultiScale(
    face_roi_gray,
    scaleFactor=1.05,  # 從 1.1 降低到 1.05（更精細）
    minNeighbors=10,
    minSize=(20, 20)
)
```

### 問題 2：眼睛偵測到過多區域（誤判）

**原因**：鼻子、眼鏡框等被誤判為眼睛

**解決方法**：
```python
# 方法 1：提高 minNeighbors
eyes = eye_cascade.detectMultiScale(
    face_roi_gray,
    scaleFactor=1.1,
    minNeighbors=15,  # 提高到 15 或 20
    minSize=(20, 20)
)

# 方法 2：過濾不合理的眼睛位置
# 眼睛通常在人臉上半部
valid_eyes = []
for (ex, ey, ew, eh) in eyes:
    # 只保留在人臉上半部的偵測結果
    if ey < fh * 0.6:  # 眼睛應該在人臉上方 60% 範圍內
        valid_eyes.append((ex, ey, ew, eh))

eyes = valid_eyes

# 方法 3：過濾不合理的大小
valid_eyes = []
for (ex, ey, ew, eh) in eyes:
    # 眼睛大小應該合理（不會太大或太小）
    area = ew * eh
    face_area = fw * fh
    ratio = area / face_area

    if 0.01 < ratio < 0.15:  # 眼睛佔人臉 1%-15%
        valid_eyes.append((ex, ey, ew, eh))

eyes = valid_eyes
```

### 問題 3：嘴巴偵測失敗

**診斷**：
```python
# 檢查嘴巴搜尋區域
mouth_roi_start = fh // 2
mouth_roi_display = face_roi_gray[mouth_roi_start:, :]

print("嘴巴搜尋區域（灰階）：")
cv2_imshow(mouth_roi_display)

print(f"搜尋區域大小: {mouth_roi_display.shape[1]}x{mouth_roi_display.shape[0]}")
```

**解決方法**：
```python
# 方法 1：擴大搜尋範圍
mouth_roi_start = fh // 3  # 從人臉 1/3 處開始（而非 1/2）

# 方法 2：降低 minNeighbors
mouths = mouth_cascade.detectMultiScale(
    mouth_roi_gray,
    scaleFactor=1.1,
    minNeighbors=10,  # 從 20 降低到 10
    minSize=(30, 20)
)

# 方法 3：調整最小尺寸
mouths = mouth_cascade.detectMultiScale(
    mouth_roi_gray,
    scaleFactor=1.1,
    minNeighbors=20,
    minSize=(25, 15)  # 降低最小尺寸
)
```

### 問題 4：馬賽克位置不正確

**原因**：座標轉換錯誤

**檢查**：
```python
# 在套用馬賽克前，先繪製框線檢查位置
for (ex, ey, ew, eh) in eyes:
    abs_x = fx + ex
    abs_y = fy + ey

    # 先繪製紅色框線檢查位置
    cv2.rectangle(img, (abs_x, abs_y), (abs_x+ew, abs_y+eh), (0, 0, 255), 2)

print("檢查標記位置：")
cv2_imshow(img)

# 確認無誤後再套用馬賽克
```

**正確的座標轉換**：
```python
# ✅ 正確：眼睛
abs_x = fx + ex
abs_y = fy + ey

# ✅ 正確：嘴巴（在下半部偵測）
abs_x = fx + mx
abs_y = fy + (fh // 2) + my

# ❌ 錯誤：忘記加上人臉座標
abs_x = ex  # 這只是 ROI 內的相對座標
abs_y = ey

# ❌ 錯誤：嘴巴忘記加上 offset
abs_x = fx + mx
abs_y = fy + my  # 忘記加上 (fh // 2)
```

---

## 💡 常見問題 FAQ

### Q1: 為什麼要在人臉區域內偵測五官，而不是在整張圖？

**A:** 優點：
1. **提高準確度**：縮小搜尋範圍，減少誤判
2. **提高效率**：只搜尋相關區域，速度更快
3. **符合邏輯**：五官一定在人臉內，不會在其他地方

```python
# 比較：
# 方法 A：在整張圖偵測（不推薦）
eyes_all = eye_cascade.detectMultiScale(gray, 1.1, 10)
# 問題：可能偵測到非人臉區域的類眼睛物體（如車燈、窗戶）

# 方法 B：在人臉 ROI 內偵測（推薦）
face_roi_gray = gray[fy:fy+fh, fx:fx+fw]
eyes = eye_cascade.detectMultiScale(face_roi_gray, 1.1, 10)
# 優點：只在人臉內搜尋，準確度高
```

### Q2: 為什麼嘴巴要在人臉下半部偵測？

**A:** 因為嘴巴一定在人臉下半部，這樣可以：
1. 避免將鼻子誤判為嘴巴
2. 提高偵測效率
3. 降低誤判率

```python
# 不限制區域：可能誤判鼻子為嘴巴
mouths = mouth_cascade.detectMultiScale(face_roi_gray, 1.1, 20)

# 限制在下半部：準確度提高
mouth_roi_gray = face_roi_gray[fh//2:, :]  # 只搜尋下半部
mouths = mouth_cascade.detectMultiScale(mouth_roi_gray, 1.1, 20)
```

### Q3: 可以偵測鼻子嗎？

**A:** 可以，使用 `haarcascade_mcs_nose.xml`：

```python
# 下載鼻子模型
url = 'https://raw.githubusercontent.com/atduskgreg/opencv-processing/master/lib/cascade-files/haarcascade_mcs_nose.xml'
urllib.request.urlretrieve(url, 'haarcascade_mcs_nose.xml')

# 載入模型
nose_cascade = cv2.CascadeClassifier('haarcascade_mcs_nose.xml')

# 在人臉中間區域偵測鼻子
nose_roi_start = fh // 3
nose_roi_end = 2 * fh // 3
nose_roi_gray = face_roi_gray[nose_roi_start:nose_roi_end, :]

noses = nose_cascade.detectMultiScale(nose_roi_gray, 1.1, 15)

for (nx, ny, nw, nh) in noses:
    abs_x = fx + nx
    abs_y = fy + nose_roi_start + ny
    apply_mosaic(img, abs_x, abs_y, nw, nh, level=10)
```

### Q4: 馬賽克和高斯模糊哪個好？

**A:** 各有優缺點：

| 特性 | 馬賽克 | 高斯模糊 |
|------|--------|---------|
| **隱私保護** | 強 | 中等 |
| **視覺效果** | 明顯、突兀 | 柔和、自然 |
| **處理速度** | 快 | 較慢 |
| **可逆性** | 不可逆 | 不可逆 |
| **適用場景** | 新聞、公開場合 | 社交媒體、藝術照 |

**選擇建議**：
- 需要強隱私保護：使用馬賽克（level=5-10）
- 追求自然效果：使用高斯模糊（blur_level=21-31）
- 極致保護：使用黑色遮罩

### Q5: 如何處理側臉照片？

**A:** Haar Cascade 對側臉效果較差，但可以嘗試：

1. **使用側臉模型**：
```python
# 下載側臉模型
url = 'https://raw.githubusercontent.com/opencv/opencv/4.x/data/haarcascades/haarcascade_profileface.xml'
urllib.request.urlretrieve(url, 'haarcascade_profileface.xml')

# 載入並使用
profile_cascade = cv2.CascadeClassifier('haarcascade_profileface.xml')
profile_faces = profile_cascade.detectMultiScale(gray, 1.1, 5)
```

2. **同時偵測正面和側面**：
```python
# 正面人臉
frontal_faces = face_cascade.detectMultiScale(gray, 1.1, 5)

# 側面人臉
profile_faces = profile_cascade.detectMultiScale(gray, 1.1, 5)

# 合併結果
all_faces = list(frontal_faces) + list(profile_faces)
```

3. **使用深度學習模型**（進階）：
- MTCNN、RetinaFace 對各種角度都有較好效果

---

## 📊 評分標準

| 項目 | 配分 | 評分重點 |
|------|------|----------|
| **功能完整性** | 40% | 所有 7 個需求都已實作並正常運作 |
| **程式碼品質** | 25% | 結構清晰、註解完整、變數命名規範、錯誤處理 |
| **執行結果** | 20% | 能正確偵測並馬賽克處理五官 |
| **測試報告** | 10% | 完整記錄測試過程與心得反思 |
| **延伸挑戰** | 5% | 完成至少一項延伸挑戰（加分項） |

---

## 📚 學習資源

### 參考文件
- 主要教學：`opencv_imageclassfy_b05.md`
- OpenCV 官方：[Face Detection](https://docs.opencv.org/4.x/db/d28/tutorial_cascade_classifier.html)
- Haar Cascade 原理：Viola-Jones 演算法

### 相關函數
- `cv2.CascadeClassifier()`：載入分類器
- `detectMultiScale()`：多尺度偵測
- `cv2.resize()`：圖片縮放（用於馬賽克）
- `cv2.GaussianBlur()`：高斯模糊
- ROI 操作：`img[y:y+h, x:x+w]`

### 進階學習
- 深度學習人臉偵測：MTCNN、RetinaFace
- 人臉關鍵點偵測：Dlib、Face Alignment
- 人臉辨識：FaceNet、ArcFace

---

**祝學習順利！記得理解座標轉換的概念，這是本題的關鍵！** 🔒
