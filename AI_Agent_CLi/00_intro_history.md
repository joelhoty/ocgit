# 前導章版本與歷史驗證紀錄

本檔保存前導章的維護紀錄，不是學習內容。內文的節號指向當時版本；紀錄描述當時的狀態，不代表目前教材或讀者電腦已重新驗證。

## 教師電腦的歷史盤點

以下是原稿查核日 2026-10-29 的教師筆電，保留為判讀案例，不代表讀者電腦或本次重新盤點。

| 工具 | 盤點結果 | 判讀與建議 |
|---|---|---|
| Claude Code 2.1.312 | 原生版，Mach-O arm64 | 符合官方推薦；不需處理 |
| Codex 0.165.0 | standalone 版，Mach-O arm64 | 歷史盤點的 standalone 安裝；依官方方式重跑安裝或使用支援的 `codex update` |
| Antigravity CLI | 未安裝 | 若要示範 Google 路線，用官方腳本安裝 |
| Gemini CLI 0.42.0 | npm 全域安裝，nvm 的 Node 22.20.0 與 `/usr/local` 的 Node 22.14.0 各有一份 | 已被 `agy` 取代且重複安裝；依 5.5 遷移到 `agy` 後移除兩份 |
| Node.js | nvm 22.20.0、`/usr/local` 官方安裝包 22.14.0、Homebrew `node` 24.x（未連結） | 三個來源並存，容易讓 `npm -g` 裝到非預期位置；保留一個管理方式即可 |

同名指令出現多個版本時，先確認目前使用哪一份，再處理舊安裝，避免誤刪正在使用的版本。

## 版本記錄

