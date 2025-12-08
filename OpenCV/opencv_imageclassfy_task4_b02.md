<!-- Path: General_python/openCV/影像辨識-傳統方法 | Timestamp: 2025-10-07 10:00:00 | Version: b02 -->
# 題目四：遊戲畫面道具定位系統

## 📋 任務說明

請撰寫一個 Python 程式，能夠在一張複雜的遊戲畫面截圖中，精準地找到所有指定的道具圖示（例如：藥水、金幣）的位置。本任務的核心是學習 **模板匹配 (Template Matching)** 技術，它適用於尋找外觀、尺寸與旋轉角度固定的物體。

---

## 🖼️ 影像選擇指引

### 適合的影像類型

#### ✅ 推薦使用的影像

1.  **像素級一致的目標**
    -   **特徵**：遊戲 UI 或道具圖示與你要尋找的「模板圖片」在尺寸、角度和外觀上完全一致。
    -   **偵測成功率**：★★★★★（95%+）
    -   **最佳範例**：從原始遊戲截圖中直接、精確地裁剪下來的圖示作為模板。

2.  **高對比度、無遮擋的圖示**
    -   **特徵**：目標圖示完整顯示，且與背景有明顯區別。
    -   **偵測成功率**：★★★★☆（90%+）

#### ⚠️ 效果較差的影像

1.  **經過縮放或旋轉**：模板匹配對尺寸和角度變化**極度敏感**，任何變形都會導致匹配失敗。
2.  **有透明度或特效**：半透明、發光等特效會改變像素值，干擾匹配。
3.  **圖片壓縮失真**：JPG 等有損壓縮會產生噪點，建議模板和主圖都使用 PNG 格式。

#### ❌ 完全不適合的影像

-   目標物有明顯的 3D 旋轉或視角變化。

---

## ✅ 詳細需求列表

### 需求 1：環境準備

**說明**：匯入套件，並建立一個包含多個目標道具的模擬遊戲畫面，以及一個道具模板。

**程式碼提示**：
```python
import cv2
import numpy as np
from google.colab.patches import cv2_imshow

print("="*60 + "\n遊戲畫面道具定位系統\n" + "="*60)

# 建立模擬遊戲畫面與模板
def create_test_images():
    game_screen = np.zeros((600, 800, 3), dtype=np.uint8); game_screen[:] = (128, 64, 0)
    potion_icon = np.zeros((50, 50, 3), dtype=np.uint8); potion_icon[:] = (0, 0, 200)
    cv2.putText(potion_icon, 'P', (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255,255,255), 3)
    # 在多個位置放置圖示，包含一個輕微重疊的狀況，以測試後續處理
    positions = [(100, 150), (500, 80), (300, 400), (110, 160)]
    for x, y in positions: game_screen[y:y+50, x:x+50] = potion_icon
    cv2.imwrite('game_screen.png', game_screen)
    cv2.imwrite('template_potion.png', potion_icon)
    print("✓ 測試圖片 'game_screen.png' 與 'template_potion.png' 建立完成")

create_test_images()
```

---

### 需求 2：讀取圖片與執行模板匹配

**說明**：讀取主畫面與模板，並使用 `cv2.matchTemplate` 執行匹配。此函數會用模板在主畫面上滑動比對，生成一張「熱力圖 (heatmap)」，圖中越亮的位置代表與模板的相似度越高。

**程式碼提示**：
```python
img_rgb = cv2.imread('game_screen.png')
img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
template = cv2.imread('template_potion.png', 0)
w, h = template.shape[::-1]
print(f"✓ 圖片讀取成功，模板尺寸: {w}x{h}\n")

# 執行模板匹配。TM_CCOEFF_NORMED 是最常用的方法，它返回一個標準化的相關係數，
# 結果介於 -1.0 到 1.0 之間，1.0 代表完美匹配。
res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)

print("匹配結果熱力圖 (越亮代表越可能匹配)：")
# 為了方便觀察，我們將熱力圖的灰階值範圍拉伸到 0-255
res_visual = cv2.normalize(res, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
cv2_imshow(res_visual)
```

---

### 需求 3：篩選高相似度位置

**說明**：使用 `np.where` 搭配閾值 (threshold) 從熱力圖中篩選出所有相似度足夠高的點。

**程式碼提示**：
```python
threshold = 0.8 # 設定信賴度閾值
loc = np.where(res >= threshold)
points = list(zip(*loc[::-1])) # 將 (y,x) 座標轉換為 (x,y) 格式
print(f"\n✓ 使用閾值 {threshold} 找到 {len(points)} 個原始匹配點")
```

---

### 需求 4：處理重疊的偵測框 (簡化版 NMS)

**說明**：單一目標周圍常有多個點的匹配值都高於閾值，導致偵測框重疊。我們需要將這些密集的點群組合併，只保留一個最具代表性的中心點。這個過程是**非極大值抑制 (Non-Maximum Suppression, NMS)** 的簡化版。

**程式碼提示**：
```python
def group_rectangles(points, group_threshold=20):
    if not points: return []
    points.sort()
    grouped_points = []
    current_group = [points[0]]
    for i in range(1, len(points)):
        dist_x = abs(points[i][0] - current_group[-1][0])
        dist_y = abs(points[i][1] - current_group[-1][1])
        if dist_x < group_threshold and dist_y < group_threshold:
            current_group.append(points[i])
        else:
            avg_x = int(np.mean([p[0] for p in current_group]))
            avg_y = int(np.mean([p[1] for p in current_group]))
            grouped_points.append((avg_x, avg_y))
            current_group = [points[i]]
    # 處理最後一個群組
    avg_x = int(np.mean([p[0] for p in current_group]))
    avg_y = int(np.mean([p[1] for p in current_group]))
    grouped_points.append((avg_x, avg_y))
    return grouped_points

grouped_points = group_rectangles(points)
print(f"✓ 經過重疊處理，最終確認 {len(grouped_points)} 個獨立目標\n")
```

