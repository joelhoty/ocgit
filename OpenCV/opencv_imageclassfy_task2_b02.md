<!-- Path: General_python/openCV/影像辨識-傳統方法 | Timestamp: 2025-10-06 18:00:00 | Version: b02 -->
# 題目二：紅綠燈辨識系統

## 📋 任務說明

請撰寫一個 Python 程式，能夠辨識圖片中的紅綠燈，偵測紅、黃、綠三種燈號的狀態，並在畫面上標示出當前亮起的燈號（例如：「紅燈」、「綠燈」等）。

---

## 🖼️ 影像選擇指引

### 適合的影像類型

#### ✅ 推薦使用的影像

1. **清晰的紅綠燈照片**
   - 特徵：紅綠燈清晰可見、燈號明亮
   - 距離：5-30 公尺內拍攝
   - 偵測成功率：★★★★★（95%+）
   - 最佳範例：
     ```
     ✅ 白天拍攝的紅綠燈（光線充足）
     ✅ 燈號清晰發光（紅/黃/綠其中一個亮）
     ✅ 紅綠燈在畫面中央、佔比適中
     ✅ 背景相對簡單（天空、建築物）
     ```

2. **直視角度拍攝**
   - 特徵：鏡頭正對紅綠燈，非極端仰角或俯角
   - 角度建議：
     ```
     ✅ 正面直視（0-15°）     → 最佳
     ⚠️ 微側面（15-30°）      → 尚可
     ❌ 大角度側面（>45°）    → 效果差
     ❌ 極端仰角/俯角（>60°） → 燈號可能變形
     ```
   - 偵測成功率：★★★★☆（85%+）

3. **單一紅綠燈為主**
   - 特徵：畫面中主要是一組紅綠燈
   - 偵測成功率：★★★★★（90%+）
   - 範例：
     ```
     ✅ 路口單一紅綠燈
     ✅ 行人專用紅綠燈
     ⚠️ 多組紅綠燈（可能混淆）
     ❌ 遠處小型紅綠燈（像素不足）
     ```

4. **光線充足的照片**
   - 特徵：白天或傍晚、燈號清晰發光
   - 拍攝時間：
     ```
     ✅ 白天晴天          → 最佳（對比清晰）
     ✅ 陰天              → 良好
     ✅ 傍晚/清晨         → 尚可（燈號較亮）
     ⚠️ 夜間              → 需要調整參數
     ❌ 逆光              → 燈號可能過曝
     ```
   - 偵測成功率：★★★★☆（85%+）

#### ⚠️ 效果較差的影像

1. **背景複雜的照片**
   - 問題：
     - 背景有紅色招牌、紅磚牆 → 誤判紅燈
     - 背景有綠色植物、草地 → 誤判綠燈
     - 廣告看板的彩色燈光 → 干擾偵測
   - 偵測成功率：★★☆☆☆（50-70%）
   - 改善方法：
     - 提高輪廓面積閾值
     - 加入圓形度檢測
     - 使用更精確的 HSV 範圍

2. **燈號不亮或微弱**
   - 問題：
     - 白天燈號關閉 → 顏色不明顯
     - 燈號故障閃爍 → 可能偵測不到
     - 燈號被遮擋 → 部分可見
   - 偵測成功率：★★☆☆☆（40-60%）
   - 最佳狀態：至少一個燈號清晰發光

3. **紅綠燈過小或過遠**
   - 問題：燈號像素不足（< 10×10 px）
   - 偵測成功率：★☆☆☆☆（20-40%）
   - 最小尺寸建議：每個燈號至少 15×15 像素

4. **天氣不佳的照片**
   - 問題：
     - 大雨、大霧 → 視線模糊
     - 雪天 → 紅綠燈被雪覆蓋
     - 強烈陽光反射 → 過曝
   - 偵測成功率：★★☆☆☆（30-60%）

#### ❌ 完全不適合的影像

- 黑白照片（無色彩資訊）
- 極度模糊或晃動的照片
- 紅綠燈完全熄滅的照片
- 紅綠燈被完全遮擋
- 極端逆光導致過曝

### 不同紅綠燈類型的影像需求

#### 標準直立式紅綠燈
```
構造：上紅、中黃、下綠（垂直排列）
最佳拍攝：
✅ 正面拍攝，三個燈都清晰可見
✅ 其中一個燈明亮發光
✅ 距離適中（5-20m）

影像特徵：
- 三個圓形燈號垂直排列
- 燈號大小相似
- 間距均勻
```

