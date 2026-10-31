# 教材改版提案：AI Agent CLI 設計教學

## Why
原教材以 Gemini CLI 與 gemini.md 為主，需改為 Codex CLI 與 Claude Code，並更新安裝、登入、操作、專案指引與教學實作。使用者要求保留原有結構與設計，包含索引與全部漸進單元，並把既有 AI_working_env_b05.md 放在前面作為 Agent 基本介紹與環境建議。

## What
- 正式教材入口為 `AI_Agent_CLi/index_content.html`，沿用目標資料夾的實際大小寫。
- 前導教材保留完整概念與實作內容，校訂時效性資訊，產生相同風格的 HTML；圖形使用現有 `AI_Agent_CLi/assets/agent_layers_b01.svg`。
- 保留六單元順序、教學目標、核心概念、操作、跨科範例、練習與問答。前導章置於單元一之前。
- 全部原有 24 個檔案逐一納入新版；HTML 與既有 Markdown 配對同步修訂，CLI 主線全面改為 Codex CLI／Claude Code。
- 保留圖片生成、NotebookLM、媒體素養等原有教學目的；不把 NotebookLM 重新命名為 CLI，也不宣稱任一 CLI 預設具有圖片生成能力。相關實作說明實際使用的服務或工具與前提。
- 新版內部連結只連向新版；根目錄網站索引與教材清單同步更新。
- 提案建議舊 HTML 路徑保留導向頁與可點擊的新版連結，舊 Markdown 保留為歷史版本。這項相容性安排尚待本提案核准。
- 不安裝 CLI、不登入付費帳號、不部署網站、不推送 Git；保留使用者現有修改 `repo.log` 與新提供的 assets。

## How
先依官方文件建立來源與指令對照，再以原頁面模板逐章改寫，最後核對來源、章節一致性、導航與桌面／手機顯示。前導章提供概念與環境全貌，單元四聚焦教學專案的環境實作，單元五聚焦規則，單元六整合讀檔與教案產出。

## Impact
完整來源／目標檔案對照見 design.md。另涉及根目錄 index.html、README.md、git_index.md、CONTRIBUTING.md 的相關課程入口與清單。驗證報告與來源紀錄留在本次變更目錄。

## Risks
- 官方功能變動：安裝與指令均記查核日期、官方來源與平台；無法確認的功能明示限制，不由產品名稱推論。
- 指引載入差異：分別核對 Codex AGENTS.md 與 Claude Code CLAUDE.md，以及新版 Claude Code 的 AGENTS.md 支援條件，不沿用舊印象。
- 網址與資源遺失：逐一檢查新版相對連結與舊網址對照；無法取回的原始大綱連結改為清楚的來源說明，不建立空白假檔案。
- 大幅改寫失去教學內容：維持原章節層級與跨科情境，逐頁對照；避免僅替換產品名稱或把完整教材縮成摘要。

## Complexity Review
- **Signals:** None；8 requirements、5 top-level tasks、7 outcome/gate checkboxes；教學內容、靜態呈現與導航兩個主要面向。
- **Expected verification cost:** Medium；24 個來源檔案加前導教材，需核對雙工具命令、HTML/Markdown 與導航。
- **Recommendation:** Keep as one change。
- **Rationale:** 使用者要求完整課程改版，安裝、規則與實作必須一致；任務分組執行，統一交付。

## 已確認的使用者決定
完整 SOS 流程；保留原結構與設計；雙 CLI 主線；AI_working_env_b05.md 前置；新版圖形來自 AI_Agent_CLi/assets；新版教材內連結以新版為主。舊網址導向屬本提案建議，尚未實作。
