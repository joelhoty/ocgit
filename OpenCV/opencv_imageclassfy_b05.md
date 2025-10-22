<!-- Path: General_python/openCV/影像辨識-傳統方法 | Timestamp: 2025-10-05 16:00:00 | Version: b05 -->
# OpenCV 影像辨識學習總彙

本篇教學統整了多個 OpenCV 影像辨識的應用，並將所有範例程式碼修改為可直接在 Google Colab 環境中執行。每個章節都增加了更詳細的程式邏輯解說與專有名詞說明，幫助你更深入地理解背後的原理。

## 1. Google Colab 環境設定

在 Colab 中，我們無法直接存取本機檔案或開啟攝影機。因此，我們需要先下載所需的模型檔案和範例圖片，並使用 `google.colab.patches` 中的 `cv2_imshow` 來顯示圖片。

請在 Colab 的程式碼儲存格中執行以下指令來下載所有必要的檔案：

```python
import urllib.request
import os

# 定義所有需要下載的檔案
files = {
    # Haar Cascade 模型檔案
    'haarcascade_frontalface_default.xml': 'https://raw.githubusercontent.com/opencv/opencv/4.x/data/haarcascades/haarcascade_frontalface_default.xml',
    'haarcascade_eye.xml': 'https://raw.githubusercontent.com/opencv/opencv/4.x/data/haarcascades/haarcascade_eye.xml',
    'haarcascade_mcs_mouth.xml': 'https://raw.githubusercontent.com/atduskgreg/opencv-processing/master/lib/cascade-files/haarcascade_mcs_mouth.xml',
    'haarcascade_mcs_nose.xml': 'https://raw.githubusercontent.com/atduskgreg/opencv-processing/master/lib/cascade-files/haarcascade_mcs_nose.xml',
    'haarcascade_fullbody.xml': 'https://raw.githubusercontent.com/opencv/opencv/4.x/data/haarcascades/haarcascade_fullbody.xml',
    'cars.xml': 'https://raw.githubusercontent.com/andrewssobral/vehicle_detection_haarcascades/master/cars.xml',

    # 範例圖片
    'mona.jpg': 'https://steam.oxxostudio.tw/down/python/ai/mona.jpg',
    'cars.jpg': 'https://steam.oxxostudio.tw/down/python/ai/cars.jpg',
    'girl.jpg': 'https://steam.oxxostudio.tw/down/python/ai/girl.jpg'
}

# 下載檔案並顯示進度
for filename, url in files.items():
    if not os.path.exists(filename):
        print(f"下載 {filename}...")
        try:
            urllib.request.urlretrieve(url, filename)
            print(f"✓ {filename} 下載完成")
        except Exception as e:
            print(f"✗ {filename} 下載失敗: {e}")
    else:
        print(f"✓ {filename} 已存在")

print("\n所有檔案準備完成！")
```

## Haar Cascade 技術原理深度解析

### 基本概念

**Haar Cascade (哈爾級聯分類器)** 是一種基於機器學習的物件偵測方法，由 Paul Viola 和 Michael Jones 於 2001 年在論文 "Rapid Object Detection using a Boosted Cascade of Simple Features" 中提出，也常被稱為 **Viola-Jones 演算法**。

這個方法在當時是革命性的創新，因為它首次實現了**即時人臉偵測**，在一般個人電腦上就能達到每秒處理數十幀的速度，這在 2001 年是非常驚人的成就。

---

### 核心技術原理

#### 1. Haar 特徵 (Haar-like Features)

Haar 特徵是由相鄰矩形區域組成的簡單圖案，用於捕捉圖像中的明暗變化。這個概念源自 Haar 小波 (Haar Wavelet)，但經過簡化以提高計算速度。

**基本 Haar 特徵類型**：

```
邊緣特徵 (Edge Features):
┌─────┬─────┐     ┌───────────┐
│ 白  │ 黑  │     │   白色    │
│     │     │     ├───────────┤
└─────┴─────┘     │   黑色    │
                  └───────────┘

線條特徵 (Line Features):
┌────┬────┬────┐
│白  │黑  │白  │
└────┴────┴────┘

對角特徵 (Diagonal Features):
┌────┬────┐
│白  │黑  │
├────┼────┤
│黑  │白  │
└────┴────┘
```

**特徵值計算**：
- 特徵值 = 白色區域像素和 - 黑色區域像素和
- 例如：左右兩個矩形，計算方式為 `右側像素和 - 左側像素和`

**實際應用範例**：
在人臉偵測中，常見的 Haar 特徵包括：
- 眼睛區域通常比周圍臉頰更暗 → 使用水平邊緣特徵
- 鼻樑比鼻翼兩側更亮 → 使用線條特徵
- 眼睛周圍的陰影模式 → 使用對角特徵

---

#### 2. 積分圖 (Integral Image)

為了快速計算 Haar 特徵，Viola 和 Jones 引入了**積分圖**技術，這是演算法能夠高速運行的關鍵。

**積分圖定義**：
積分圖中位置 (x, y) 的值，等於原圖中從左上角 (0, 0) 到 (x, y) 形成的矩形區域內所有像素值的總和。

**數學表示**：
```
II(x, y) = Σ(i≤x, j≤y) I(i, j)
```
其中 I(i, j) 是原始圖像在位置 (i, j) 的像素值。

**快速計算任意矩形區域的像素和**：

給定矩形的四個角點 A、B、C、D：
```
A ──────── B
│          │
│  矩形區  │
│          │
C ──────── D
```

矩形區域的像素和 = `II(D) + II(A) - II(B) - II(C)`

**速度優勢**：
- 傳統方法：計算一個矩形需要 O(w × h) 次操作
- 積分圖方法：只需要 **4 次** 查表和 **3 次** 加減運算
- 無論矩形大小，計算時間都是常數 **O(1)**

這使得即使在一張圖像中計算數萬個 Haar 特徵也能保持高速。

---

#### 3. AdaBoost 演算法 (自適應增強學習)

單個 Haar 特徵的判別能力很弱（稱為「弱分類器」），Viola-Jones 使用 **AdaBoost** 演算法將多個弱分類器組合成一個強分類器。

**訓練過程**：

**步驟 1：初始化權重**
```
對 N 個訓練樣本，初始權重 w_i = 1/N
```

**步驟 2：迭代選擇最佳特徵**
```
For t = 1 to T:
  1. 對每個 Haar 特徵，計算其加權錯誤率
  2. 選擇錯誤率最低的特徵作為弱分類器 h_t
  3. 計算此分類器的權重 α_t
  4. 更新樣本權重：
     - 正確分類的樣本 → 權重降低
     - 錯誤分類的樣本 → 權重提高
```

**步驟 3：組合強分類器**
```
H(x) = sign(Σ α_t × h_t(x))
```

**實際意義**：
- 每次迭代都專注於之前被錯誤分類的「困難樣本」
- 最終的強分類器通常由 100-200 個弱分類器組成
- 每個弱分類器對應一個特定的 Haar 特徵

**範例**：
```
弱分類器 1 (α=0.8): 檢測眼睛區域是否比臉頰暗
弱分類器 2 (α=0.6): 檢測鼻樑是否比鼻翼亮
弱分類器 3 (α=0.5): 檢測眉毛區域的明暗模式
...
最終決策 = 0.8×h1 + 0.6×h2 + 0.5×h3 + ...
```

---

#### 4. 級聯分類器 (Cascade Classifier)

這是 Viola-Jones 演算法最重要的創新。級聯結構像一個「篩子」，快速排除明顯不是目標的區域。

**級聯結構**：

```
輸入圖像區域
     ↓
┌────────────────┐
│  第 1 層 (2 特徵)  │ → 99% 排除率，保留 1% 候選
└────┬───────────┘
     ↓ 通過
┌────────────────┐
│  第 2 層 (10 特徵) │ → 90% 排除率，保留 10% 候選
└────┬───────────┘
     ↓ 通過
┌────────────────┐
│  第 3 層 (25 特徵) │ → 80% 排除率，保留 20% 候選
└────┬───────────┘
     ↓ 通過
      ...
     ↓ 通過
┌────────────────┐
│ 第 N 層 (200特徵)│ → 最終判決
└────┬───────────┘
     ↓
   人臉！
```