#### 橫式紅綠燈
```
構造：左紅、中黃、右綠（水平排列）
最佳拍攝：
✅ 平視角度
✅ 避免極端側角

影像特徵：
- 三個圓形燈號水平排列
- 燈號大小相似
```

#### 行人號誌
```
構造：上紅（站立人形）、下綠（行走人形）
最佳拍攝：
✅ 清晰可見人形符號
✅ 燈號明亮

注意：
本題目主要針對圓形車輛紅綠燈
行人號誌可作為進階挑戰
```

### 測試影像建議

#### 初學者測試（難度：★☆☆☆☆）

**自行建立簡單測試圖**
```python
# 建立模擬紅綠燈圖片
import numpy as np
import cv2

# 建立 600x400 深灰色畫布（模擬天空/背景）
img = np.ones((600, 400, 3), dtype=np.uint8) * 100

# 繪製紅綠燈外框（黑色矩形）
cv2.rectangle(img, (150, 100), (250, 450), (30, 30, 30), -1)

# 繪製三個燈號位置（深灰色圓形 = 熄滅狀態）
cv2.circle(img, (200, 180), 35, (60, 60, 60), -1)  # 紅燈位置
cv2.circle(img, (200, 300), 35, (60, 60, 60), -1)  # 黃燈位置
cv2.circle(img, (200, 420), 35, (60, 60, 60), -1)  # 綠燈位置

# 讓其中一個燈亮起（例如：紅燈）
cv2.circle(img, (200, 180), 35, (0, 0, 255), -1)  # 紅燈亮

cv2.imwrite('test_traffic_light.jpg', img)
```

**特點**：
- 背景簡單，無干擾
- 燈號清晰、顏色飽和
- 預期結果：100% 偵測成功

#### 中級測試（難度：★★★☆☆）

**拍攝真實紅綠燈**
```
建議場景：
1. 路口紅綠燈（白天、晴天）
2. 距離 10-15 公尺
3. 使用手機相機拍攝
4. 正面角度

拍攝要點：
- 確保至少一個燈號亮起
- 背景盡量簡單（如天空）
- 避免逆光
- 紅綠燈佔畫面 1/4 到 1/2

預期結果：80-90% 偵測成功
```

#### 進階測試（難度：★★★★☆）

**複雜場景**
```
挑戰場景：
1. 繁忙路口（多組紅綠燈）
2. 夜間紅綠燈
3. 有招牌干擾的街道
4. 雨天或陰天拍攝

挑戰點：
- 背景複雜
- 光線條件差
- 可能有多個紅綠燈
- 需要精確辨識是哪一個

預期結果：60-75% 偵測成功
需要：精細調整參數、加入額外篩選條件
```

### 紅綠燈 HSV 顏色範圍

不同燈號的 HSV 範圍參考：

| 燈號 | H (色相) | S (飽和度) | V (亮度) | 備註 |
|------|---------|-----------|---------|------|
| 紅燈 | 0-10 或 170-180 | 150-255 | 150-255 | 亮起時飽和度和亮度高 |
| 黃燈 | 20-35 | 150-255 | 200-255 | 偏黃橙色 |
| 綠燈 | 40-80 | 100-255 | 150-255 | 範圍較寬 |

**注意**：
- 亮起的燈號：高 S（飽和度）、高 V（亮度）
- 熄滅的燈號：低 S、低 V（接近灰色）
- 需根據實際照片微調

### 影像品質檢查清單

測試前請確認：
- [ ] 影像格式：JPG、PNG
- [ ] 解析度：至少 640×480（建議 1024×768）
- [ ] 紅綠燈清晰可見
- [ ] 至少一個燈號明亮發光
- [ ] 拍攝角度：正面或微側面（< 30°）
- [ ] 背景：盡量簡單（天空最佳）
- [ ] 光線：充足均勻
- [ ] 燈號大小：每個燈至少 15×15 像素

---

## ✅ 詳細需求列表

### 需求 1：匯入套件與建立測試圖片

**說明**：匯入必要套件，並建立模擬紅綠燈的測試圖片。

