<!-- Path: AI_Agent_CLi | Updated: 2026-10-31 | Edition: Codex CLI / Claude Code -->
# 單元四補充內容：進階章節

> **本版查核：2026-10-31。**先閱讀[前導章：Agent 基本概念與工作環境](00_intro.html)，安裝並登入 Codex CLI 或 Claude Code 任選一款即可。本課使用虛構／去識別化資料，所有結果都要以來源與實際檔案驗收。


**銜接**：搭配[單元四](04_workspace.html)閱讀，練習多檔案、Markdown 與流程圖。

---

### 雙 CLI 操作約定

在專案資料夾開啟終端機，先用 `codex` 或 `claude` 啟動互動會話，再貼上本章的自然語言提示。逐輪等待完成，追問時維持同一會話；另開一次指令不會自動承接剛才內容。

| 情境 | Codex CLI | Claude Code |
|---|---|---|
| 互動操作（初學者主線） | `codex` | `claude` |
| 帶第一個提示開始會話 | `codex "閱讀 lesson.txt 並摘要"` | `claude "閱讀 lesson.txt 並摘要"` |
| 單次輸出後結束 | `codex exec "閱讀 lesson.txt 並摘要"` | `claude -p "閱讀 lesson.txt 並摘要"` |
| 專案規則 | `AGENTS.md` | `CLAUDE.md`；AGENTS.md 的相容條件見單元五 |

以下標示 **Codex CLI／Claude Code** 的 shell 範例是兩個替代選項，選一組執行即可。`bash` 中的 `for ...; do`、`$(date ...)` 是 macOS／Linux／WSL 範例，Windows PowerShell 請使用文中的 PowerShell 版本或互動主線。簡單雙引號指令可在 PowerShell 7 使用。

單次模式要先完成登入。Codex `exec` 預設唯讀，且通常要求位於 Git 專案，先在教學資料夾執行 `git init`；需要直接寫檔時，改用互動會話並確認權限，或明確使用 `--sandbox workspace-write`。Claude `-p` 不會彈出互動授權；需要未預先允許的工具時，改回互動模式檢查授權，不使用全面略過權限的旗標。下列 `> file.md` 是 shell 儲存標準輸出，會覆寫同名檔；先選用新檔名。不要同時要求 Agent 寫入同一個重新導向的檔案。

