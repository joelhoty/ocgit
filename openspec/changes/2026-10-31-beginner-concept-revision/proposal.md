# Proposal: 入門概念版重整

## Why
使用者審查 AI_Agent_CLi 教材後確認：受眾是想學 AI 應用的入門使用者，不限高中生或教師；教材定位為概念教材，實作問題另行記錄修正；主要環境是 VS Code 管理檔案、終端機 Agent 產生與管理內容。

## What
- 前導章改為短版概念 → VS Code 工作台 → CLI → 第一個任務 → 專案規則 → 回看系統架構 → 會話 → 穩定工作 → 基礎評量 → Python 延伸；排錯集中為索引，附錄 A 依查閱頻率排序，歷史紀錄移至 00_intro_history.md。
- 單元一至六修正事實、矛盾與受眾說明；單元四改以多檔案工作為重點。
- 07、09 移除與前導章重複的安裝與指令表；08 併入前導章；11、12 併入 10。舊網址保留導向。
- 參考資料與查證紀錄集中於 AI_Agent_CLi/index.html，記錄檢索日期與查證方式。

## Not in scope
練習資料包、各單元專案資料夾統一、Windows 實測，留待實作修正時處理。

## Validation
validation/render_intro.py 由 Markdown 渲染前導章並保留舊錨點；validation/check_intro.py 檢查順序、錨點、程式未變與 Markdown/HTML 一致。anchor-map.json 是舊錨點對照表。