**程式碼提示**：
```python
import cv2
import numpy as np
from google.colab.patches import cv2_imshow

print("="*60)
print("紅綠燈辨識系統")
print("="*60)

# 建立模擬紅綠燈測試圖片
def create_traffic_light(light_on='red'):
    """
    建立模擬紅綠燈圖片

    參數:
        light_on: 'red', 'yellow', 'green' 或 'none'
    """
    # 建立 600x400 深灰色畫布
    img = np.ones((600, 400, 3), dtype=np.uint8) * 100

    # 繪製紅綠燈外框
    cv2.rectangle(img, (150, 100), (250, 450), (30, 30, 30), -1)

    # 定義三個燈的位置
    red_pos = (200, 180)
    yellow_pos = (200, 300)
    green_pos = (200, 420)
    radius = 35

    # 繪製熄滅狀態的燈（深灰色）
    cv2.circle(img, red_pos, radius, (60, 60, 60), -1)
    cv2.circle(img, yellow_pos, radius, (60, 60, 60), -1)
    cv2.circle(img, green_pos, radius, (60, 60, 60), -1)

    # 根據參數點亮對應的燈
    if light_on == 'red':
        cv2.circle(img, red_pos, radius, (0, 0, 255), -1)      # BGR: 紅色
    elif light_on == 'yellow':
        cv2.circle(img, yellow_pos, radius, (0, 255, 255), -1)  # BGR: 黃色
    elif light_on == 'green':
        cv2.circle(img, green_pos, radius, (0, 255, 0), -1)    # BGR: 綠色

    return img

# 建立測試圖片（預設紅燈亮）
img = create_traffic_light('red')  # 可改為 'yellow' 或 'green'

print("✓ 測試圖片建立完成")
print(f"圖片尺寸: {img.shape[1]} x {img.shape[0]} 像素")

# 顯示原始測試圖片
print("\n原始測試圖片：")
cv2_imshow(img)

# 保存原圖副本
img_result = img.copy()
```

---

### 需求 2：設定紅綠燈顏色 HSV 範圍

**說明**：定義紅、黃、綠三種燈號的 HSV 範圍。

**程式碼提示**：
```python
# 定義紅綠燈顏色範圍字典
traffic_light_colors = {
    '紅燈': {
        'lower': np.array([0, 150, 150]),      # HSV 下限
        'upper': np.array([10, 255, 255]),     # HSV 上限
        'display_color': (0, 0, 255),          # BGR 格式（繪製用）
        'status': 'STOP'                       # 狀態
    },
    '黃燈': {
        'lower': np.array([20, 150, 200]),
        'upper': np.array([35, 255, 255]),
        'display_color': (0, 255, 255),
        'status': 'CAUTION'
    },
    '綠燈': {
        'lower': np.array([40, 100, 150]),
        'upper': np.array([80, 255, 255]),
        'display_color': (0, 255, 0),
        'status': 'GO'
    }
}

print("✓ 紅綠燈顏色範圍設定完成")
print("將偵測以下燈號：")
for light_name, info in traffic_light_colors.items():
    print(f"  - {light_name} ({info['status']})")

print("")
```

---

### 需求 3：轉換色彩空間為 HSV

**說明**：將 BGR 圖片轉換為 HSV 格式。

**程式碼提示**：
```python
# 將圖片從 BGR 轉換為 HSV 色彩空間
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
print("✓ 圖片已轉換為 HSV 色彩空間\n")
```

---

### 需求 4：偵測並標記紅綠燈燈號

**說明**：遍歷三種燈號，建立遮罩、尋找輪廓、並進行圓形度檢測。

**程式碼提示**：
```python
# 統計變數
detected_lights = []  # 儲存偵測到的燈號

print("="*60)
print("開始偵測紅綠燈")
print("="*60)

# 遍歷每種燈號
for light_name, light_info in traffic_light_colors.items():
    print(f"\n偵測 {light_name}...")

    # === 步驟 1: 建立顏色遮罩 ===
    mask = cv2.inRange(
        hsv,
        light_info['lower'],
        light_info['upper']
    )

    # 可選：形態學操作，去除雜訊
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)

    # 可選：顯示遮罩（除錯用）
    # print(f"{light_name} 遮罩：")
    # cv2_imshow(mask)

    # === 步驟 2: 尋找輪廓 ===
    contours, _ = cv2.findContours(
        mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    print(f"  找到 {len(contours)} 個輪廓")

    # === 步驟 3: 篩選有效輪廓（圓形度檢測）===
    valid_count = 0
    for contour in contours:
        # 計算輪廓面積
        area = cv2.contourArea(contour)

        # 過濾太小的輪廓
        if area < 200:  # 面積閾值，可調整
            continue

        # 計算輪廓的周長
        perimeter = cv2.arcLength(contour, True)

        if perimeter == 0:
            continue

        # 計算圓形度：4π * 面積 / 周長^2
        # 完美圓形的圓形度 = 1.0
        # 一般接受範圍：0.7 ~ 1.3
        circularity = 4 * np.pi * area / (perimeter * perimeter)

        # 只接受接近圓形的輪廓
        if 0.7 < circularity < 1.3:
            valid_count += 1

            # 取得邊界矩形（用於標記）
            x, y, w, h = cv2.boundingRect(contour)

            # 計算中心點
            center_x = x + w // 2
            center_y = y + h // 2

            # 繪製圓形標記
            radius = max(w, h) // 2 + 5
            cv2.circle(
                img_result,
                (center_x, center_y),
                radius,
                light_info['display_color'],
                3
            )

            # 加上文字標籤
            label = f"{light_name} ({light_info['status']})"
            cv2.putText(
                img_result,
                label,
                (x, y - 10 if y > 40 else y + h + 25),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                light_info['display_color'],
                2
            )

            # 記錄偵測結果
            detected_lights.append({
                'name': light_name,
                'status': light_info['status'],
                'position': (center_x, center_y),
                'area': area,
                'circularity': circularity
            })

            print(f"    ✓ {light_name}: 位置({center_x},{center_y}), "
                  f"面積{area:.0f}px, 圓形度{circularity:.2f}")

    if valid_count == 0:
        print(f"  ✗ 未偵測到有效的{light_name}")

print("\n" + "="*60)
```

