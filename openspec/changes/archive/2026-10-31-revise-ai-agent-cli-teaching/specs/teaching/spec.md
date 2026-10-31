# Delta for Teaching

## ADDED Requirements

### Requirement: REQ-TEACH-001 — 新版入口與前導章
系統 MUST 在 AI_Agent_CLi/index_content.html 將 AI_working_env_b05.html 與其 Markdown 來源列於六單元之前；保留完整前導教材並使用既有 assets 圖形。

#### Scenario: 新版入口與前導章驗收
- GIVEN 新版教材已產生
- WHEN 開啟課程目錄
- THEN 先看見前導章，圖片載入且可進入單元一

### Requirement: REQ-TEACH-002 — 保留課程結構與設計
教材 MUST 保留原六單元順序、章節功能、跨科練習、補充與素養教材及深色卡片／程式碼／圖表設計；既有 HTML/Markdown 配對內容 MUST 一致。

#### Scenario: 保留課程結構與設計驗收
- GIVEN 新版教材已產生
- WHEN 逐頁比較新舊教材
- THEN 原教學目的與結構仍可對照，沒有以摘要替代整份教材

### Requirement: REQ-TEACH-003 — 官方安裝與操作依據
雙 CLI 教材 MUST 提供按平台區分的安裝、更新、版本檢查、登入、專案啟動、互動及單次執行與排錯資訊，逐項引用官方來源與查核日期；區分 shell 指令和會話指令、安裝依賴與專案依賴。

#### Scenario: 官方安裝與操作依據驗收
- GIVEN 新版教材已產生
- WHEN 初學者依 Windows 或 macOS 路線閱讀
- THEN 能選一款 CLI 完成首個任務並辨識成功判準，不需安裝另一款

### Requirement: REQ-TEACH-004 — 專案指引與權限
教材 MUST 分別教授 Codex AGENTS.md 與 Claude Code CLAUDE.md，核對當前 AGENTS.md 相容條件；說明指引、工具權限與 sandbox 的差別。

#### Scenario: 專案指引與權限驗收
- GIVEN 新版教材已產生
- WHEN 學習者完成單元五
- THEN 能建立各工具有效的規則並驗證載入，不誤認文字規則具有強制隔離能力

### Requirement: REQ-TEACH-005 — 漸進實作與能力邊界
六單元 MUST 維持教材生成、圖片、來源知識庫、環境、規則及讀檔教案的進程；雙 CLI 任務提供輸入、提示、產物與驗收條件；圖片與 NotebookLM 功能不誤植為 CLI 內建。

#### Scenario: 漸進實作與能力邊界驗收
- GIVEN 新版教材已產生
- WHEN 依任一 CLI 路線完成實作
- THEN 能核對輸出與來源，辨識額外工具、人工操作與可用性限制

### Requirement: REQ-TEACH-006 — 新版導航完整性
新版所有課內頁面與圖片連結 MUST 指向 AI_Agent_CLi 內對應資源，索引與前後導覽一致；外部參考保持原官方目的地。

#### Scenario: 新版導航完整性驗收
- GIVEN 新版教材已產生
- WHEN 由新版索引巡覽所有課程連結
- THEN 沒有返回 GeminiForDesignTeaching 的內部導航或失效本地連結

### Requirement: REQ-TEACH-007 — 舊入口相容與網站清單
既有 HTML 網址 MUST 保留可用的新版對應連結與導向，根目錄課程索引與清單 MUST 更新至新版；舊 Markdown 保留作為歷史檔。

#### Scenario: 舊入口相容與網站清單驗收
- GIVEN 新版教材已產生
- WHEN 開啟任一舊 HTML 入口，包含停用 JavaScript 的情境
- THEN 可到達對應新版，仍有明確可點擊的替代連結

### Requirement: REQ-TEACH-008 — 可追溯驗證
交付 MUST 附來源查核、檔案對照、連結檢查與代表性桌面／手機視覺證據；不得把文件查核說成已執行付費 CLI 或全平台安裝測試。

#### Scenario: 可追溯驗證驗收
- GIVEN 新版教材已產生
- WHEN 審閱驗證報告
- THEN 每項需求有證據或明確限制，使用者原有無關修改未被覆寫

## MODIFIED Requirements

無既有主規格；本次將教材需求首次規格化，全部列於 ADDED。

## REMOVED Requirements

無。