[Codex 非互動模式官方說明](https://learn.chatgpt.com/docs/non-interactive-mode)、[Claude Code CLI reference](https://code.claude.com/docs/en/cli-reference)（查核 2026-10-31）。


## CLI + VSCode 整合的五大優勢

### 優勢一：一站式工作環境
**傳統方式**：
- 瀏覽器開 網頁 AI → 複製結果 → 貼到 Word → 存檔
- 需要在多個視窗間切換
- 容易遺失內容

**CLI + VSCode 方式**：
```
同一個視窗內：
├── 左側：檔案總管（看到所有教材）
├── 中間：編輯區（檢視與編輯內容）
└── 下方：終端機（與 AI 對話）
```

**效益**：工作可減少視窗切換；效益需以自己的任務時間紀錄評估

---

### 優勢二：批次處理多檔案（類似 NotebookLM）

**核心能力**：Codex CLI／Claude Code 可依指定路徑逐步讀檔並整合分析；先列出讀取清單，不能假定所有檔案都已進入 context

**情境範例**：整週教案統整

**資料夾結構**：
```
week5_lessons/
├── monday_math.txt
├── wednesday_science.txt
├── friday_social.txt
└── assessment.txt
```

**指令**：
**Codex CLI（擇一）**
```bash
codex exec "分析這個資料夾中的所有檔案，整理出本週的教學重點、學生表現與需改進之處"
```

**Claude Code（擇一）**
```bash
claude -p "分析這個資料夾中的所有檔案，整理出本週的教學重點、學生表現與需改進之處"
```

**要求 Agent 執行並確認紀錄**：
1. 讀取所有 4 個檔案
2. 整合資訊
3. 生成綜合報告

**vs NotebookLM 的差異**：

| 比較項目 | NotebookLM | Codex CLI／Claude Code + VSCode |
|---------|-----------|---------------------|
| **檔案管理** | 網頁上傳，分散 | 本機資料夾，集中 |
| **修改檔案** | 需重新上傳 | 下一次讀檔取得更新內容；已載入 context 需重讀 |
| **工作流程** | 瀏覽器 → 複製 → 貼上 | 終端機 → 直接輸出檔案 |
| **隱私性** | 雲端處理 | 工具在本機執行；提示與已讀資料仍可能送至雲端模型 |
| **整合性** | 獨立工具 | 整合在開發環境 |

---

### 優勢三：輸出結果可直接存檔

**傳統方式**：
1. AI 生成內容
2. 手動複製
3. 開啟 Word
4. 貼上
5. 調整格式
6. 存檔

**CLI 方式**：
**Codex CLI（擇一）**
```bash
codex exec "設計教案" > lesson_plan.md
```

**Claude Code（擇一）**
```bash
claude -p "設計教案" > lesson_plan.md
```
**完成後檢查**：確認命令成功、檔案非空且內容符合要求，再改名為正式稿。

---

### 優勢四：版本控制與歷程追蹤

**搭配 Git 使用**：
```bash
git add lesson_plan.md
git commit -m "AI生成初稿"

# 修改後
git add lesson_plan.md
git commit -m "調整難度"
```

**優點**：
- 追蹤每次修改
- 可回溯舊版本
- 團隊協作更容易

---

### 優勢五：自動化工作流程

**範例：每週自動生成教學週報**

建立腳本 `weekly_report.sh`（macOS／Linux／WSL）：先建立並確認對應的週次資料夾，放入本週來源；若使用 Codex 單次模式，該資料夾須屬於 Git 專案。`set -euo pipefail` 使切換目錄或 CLI 失敗時停止，不繼續宣告完成。
**Codex CLI（擇一）**
```bash
#!/bin/bash
set -euo pipefail
cd "$HOME/teaching/week_$(date +%U)"
codex exec "整理本週教學檔案,生成週報" > weekly_report_$(date +%Y%m%d).md
test -s "weekly_report_$(date +%Y%m%d).md"
echo "週報草稿已生成；請核對來源與內容。"
```

**Claude Code（擇一）**
```bash
#!/bin/bash
set -euo pipefail
cd "$HOME/teaching/week_$(date +%U)"
claude -p "整理本週教學檔案,生成週報" > weekly_report_$(date +%Y%m%d).md
test -s "weekly_report_$(date +%Y%m%d).md"
echo "週報草稿已生成；請核對來源與內容。"
```

**執行**：
```bash
bash weekly_report.sh
```

---

## Markdown 格式輸出的優勢與應用

### 什麼是 Markdown？

**簡單定義**：一種輕量級的標記語言，用簡單符號表示格式

**核心理念**：
- 純文字，任何編輯器都能開啟
- 語法簡單，5 分鐘上手
- 轉換方便，可轉成 PDF、Word、HTML

### Markdown 基本語法

```markdown
# 這是標題 1
## 這是標題 2
### 這是標題 3

**粗體文字**
*斜體文字*

- 項目一
- 項目二
  - 子項目

1. 第一點
2. 第二點

[連結文字](https://example.com)

![圖片說明](image.png)
```

### 為何用 Markdown 撰寫教材？

#### 優勢 1：專注內容，不被格式干擾

**Word 的問題**：
- 調整字體、大小、顏色
- 對齊、縮排
- 可能花費額外時間調整格式，請依實際作業記錄

**Markdown 的解法**：
- 只用符號標記
- 格式統一自動套用
- 專注在內容撰寫

#### 優勢 2：跨平台、容易保存

- 純文字較容易跨工具讀取，仍需保存編碼與外部資源
- 不依賴特定軟體（Word、Pages）
- 任何裝置都能編輯

#### 優勢 3：整合程式碼與圖表

**傳統方式**：
1. 用軟體畫流程圖
2. 截圖
3. 插入 Word
4. 修改？重新畫→截圖→插入

**Markdown + Mermaid**：
````markdown
```mermaid
graph TD
    A[開始] --> B[步驟一]
    B --> C[步驟二]
    C --> D[結束]
```
````
**修改？直接改文字！**

---

### AI 輸出 Markdown 的範例

**Prompt**：
**Codex CLI（擇一）**
```bash
codex exec "設計一份國小數學「分數加減」教案，用 Markdown 格式輸出，包含：
- 教學目標（條列）
- 教學流程（分段，用標題區分）
- 評量方式（表格呈現）
"
```

**Claude Code（擇一）**
```bash
claude -p "設計一份國小數學「分數加減」教案，用 Markdown 格式輸出，包含：
- 教學目標（條列）
- 教學流程（分段，用標題區分）
- 評量方式（表格呈現）
"
```

**AI 輸出**：
```markdown
# 分數加減教案

## 教學目標
- 學生能理解同分母分數相加
- 學生能運用分數解決生活問題
- 學生能說明分數加法的意義

## 教學流程

### 引起動機（10 分鐘）
使用披薩切片的例子...

### 發展活動（25 分鐘）
1. 教師示範...
2. 學生練習...

## 評量方式

| 評量項目 | 方式 | 佔分 |
|---------|------|------|
| 課堂練習 | 紙筆測驗 | 40% |
| 小組討論 | 觀察紀錄 | 30% |
| 回家作業 | 作業批改 | 30% |
```

---

### Markdown 進階應用：嵌入圖表

#### Mermaid：流程圖、架構圖

**範例：教學流程圖**
````markdown
```mermaid
graph LR
    A[課前準備] --> B[引起動機]
    B --> C[概念講解]
    C --> D[練習活動]
    D --> E[總結評量]
```
````

**優點**：
- 文字描述就能生成圖表
- 修改方便
- 風格統一

---

## Mermaid vs PlantUML：差異與選擇

### 快速比較表

| 比較項目 | Mermaid | PlantUML |
|---------|---------|----------|
| **學習難度** | ⭐⭐ 簡單 | ⭐⭐⭐ 中等 |
| **圖表類型** | 流程圖、甘特圖、類別圖 | UML 全系列、架構圖 |
| **渲染方式** | 瀏覽器即時渲染 | 需要外部工具 |
| **適用對象** | 教師、一般用途 | 軟體工程師 |
| **VSCode 支援** | 內建預覽 | 需安裝擴充 |
| **適合情境** | 教學流程、概念圖 | 系統架構、程式設計 |

### Mermaid 適用情境

#### 1. 教學流程圖
```mermaid
graph TD
    A[第一節課<br/>認識昆蟲] --> B[第二節課<br/>觀察實作]
    B --> C[第三節課<br/>分類整理]
    C --> D[第四節課<br/>成果發表]
```

#### 2. 概念關係圖
```mermaid
graph LR
    A[植物] --> B[光合作用]
    B --> C[氧氣]
    B --> D[養分]
    E[陽光] --> B
    F[水] --> B
    G[二氧化碳] --> B
```

#### 3. 甘特圖（進度規劃）
```mermaid
gantt
    title 專題研究進度
    section 階段一
    文獻蒐集: 2024-10-01, 7d
    section 階段二
    實驗設計: 2024-10-08, 5d
    資料蒐集: 2024-10-13, 10d
    section 階段三
    分析報告: 2024-10-23, 5d
```

### PlantUML 適用情境

#### 1. 系統架構圖
```plantuml
@startuml
package "教學系統" {
  [教案管理]
  [學生管理]
  [成績系統]
}

package "資料庫" {
  database "MySQL"
}

[教案管理] --> [MySQL]
[學生管理] --> [MySQL]
[成績系統] --> [MySQL]
@enduml
```

#### 2. 類別圖（程式設計用）
```plantuml
@startuml
class 學生 {
  +姓名
  +學號
  +成績
  +計算平均()
}

class 教師 {
  +姓名
  +科目
  +教學()
  +評分()
}

學生 "多" -- "1" 教師 : 學習
@enduml
```

### 教師實務建議

**建議使用 Mermaid，理由：**
1. ✅ 學習曲線平緩，30 分鐘上手
2. ✅ VSCode 原生支援，即時預覽
3. ✅ 足夠應付教學需求（流程、概念圖）
4. ✅ Markdown 直接嵌入，不需額外工具

**PlantUML 適合：**
- 資訊科技老師
- 需要繪製軟體架構
- 專案管理複雜圖表

---

## 完整實戰案例：從大綱到完整教材設計

### 情境：設計「大型語言模型」教學教材

**對象**：高中資訊科技課程
**時間**：4 週，每週 2 小時

---

### 階段一：生成教學大綱

**檔案準備**：
在 VS Code 建立並開啟 `llm_course/`，終端機也切換至此資料夾；所有檔案以下採同一層目錄。

**Prompt**：
**Codex CLI（擇一）**
```bash
codex exec "我要為高中生設計『大型語言模型入門』課程，共 4 週。

請生成課程大綱，以 Markdown 格式輸出：

## 課程名稱
## 目標學生
## 課程目標（3-5 點）
## 週次規劃

### 第一週：
- 主題
- 重點概念
- 教學活動

### 第二週：
...

請以 Markdown 格式完整輸出。" > course_outline.md
```

**Claude Code（擇一）**
```bash
claude -p "我要為高中生設計『大型語言模型入門』課程，共 4 週。

請生成課程大綱，以 Markdown 格式輸出：

## 課程名稱
## 目標學生
## 課程目標（3-5 點）
## 週次規劃

### 第一週：
- 主題
- 重點概念
- 教學活動

### 第二週：
...

請以 Markdown 格式完整輸出。" > course_outline.md
```

**生成結果**（部分）：
```markdown
# 大型語言模型入門課程

## 目標學生
高中一、二年級，具備基本電腦操作能力

## 課程目標
- 理解 AI 與大型語言模型的基本概念
- 能操作並評估 AI 工具（如 ChatGPT）
- 認識 AI 的應用與倫理議題
- 培養批判思考與資訊素養

## 週次規劃

### 第一週：認識 AI 與語言模型
**主題**：什麼是 AI？語言模型如何運作？

**重點概念**：
- AI、機器學習、深度學習的關係
- 語言模型的訓練方式
- Transformer 架構（簡化說明）

**教學活動**：
1. 破冰：讓學生試用 ChatGPT，紀錄驚訝與疑問
2. 講解：用比喻說明 AI 如何學習語言
3. 實作：設計不同提示詞，觀察 AI 回應差異

---

### 第二週：提示工程（Prompt Engineering）
...
```

---

### 階段二：根據大綱細化每週教材

**針對第一週，生成詳細教案**：

**Prompt**：
**Codex CLI（擇一）**
```bash
codex exec "根據 course_outline.md 的第一週內容，設計完整的 2 小時教案。

輸出格式（Markdown）：
# 第一週教案：認識 AI 與語言模型

## 教學目標
## 教學準備
## 教學流程（分段，含時間）
### 引起動機（15 分鐘）
### 概念講解（30 分鐘）
### 實作活動（40 分鐘）
### 討論與總結（20 分鐘）
### 休息與轉場（15 分鐘）
## 學習單設計
## 評量方式
## 延伸閱讀

請生成完整內容。" > week1_lesson_plan.md
```

**Claude Code（擇一）**
```bash
claude -p "根據 course_outline.md 的第一週內容，設計完整的 2 小時教案。

輸出格式（Markdown）：
# 第一週教案：認識 AI 與語言模型

## 教學目標
## 教學準備
## 教學流程（分段，含時間）
### 引起動機（15 分鐘）
### 概念講解（30 分鐘）
### 實作活動（40 分鐘）
### 討論與總結（20 分鐘）
### 休息與轉場（15 分鐘）
## 學習單設計
## 評量方式
## 延伸閱讀

請生成完整內容。" > week1_lesson_plan.md
```

---

### 階段三：生成教學簡報大綱

**Prompt**：
**Codex CLI（擇一）**
```bash
codex exec "根據 week1_lesson_plan.md，設計一份教學簡報大綱（15-20 頁）。

以 Markdown 列表方式輸出，每個項目是一頁投影片的標題與重點：

## 投影片大綱

### 第 1 頁：課程標題
- 標題：認識 AI 與語言模型
- 副標題：探索 ChatGPT 背後的科學

### 第 2 頁：破冰活動
- 提問：你用過哪些 AI 工具？
- 互動：掃碼體驗 ChatGPT

...

請包含流程圖建議（用 Mermaid 語法）" > week1_slides_outline.md
```

**Claude Code（擇一）**
```bash
claude -p "根據 week1_lesson_plan.md，設計一份教學簡報大綱（15-20 頁）。

以 Markdown 列表方式輸出，每個項目是一頁投影片的標題與重點：

## 投影片大綱

### 第 1 頁：課程標題
- 標題：認識 AI 與語言模型
- 副標題：探索 ChatGPT 背後的科學

### 第 2 頁：破冰活動
- 提問：你用過哪些 AI 工具？
- 互動：掃碼體驗 ChatGPT

...

請包含流程圖建議（用 Mermaid 語法）" > week1_slides_outline.md
```

---

### 階段四：生成學習單

**Prompt**：
**Codex CLI（擇一）**
```bash
codex exec "根據 week1_lesson_plan.md，設計一份學習單。

格式：
# 學習單：認識 AI 與語言模型

## 第一部分：課前暖身（3 題）
## 第二部分：實作紀錄
### 任務一：設計 3 個提示詞
| 提示詞 | AI 回應摘要 | 你的觀察 |
|--------|------------|---------|
| ... | ... | ... |

## 第三部分：反思問題（2 題）
## 第四部分：延伸挑戰（選做）

請以 Markdown 表格與條列方式輸出完整內容。" > week1_worksheet.md
```

**Claude Code（擇一）**
```bash
claude -p "根據 week1_lesson_plan.md，設計一份學習單。

格式：
# 學習單：認識 AI 與語言模型

## 第一部分：課前暖身（3 題）
## 第二部分：實作紀錄
### 任務一：設計 3 個提示詞
| 提示詞 | AI 回應摘要 | 你的觀察 |
|--------|------------|---------|
| ... | ... | ... |

## 第三部分：反思問題（2 題）
## 第四部分：延伸挑戰（選做）

請以 Markdown 表格與條列方式輸出完整內容。" > week1_worksheet.md
```

---

### 階段五：生成評量試題

**Prompt**：
**Codex CLI（擇一）**
```bash
codex exec "根據 week1_lesson_plan.md，設計評量題目。

# 第一週評量

## 選擇題（5 題）
測驗基本概念理解

## 簡答題（3 題）
測驗應用與思考

## 實作題（1 題）
設計一個教學情境的 AI 應用，並說明提示詞設計

請附標準答案與評分標準。" > week1_assessment.md
```

**Claude Code（擇一）**
```bash
claude -p "根據 week1_lesson_plan.md，設計評量題目。

# 第一週評量

## 選擇題（5 題）
測驗基本概念理解

## 簡答題（3 題）
測驗應用與思考

## 實作題（1 題）
設計一個教學情境的 AI 應用，並說明提示詞設計

請附標準答案與評分標準。" > week1_assessment.md
```

---

### 階段六：整合所有檔案

**資料夾結構**（第一週完成後，與上面指令一致）：
```
llm_course/
├── course_outline.md
├── week1_lesson_plan.md
├── week1_slides_outline.md
├── week1_worksheet.md
└── week1_assessment.md
```

其他週次請同樣建立對應檔案後再整合；不存在的週次不可讓 AI 補寫成「已完成」。

**最後整合指令**：
**Codex CLI（擇一）**
```bash
codex exec "統整目前資料夾中 course_outline.md 與 week1_ 開頭的檔案，生成一份『完整課程手冊』，包含：
- 目錄（自動生成連結）
- 課程概覽
- 各週教學內容（引用各檔案）
- 附錄（參考資源、延伸閱讀）

只回傳手冊 Markdown 內容，不要自行寫入檔案" > course_handbook.md
```

**Claude Code（擇一）**
```bash
claude -p "統整目前資料夾中 course_outline.md 與 week1_ 開頭的檔案，生成一份『完整課程手冊』，包含：
- 目錄（自動生成連結）
- 課程概覽
- 各週教學內容（引用各檔案）
- 附錄（參考資源、延伸閱讀）

只回傳手冊 Markdown 內容，不要自行寫入檔案" > course_handbook.md
```

---

### 完整流程圖

```mermaid
graph TD
    A[生成課程大綱] --> B[細化週次教案]
    B --> C1[教學簡報大綱]
    B --> C2[學習單]
    B --> C3[評量試題]
    C1 --> D[整合成課程手冊]
    C2 --> D
    C3 --> D
    D --> E[轉換成 PDF/Word]
```

---

### 時間效益分析（課堂試算，非實測保證）

| 任務 | 傳統方式 | AI + CLI 方式 | 節省時間 |
|------|---------|--------------|---------|
| 課程大綱 | 2 小時 | 5 分鐘 + 調整 15 分鐘 | 約 83% |
| 單週教案 | 3 小時 | 10 分鐘 + 調整 30 分鐘 | 約 78% |
| 學習單 | 1.5 小時 | 5 分鐘 + 調整 20 分鐘 | 約 72% |
| 評量設計 | 2 小時 | 10 分鐘 + 調整 30 分鐘 | 約 67% |
| **表內四項合計** | **8.5 小時** | **2 小時 5 分鐘** | **約 75%（試算）** |

---

## 實用指令總結

### 多檔案整合分析
**Codex CLI（擇一）**
```bash
# 分析整個資料夾
codex exec "分析這個資料夾的所有檔案並生成摘要"

# 指定特定檔案
codex exec "整合 file1.txt, file2.txt, file3.txt 的內容"
```

**Claude Code（擇一）**
```bash
# 分析整個資料夾
claude -p "分析這個資料夾的所有檔案並生成摘要"

# 指定特定檔案
claude -p "整合 file1.txt, file2.txt, file3.txt 的內容"
```

### 輸出為 Markdown 檔案
**Codex CLI（擇一）**
```bash
# 直接輸出
codex exec "生成教案" > lesson.md

# 追加內容
codex exec "生成評量" >> lesson.md
```

**Claude Code（擇一）**
```bash
# 直接輸出
claude -p "生成教案" > lesson.md

# 追加內容
claude -p "生成評量" >> lesson.md
```

### 使用 Mermaid 圖表
**Codex CLI（擇一）**
```bash
codex exec "設計教學流程，用 Mermaid 流程圖呈現" > flow.md
```

**Claude Code（擇一）**
```bash
claude -p "設計教學流程，用 Mermaid 流程圖呈現" > flow.md
```

### 批次處理
**Codex CLI（擇一）**
```bash
# 為每個單元生成教案
for unit in unit1 unit2 unit3; do
  codex exec "閱讀 $unit/source.md，僅依來源生成教案，不要寫檔" > ${unit}_plan.md
done
```

**Claude Code（擇一）**
```bash
# 為每個單元生成教案
for unit in unit1 unit2 unit3; do
  claude -p "閱讀 $unit/source.md，僅依來源生成教案，不要寫檔" > ${unit}_plan.md
done
```

---

**學習銜接**：完成後回到[單元四](04_workspace.html)的練習任務。

### PowerShell 7 批次操作對照

先確認 `unit1`、`unit2`、`unit3` 各有 `source.md`，以下兩種選一種；每次產生的是獨立任務，提示需指定來源。

```powershell
foreach ($unit in @('unit1', 'unit2', 'unit3')) {
    codex exec "閱讀 $unit/source.md，僅依來源生成教案，將 Markdown 內容回傳，不要寫檔" > "${unit}_plan.md"
    if ($LASTEXITCODE -ne 0) { throw "生成失敗：$unit" }
}
```

Claude Code 路線把該行改為 `claude -p "閱讀 $unit/source.md，僅依來源生成教案，將 Markdown 內容回傳，不要寫檔" > "${unit}_plan.md"`。不把失敗後留下的空檔當成完成。