---

### 需求 5：判斷紅綠燈狀態

**說明**：根據偵測結果，判斷當前紅綠燈的狀態。

**程式碼提示**：
```python
# 判斷紅綠燈狀態
print("紅綠燈狀態判斷")
print("="*60)

if len(detected_lights) == 0:
    current_status = "未知（無燈號偵測）"
    print("⚠️ 未偵測到任何亮起的燈號")
elif len(detected_lights) == 1:
    # 只有一個燈亮
    light = detected_lights[0]
    current_status = f"{light['name']} - {light['status']}"
    print(f"✓ 當前狀態: {current_status}")
else:
    # 多個燈亮（異常情況或誤判）
    print(f"⚠️ 警告: 偵測到 {len(detected_lights)} 個亮燈")
    print("可能原因：")
    print("  1. 多組紅綠燈")
    print("  2. 背景干擾（誤判）")
    print("  3. 燈號切換瞬間")

    # 列出所有偵測到的燈
    for i, light in enumerate(detected_lights, 1):
        print(f"  {i}. {light['name']} - {light['status']}")

    # 取面積最大的作為主要燈號
    main_light = max(detected_lights, key=lambda x: x['area'])
    current_status = f"{main_light['name']} - {main_light['status']} (主要)"
    print(f"\n推測主要狀態: {current_status}")

print("="*60 + "\n")
```

---

### 需求 6：顯示結果與統計

**說明**：顯示處理結果並輸出統計資訊。

**程式碼提示**：
```python
# 在圖片上顯示狀態資訊
info_y = 40
cv2.putText(
    img_result,
    f"Status: {current_status}",
    (10, info_y),
    cv2.FONT_HERSHEY_SIMPLEX,
    0.8,
    (255, 255, 255),
    2
)

cv2.putText(
    img_result,
    f"Detected: {len(detected_lights)} light(s)",
    (10, info_y + 35),
    cv2.FONT_HERSHEY_SIMPLEX,
    0.6,
    (255, 255, 255),
    2
)

# 顯示統計
print("偵測統計：")
print(f"  偵測到的燈號數量: {len(detected_lights)}")
for light in detected_lights:
    print(f"  - {light['name']}: 位置{light['position']}")

# 顯示原圖和結果
print("\n原始圖片：")
cv2_imshow(img)

print("\n標記後的結果：")
cv2_imshow(img_result)

# 儲存結果
output_filename = 'result_traffic_light.jpg'
cv2.imwrite(output_filename, img_result)
print(f"\n✓ 結果已儲存為 {output_filename}")
```

---

## 📝 完整可執行程式碼

