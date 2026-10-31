# Proposal: 以前置依賴與學習任務重整前導章

## Why
00_intro.md 目前混合概念、安裝比較、操作、歷史盤點與維護紀錄。第5.9節先使用第6章才建立的專案及第7.4節才提供的筆記；Node安裝細節阻斷入門；macOS路線後置；Python實作又插入Node安裝。使用者要求更清楚的架構與邏輯順序。

## What
只重整前導章的章節、銜接、重複敘述與內文引用，保留完整教材的有效內容、範例與圖形。主線依先備條件排列，進階背景與歷史移至同文件附錄。同步00_intro.html與課程索引的介紹文字；其他章節的既有深層連結保持可用。沿用已核准的互動CLI操作與斜線指令教學。

## How
以 proposed-outline.md 的章節對照執行；先建立學習者能完成的最短連續路線，再安置選讀細節。每節寫清楚目的、前提、操作與成功判準，避免要求讀者往後找尚未準備的檔案。

## Impact
AI_Agent_CLi/00_intro.md、00_intro.html、index.html。檔名、課程序號與整體設計保留。前一互動修訂已驗證並推送至feat/prioritize-interactive-cli-teaching，尚未合併；本次完成後一起交付PR。

## Risks
移動段落可能遺漏來源、範例、舊錨點或把歷史測試誤當本次測試。保留內容對照表，重編主文引用，明確區隔歷史紀錄；舊錨點映射到相同主題的新位置。

## Complexity Review
- **Signals:** None；2需求、2任務，單一靜態教材表面。
- **Expected verification cost:** Medium；需要前置依賴與內容保留人工審查，以及深層連結驗證。
- **Recommendation:** Keep as one change。
- **Rationale:** 前導章的順序與引用需一併調整才能連續閱讀。