| 版本 | 日期 | 變更 |
|---|---|---|
| b01 | 2026-10-29 | 由原始大綱擴寫完整教材；納入 Joel 六層分層圖；查核原生 CLI 與 Node.js 依賴；加入 Windows／macOS、Git、AGENTS.md、uv、Python 實作與評量 |
| b02 | 2026-10-29 | 依官方安裝頁重新核對三款 CLI：3.2 拆分「安裝時／執行時」Node 依賴並加安裝方式總表；Codex 改用官方一行安裝指令並補 `codex update`、npm 版需 Node 執行；Claude Code 補 CMD 指令、`claude doctor`、帳號前提與 Git for Windows 說明；Antigravity 補 CMD、安裝位置、驗證方式與自動更新；Google 路線改為只用 `agy`，刪除 Gemini CLI 的安裝步驟與比較列，5.5 只保留舊 `gemini` 指令的遷移與移除；3.2 新增「Rust 撰寫是否就不需要 Node」說明；新增 5.8 既有安裝盤點；補 macOS Homebrew cask、Node LTS 現況與 Q&A |
| b03 | 2026-10-29 | 3.2 重寫為 6 小節：先定義原生執行檔、腳本、安裝腳本、套件管理器，再釐清「原生版」「standalone」「npm 版」的差別，分開說明安裝時、執行時、任務時的需求，加 Mermaid 流程圖、逐一對照表與自我檢查指令；Codex 官方來源改為 [Codex CLI 官方頁](https://learn.chatgpt.com/docs/codex/cli)，5.3 新增官方四個安裝分頁（macOS/Linux、Windows、npm、Homebrew）的安裝與更新指令對照，更新方式改以官方「重跑安裝指令」為主 |
| b04 | 2026-10-29 | 3.2 開頭新增「總結：不需要先裝好 Node.js」，附 6 種情況的判斷表與 Mermaid 決策圖；3.2.6 改為只列官方安裝指令，結論集中在開頭 |
| b05 | 2026-10-29 | 3.2 改為「先比較安裝方式，再下結論」：新增 3.2.1 四種安裝方式（官方安裝腳本、Homebrew、WinGet、npm）的基本資料與優缺點比較、3.2.2 依使用者情境的建議與結論；原 3.2.1–3.2.6 順延為 3.2.3–3.2.8 |
| b05 課程改版 | 2026-10-31 | 前置為課程基礎章，採 Codex CLI／Claude Code 雙主線；保留 Antigravity 選讀；明列 CLAUDE.md 與 AGENTS.md 的版本／載入條件；補互動及單次操作，複核 Homebrew 平台與修正 PowerShell 版本差異；保留原稿歷史測試並標明本次未重跑 |
| 本次閱讀順序重整 | 2026-10-31 | 主線依概念、環境、專案、CLI、首次任務與會話管理排列；平台步驟前置，Node 與安裝細節、Google 遷移、歷史紀錄集中附錄；保留互動操作與斜線指令教學 |
| 入門概念版重整 | 2026-10-31 | 受眾改為入門使用者；以 VS Code 工作台為主場；主線改為短版概念 → 工作台 → CLI → 第一個任務 → 專案規則 → 回看系統架構；Python 改為基礎評量後的延伸；排錯集中為索引；附錄 A 依查閱頻率排序；歷史紀錄移至本檔 |

## 原 b05 歷史驗證紀錄與本次限制

以下 2026-10-29 的實測與 Jev 紀錄隨使用者提供的原稿保留，僅描述原版，不能作為本次課程改版已重新執行的證據。本次 2026-10-31 核對官方文件、Markdown/HTML 內容及本地資源，未安裝 CLI、登入帳號或呼叫 Jev API。

- 已以本機 Python 3.13 執行第 9 章完整程式，核對英文 50、Python 80、數學 40、總和 170。
- 已測試重跑不覆蓋、來源保留、UTF-8 BOM，以及負數、非數字、缺欄位、只有表頭、空科目、無效日期、缺儲存格與多儲存格等 8 種異常資料。
- 已以本機 uv 0.9.4 離線測試初始化、Python 版本指定、環境同步與專案直譯器；此版本是測試環境紀錄，不是建議下載的最新版。
- 已由 PowerShell 解析器檢查 33 段範例語法，未實際執行 Windows 安裝程式或修改 Windows 設定。
- 已擷取原始 SVG 並轉成影像檢視；本地版本補白色底。Mermaid 圖已檢查結構，實際顯示依閱讀器支援而定。
- CLI 安裝與依賴根據查核當日官方文件編寫；未在乾淨 Windows、無 Node.js 環境逐一重裝，也未代替學習者完成各家付費或組織帳號登入。
- b02：2026-10-29 重新讀取 Claude Code Setup、Codex CLI 入門與 GitHub README、Codex Windows 部署、Antigravity CLI 入門與遷移頁、Gemini CLI 安裝頁；以 `npm view` 查得 `@anthropic-ai/claude-code` 2.1.312（`node >= 22`，入口 `claude.exe`）、`@openai/codex` 0.165.0（`node >= 16`，入口 `codex.js`）、`@google/gemini-cli` 0.66.0（`node >= 20`，入口 `gemini.js`）；以 `brew info` 確認 `claude-code`、`codex`、`antigravity-cli` cask 存在，`gemini-cli` formula 標示 2026-12-18 停用；已讀取 Antigravity 與 Codex 的 macOS 安裝腳本內容確認安裝位置與更新行為。
- b02：3.2 的實作語言判讀，以 `strings` 檢查本機 macOS 執行檔：Codex 0.165.0 含 `rustc` 編譯資訊，Claude Code 2.1.312 含 `Bun v1.4.4` runtime 標記；Antigravity CLI 未安裝、未檢查，只依官方「native build」描述。
- b03：Codex 四個安裝分頁的指令，取自 Codex CLI 官方頁的安裝元件原始碼（`CliInstallMethodSelector`），因為分頁內容由網頁前端動態顯示，一般擷取只看得到 macOS/Linux 分頁；`brew info --cask codex`、`brew info --cask claude-code` 確認 cask 安裝內容為原生執行檔（Binary）。
- b02：第 5.8 節判讀範例取自教師 macOS 筆電實際盤點結果；未在 Windows 上執行盤點指令，PowerShell 區塊只做語法撰寫。
- 未執行 Jev 外部 API 檢查；該選用檢查需另取得同意。

## Jev 合規檢查紀錄（原稿歷史紀錄）

- **2026-10-29 20:14:13** ｜ 版本 `b02` ｜ Jev 模型 `jev-latest` ｜ ✅ PASS
  - 缺少模組：無
  - 缺少延伸問題子項：無
  - 過於理論：否
  - 分段檢查：全文超過 32,000 字，依章節分 2 段送出後合併

- **2026-10-29 20:22:19** ｜ 版本 `b05` ｜ Jev 模型 `jev-latest` ｜ ✅ PASS
  - 缺少模組：無
  - 缺少延伸問題子項：無
  - 過於理論：否
  - 分段檢查：全文超過 32,000 字，依章節分 2 段送出後合併

## Jev 圖表選型檢查紀錄（原稿歷史紀錄）

- **2026-10-29 20:14:20** ｜ 版本 `b02` ｜ Jev 模型 `jev-latest` ｜ ✅ PASS
  - 格式不符建議：無
  - CJK/ASCII 排版疑慮：無
  - 需人工確認（信心 < 0.70）：無
  - 分段檢查：區塊較多，依章節分 2 段送出後合併

- **2026-10-29 20:22:20** ｜ 版本 `b05` ｜ Jev 模型 `jev-latest` ｜ ✅ PASS
  - 格式不符建議：無
  - CJK/ASCII 排版疑慮：無
  - 需人工確認（信心 < 0.70）：無
  - 分段檢查：區塊較多，依章節分 2 段送出後合併