```python
# ========================================
# 題目二：紅綠燈辨識系統
# ========================================

import cv2
import numpy as np
from google.colab.patches import cv2_imshow

print("="*60)
print("紅綠燈辨識系統")
print("="*60)

# === 1. 建立測試圖片 ===
def create_traffic_light(light_on='red'):
    """建立模擬紅綠燈圖片"""
    img = np.ones((600, 400, 3), dtype=np.uint8) * 100
    cv2.rectangle(img, (150, 100), (250, 450), (30, 30, 30), -1)

    red_pos = (200, 180)
    yellow_pos = (200, 300)
    green_pos = (200, 420)
    radius = 35

    # 繪製熄滅狀態
    cv2.circle(img, red_pos, radius, (60, 60, 60), -1)
    cv2.circle(img, yellow_pos, radius, (60, 60, 60), -1)
    cv2.circle(img, green_pos, radius, (60, 60, 60), -1)

    # 點亮指定燈號
    if light_on == 'red':
        cv2.circle(img, red_pos, radius, (0, 0, 255), -1)
    elif light_on == 'yellow':
        cv2.circle(img, yellow_pos, radius, (0, 255, 255), -1)
    elif light_on == 'green':
        cv2.circle(img, green_pos, radius, (0, 255, 0), -1)

    return img

# 建立測試圖片
img = create_traffic_light('red')  # 可改為 'yellow', 'green'
img_result = img.copy()

print("✓ 測試圖片建立完成\n")
print("原始測試圖片：")
cv2_imshow(img)

# === 2. 設定顏色範圍 ===
traffic_light_colors = {
    '紅燈': {
        'lower': np.array([0, 150, 150]),
        'upper': np.array([10, 255, 255]),
        'display_color': (0, 0, 255),
        'status': 'STOP'
    },
    '黃燈': {
        'lower': np.array([20, 150, 200]),
        'upper': np.array([35, 255, 255]),
        'display_color': (0, 255, 255),
        'status': 'CAUTION'
    },
    '綠燈': {
        'lower': np.array([40, 100, 150]),
        'upper': np.array([80, 255, 255]),
        'display_color': (0, 255, 0),
        'status': 'GO'
    }
}

print("\n✓ 顏色範圍設定完成")

# === 3. 轉換色彩空間 ===
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# === 4. 偵測燈號 ===
detected_lights = []

print("\n" + "="*60)
print("開始偵測紅綠燈")
print("="*60)

for light_name, light_info in traffic_light_colors.items():
    print(f"\n偵測 {light_name}...")

    # 建立遮罩
    mask = cv2.inRange(hsv, light_info['lower'], light_info['upper'])

    # 形態學操作去除雜訊
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)

    # 尋找輪廓
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    print(f"  找到 {len(contours)} 個輪廓")

    # 篩選圓形輪廓
    for contour in contours:
        area = cv2.contourArea(contour)

        if area < 200:
            continue

        perimeter = cv2.arcLength(contour, True)
        if perimeter == 0:
            continue

        # 圓形度檢測
        circularity = 4 * np.pi * area / (perimeter * perimeter)

        if 0.7 < circularity < 1.3:
            x, y, w, h = cv2.boundingRect(contour)
            center_x = x + w // 2
            center_y = y + h // 2
            radius = max(w, h) // 2 + 5

            # 繪製標記
            cv2.circle(img_result, (center_x, center_y), radius,
                      light_info['display_color'], 3)

            label = f"{light_name} ({light_info['status']})"
            cv2.putText(img_result, label, (x, y - 10 if y > 40 else y + h + 25),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                       light_info['display_color'], 2)

            # 記錄結果
            detected_lights.append({
                'name': light_name,
                'status': light_info['status'],
                'position': (center_x, center_y),
                'area': area,
                'circularity': circularity
            })

            print(f"    ✓ {light_name}: 位置({center_x},{center_y}), "
                  f"面積{area:.0f}px, 圓形度{circularity:.2f}")

# === 5. 判斷狀態 ===
print("\n" + "="*60)
print("紅綠燈狀態判斷")
print("="*60)

if len(detected_lights) == 0:
    current_status = "未知"
    print("⚠️ 未偵測到任何亮起的燈號")
elif len(detected_lights) == 1:
    light = detected_lights[0]
    current_status = f"{light['name']} - {light['status']}"
    print(f"✓ 當前狀態: {current_status}")
else:
    print(f"⚠️ 偵測到 {len(detected_lights)} 個亮燈")
    main_light = max(detected_lights, key=lambda x: x['area'])
    current_status = f"{main_light['name']} - {main_light['status']}"
    print(f"推測主要狀態: {current_status}")

# === 6. 顯示結果 ===
cv2.putText(img_result, f"Status: {current_status}", (10, 40),
           cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

cv2.putText(img_result, f"Detected: {len(detected_lights)} light(s)", (10, 75),
           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

print("\n標記後的結果：")
cv2_imshow(img_result)

cv2.imwrite('result_traffic_light.jpg', img_result)
print("\n✓ 結果已儲存為 result_traffic_light.jpg")
```

---

## 🎯 測試建議

### 測試 1：不同燈號測試

