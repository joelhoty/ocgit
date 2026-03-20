# Git版本管理與GitHub協作 (v0.1)
學習基本操作並了解運作原理及邏輯

根據這個目標大綱，設計完整的網頁內容，包含index.html並擴充教材各章節與檔案，作為完整的學習教材資源
之後的變更計劃都需保留在 plan.md 中，並以時間戳記條目方式追加紀錄，不覆蓋既有內容。
## Git版本管理介紹與基本操作

### Repo的概念與原理
1.  Repo的定義與用途
2.  Repo id
3.  資料庫與索引、hash?  
### init的指令
1.  指令概念
2.  git init後程式做了哪些動作

### commit
1.  commit的概念與用途
2.  commit id
3.  commit的內容與結構 
4.  commit的歷史紀錄與版本回溯
5.  commit 後程式做了哪些動作

## GitHub協作與版本控制
### GitHub的概念與功能
1.  GitHub帳號註冊與設定
2.  GitHub上的Repo管理與操作
3.  GitHub的協作功能：Pull Request、Issue、Branch等
4.  GitHub的版本控制與歷史紀錄

## PR、Issue、Branch的概念與應用深入探討
### Pull Request的概念與流程
### Branch
### ISSUE
### merge


## 進階使用
### rebase
### revert
### reset
### stash

---

## 變更紀錄

### 2026-03-19 19:17 — v1 初版教材建立
- **版本資料夾**: `v1/`
- **建立檔案**:
  - `v1/index.html` — 課程首頁（目錄、學習路徑、章節導航）
  - `v1/assets/styles_b01.css` — 全站樣式（Git 主題色 #f05033）
  - `v1/assets/app_b01.js` — 側邊導航、頁面導航、Tab 切換、Mermaid 初始化
  - `v1/pages/01-repo-concept.html` — Repository 概念與原理（物件資料庫、SHA-1、暫存區、三層架構）
  - `v1/pages/02-git-init.html` — Git Init 指令（.git 目錄結構、HEAD、常用初始設定）
  - `v1/pages/03-commit.html` — Commit 提交（快照概念、commit ID、內部結構、git log、版本回溯、Commit Message 規範）
  - `v1/pages/04-github-collaboration.html` — GitHub 協作平台（帳號設定、SSH Key、Remote 操作、push/pull 流程）
  - `v1/pages/05-pr-issue-branch.html` — PR / Issue / Branch（分支操作、Merge、衝突解決、PR 流程、Issue 管理、分支策略）
  - `v1/pages/06-advanced-usage.html` — 進階操作（rebase、revert、reset 三種模式、stash、四指令比較）
- **設計特色**:
  - 沿用 WEB Service 教學網站的 sidebar + content 佈局與 CSS 架構
  - 每章皆含 Mermaid 流程圖、表格比較、Example Showcase（Tab 切換）、動手練習與章節小結
  - 頁面導航（上一頁/下一頁）與側邊導航由 JS 動態產生
  - Mermaid 透過本機 node_modules 載入，支援離線瀏覽

### 2026-03-19 19:49 — Hub 頁面與第 07 章（GitHub Pages & Actions）
- **新增檔案**:
  - `Network/Git/index.html` — 版本 Hub 頁面，統整所有版本入口（自包含 CSS，無外部依賴）
  - `v1/pages/07-github-pages-actions.html` — 第 07 章：GitHub Pages、Actions 與進階應用
  - `v1/assets/app_b02.js` — 更新導航設定，新增第 07 章條目（共 8 頁：index + ch01–07）
  - `v1/index_b02.html` — 更新課程首頁，新增第 07 章卡片、更新學習路徑流程圖與能力清單
- **第 07 章內容涵蓋**:
  - GitHub Pages 三種部署方式（手動分支、docs 資料夾、Actions 自動部署）
  - GitHub Actions 概念（CI/CD、Workflow、Runner、Job、Step）
  - YAML 語法與三個完整工作流範例（靜態網站部署、Node.js CI、自動建立 Release）
  - 進階工具：Codespaces、Copilot、Discussions、Packages、Projects、Dependabot、Branch Protection
  - GitHub 免費方案額度說明
  - 動手練習與章節小結
- **注意事項**:
  - Hub 頁面（`Network/Git/index.html`）連結至 `v1/index_b02.html`
  - 第 01–06 章仍參照 `app_b01.js`（6 章導航），第 07 章與 index_b02 參照 `app_b02.js`（7 章導航）
  - 各版本內部導航保持一致，不影響既有頁面功能