**工作原理**：
1. **前幾層**：只有少數特徵（2-10 個），非常快速
   - 目標：快速排除 90% 以上的「絕對不是人臉」的區域
   - 例如：純白天空、均勻牆面等

2. **中間層**：特徵數量逐漸增加（10-50 個）
   - 目標：排除「可能像但不是」的區域
   - 例如：窗戶、車燈等類人臉物體

3. **後幾層**：包含大量特徵（50-200 個），最精細
   - 目標：精確判斷剩餘候選是否為真正的人臉
   - 只有通過所有層的區域才被認定為人臉

**效率優勢**：
```
假設圖像中有 100,000 個候選區域：
- 第 1 層（2 特徵）：處理 100,000 個區域，保留 1,000 個
- 第 2 層（10 特徵）：只處理 1,000 個區域，保留 100 個
- 第 3 層（25 特徵）：只處理 100 個區域，保留 10 個
- ...
- 第 N 層（200特徵）：只處理 <10 個區域

平均每個區域只需計算約 3-5 個特徵，而非全部 200+ 個！
```

**類比**：
就像機場安檢：
1. 第一關：X 光機快速掃描所有行李（簡單快速）
2. 第二關：可疑行李開箱初檢
3. 第三關：仍可疑的詳細檢查
大部分行李在第一關就通過，只有極少數需要深度檢查。

---

#### 5. 多尺度偵測 (Multi-Scale Detection)

由於人臉在圖像中可能有不同大小，演算法需要在多個尺度上掃描。

**掃描策略**：

**方法 A：縮放圖像**（OpenCV 採用）
```
原始圖像 (800×600)
  ↓
縮小 10% → 720×540 → 使用固定大小檢測窗口掃描
  ↓
縮小 20% → 640×480 → 使用固定大小檢測窗口掃描
  ↓
縮小 30% → 560×420 → 使用固定大小檢測窗口掃描
  ...
```

**方法 B：縮放檢測窗口**
```
固定圖像
  ↓
24×24 窗口掃描
  ↓
30×30 窗口掃描
  ↓
40×40 窗口掃描
  ...
```

**滑動窗口**：
```
┌──┐              檢測窗口在圖像上滑動
│  │→ → → → →     步長通常是窗口大小的 10-20%
└──┘   ↓          水平掃描完一行後，垂直移動
    ┌──┐          繼續下一行掃描
    │  │→ → →
    └──┘
```

**scaleFactor 參數**：
```python
scaleFactor = 1.1  # 每次縮小 10%
# 掃描尺度：100% → 90% → 81% → 73% → ...

scaleFactor = 1.05  # 每次縮小 5%
# 掃描尺度：100% → 95% → 90% → 86% → ...
# 更密集 → 更可能找到人臉但更慢
```

---

#### 6. 非極大值抑制 (Non-Maximum Suppression)

多尺度掃描會產生許多重疊的偵測框，需要合併成最終結果。

**問題**：
```
一張人臉可能產生多個偵測框：
┌────┐
│  ┌─┼──┐
│  │ │  │
└──┼─┘  │
   └─────┘
```

**minNeighbors 參數的作用**：
```python
minNeighbors = 3
# 一個偵測框周圍至少要有 3 個其他偵測框重疊
# 才認為是有效偵測

原始偵測結果：
位置 A：6 個重疊框 ✓ (保留)
位置 B：2 個重疊框 ✗ (丟棄，可能是誤判)
位置 C：1 個孤立框 ✗ (丟棄，很可能是雜訊)
```

**合併策略**：
```
1. 將所有重疊的偵測框分組
2. 計算每組的平均位置和大小
3. 只保留「鄰居數量 ≥ minNeighbors」的組
4. 輸出合併後的偵測框
```

---

### 訓練過程詳解

訓練一個 Haar Cascade 人臉偵測器需要以下步驟：

#### 1. 準備訓練資料

**正樣本 (Positive Samples)**：
- 數量：通常需要 5,000 - 10,000 張人臉圖像
- 要求：
  - 包含各種角度（正面、側面、仰角、俯角）
  - 不同光照條件（明亮、昏暗、逆光）
  - 各種年齡、性別、膚色
  - 統一縮放到固定大小（如 24×24 像素）

**負樣本 (Negative Samples)**：
- 數量：通常是正樣本的 2-3 倍（10,000 - 30,000 張）
- 要求：
  - 不包含任何人臉的圖像
  - 包含各種「容易混淆」的物體（窗戶、車燈、圓形物體等）
  - 各種自然場景和紋理

#### 2. 特徵提取與選擇

```
步驟流程：
1. 在 24×24 的窗口中，可能的 Haar 特徵數量 > 180,000 個
2. 使用 AdaBoost 從中選出最具判別力的數百個特徵
3. 對每個特徵，找出最佳閾值來分隔正負樣本
```

**範例**：
```
特徵 #42: 眼睛區域 Haar 特徵
  閾值：-0.5
  規則：如果特徵值 < -0.5 → 可能是人臉
       如果特徵值 ≥ -0.5 → 可能不是人臉
  錯誤率：15%
```

#### 3. 級聯結構訓練

```
For 每一層 i = 1 to N:
  1. 訓練一個強分類器（包含 K_i 個弱分類器）
  2. 調整閾值，使該層能：
     - 保留 ≥99.5% 的正樣本（高召回率）
     - 排除 ≥50% 的負樣本（適度排除率）
  3. 使用當前級聯鏈測試負樣本
  4. 將仍被誤判為人臉的負樣本加入下一層的訓練集
  5. 重複直到達到目標準確率
```

**實際參數範例**：
```
OpenCV haarcascade_frontalface_default.xml 模型：
- 級聯層數：25 層
- 總特徵數：~2,913 個
- 層分布：
  第 1 層：3 個特徵
  第 2 層：5 個特徵
  第 3 層：13 個特徵
  ...
  第 25 層：213 個特徵
```

---

### 優點與限制

#### 優點

1. **速度快**
   - 積分圖使特徵計算為 O(1)
   - 級聯結構使 95% 以上的區域在前幾層就被排除
   - 可在一般 CPU 上達到即時處理（15-30 FPS）

2. **準確率高**
   - 在正面人臉偵測上可達 95% 以上準確率
   - 誤判率低（低假陽性率）

3. **不需要大量計算資源**
   - 2001 年的技術，可在普通 PC 上運行
   - 不需要 GPU 或專用硬體

4. **模型小**
   - `.xml` 模型檔案通常只有幾百 KB
   - 易於部署到嵌入式系統

#### 限制

1. **對姿態變化敏感**
   - 側臉、仰角、俯角會導致偵測率大幅下降
   - 需要針對不同角度訓練多個模型

2. **對光照變化敏感**
   - 極端光照條件（強逆光、全黑）效果不佳
   - 雖然 Haar 特徵有一定抗干擾能力，但仍有限

3. **對遮擋敏感**
   - 口罩、墨鏡、手遮擋會嚴重影響偵測
   - 因為關鍵特徵（眼睛、鼻子、嘴巴）被遮擋

4. **訓練困難**
   - 需要大量標註資料（數萬張圖像）
   - 訓練時間長（數小時到數天）
   - 參數調整需要經驗

5. **無法辨識身份**
   - 只能偵測「是否為人臉」
   - 無法區分「誰的人臉」（需要額外的辨識演算法，如 LBPH）

---

### 與現代深度學習方法的比較

| 特性 | Haar Cascade | 深度學習 (如 MTCNN, RetinaFace) |
|------|--------------|----------------------------------|
| **準確率** | 85-95% (正面臉) | 98-99%+ (各種角度) |
| **速度 (CPU)** | 15-30 FPS | 1-5 FPS |
| **速度 (GPU)** | 15-30 FPS (無提升) | 30-100 FPS |
| **模型大小** | ~1 MB | 10-100 MB |
| **訓練時間** | 數小時-數天 | 數天-數週 |
| **訓練資料** | 5,000-10,000 張 | 100,000-1,000,000 張 |
| **角度適應** | 差 (需多個模型) | 優 (單一模型) |
| **遮擋處理** | 差 | 優 |
| **適用場景** | 資源受限、即時性要求高 | 準確率要求高、有 GPU |

---