```python
# 測試三種燈號
light_states = ['red', 'yellow', 'green']

for state in light_states:
    print(f"\n{'='*60}")
    print(f"測試: {state.upper()} 燈")
    print(f"{'='*60}")

    img = create_traffic_light(state)
    # ... 執行完整偵測流程 ...

    cv2.imwrite(f'test_{state}_light.jpg', img_result)
```

### 測試 2：使用真實照片

```python
# 上傳真實紅綠燈照片
from google.colab import files
uploaded = files.upload()

# 讀取照片
img = cv2.imread('your_traffic_light.jpg')

# 其餘程式碼相同...
```

### 測試 3：調整 HSV 範圍

```python
# 針對實際照片調整紅燈的 HSV 範圍
red_ranges = [
    ([0, 150, 150], [10, 255, 255]),    # 嚴格
    ([0, 120, 120], [10, 255, 255]),    # 寬鬆
    ([0, 100, 100], [15, 255, 255]),    # 更寬鬆
]

for lower, upper in red_ranges:
    mask = cv2.inRange(hsv, np.array(lower), np.array(upper))
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    valid = sum(1 for c in contours if cv2.contourArea(c) > 200)
    print(f"H:{lower[0]}-{upper[0]}, S:{lower[1]}+, V:{lower[2]}+: {valid} 個紅燈")
```

---

## 🚀 延伸挑戰（選做）

### 挑戰 1：偵測紅綠燈方向（直行/左轉/右轉）

```python
# 根據箭頭形狀判斷方向
# 提示：使用模板匹配或更複雜的形狀分析

# 定義箭頭類型
arrow_types = {
    '直行': 'straight',
    '左轉': 'left',
    '右轉': 'right'
}

# 可以使用輪廓的長寬比、方向等特徵
for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    aspect_ratio = w / h

    if aspect_ratio > 1.2:
        arrow_type = '左轉或右轉'
    else:
        arrow_type = '直行'
```

### 挑戰 2：計算紅綠燈剩餘時間

```python
# 如果紅綠燈有數字顯示，使用 OCR 辨識
# 需要額外的 pytesseract 套件

import pytesseract

# 擷取數字顯示區域
number_region = img[y:y+h, x:x+w]

# 轉換為灰階
gray_region = cv2.cvtColor(number_region, cv2.COLOR_BGR2GRAY)

# OCR 辨識
text = pytesseract.image_to_string(gray_region, config='--psm 6 digits')
remaining_time = text.strip()

print(f"剩餘時間: {remaining_time} 秒")
```

### 挑戰 3：影片即時辨識

```python
# 處理影片中的紅綠燈
cap = cv2.VideoCapture('traffic_video.mp4')

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # 對每一幀進行紅綠燈偵測
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # ... 完整偵測流程 ...

    # 顯示結果
    cv2_imshow(frame)

cap.release()
```

### 挑戰 4：多組紅綠燈辨識

```python
# 在複雜場景中辨識多組紅綠燈
# 並標註「我方」和「對向」

# 根據位置判斷
def classify_traffic_light(center_y, img_height):
    """根據垂直位置判斷紅綠燈是哪一方的"""
    if center_y < img_height * 0.4:
        return "對向"
    elif center_y > img_height * 0.6:
        return "我方"
    else:
        return "側向"

# 為每個偵測到的燈加上分類
for light in detected_lights:
    classification = classify_traffic_light(light['position'][1], img.shape[0])
    light['classification'] = classification
    print(f"{light['name']} - {classification}")
```

---

## 🔧 除錯技巧

### 問題 1：偵測不到紅綠燈

**診斷工具**：
```python
# 顯示 HSV 遮罩，檢查顏色範圍是否正確
for light_name, light_info in traffic_light_colors.items():
    mask = cv2.inRange(hsv, light_info['lower'], light_info['upper'])
    print(f"\n{light_name} 遮罩：")
    cv2_imshow(mask)

    # 檢查遮罩中的白色像素數量
    white_pixels = cv2.countNonZero(mask)
    total_pixels = mask.shape[0] * mask.shape[1]
    percentage = (white_pixels / total_pixels) * 100

    print(f"{light_name} 遮罩覆蓋率: {percentage:.2f}%")

    if percentage < 0.1:
        print(f"⚠️ {light_name} 遮罩幾乎沒有內容，請調整 HSV 範圍")
```

### 問題 2：背景干擾（誤判）