---

### 需求 5：標記與顯示結果

**說明**：在原始彩色圖片上，根據處理後的座標點繪製矩形框，標示出所有找到的目標。

**程式碼提示**：
```python
img_result = img_rgb.copy()
for i, pt in enumerate(grouped_points):
    cv2.rectangle(img_result, pt, (pt[0] + w, pt[1] + h), (0, 255, 255), 2)
    cv2.putText(img_result, str(i+1), (pt[0] + 5, pt[1] + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    print(f"  目標 {i+1}: 位置 ({pt[0]}, {pt[1]})")

print("\n原始遊戲畫面：")
cv2_imshow(img_rgb)
print("\n標記後的結果：")
cv2_imshow(img_result)

output_filename = 'result_template_matching.png'
cv2.imwrite(output_filename, img_result)
print(f"\n✓ 結果已儲存為 {output_filename}")
```

---

## 📝 完整可執行程式碼

```python
# ========================================
# 題目四：遊戲畫面道具定位系統 (v2)
# ========================================
import cv2
import numpy as np
from google.colab.patches import cv2_imshow

# === 1. 環境準備 ===
def create_test_images():
    game_screen = np.zeros((600, 800, 3), dtype=np.uint8); game_screen[:] = (128, 64, 0)
    potion_icon = np.zeros((50, 50, 3), dtype=np.uint8); potion_icon[:] = (0, 0, 200)
    cv2.putText(potion_icon, 'P', (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255,255,255), 3)
    positions = [(100, 150), (500, 80), (300, 400), (110, 160)]
    for x, y in positions: game_screen[y:y+50, x:x+50] = potion_icon
    cv2.imwrite('game_screen.png', game_screen)
    cv2.imwrite('template_potion.png', potion_icon)
create_test_images()

# === 2. 讀取與匹配 ===
img_rgb = cv2.imread('game_screen.png')
img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
template = cv2.imread('template_potion.png', 0)
w, h = template.shape[::-1]
res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)

# === 3. 篩選與群組 ===
threshold = 0.8
loc = np.where(res >= threshold)
points = list(zip(*loc[::-1]))

def group_rectangles(points, group_threshold=20):
    if not points: return []
    points.sort()
    grouped_points, current_group = [], [points[0]]
    for i in range(1, len(points)):
        dist_x = abs(points[i][0] - current_group[-1][0])
        dist_y = abs(points[i][1] - current_group[-1][1])
        if dist_x < group_threshold and dist_y < group_threshold:
            current_group.append(points[i])
        else:
            avg_x = int(np.mean([p[0] for p in current_group])); avg_y = int(np.mean([p[1] for p in current_group]))
            grouped_points.append((avg_x, avg_y))
            current_group = [points[i]]
    avg_x = int(np.mean([p[0] for p in current_group])); avg_y = int(np.mean([p[1] for p in current_group]))
    grouped_points.append((avg_x, avg_y))
    return grouped_points

grouped_points = group_rectangles(points)
print(f"找到 {len(grouped_points)} 個獨立目標\n")

# === 4. 標記與顯示 ===
img_result = img_rgb.copy()
for i, pt in enumerate(grouped_points):
    cv2.rectangle(img_result, pt, (pt[0] + w, pt[1] + h), (0, 255, 255), 2)
    print(f"  目標 {i+1}: 位置 ({pt[0]}, {pt[1]})")

print("\n標記後的結果：")
cv2_imshow(img_result)
cv2.imwrite('result_template_matching.png', img_result)
```

---

## 🔧 除錯與進階技巧

### 問題 1：找不到目標或誤判太多
**解法**：關鍵在於調整 `threshold`。
-   **找不到目標**：逐步**降低** `threshold` (例如 `0.9` -> `0.8` -> `0.7`)。原因可能是圖片壓縮、微小特效導致無法完美匹配。
-   **誤判太多**：逐步**提高** `threshold` (例如 `0.8` -> `0.9` -> `0.95`)。原因可能是模板太簡單，容易在背景中找到相似區域。

### 挑戰 1：多尺度模板匹配
**問題**：如果目標物大小會變化怎麼辦？
**解法**：將模板縮放成多種尺寸，對每個尺寸都進行一次模板匹配，最後匯總結果。
```python
# 範例：在 80% 到 120% 的尺寸範圍內搜索
for scale in np.linspace(0.8, 1.2, 20):
    resized_template = cv2.resize(template, (int(w * scale), int(h * scale)))
    # ... 執行 matchTemplate 並保存結果 ...
```

### 挑戰 2：遮罩匹配 (Mask Matching)
**問題**：如果模板是不規則形狀（例如圓形藥水），如何忽略矩形框中的背景？
**解法**：為模板建立一個二值化的遮罩 (mask)，在匹配時傳入 `mask` 參數，OpenCV 就會只比對遮罩為白色的區域。

---

## 📚 學習資源

-   OpenCV 官方文件：[Template Matching](https://docs.opencv.org/4.x/d4/dc6/tutorial_py_template_matching.html)
-   PyImageSearch 教學 (含多尺度匹配)：[OpenCV Template Matching](https://pyimagesearch.com/2021/03/22/opencv-template-matching-cv2-matchtemplate/)

```
```