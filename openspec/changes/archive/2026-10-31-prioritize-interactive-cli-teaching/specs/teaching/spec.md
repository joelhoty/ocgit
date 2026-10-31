# Delta for Teaching

## ADDED Requirements

### Requirement: REQ-TEACH-009 — 互動會話教學主線
教材 MUST 以啟動一次 CLI 後在同一會話輸入自然語言作為一般教學任務主線，清楚區分 shell 與 AI 會話輸入。

#### Scenario: 讀檔並追問
- GIVEN 學習者在專案資料夾啟動 codex 或 claude
- WHEN 依教材完成摘要與後續修改
- THEN 使用共用自然語言提示，不需每輪重啟 CLI；保留來源、輸出檔名及驗收要求。

### Requirement: REQ-TEACH-010 — 進階互動管理與專案指引分離
教材 MUST 在進階任務繼續以 CLI 對話與內建介面為主，不推薦 exec／-p 或啟動指令附帶 prompt；MUST 說明 session、context、token 用量及模型選擇的工具差異與實際可用操作。專案指引檔 MUST 獨立說明，不列為操作指令。

#### Scenario: 初學者閱讀操作約定
- GIVEN 學習者閱讀章首約定
- WHEN 學習啟動與提問
- THEN 不需先學單次輸出或批次腳本，且能另循連結了解 AGENTS.md／CLAUDE.md。

#### Scenario: 進階批次處理
- GIVEN 學習者在 CLI 會話處理批次任務
- WHEN 以自然語言要求規劃、建立及執行腳本
- THEN 教材引導檢查腳本、授權與結果，並示範管理會話、context、用量及模型，不需使用指令附帶 prompt。

### Requirement: REQ-TEACH-011 — 互動修訂跨版本一致
修訂 MUST 同步 Markdown 與 HTML，保留既有教學情境、編號、檔名、視覺設計、導覽與圖片。

#### Scenario: 閱讀兩種格式
- GIVEN 同一章的 Markdown 與 HTML
- WHEN 比對操作案例與閱讀連結
- THEN 操作步驟與提示一致，連結可用且頁面保留原設計。

#### Scenario: 會話內常用指令速查
- GIVEN 學習者已進入 Codex CLI 或 Claude Code
- WHEN 查詢模型、用量、狀態或管理會話與 context
- THEN 教材分別列出官方支援的斜線指令（查核 /model、/usage、/status、/compact、/resume、/help 等），說明輸入位置、用途、使用時機及功能差異，不假設同名指令兩款皆有。

## MODIFIED Requirements

### Requirement: REQ-TEACH-003 — 官方安裝與操作依據
雙 CLI 教材 MUST 提供按平台區分的安裝、更新、版本檢查、登入、專案啟動、互動會話操作與排錯資訊，逐項引用官方來源與查核日期；區分 shell 指令和會話指令、安裝依賴與專案依賴。一般與進階任務均以會話為主，不要求教授啟動指令附帶 prompt 或單次執行。
(Previously: 操作資訊要求包含互動及單次執行；依使用者本次明確指示，取消單次執行教學要求。)

#### Scenario: 官方安裝與操作依據驗收
- GIVEN 新版教材已產生
- WHEN 初學者依 Windows 或 macOS 路線閱讀
- THEN 能選一款 CLI 完成首個互動任務並辨識成功判準，不需安裝另一款