**解決方法**：
```python
# 方法 1：提高面積閾值
min_area = 500  # 增加到 500 或 1000

# 方法 2：加入圓形度檢測（已在程式中）
if 0.7 < circularity < 1.3:  # 只接受接近圓形

# 方法 3：限制偵測區域（如果知道紅綠燈大概位置）
# 只在畫面上半部偵測
roi_y_start = 0
roi_y_end = img.shape[0] // 2
roi = hsv[roi_y_start:roi_y_end, :]

mask = cv2.inRange(roi, light_info['lower'], light_info['upper'])

# 方法 4：加入位置關係檢測
# 紅綠燈的三個燈應該垂直或水平排列
def check_alignment(lights):
    """檢查燈號是否對齊（垂直或水平）"""
    if len(lights) < 2:
        return True

    positions = [light['position'] for light in lights]

    # 檢查垂直對齊（x 座標相近）
    x_coords = [pos[0] for pos in positions]
    x_variance = np.var(x_coords)

    # 檢查水平對齊（y 座標相近）
    y_coords = [pos[1] for pos in positions]
    y_variance = np.var(y_coords)

    # 如果 x 或 y 座標的變異數很小，表示對齊
    return x_variance < 100 or y_variance < 100
```

### 問題 3：夜間或暗處偵測失敗

**解決方法**：
```python
# 方法 1：降低 V (亮度) 的下限
'紅燈': {
    'lower': np.array([0, 150, 100]),  # V 從 150 降到 100
    'upper': np.array([10, 255, 255]),
    ...
}

# 方法 2：影像預處理 - 提高亮度和對比度
img_enhanced = cv2.convertScaleAbs(img, alpha=1.5, beta=30)

# 方法 3：使用自適應處理
# 根據影像的平均亮度動態調整 HSV 範圍
mean_brightness = np.mean(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY))

if mean_brightness < 100:  # 暗處
    v_min = 80
else:  # 亮處
    v_min = 150
```

### 問題 4：紅色偵測不完整

**原因**：紅色在 HSV 橫跨 0-10 和 170-180

**完整解決方法**：
```python
# 紅燈需要兩個 HSV 範圍
red_lower1 = np.array([0, 150, 150])
red_upper1 = np.array([10, 255, 255])

red_lower2 = np.array([170, 150, 150])
red_upper2 = np.array([180, 255, 255])

# 建立兩個遮罩並合併
mask_red1 = cv2.inRange(hsv, red_lower1, red_upper1)
mask_red2 = cv2.inRange(hsv, red_lower2, red_upper2)
mask_red = cv2.bitwise_or(mask_red1, mask_red2)

# 使用合併後的遮罩
contours, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
```

---

## 💡 常見問題 FAQ

### Q1: 為什麼要使用圓形度檢測？

**A:** 紅綠燈的燈號是圓形的，圓形度檢測可以：
1. 過濾掉矩形的招牌、窗戶
2. 過濾掉不規則形狀的雜訊
3. 提高偵測準確度

```python
# 圓形度公式：4π × 面積 / 周長²
# 完美圓形 = 1.0
# 正方形 ≈ 0.785
# 長方形 < 0.785

circularity = 4 * np.pi * area / (perimeter ** 2)

# 我們接受 0.7 ~ 1.3 的範圍
# 考慮到實際拍攝角度、像素化等因素
```

### Q2: 如何區分紅綠燈和其他紅/綠色物體？

**A:** 多重篩選條件：

1. **顏色** - HSV 範圍（亮起的燈高飽和度、高亮度）
2. **形狀** - 圓形度檢測
3. **大小** - 面積閾值
4. **位置** - 紅綠燈通常在畫面上方
5. **數量** - 三個燈（紅黃綠）
6. **對齊** - 垂直或水平排列

```python
# 綜合判斷函數
def is_traffic_light(contour, hsv, img_height):
    area = cv2.contourArea(contour)

    # 檢查 1: 大小
    if area < 200 or area > 10000:
        return False

    # 檢查 2: 圓形度
    perimeter = cv2.arcLength(contour, True)
    circularity = 4 * np.pi * area / (perimeter ** 2)
    if not (0.7 < circularity < 1.3):
        return False

    # 檢查 3: 位置（紅綠燈通常不在畫面底部）
    x, y, w, h = cv2.boundingRect(contour)
    if y > img_height * 0.8:
        return False

    return True
```

### Q3: 為什麼有時候會同時偵測到多個燈？

**A:** 可能原因：
1. **切換瞬間**：黃燈時紅燈剛熄滅、綠燈未亮
2. **多組紅綠燈**：路口有多個方向的紅綠燈
3. **參數過於寬鬆**：HSV 範圍太寬，誤判其他物體