### 實務應用建議

**適合使用 Haar Cascade 的情境**：
- ✅ 嵌入式系統（樹莓派、Arduino 等）
- ✅ 低功耗設備
- ✅ 即時影像處理（無 GPU）
- ✅ 正面人臉偵測（如自拍相機、門禁系統）
- ✅ 教學用途（理解傳統電腦視覺）

**建議使用深度學習的情境**：
- ✅ 需要高準確率
- ✅ 各種角度、遮擋、光照條件
- ✅ 有 GPU 資源
- ✅ 需要額外功能（關鍵點偵測、年齡性別辨識等）

---

### 延伸閱讀與參考資料

**經典論文**：
- Viola, P., & Jones, M. (2001). "Rapid Object Detection using a Boosted Cascade of Simple Features". CVPR.
- Viola, P., & Jones, M. (2004). "Robust Real-Time Face Detection". IJCV.

**OpenCV 官方文件**：
- [Cascade Classifier Tutorial](https://docs.opencv.org/4.x/db/d28/tutorial_cascade_classifier.html)
- [Training Cascade Classifier](https://docs.opencv.org/4.x/dc/d88/tutorial_traincascade.html)

**進階主題**：
- LBP Cascade（使用 Local Binary Patterns 代替 Haar 特徵）
- Soft Cascade（改進的級聯結構）
- Multi-view Face Detection（多視角人臉偵測）


---

## 2. 追蹤並標記特定顏色

我們可以透過設定顏色的 HSV 範圍來追蹤畫面中的特定顏色。

### 處理邏輯說明

1.  **色彩空間轉換 (BGR to HSV)**: 相比於電腦螢幕使用的 BGR (藍綠紅) 色彩模型，HSV (色相、飽和度、亮度) 更符合人類對顏色的感知。在 HSV 模型中，顏色 (色相 Hue) 是獨立於飽和度 (Saturation) 和亮度 (Value) 的，這使得在不同光照條件下辨識特定顏色變得更加穩定和準確。
2.  **建立顏色遮罩 (Mask)**: 使用 `cv2.inRange()` 函數，我們可以定義一個顏色的上下限範圍。所有在 BGR 圖像轉換後的 HSV 圖像中，落在這個顏色範圍內的像素會被設定為白色 (255)，其餘的則為黑色 (0)。這樣就產生了一個二值化的「遮罩」，只突顯出我們感興趣的顏色區域。
3.  **尋找輪廓 (Contours)**: `cv2.findContours()` 函數會分析這個遮罩，找出所有連續的白色區域，並將這些區域的邊界點記錄下來，形成「輪廓」。
4.  **繪製邊界框 (Bounding Box)**: 遍歷所有找到的輪廓，我們可以計算每個輪廓的面積 (`cv2.contourArea`) 來過濾掉過小的雜訊。對於足夠大的輪廓，使用 `cv2.boundingRect()` 計算出能剛好包圍它的最小矩形，並將這個矩形繪製回原始圖像上，從而標記出目標物體。

### 常見顏色的 HSV 範圍參考表

| 顏色 | H (色相) 範圍 | S (飽和度) 範圍 | V (亮度) 範圍 | 備註 |
|------|--------------|----------------|--------------|------|
| 紅色 | 0-10 或 170-180 | 40-255 | 40-255 | 紅色橫跨 HSV 色環兩端 |
| 橙色 | 11-25 | 40-255 | 40-255 | - |
| 黃色 | 26-40 | 40-255 | 40-255 | - |
| 綠色 | 41-80 | 40-255 | 40-255 | - |
| 青色 | 81-100 | 40-255 | 40-255 | - |
| 藍色 | 101-130 | 40-255 | 40-255 | - |
| 紫色 | 131-160 | 40-255 | 40-255 | - |
| 粉紅 | 161-169 | 40-255 | 40-255 | - |

**專有名詞說明：**
- **HSV (Hue-Saturation-Value)**: 色相-飽和度-明度色彩模型，其中 H (0-180) 代表顏色種類，S (0-255) 代表顏色純度，V (0-255) 代表明暗程度。
- **Contour (輪廓)**: 圖像中連續點的曲線，這些點具有相同的顏色或強度，常用於形狀分析和物件偵測。

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

# 視覺化結果
print("原始圖像:")
cv2_imshow(img)
print("\nHSV 遮罩 (白色 = 偵測到的紅色區域):")
cv2_imshow(mask)
print("\n標記後的結果:")
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

### 參數調校技巧

- **scaleFactor 調整**:
  - `1.05` → 偵測更精準、速度較慢、可能找到更多人臉
  - `1.1` → 平衡的選擇（推薦起始值）
  - `1.3` → 偵測較快、可能遺漏較小的人臉

- **minNeighbors 調整**:
  - `3` → 可能產生較多誤判，但不會遺漏真實人臉
  - `5` → 平衡的選擇（推薦起始值）
  - `8-10` → 大幅減少誤判，但可能遺漏部分真實人臉

- **調校建議**: 從 `(scaleFactor=1.1, minNeighbors=5)` 開始測試，根據結果微調。若誤判太多則提高 `minNeighbors`，若遺漏人臉則降低 `scaleFactor`。

### 範例：偵測圖片中的人臉

```python
# 在 Colab 中執行
import cv2
import numpy as np
from google.colab.patches import cv2_imshow

# 讀取圖片並檢查是否成功
img = cv2.imread('mona.jpg')
if img is None:
    print("錯誤: 無法讀取圖片，請確認檔案已正確下載")
else:
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 載入人臉模型
    face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    # 偵測人臉
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    # 繪製人臉方框
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

    print(f"偵測到 {len(faces)} 張人臉")
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

**專有名詞說明：**
- **INTER_LINEAR (雙線性插值)**: 使用周圍 2x2 鄰域的像素進行加權平均，產生平滑的結果。
- **INTER_NEAREST (最近鄰插值)**: 直接使用最近的像素值，不進行平滑處理，放大時會產生方塊狀效果。

### 範例：將偵測到的人臉打上馬賽克

```python
# 在 Colab 中執行
import cv2
from google.colab.patches import cv2_imshow

img = cv2.imread('mona.jpg')
if img is None:
    print("錯誤: 無法讀取圖片，請確認檔案已正確下載")
else:
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    faces = face_cascade.detectMultiScale(gray, 1.2, 3)

    for (x, y, w, h) in faces:
        # 擷取人臉區域
        mosaic = img[y:y+h, x:x+w]
        level = 15 # 馬賽克程度，數值越小越模糊
        mh = max(1, int(h/level))  # 確保至少為 1
        mw = max(1, int(w/level))  # 確保至少為 1
        # 先縮小再放大，產生馬賽克效果
        mosaic = cv2.resize(mosaic, (mw, mh), interpolation=cv2.INTER_LINEAR)
        mosaic = cv2.resize(mosaic, (w, h), interpolation=cv2.INTER_NEAREST)
        # 將馬賽克放回原圖
        img[y:y+h, x:x+w] = mosaic

    print(f"已對 {len(faces)} 張人臉進行馬賽克處理")
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
if img is None:
    print("錯誤: 無法讀取圖片，請確認檔案已正確下載")
else:
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

    print(f"偵測結果: {len(eyes)} 個眼睛, {len(noses)} 個鼻子, {len(mouths)} 個嘴巴")
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
if img is None:
    print("錯誤: 無法讀取圖片，請確認檔案已正確下載")
else:
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

    print(f"偵測結果: {len(pedestrians)} 個行人, {len(cars)} 輛汽車")
    print("行人(綠)與汽車(藍)偵測結果：")
    cv2_imshow(img)
```

---

## 7. 單物件追蹤

在 Colab 中，我們無法使用 `cv2.selectROI` 進行互動式選取。因此，我們需要手動指定要追蹤的物件初始位置 (Bounding Box)。

### 處理邏輯說明

物件追蹤與物件偵測不同。偵測是在每一幀都重新尋找物件，而追蹤則是在第一幀指定物件後，試圖在後續的每一幀中「跟隨」這個物件。

1.  **建立追蹤器**: `cv2.legacy.TrackerCSRT_create()` 會建立一個 CSRT 追蹤器。
2.  **初始化追蹤器**: `tracker.init(frame, bbox)` 是關鍵步驟。我們提供第一幀影像和一個手動指定的 `bbox` (bounding box，格式為 `(x, y, w, h)`) 給追蹤器，告訴它「這就是你要追蹤的目標」。
3.  **更新追蹤器**: 在迴圈中，對影片的每一幀呼叫 `tracker.update(frame)`。追蹤器會在這新的一幀中尋找它認為是目標的物體，並返回兩個值：`success` (布林值，表示是否成功追蹤到) 和更新後的 `bbox`。
4.  **繪製結果**: 如果 `success` 為 `True`，我們就用新的 `bbox` 繪製方框，實現視覺上的追蹤效果。

### 常見追蹤器比較

OpenCV 提供多種追蹤演算法，各有優缺點：

| 追蹤器 | 全名 | 速度 | 精準度 | 適用場景 | 說明 |
|--------|------|------|--------|----------|------|
| **CSRT** | Discriminative Correlation Filter with Channel and Spatial Reliability | 慢 | 高 | 需要高精準度的場景 | 使用空間可靠性圖來調整濾波器支援，能處理非矩形物件和遮擋情況 |
| **KCF** | Kernelized Correlation Filters | 快 | 中 | 平衡速度與精準度 | 利用循環矩陣的性質加速計算，適合即時應用 |
| **MOSSE** | Minimum Output Sum of Squared Error | 非常快 | 低 | 需要極高速度的場景 | 最快的追蹤器，但對遮擋和光線變化敏感 |
| **MIL** | Multiple Instance Learning | 中 | 中 | 一般場景 | 較舊的演算法，對部分遮擋有一定抵抗力 |
| **Boosting** | AdaBoost-based Tracker | 慢 | 低 | 不推薦 | 最早的追蹤器之一，已被更好的演算法取代 |
| **MedianFlow** | - | 快 | 中 | 可預測運動的場景 | 適合物件運動平滑且可預測的情況 |
| **TLD** | Tracking-Learning-Detection | 中 | 中 | 長時間追蹤 | 結合追蹤、學習和偵測，能從失敗中恢復 |

**專有名詞詳細說明：**

- **CSRT (Discriminative Correlation Filter with Channel and Spatial Reliability)**:
  - 使用**判別式相關濾波器** (Discriminative Correlation Filter, DCF) 技術
  - 引入**空間可靠性圖** (Spatial Reliability Map)，能夠識別目標的哪些部分更可靠
  - 支援**多通道特徵**，不僅使用顏色，還結合 HOG 等特徵
  - 能夠處理**非矩形區域**和**部分遮擋**的情況

- **KCF (Kernelized Correlation Filters)**:
  - 基於**相關濾波器** (Correlation Filter) 的核心化版本
  - 利用**循環矩陣**的傅立葉域對角化性質，大幅加速計算
  - 使用**核技巧** (Kernel Trick) 將線性濾波器擴展到非線性空間
  - 在速度和精準度間取得良好平衡

- **MOSSE (Minimum Output Sum of Squared Error)**:
  - 基於**相關濾波器**的最早實現之一
  - 使用**最小化輸出誤差平方和**的方式訓練濾波器
  - 在**頻域** (Frequency Domain) 中操作，運算極快
  - 對**光線變化**和**形變**較為敏感

- **Bounding Box (邊界框)**: 完全包圍目標物件的最小矩形框，用 `(x, y, w, h)` 表示，其中 (x, y) 是左上角座標，w 是寬度，h 是高度。

### 範例：追蹤影片中的特定物件並儲存結果

**注意：** 此範例需要您先上傳一個名為 `test.mp4` 的影片檔到 Colab。

```python
# 在 Colab 中執行
import cv2
from google.colab.patches import cv2_imshow

# 建立追蹤器 (可以嘗試不同的追蹤器)
# tracker = cv2.legacy.TrackerMOSSE_create()  # 最快速
# tracker = cv2.legacy.TrackerKCF_create()    # 平衡選擇
tracker = cv2.legacy.TrackerCSRT_create()     # 最精準

# 開啟影片檔案
cap = cv2.VideoCapture('test.mp4')

# 讀取第一幀
ret, frame = cap.read()

if not ret:
    print("錯誤: 無法讀取影片檔案")
else:
    # 取得影片資訊
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # 建立影片寫入器
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('output.mp4', fourcc, fps, (width, height))

    # 手動設定初始追蹤框 (x, y, w, h)
    # 這裡的數值需要您根據您的影片內容手動調整
    bbox = (200, 100, 50, 50)

    # 初始化追蹤器
    tracker.init(frame, bbox)

    frame_count = 0
    success_count = 0

    # 讀取影片並追蹤
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1

        # 更新追蹤器
        success, bbox = tracker.update(frame)

        # 如果追蹤成功，繪製方框
        if success:
            (x, y, w, h) = [int(v) for v in bbox]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            success_count += 1
        else:
            cv2.putText(frame, "Tracking failure", (100, 80),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)

        # 寫入影片
        out.write(frame)

    # 釋放資源
    cap.release()
    out.release()

    print(f"追蹤完成！")
    print(f"總幀數: {frame_count}, 成功追蹤: {success_count}, 成功率: {success_count/frame_count*100:.1f}%")
    print("結果已儲存為 output.mp4")
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
    *   然後，它會將計算出的特徵與對應的 `id` 關聯起來並儲存。簡單來說，就是建立一個「ID → 人臉特徵」的對照表。
    *   `recognizer.save()` 會將這個學習到的對照表儲存成一個 `.yml` 檔案，方便未來直接載入使用，無需重新訓練。

4.  **步驟三：進行辨識**:
    *   `recognizer.read()` 載入訓練好的模型。
    *   在一張新的測試圖片上，同樣先用 Haar Cascade 偵測出人臉。
    *   對於偵測到的每張臉，呼叫 `recognizer.predict()`。這個函數會計算這張新臉的 LBPH 特徵，然後去模型裡比對，找出特徵最接近的那個已知 ID。
    *   `predict()` 會返回兩個值：預測的 `id_num` 和一個 `confidence` (信心指數)。
    *   **重要**: 對於 LBPH 演算法，`confidence` 代表的是「距離」，所以**數值越低，表示特徵越接近，可信度越高**。一個常見的門檻值是 50 或 100，低於這個值我們就認為辨識成功。

**專有名詞詳細說明：**

- **LBPH (Local Binary Patterns Histograms, 局部二值模式直方圖)**:
  - **LBP 運算**: 對每個像素，比較它與周圍 8 個鄰居的灰度值。如果鄰居的值 ≥ 中心像素，記為 1，否則記為 0。這樣會得到一個 8 位元的二進位數。
  - **直方圖統計**: 將人臉分成多個小區域，統計每個區域的 LBP 值分布，形成直方圖。
  - **特徵比對**: 使用卡方距離 (Chi-Square) 或歐氏距離來比較兩個直方圖的相似度。
  - **優點**: 對光照變化不敏感、計算速度快、實作簡單。
  - **缺點**: 對姿態變化和表情變化較敏感。

- **Confidence (信心指數)**: 在 LBPH 中代表預測結果與訓練資料的距離，數值越低表示越相似。通常設定閾值（如 50-100）來判斷是否為同一人。

### 步驟一：下載並準備訓練資料

**重要提示**: 由於 Haar Cascade 人臉模型對真實人臉效果最好，建議您使用實際的人臉照片。以下範例僅作為流程示範。

```python
# 在 Colab 中執行
import os
import cv2
import numpy as np
from google.colab.patches import cv2_imshow

# 建立資料夾結構
!mkdir -p face_data/person1
!mkdir -p face_data/person2

# 這裡使用公開的人臉資料集作為範例
# 您應該替換成自己的人臉照片以獲得最佳效果

# Person 1 的照片
!wget -O face_data/person1/1.jpg https://faces.cs.unibas.ch/bfm/bfm2019/restricted/model2019_face12.jpg
!wget -O face_data/person1/2.jpg https://faces.cs.unibas.ch/bfm/bfm2019/restricted/model2019_face12.jpg

# Person 2 的照片
!wget -O face_data/person2/1.jpg https://faces.cs.unibas.ch/bfm/bfm2019/restricted/model2019_face12.jpg
!wget -O face_data/person2/2.jpg https://faces.cs.unibas.ch/bfm/bfm2019/restricted/model2019_face12.jpg

print("資料準備完成！建議使用自己的人臉照片以獲得最佳辨識效果。")
```

**實務建議**：
- 每個人至少準備 10-20 張不同角度、表情的照片
- 確保照片光線充足且清晰
- 避免過度遮擋（如墨鏡、口罩）
- 背景盡量簡單乾淨

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
id_name_map = {}  # 建立 ID 與資料夾名稱的對應

for person_folder in person_folders:
    if not os.path.isdir(person_folder):
        continue

    folder_name = os.path.basename(person_folder)
    id_name_map[id_counter] = folder_name

    # 取得資料夾內所有圖片的路徑
    person_images = [os.path.join(person_folder, f) for f in os.listdir(person_folder)]

    for image_path in person_images:
        img = cv2.imread(image_path)
        if img is None:
            print(f"警告: 無法讀取 {image_path}")
            continue

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img_np = np.array(gray, 'uint8')

        # 偵測人臉
        face_rects = detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        if len(face_rects) == 0:
            print(f"警告: 在 {image_path} 中未偵測到人臉")

        for (x, y, w, h) in face_rects:
            faces.append(img_np[y:y+h, x:x+w]) # 加入人臉 ROI
            ids.append(id_counter) # 加入對應的 ID

    id_counter += 1

if len(faces) == 0:
    print("錯誤: 沒有找到任何人臉，無法訓練模型")
else:
    print(f'找到 {len(faces)} 張人臉，開始訓練模型...')
    recognizer.train(faces, np.array(ids))
    recognizer.save('face_model.yml')
    print('模型訓練完成並儲存為 face_model.yml！')
    print(f'ID 對應表: {id_name_map}')
```

### 步驟三：進行人臉辨識

```python
# 在 Colab 中執行
# recognizer = cv2.face.LBPHFaceRecognizer_create() # OpenCV 3.x
recognizer = cv2.legacy.LBPHFaceRecognizer_create() # OpenCV 4.x

# 檢查模型檔案是否存在
if not os.path.exists('face_model.yml'):
    print("錯誤: 找不到訓練好的模型檔案 face_model.yml")
else:
    recognizer.read('face_model.yml')
    face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

    # 建立 ID 和姓名的對照表（根據訓練時的資料夾名稱）
    name_map = {
        1: 'Person 1',
        2: 'Person 2'
    }

    # 讀取測試圖片
    # 您可以上傳自己的圖片或使用訓練資料中的圖片來測試
    test_img_path = 'face_data/person1/1.jpg'  # 修改成您要測試的圖片路徑

    img = cv2.imread(test_img_path)
    if img is None:
        print(f"錯誤: 無法讀取測試圖片 {test_img_path}")
    else:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        if len(faces) == 0:
            print("未偵測到人臉")

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
            # 進行預測
            id_num, confidence = recognizer.predict(gray[y:y+h, x:x+w])

            # LBPH 的信心指數越低表示匹配度越高
            # 通常 < 50 表示很可能是同一人，< 100 可以接受
            if confidence < 100:
                text = name_map.get(id_num, "Unknown")
                # 轉換為更容易理解的百分比 (0=完美匹配, 100=門檻值)
                match_percentage = max(0, 100 - confidence)
                confidence_text = f" ({match_percentage:.0f}%)"
            else:
                text = "Unknown"
                confidence_text = ""

            # 根據信心指數選擇顏色
            color = (0, 255, 0) if confidence < 100 else (0, 0, 255)

            cv2.putText(img, text + confidence_text, (x, y-10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
            cv2.putText(img, f"Dist: {confidence:.1f}", (x, y+h+20),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

        print("辨識結果：")
        cv2_imshow(img)
```

---

## 9. 追蹤器效能比較

讓我們實際比較不同追蹤器的速度與精準度。

### 範例：比較 CSRT、KCF、MOSSE 追蹤器

```python
# 在 Colab 中執行
import cv2
import time
from google.colab.patches import cv2_imshow

# 定義要測試的追蹤器
trackers = {
    'MOSSE': cv2.legacy.TrackerMOSSE_create(),
    'KCF': cv2.legacy.TrackerKCF_create(),
    'CSRT': cv2.legacy.TrackerCSRT_create()
}

# 開啟影片
cap = cv2.VideoCapture('test.mp4')
ret, frame = cap.read()

if not ret:
    print("錯誤: 無法讀取影片")
else:
    # 手動設定追蹤框
    bbox = (200, 100, 50, 50)

    results = {}

    for name, tracker in trackers.items():
        print(f"\n測試 {name} 追蹤器...")

        # 重新讀取影片
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        ret, frame = cap.read()

        # 初始化追蹤器
        tracker.init(frame, bbox)

        frame_count = 0
        success_count = 0
        total_time = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame_count += 1

            # 測量追蹤時間
            start_time = time.time()
            success, bbox_new = tracker.update(frame)
            elapsed_time = time.time() - start_time

            total_time += elapsed_time
            if success:
                success_count += 1

        # 計算統計資料
        avg_fps = frame_count / total_time if total_time > 0 else 0
        success_rate = (success_count / frame_count * 100) if frame_count > 0 else 0

        results[name] = {
            'fps': avg_fps,
            'success_rate': success_rate,
            'total_frames': frame_count,
            'success_frames': success_count
        }

        print(f"{name} - FPS: {avg_fps:.1f}, 成功率: {success_rate:.1f}%")

    # 顯示比較結果
    print("\n" + "="*50)
    print("追蹤器效能比較")
    print("="*50)
    print(f"{'追蹤器':<10} {'FPS':<10} {'成功率':<10} {'評級':<10}")
    print("-"*50)

    for name, data in sorted(results.items(), key=lambda x: x[1]['fps'], reverse=True):
        rating = "⭐⭐⭐" if data['fps'] > 100 else "⭐⭐" if data['fps'] > 50 else "⭐"
        print(f"{name:<10} {data['fps']:<10.1f} {data['success_rate']:<10.1f}% {rating:<10}")

    cap.release()
```

---

## 10. 常見問題排解

### Q1: 人臉偵測失敗或偵測不到人臉
**可能原因與解決方法**:
- **光線不足**: 確保圖片有充足且均勻的光線
- **人臉角度**: Haar Cascade 對正面人臉效果最好，側臉或仰/俯角度會降低偵測率
- **圖片解析度**: 太小的圖片可能偵測不到，建議至少 640x480
- **參數調整**:
  ```python
  # 降低 scaleFactor 提高偵測敏感度
  faces = face_cascade.detectMultiScale(gray, scaleFactor=1.05, minNeighbors=3)
  ```

### Q2: 顏色追蹤不準確
**可能原因與解決方法**:
- **光線影響**: HSV 雖對光線不敏感，但極端光線仍會影響。可擴大 S 和 V 的範圍
- **顏色範圍**: 調整 HSV 上下限，可先用 `cv2.cvtColor()` 查看目標顏色的實際 HSV 值
  ```python
  # 查看特定顏色的 HSV 值
  color_bgr = np.uint8([[[0, 0, 255]]])  # 紅色 BGR
  color_hsv = cv2.cvtColor(color_bgr, cv2.COLOR_BGR2HSV)
  print(f"紅色的 HSV 值: {color_hsv[0][0]}")
  ```

### Q3: 物件追蹤中途失敗
**可能原因與解決方法**:
- **遮擋問題**: 當物件被遮擋時，MOSSE 和 KCF 容易失敗，改用 CSRT 或 TLD
- **快速移動**: 物件移動過快會導致追蹤失敗，可提高影片 FPS 或使用 KCF
- **光線變化**: 光線突變會影響追蹤，CSRT 對此較有抵抗力
- **重新初始化**: 可在偵測到失敗時，用偵測器重新找到物件並重新初始化追蹤器

### Q4: 人臉辨識準確率低
**可能原因與解決方法**:
- **訓練資料不足**: 每個人至少需要 10-20 張不同角度和表情的照片
- **照片品質**: 確保訓練照片清晰、光線充足、人臉完整
- **參數調整**: 調整 LBPH 的參數
  ```python
  # radius: LBP 半徑, neighbors: 鄰居數量, grid_x/y: 網格劃分
  recognizer = cv2.legacy.LBPHFaceRecognizer_create(
      radius=1, neighbors=8, grid_x=8, grid_y=8
  )
  ```
- **閾值調整**: 根據實際情況調整 confidence 門檻值

### Q5: 程式執行速度太慢
**優化建議**:
- **降低解析度**:
  ```python
  img = cv2.resize(img, (640, 480))
  ```
- **ROI 處理**: 只在感興趣區域 (Region of Interest) 進行偵測
- **調整參數**: 提高 `scaleFactor` 減少偵測次數
- **使用更快的追蹤器**: MOSSE > KCF > CSRT
- **GPU 加速**: 如果有 GPU，考慮使用 CUDA 版本的 OpenCV

### Q6: Colab 環境限制
**常見問題與解決方法**:
- **無法使用 cv2.imshow()**: 使用 `cv2_imshow()` 替代
- **無法使用 cv2.selectROI()**: 手動指定座標
- **記憶體不足**:
  - 分批處理大型影片
  - 釋放不用的變數 `del variable_name`
  - 重啟 Runtime
- **檔案上傳**:
  ```python
  from google.colab import files
  uploaded = files.upload()  # 上傳檔案
  ```

---

## 11. OpenCV 函數完整參考

本章節詳細說明教學中使用到的所有 OpenCV 函數及其參數。

### 11.1 圖像讀取與顯示

#### `cv2.imread(filename, flags=cv2.IMREAD_COLOR)`
從檔案讀取圖像。

**參數**:
- `filename` (str): 圖像檔案路徑
- `flags` (int, 可選): 讀取模式
  - `cv2.IMREAD_COLOR` (預設): 讀取彩色圖像，忽略透明通道
  - `cv2.IMREAD_GRAYSCALE`: 讀取為灰階圖像
  - `cv2.IMREAD_UNCHANGED`: 讀取包含透明通道的圖像

**返回值**:
- `numpy.ndarray`: 圖像陣列，若讀取失敗則返回 `None`

**範例**:
```python
img = cv2.imread('image.jpg')  # 彩色
gray = cv2.imread('image.jpg', cv2.IMREAD_GRAYSCALE)  # 灰階
```

---

#### `cv2_imshow(img)`
在 Google Colab 環境中顯示圖像 (非標準 OpenCV 函數)。

**參數**:
- `img` (numpy.ndarray): 要顯示的圖像陣列

**返回值**: 無

**範例**:
```python
from google.colab.patches import cv2_imshow
cv2_imshow(img)
```

**注意**: 標準環境使用 `cv2.imshow(window_name, img)` 和 `cv2.waitKey(0)`

---

### 11.2 色彩空間轉換

#### `cv2.cvtColor(src, code)`
轉換圖像的色彩空間。

**參數**:
- `src` (numpy.ndarray): 原始圖像
- `code` (int): 色彩空間轉換代碼
  - `cv2.COLOR_BGR2GRAY`: BGR 轉灰階
  - `cv2.COLOR_BGR2HSV`: BGR 轉 HSV
  - `cv2.COLOR_BGR2RGB`: BGR 轉 RGB
  - `cv2.COLOR_HSV2BGR`: HSV 轉 BGR
  - `cv2.COLOR_GRAY2BGR`: 灰階轉 BGR

**返回值**:
- `numpy.ndarray`: 轉換後的圖像

**範例**:
```python
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
```

**說明**: OpenCV 預設使用 BGR 順序，而非常見的 RGB 順序

---

### 11.3 顏色範圍篩選

#### `cv2.inRange(src, lowerb, upperb)`
檢查圖像中的像素是否在指定範圍內。

**參數**:
- `src` (numpy.ndarray): 輸入圖像
- `lowerb` (numpy.ndarray): 範圍下限，格式為 `np.array([H, S, V])`
- `upperb` (numpy.ndarray): 範圍上限，格式為 `np.array([H, S, V])`

**返回值**:
- `numpy.ndarray`: 二值化遮罩，範圍內的像素為 255 (白色)，範圍外為 0 (黑色)

**範例**:
```python
lower_red = np.array([0, 40, 40])
upper_red = np.array([10, 255, 255])
mask = cv2.inRange(hsv, lower_red, upper_red)
```

---

### 11.4 輪廓偵測與分析

#### `cv2.findContours(image, mode, method)`
在二值化圖像中尋找輪廓。

**參數**:
- `image` (numpy.ndarray): 輸入的二值化圖像 (通常是遮罩)
- `mode` (int): 輪廓檢索模式
  - `cv2.RETR_EXTERNAL`: 只檢測外部輪廓
  - `cv2.RETR_LIST`: 檢測所有輪廓，不建立階層關係
  - `cv2.RETR_TREE`: 檢測所有輪廓，建立完整階層關係
- `method` (int): 輪廓近似方法
  - `cv2.CHAIN_APPROX_NONE`: 儲存所有輪廓點
  - `cv2.CHAIN_APPROX_SIMPLE`: 壓縮水平、垂直和對角線段，只保留端點

**返回值**:
- `contours` (list): 輪廓列表，每個輪廓是點的 numpy 陣列
- `hierarchy` (numpy.ndarray): 輪廓階層資訊

**範例**:
```python
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
```

---

#### `cv2.contourArea(contour)`
計算輪廓的面積。

**參數**:
- `contour` (numpy.ndarray): 輪廓點陣列

**返回值**:
- `float`: 輪廓面積 (像素平方)

**範例**:
```python
for contour in contours:
    area = cv2.contourArea(contour)
    if area > 100:  # 過濾小於 100 像素的輪廓
        # 處理輪廓
```

---

#### `cv2.boundingRect(contour)`
計算輪廓的最小外接矩形。

**參數**:
- `contour` (numpy.ndarray): 輪廓點陣列

**返回值**:
- `x` (int): 矩形左上角 x 座標
- `y` (int): 矩形左上角 y 座標
- `w` (int): 矩形寬度
- `h` (int): 矩形高度

**範例**:
```python
x, y, w, h = cv2.boundingRect(contour)
cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
```

---

### 11.5 繪圖函數

#### `cv2.rectangle(img, pt1, pt2, color, thickness)`
在圖像上繪製矩形。

**參數**:
- `img` (numpy.ndarray): 輸入/輸出圖像
- `pt1` (tuple): 矩形左上角座標 `(x, y)`
- `pt2` (tuple): 矩形右下角座標 `(x, y)`
- `color` (tuple): BGR 顏色 `(B, G, R)`，範圍 0-255
- `thickness` (int): 線條粗細
  - 正數: 邊框線條粗細 (像素)
  - `-1` 或 `cv2.FILLED`: 填滿矩形

**返回值**:
- `numpy.ndarray`: 繪製後的圖像 (修改原圖)

**範例**:
```python
cv2.rectangle(img, (50, 50), (200, 200), (0, 255, 0), 2)  # 綠色邊框
cv2.rectangle(img, (50, 50), (200, 200), (255, 0, 0), -1)  # 藍色填滿
```

---

#### `cv2.putText(img, text, org, fontFace, fontScale, color, thickness)`
在圖像上繪製文字。

**參數**:
- `img` (numpy.ndarray): 輸入/輸出圖像
- `text` (str): 要顯示的文字
- `org` (tuple): 文字左下角座標 `(x, y)`
- `fontFace` (int): 字體類型
  - `cv2.FONT_HERSHEY_SIMPLEX`: 正常大小的無襯線字體
  - `cv2.FONT_HERSHEY_PLAIN`: 小型無襯線字體
  - `cv2.FONT_HERSHEY_COMPLEX`: 正常大小的襯線字體
- `fontScale` (float): 字體縮放係數 (基於字體基礎大小)
- `color` (tuple): BGR 顏色
- `thickness` (int): 線條粗細 (像素)

**返回值**:
- `numpy.ndarray`: 繪製後的圖像

**範例**:
```python
cv2.putText(img, "Hello OpenCV", (50, 50),
            cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)
```

---

### 11.6 圖像變換

#### `cv2.resize(src, dsize, fx, fy, interpolation)`
調整圖像大小。

**參數**:
- `src` (numpy.ndarray): 原始圖像
- `dsize` (tuple): 目標大小 `(width, height)`，若為 `None` 則使用 `fx` 和 `fy`
- `fx` (float, 可選): 水平縮放係數
- `fy` (float, 可選): 垂直縮放係數
- `interpolation` (int, 可選): 插值方法
  - `cv2.INTER_NEAREST`: 最近鄰插值 (最快，品質最低)
  - `cv2.INTER_LINEAR`: 雙線性插值 (預設，平衡)
  - `cv2.INTER_CUBIC`: 雙三次插值 (慢，品質高)
  - `cv2.INTER_AREA`: 區域插值 (適合縮小)

**返回值**:
- `numpy.ndarray`: 調整大小後的圖像

**範例**:
```python
# 指定尺寸
resized = cv2.resize(img, (640, 480))

# 使用縮放係數
resized = cv2.resize(img, None, fx=0.5, fy=0.5)

# 馬賽克效果 (縮小再放大)
small = cv2.resize(img, (50, 50), interpolation=cv2.INTER_LINEAR)
mosaic = cv2.resize(small, (width, height), interpolation=cv2.INTER_NEAREST)
```

---

#### `np.zeros(shape, dtype)`
建立指定形狀和類型的零陣列 (NumPy 函數)。

**參數**:
- `shape` (tuple): 陣列形狀 `(height, width, channels)`
- `dtype` (type): 資料類型，通常使用 `np.uint8` (0-255)

**返回值**:
- `numpy.ndarray`: 零陣列

**範例**:
```python
# 建立黑色畫布
black_img = np.zeros((300, 400, 3), dtype=np.uint8)  # 300x400 彩色
gray_img = np.zeros((300, 400), dtype=np.uint8)      # 300x400 灰階
```

---

### 11.7 物件偵測 (Haar Cascade)

#### `cv2.CascadeClassifier(filename)`
載入 Haar Cascade 分類器。

**參數**:
- `filename` (str): XML 模型檔案路徑

**返回值**:
- `CascadeClassifier`: 分類器物件

**範例**:
```python
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
```

---

#### `cascade.detectMultiScale(image, scaleFactor, minNeighbors, minSize, maxSize)`
在多尺度上偵測物件。

**參數**:
- `image` (numpy.ndarray): 輸入圖像 (建議使用灰階)
- `scaleFactor` (float, 可選): 每次縮小的比例，預設 1.1
  - 範圍: > 1.0，通常 1.05-1.3
  - 較小值 → 更精準但更慢
- `minNeighbors` (int, 可選): 保留候選框的最小鄰居數，預設 3
  - 範圍: 通常 3-10
  - 較大值 → 減少誤判但可能遺漏
- `minSize` (tuple, 可選): 最小物件大小 `(width, height)`
- `maxSize` (tuple, 可選): 最大物件大小 `(width, height)`

**返回值**:
- `numpy.ndarray`: 偵測到的矩形陣列，格式為 `[[x, y, w, h], ...]`

**範例**:
```python
faces = face_cascade.detectMultiScale(
    gray,
    scaleFactor=1.1,
    minNeighbors=5,
    minSize=(30, 30)
)

for (x, y, w, h) in faces:
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
```

---

### 11.8 影片處理

#### `cv2.VideoCapture(source)`
開啟影片檔案或攝影機。

**參數**:
- `source` (str 或 int): 影片檔案路徑，或攝影機編號 (0 為預設攝影機)

**返回值**:
- `VideoCapture`: 影片捕捉物件

**範例**:
```python
cap = cv2.VideoCapture('video.mp4')  # 開啟影片檔
cap = cv2.VideoCapture(0)            # 開啟攝影機
```

---

#### `cap.read()`
讀取影片的下一幀。

**參數**: 無

**返回值**:
- `ret` (bool): 是否成功讀取
- `frame` (numpy.ndarray): 讀取到的影像幀

**範例**:
```python
ret, frame = cap.read()
if not ret:
    print("無法讀取影片")
```

---

#### `cap.get(propId)`
取得影片屬性。

**參數**:
- `propId` (int): 屬性 ID
  - `cv2.CAP_PROP_FPS`: 影片幀率 (FPS)
  - `cv2.CAP_PROP_FRAME_WIDTH`: 影片寬度
  - `cv2.CAP_PROP_FRAME_HEIGHT`: 影片高度
  - `cv2.CAP_PROP_FRAME_COUNT`: 總幀數
  - `cv2.CAP_PROP_POS_FRAMES`: 當前幀位置

**返回值**:
- `float`: 屬性值

**範例**:
```python
fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
```

---

#### `cap.set(propId, value)`
設定影片屬性。

**參數**:
- `propId` (int): 屬性 ID (同 `get()`)
- `value` (float): 要設定的值

**返回值**:
- `bool`: 是否成功設定

**範例**:
```python
cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # 跳到第一幀
cap.set(cv2.CAP_PROP_POS_FRAMES, 100)  # 跳到第 100 幀
```

---

#### `cap.release()`
釋放影片資源。

**參數**: 無

**返回值**: 無

**範例**:
```python
cap.release()  # 關閉影片檔或攝影機
```

---

#### `cv2.VideoWriter(filename, fourcc, fps, frameSize)`
建立影片寫入器。

**參數**:
- `filename` (str): 輸出影片檔案路徑
- `fourcc` (int): 編碼格式 (使用 `cv2.VideoWriter_fourcc()` 建立)
- `fps` (float): 影片幀率
- `frameSize` (tuple): 影像大小 `(width, height)`

**返回值**:
- `VideoWriter`: 影片寫入物件

**範例**:
```python
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (640, 480))
```

---

#### `cv2.VideoWriter_fourcc(*code)`
建立影片編碼格式代碼。

**參數**:
- `code` (str): 4 字元編碼代碼
  - `'mp4v'`: MPEG-4 編碼
  - `'XVID'`: XVID 編碼
  - `'MJPG'`: Motion-JPEG 編碼
  - `'X264'`: H.264 編碼

**返回值**:
- `int`: 編碼格式代碼

**範例**:
```python
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')  # 等同於上面
```

---

#### `out.write(frame)`
寫入一幀影像到影片。

**參數**:
- `frame` (numpy.ndarray): 要寫入的影像幀

**返回值**: 無

**範例**:
```python
while True:
    ret, frame = cap.read()
    if not ret:
        break
    # 處理 frame...
    out.write(frame)
```

---

#### `out.release()`
釋放影片寫入器資源。

**參數**: 無

**返回值**: 無

**範例**:
```python
out.release()  # 關閉並儲存影片檔
```

---

### 11.9 物件追蹤

#### `cv2.legacy.TrackerCSRT_create()`
建立 CSRT 追蹤器 (高精準度)。

**參數**: 無

**返回值**:
- `Tracker`: CSRT 追蹤器物件

**特性**:
- 精準度: 高
- 速度: 慢
- 適用: 需要高精準度的場景

**範例**:
```python
tracker = cv2.legacy.TrackerCSRT_create()
```

---

#### `cv2.legacy.TrackerKCF_create()`
建立 KCF 追蹤器 (平衡選擇)。

**參數**: 無

**返回值**:
- `Tracker`: KCF 追蹤器物件

**特性**:
- 精準度: 中
- 速度: 快
- 適用: 平衡速度與精準度的場景

**範例**:
```python
tracker = cv2.legacy.TrackerKCF_create()
```

---

#### `cv2.legacy.TrackerMOSSE_create()`
建立 MOSSE 追蹤器 (高速度)。

**參數**: 無

**返回值**:
- `Tracker`: MOSSE 追蹤器物件

**特性**:
- 精準度: 低
- 速度: 非常快
- 適用: 需要極高速度的場景

**範例**:
```python
tracker = cv2.legacy.TrackerMOSSE_create()
```

---

#### `tracker.init(image, bbox)`
初始化追蹤器。

**參數**:
- `image` (numpy.ndarray): 第一幀影像
- `bbox` (tuple): 初始邊界框 `(x, y, width, height)`

**返回值**:
- `bool`: 是否成功初始化

**範例**:
```python
bbox = (200, 100, 50, 50)  # (x, y, w, h)
success = tracker.init(frame, bbox)
```

---

#### `tracker.update(image)`
更新追蹤器並取得新的邊界框。

**參數**:
- `image` (numpy.ndarray): 當前幀影像

**返回值**:
- `success` (bool): 是否成功追蹤
- `bbox` (tuple): 更新後的邊界框 `(x, y, width, height)`

**範例**:
```python
success, bbox = tracker.update(frame)
if success:
    (x, y, w, h) = [int(v) for v in bbox]
    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
```

---

### 11.10 人臉辨識 (LBPH)

#### `cv2.legacy.LBPHFaceRecognizer_create(radius, neighbors, grid_x, grid_y, threshold)`
建立 LBPH 人臉辨識器。

**參數** (全部可選):
- `radius` (int): LBP 半徑，預設 1
- `neighbors` (int): LBP 鄰居數量，預設 8
- `grid_x` (int): 水平方向網格數量，預設 8
- `grid_y` (int): 垂直方向網格數量，預設 8
- `threshold` (float): 辨識閾值，預設 DBL_MAX

**返回值**:
- `LBPHFaceRecognizer`: 辨識器物件

**範例**:
```python
# 使用預設參數
recognizer = cv2.legacy.LBPHFaceRecognizer_create()

# 自訂參數
recognizer = cv2.legacy.LBPHFaceRecognizer_create(
    radius=1,
    neighbors=8,
    grid_x=8,
    grid_y=8
)
```

---

#### `recognizer.train(src, labels)`
訓練辨識模型。

**參數**:
- `src` (list): 人臉圖像列表 (灰階 numpy 陣列)
- `labels` (numpy.ndarray): 對應的標籤 ID 陣列

**返回值**: 無

**範例**:
```python
faces = []  # 人臉圖像列表
ids = []    # 對應的 ID 列表

# 收集訓練資料
for image_path, person_id in training_data:
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    faces.append(img)
    ids.append(person_id)

# 訓練模型
recognizer.train(faces, np.array(ids))
```

---

#### `recognizer.save(filename)`
儲存訓練好的模型。

**參數**:
- `filename` (str): 模型檔案路徑 (通常使用 `.yml` 副檔名)

**返回值**: 無

**範例**:
```python
recognizer.save('face_model.yml')
```

---

#### `recognizer.read(filename)`
載入訓練好的模型。

**參數**:
- `filename` (str): 模型檔案路徑

**返回值**: 無

**範例**:
```python
recognizer.read('face_model.yml')
```

---

#### `recognizer.predict(src)`
辨識人臉。

**參數**:
- `src` (numpy.ndarray): 要辨識的人臉圖像 (灰階)

**返回值**:
- `label` (int): 預測的標籤 ID
- `confidence` (float): 信心指數 (距離值，**越低越相似**)

**範例**:
```python
id_num, confidence = recognizer.predict(face_gray)

if confidence < 100:  # 閾值判斷
    print(f"辨識為 ID {id_num}，信心度距離: {confidence:.2f}")
else:
    print("未知人臉")
```

**重要說明**:
- LBPH 的 `confidence` 代表距離，**數值越低表示越相似**
- 通常設定閾值 50-100 來判斷是否為同一人
- 可以轉換為百分比: `match_percentage = max(0, 100 - confidence)`

---

### 11.11 函數快速查詢表

| 分類 | 函數 | 用途 | 重要參數 |
|------|------|------|----------|
| **圖像 I/O** | `cv2.imread()` | 讀取圖像 | `filename`, `flags` |
| | `cv2_imshow()` | 顯示圖像 (Colab) | `img` |
| **色彩轉換** | `cv2.cvtColor()` | 轉換色彩空間 | `src`, `code` |
| | `cv2.inRange()` | 顏色範圍篩選 | `src`, `lowerb`, `upperb` |
| **輪廓** | `cv2.findContours()` | 尋找輪廓 | `image`, `mode`, `method` |
| | `cv2.contourArea()` | 計算輪廓面積 | `contour` |
| | `cv2.boundingRect()` | 取得外接矩形 | `contour` |
| **繪圖** | `cv2.rectangle()` | 繪製矩形 | `img`, `pt1`, `pt2`, `color`, `thickness` |
| | `cv2.putText()` | 繪製文字 | `img`, `text`, `org`, `fontFace`, `fontScale`, `color` |
| **變換** | `cv2.resize()` | 調整大小 | `src`, `dsize`, `interpolation` |
| | `np.zeros()` | 建立零陣列 | `shape`, `dtype` |
| **物件偵測** | `cv2.CascadeClassifier()` | 載入 Haar 模型 | `filename` |
| | `.detectMultiScale()` | 偵測物件 | `image`, `scaleFactor`, `minNeighbors` |
| **影片** | `cv2.VideoCapture()` | 開啟影片 | `source` |
| | `.read()` | 讀取幀 | - |
| | `.get()` | 取得屬性 | `propId` |
| | `.set()` | 設定屬性 | `propId`, `value` |
| | `cv2.VideoWriter()` | 建立寫入器 | `filename`, `fourcc`, `fps`, `frameSize` |
| | `.write()` | 寫入幀 | `frame` |
| | `.release()` | 釋放資源 | - |
| **追蹤** | `TrackerCSRT_create()` | 建立 CSRT 追蹤器 | - |
| | `TrackerKCF_create()` | 建立 KCF 追蹤器 | - |
| | `TrackerMOSSE_create()` | 建立 MOSSE 追蹤器 | - |
| | `.init()` | 初始化追蹤器 | `image`, `bbox` |
| | `.update()` | 更新追蹤 | `image` |
| **人臉辨識** | `LBPHFaceRecognizer_create()` | 建立 LBPH 辨識器 | `radius`, `neighbors`, `grid_x`, `grid_y` |
| | `.train()` | 訓練模型 | `src`, `labels` |
| | `.save()` | 儲存模型 | `filename` |
| | `.read()` | 載入模型 | `filename` |
| | `.predict()` | 辨識人臉 | `src` |

---

## 總結與後續學習

### 本教學涵蓋內容
✅ 基於顏色的物件偵測 (HSV 色彩空間)
✅ Haar Cascade 人臉/五官/物件偵測
✅ 人臉隱私處理 (馬賽克)
✅ 多種物件追蹤演算法 (CSRT, KCF, MOSSE)
✅ LBPH 人臉辨識
✅ 效能比較與優化技巧
✅ **OpenCV 函數完整參考手冊**

### 進階學習方向
1. **深度學習物件偵測**: YOLO, SSD, Faster R-CNN
2. **深度學習人臉辨識**: FaceNet, ArcFace, DeepFace
3. **即時影像處理**: 攝影機串流、多執行緒處理
4. **姿態估計**: OpenPose, MediaPipe
5. **影像分割**: Mask R-CNN, U-Net

### 實用資源
- [OpenCV 官方文件](https://docs.opencv.org/)
- [OpenCV Python 教學](https://opencv-python-tutroals.readthedocs.io/)
- [預訓練模型庫](https://github.com/opencv/opencv/tree/master/data)
- [影像處理社群](https://stackoverflow.com/questions/tagged/opencv)

---

**文件更新說明 (v.b04)**:
- ✨ 新增第 11 章：OpenCV 函數完整參考手冊
- 📚 詳細說明所有範例中使用的函數及其參數
- 📊 加入函數快速查詢表
- 💡 提供每個函數的完整範例程式碼
- 🔍 包含參數說明、返回值與使用注意事項
- ⚡ 涵蓋圖像處理、物件偵測、追蹤、人臉辨識等所有類別

**文件更新說明 (v.b05)**:
- 🎯 **大幅加強 Haar Cascade 技術原理說明**
- 📖 新增完整的 Viola-Jones 演算法解析
- 🔬 詳細說明六大核心技術：
  - Haar 特徵 (Haar-like Features) 及其計算方式
  - 積分圖 (Integral Image) 加速技術
  - AdaBoost 自適應增強學習演算法
  - 級聯分類器 (Cascade Classifier) 結構
  - 多尺度偵測 (Multi-Scale Detection) 策略
  - 非極大值抑制 (Non-Maximum Suppression) 原理
- 💡 提供訓練過程詳解與實際參數範例
- 📊 加入優缺點分析與現代深度學習方法比較
- 🛠️ 提供實務應用建議與延伸閱讀資源