### 2026-03-19 19:59 — 第 07 章 GitHub Actions 內容強化（b02）
- **新增檔案**:
  - `v1/pages/07-github-pages-actions_b02.html` — 大幅擴充 GitHub Actions 的六大核心概念說明
- **強化內容**:
  - 新增「六大核心概念」總覽段落，含彩色層級架構圖（Mermaid）與劇場類比表
  - 新增六個獨立深入解說段落：
    - **① Workflow**：檔案結構、多 workflow 管理、YAML 基本結構範例
    - **② Event**：6 種常用事件表格、進階篩選（分支 / 路徑 / cron / 手動觸發）各含 Tab 範例
    - **③ Job**：平行 vs 依賴執行（Mermaid 圖）、6 個重要屬性表、needs / matrix / 條件執行三個 Tab 範例
    - **④ Step**：run vs uses 兩種類型對照、8 個常用屬性表、Step 間傳遞資料（$GITHUB_OUTPUT）
    - **⑤ Action**：Marketplace 生態、uses 語法格式、7 個常用官方 Action 表、安全建議
    - **⑥ Runner**：GitHub-hosted vs Self-hosted 比較、三種 OS 規格與費率表、預裝工具
  - 新增「六大概念互動關係回顧」段落：Sequence Diagram + 完整標註範例
  - 新增「Secrets 與環境變數」段落：安全管理機密、三層級 env 設定
  - 練習擴充：新增練習 3（矩陣策略）與練習 4（Actions 部署 Pages）
  - 小結更新：知識重點從 5 點擴充至 9 點，涵蓋六大概念與 Secrets
- **注意事項**:
  - b02 為完整獨立檔案，b01 保留不變
  - 導航仍使用 `app_b02.js`，與 index_b02.html 一致
---

### 變更紀錄 — 2026-03-19 20:15 (UTC+8)

- **變更主題**: 新增 VM 通識概念（ch07 b03）+ 新建第 08 章 Runner 進階應用
- **變更動機**: 使用者想了解 Runner VM 能做什麼、虛擬機器的通識概念，以及 Runner 的進階應用場景
- **新增 / 修改檔案**:
  1. `v1/pages/07-github-pages-actions_b03.html` — 第 07 章 b03 版
     - 在 Runner 概念 ⑥ 後新增「虛擬機器（VM）通識概念」段落
     - 涵蓋：VM 定義、Hypervisor（Type-1/Type-2）、VM 架構圖（Mermaid）、VM vs Container 比較表、VM 在現代開發中的 6 大角色、為什麼 Runner 使用 VM
     - 章末導航更新：下一章指向第 08 章
     - 小結更新：新增 VM 相關知識點、課程回顧提及第 08 章
  2. `v1/pages/08-runner-advanced.html` — 全新第 08 章（674 行）
     - 8.1 Runner 在 CI/CD 中的角色
     - 8.2 GitHub-hosted Runner 深入（規格、預裝軟體、Image 更新週期、Larger Runner）
     - 8.3 Self-hosted Runner 完整指南（安裝步驟、Runner Group、Label 系統）
     - 8.4 Docker 整合模式（Container Job、Service Container、自訂 Image）
     - 8.5 進階技巧（快取 actions/cache、Artifact、Matrix 策略、除錯 ACTIONS_STEP_DEBUG / tmate）
     - 8.6 實際應用場景（前端部署、後端 Docker、作業批改、文件生成、安全掃描、多平台發布）
     - 8.7 動手練習 × 4 題
     - 8.8 章節小結
  3. `v1/assets/app_b03.js` — 導航 JS 更新至 9 頁（index + ch01–08）
  4. `v1/index_b03.html` — 首頁 b03 版
     - 新增第 08 章卡片
     - Mermaid 學習路徑圖新增 ch08 節點
     - 新增「想深入 CI/CD」閱讀路徑卡片
     - 能力清單新增 VM 通識與 Runner 進階技能
     - script 引用更新至 app_b03.js
  5. `Network/Git/index.html` — Hub 頁面
     - v1 連結更新至 index_b03.html
     - 章節清單新增第 08 章
     - 描述文字更新
- **注意事項**:
  - b03 / 新檔案皆為完整獨立文件
  - 第 08 章 `data-page` ID 為 `runner-advanced`
  - ch01–06 仍引用 app_b01.js，ch07 b01 引用 app_b02.js，保持舊版內部一致性
