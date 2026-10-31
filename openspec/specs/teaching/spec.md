# Teaching Specification

Synced from approved revise-ai-agent-cli-teaching and explicit user filename amendment, 2026-10-31.


### Requirement: REQ-TEACH-001 — 新版入口與前導章
系統 MUST 在 AI_Agent_CLi/index.html 將 00_intro.html 與其 Markdown 來源列於六單元之前；保留完整前導教材並使用既有 assets 圖形。

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
雙 CLI 教材 MUST 提供按平台區分的安裝、更新、版本檢查、登入、專案啟動、互動會話操作與排錯資訊，逐項引用官方來源與查核日期；區分 shell 指令和會話指令、安裝依賴與專案依賴。一般與進階任務均以會話為主，不要求教授啟動指令附帶 prompt 或單次執行。

#### Scenario: 官方安裝與操作依據驗收
- GIVEN 新版教材已產生
- WHEN 初學者依 Windows 或 macOS 路線閱讀
- THEN 能選一款 CLI 完成首個互動任務並辨識成功判準，不需安裝另一款

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