**處理方法**：
```python
if len(detected_lights) > 1:
    # 方法 1: 取面積最大的
    main_light = max(detected_lights, key=lambda x: x['area'])

    # 方法 2: 檢查是否為同一組紅綠燈
    # 如果三個燈垂直排列且間距相似，則為同一組
    def is_same_group(lights):
        if len(lights) != 3:
            return False

        # 按 y 座標排序
        lights_sorted = sorted(lights, key=lambda x: x['position'][1])

        # 檢查 x 座標是否相近（垂直排列）
        x_coords = [l['position'][0] for l in lights_sorted]
        x_std = np.std(x_coords)

        if x_std > 20:  # x 座標差異太大
            return False

        # 檢查間距是否均勻
        y1, y2, y3 = [l['position'][1] for l in lights_sorted]
        gap1 = y2 - y1
        gap2 = y3 - y2

        if abs(gap1 - gap2) < 20:  # 間距相似
            return True

        return False
```

### Q4: 如何處理傾斜拍攝的紅綠燈？

**A:** 方法：

1. **放寬圓形度範圍**：
```python
# 傾斜角度會讓圓形看起來像橢圓
# 放寬圓形度範圍到 0.6 ~ 1.4
if 0.6 < circularity < 1.4:
    # 接受
```

2. **使用橢圓檢測**：
```python
# 使用 OpenCV 的橢圓擬合
if len(contour) >= 5:  # 至少需要 5 個點
    ellipse = cv2.fitEllipse(contour)
    (center, axes, angle) = ellipse

    # 檢查長短軸比例
    major_axis = max(axes)
    minor_axis = min(axes)
    ratio = major_axis / minor_axis

    if ratio < 2.0:  # 不是太扁的橢圓
        # 這可能是傾斜的紅綠燈
        pass
```

### Q5: 可以用在行車記錄器或自駕車嗎？

**A:** 可以，但需要加強：

**基礎版本（本題目）**：
- 適合：靜態圖片、簡單場景
- 限制：速度、準確率、穩定性

**進階版本（實際應用）**：
1. **使用深度學習**：YOLO、Faster R-CNN
2. **即時處理**：優化演算法、使用 GPU
3. **追蹤技術**：卡爾曼濾波器、光流追蹤
4. **多幀融合**：結合前後幀資訊提高穩定性
5. **距離估計**：根據紅綠燈大小估計距離

```python
# 進階：使用 YOLO 偵測紅綠燈（需要預訓練模型）
import cv2
import numpy as np

# 載入 YOLO 模型（需要事先訓練或下載）
net = cv2.dnn.readNet("yolo_traffic_light.weights", "yolo_traffic_light.cfg")

# 進行偵測
blob = cv2.dnn.blobFromImage(img, 1/255.0, (416, 416), swapRB=True, crop=False)
net.setInput(blob)
outputs = net.forward(net.getUnconnectedOutLayersNames())

# 處理輸出...
```

---

## 📊 評分標準

| 項目 | 配分 | 評分重點 |
|------|------|----------|
| **功能完整性** | 40% | 正確偵測紅黃綠三種燈號、圓形度檢測、狀態判斷 |
| **程式碼品質** | 25% | 結構清晰、註解完整、變數命名規範 |
| **執行結果** | 20% | 能正確辨識紅綠燈狀態、標記清晰 |
| **測試報告** | 10% | 完整記錄測試過程與心得反思 |
| **延伸挑戰** | 5% | 完成至少一項延伸挑戰（加分項） |

---

## 📚 學習資源

### 參考文件
- 主要教學：`opencv_imageclassfy_b05.md`
- OpenCV 官方：[Color Spaces](https://docs.opencv.org/4.x/df/d9d/tutorial_py_colorspaces.html)
- 輪廓分析：[Contour Features](https://docs.opencv.org/4.x/dd/d49/tutorial_py_contour_features.html)

### 相關函數
- `cv2.cvtColor()`：色彩空間轉換
- `cv2.inRange()`：建立顏色遮罩
- `cv2.findContours()`：尋找輪廓
- `cv2.contourArea()`：計算輪廓面積
- `cv2.arcLength()`：計算輪廓周長
- `cv2.morphologyEx()`：形態學操作

### 實際應用
- 自動駕駛系統
- 交通監控系統
- 行車輔助系統（ADAS）
- 智慧城市交通管理

---

**祝學習順利！紅綠燈辨識是電腦視覺的經典應用，掌握後可以應用到更多實際場景！** 🚦
