# Proposal: CLI 教材以互動對話為主線

## Why
使用者指出初學者日常操作應在 CLI 會話中以自然語言溝通。目前多章雖稱互動為主線，實例卻反覆使用 `codex exec`、`claude -p`，造成教學順序與實作不一致。

## What
- 統一為：在專案終端機輸入 `codex` 或 `claude` 一次，進入會話後輸入自然語言，逐輪追問與驗收。
- 一般讀檔、摘要、教案、評量與保存產物改為共用的自然語言提示；保留原學科情境與任務要求。
- 進階章節同樣使用 CLI 對話：透過介面管理 session、context、token 用量與模型；批次任務由對話引導 Agent 建立及執行腳本，不推薦「CLI 指令＋prompt」操作。
- AGENTS.md／CLAUDE.md 改為獨立的專案指引說明，連至 05_instructions.html。
- 同步 Markdown 與 HTML，巡查索引與其他章節的操作說明。保留編號、檔名、設計、圖片及既有舊網址導向。

- 加入兩款 CLI 各自的常用會話內斜線指令速查，涵蓋模型、用量、狀態、context 與會話管理；查核 `/model`、`/usage`、`/status`、`/compact`、`/resume`、`/help` 等候選指令，僅列各工具實際支援者，附使用時機與自然語言銜接範例。

## How
先修正入門與重複的操作約定，再逐一依教學目的改寫案例，區分終端機指令與會話提示。最後檢查雙版本、連結與代表頁面。

## Impact
主要涉及 00_intro、04_workspace、04a_workflows、06_lesson_plans、06a_assessment 的 Markdown／HTML，以及 07_agents_cli.html、09_cli_practice.html；其餘教材唯讀巡查一致性。

## Risks
不可只移除指令前綴而遺失輸出檔名、來源或驗收條件；保存檔案須在提示中明確指定並檢查實際產物。自然語言的「不要修改」不是系統權限設定。批次教學保留任務規劃、腳本檢查、執行授權及失敗處理，但從對話驅動。介面功能依各工具官方支援說明，不假設兩款工具功能或用量顯示完全相同。

## Complexity Review
- **Signals:** None（3 個需求、2 個任務、單一教材表面）。
- **Expected verification cost:** Medium；多份 Markdown／HTML 需一致，並需人工判讀實例語境。
- **Recommendation:** Keep as one change。
- **Rationale:** 所有修改共同建立同一操作主線；拆分會使章節互相矛盾。
