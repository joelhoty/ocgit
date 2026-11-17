# 前導章版本與歷史驗證紀錄

本檔保存前導章的維護紀錄，不是學習內容。內文的節號指向當時版本；紀錄描述當時的狀態，不代表目前教材或讀者電腦已重新驗證。

## 教師電腦的歷史盤點

以下是原稿查核日 2026-10-29 的教師筆電，保留為判讀案例，不代表讀者電腦或本次重新盤點。2026-11-17 的 agy 補充盤點列在本節最後。

| 工具 | 盤點結果 | 判讀與建議 |
|---|---|---|
| Claude Code 2.1.312 | 原生版，Mach-O arm64 | 符合官方推薦；不需處理 |
| Codex 0.165.0 | standalone 版，Mach-O arm64 | 歷史盤點的 standalone 安裝；依官方方式重跑安裝或使用支援的 `codex update` |
| Antigravity CLI | 未安裝 | 若要示範 Google 路線，用官方腳本安裝 |
| Gemini CLI 0.42.0 | npm 全域安裝，nvm 的 Node 22.20.0 與 `/usr/local` 的 Node 22.14.0 各有一份 | 已被 `agy` 取代且重複安裝；依 5.5 遷移到 `agy` 後移除兩份 |
| Node.js | nvm 22.20.0、`/usr/local` 官方安裝包 22.14.0、Homebrew `node` 24.x（未連結） | 三個來源並存，容易讓 `npm -g` 裝到非預期位置；保留一個管理方式即可 |

同名指令出現多個版本時，先確認目前使用哪一份，再處理舊安裝，避免誤刪正在使用的版本。

### 2026-11-17 agy 補充盤點

同一台教師 macOS 筆電，為 agy 主線化重新盤點 Google 路線的工具。

| 工具 | 盤點結果 | 判讀與建議 |
|---|---|---|
| Antigravity CLI 1.5.10 | 原生版 `~/.local/bin/agy`，Mach-O 64-bit arm64，約 225 MB；`strings` 可見 Go runtime 標記（`go1.x`） | 符合官方原生安裝，背景自動更新；不需 Node.js |
| Antigravity CLI Homebrew cask | `brew info --cask antigravity-cli` 顯示 1.5.9，未安裝；需 macOS 12+；cask 會停用 `agy` 自動更新 | 已有原生版，不要再裝 cask |
| Gemini CLI | `type -a gemini` 只找到 nvm Node 22.20.0 底下的一份；2026-10-29 盤點時 `/usr/local` 底下的另一份已不在 PATH | 依前導章附錄 B.3 確認 `agy` 可用後移除 |

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
| agy 主線化 | 2026-11-17 | Antigravity CLI 由附錄選讀改為主線路線 C：2.4 新增三款 CLI 對照與 agy 介紹；2.5 補 agy 系統條件；新增 3.4 agy 安裝登入（原 3.4、3.5 順延為 3.5、3.6）；5.2 補 agy 規則載入（本機 agy 1.5.10 實測）；7.1 斜線指令表加 agy 欄；修正 Homebrew cask 會停用 agy 自動更新（`brew info --cask antigravity-cli` 1.5.9）；新增延伸章 agy_cli.md。編修：Claude Opus 5.5（claude-opus-5-5），Claude Code |
| agy 主線化（補齊） | 2026-11-17 | 2.1 工作台表加入 `agy`；2.3 擴充功能說明含 Antigravity；5.1 說明 Codex 與 `agy` 直接載入 AGENTS.md；排錯索引新增 5 列 agy 症狀；附錄 A.1 登入與診斷表加 agy 欄；A.2 盤點指令加 `agy`；A.4 Homebrew 加 `antigravity-cli`；A.5／A.6 補 agy；A.10 實作語言補本機 Go runtime 判讀；本檔新增 agy 補充盤點與驗證紀錄。編修：Claude Opus 5.5（claude-opus-5-5），Claude Code |
| Agent 會話操作化 | 2026-11-17 | 全課程複審：安裝之後的操作改以 Agent 會話的自然語言與內建指令示範。0.3 改為「一個終端機＋四種輸入（自然語言、`/`、`@`、`!`）」；2.1 移除另開 shell 終端機；2.7 不再要求安裝 PowerShell 7、版本檢查改看 VS Code 介面；2.9 改為看懂工作資料夾與 Agent 會執行的指令；2.10 以 VS Code 開啟資料夾對話框建立專案；4.1 由 Agent 建立 inputs／outputs／scripts、README、.gitignore；4.2、4.4、5.3、5.5、8.1、10.11 的 Git 操作改為自然語言提示並搭配 `/diff`、`!`；7.1 新增 `/diff`、`!`、`@`、`/rewind`、`/review`、`/init` 三款對照；10.2–10.13 的 uv 操作交給 Agent；附錄 A.2、A.3、B.3 改為提示。同步調整 04a、05、06a、07 與 index.html。依據：Codex developer commands、Claude Code interactive mode／checkpointing、Antigravity CLI reference（2026-11-17）。編修：Claude Opus 5.5（claude-opus-5-5），Claude Code |

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

## agy 主線化驗證紀錄（2026-11-17）

> **紀錄時間**：2026-11-17 22:09（UTC+8）
> **使用模型**：Claude Opus 5.5（模型代號 `claude-opus-5-5`）
> **執行 Agent**：Claude Code

- 官方文件：讀取 Antigravity CLI 入門、登入驗證、CLI 指令參考、Modes、Permissions、Settings、Sandbox、Rules、Customization discovery、Skills、At-mentions、VS Code extension、Troubleshooting、Gemini CLI migration 共 14 頁（網址列於 agy_cli.md 附錄 B）。官方未記載 `/init`、`/compact`、`/memory`、`/ide`、移除指令。
- 本機指令：`agy --help`、`agy help install／mcp／plugin／models／agents`、`agy changelog`（1.5.5–1.5.9）。確認 1.5.7 起預設 Agent Mode 為 `auto`；1.5.9 修正 Windows PowerShell 下 `!` 指令列的引號處理。
- Homebrew：`brew info --cask antigravity-cli` 顯示 1.5.9、需 macOS 12+，並註明「automatic updates are disabled so that Homebrew manages them」。據此修正前導章原本「cask 會自行更新」的敘述。
- 規則載入實測：在 scratch 資料夾以 `agy -p "<問題>" --mode plan` 詢問，要求不讀檔。第一次只放 `AGENTS.md`，正確回答規則內容。第二次另加含 `trigger: always_on` 的 `.agents/rules/output.md`，以及由 `AGENTS.md` 以 `@[寫作風格](docs/style.md)` 引用的檔案，三份規則都正確回答。其中一次因 `--print-timeout 120s` 逾時中斷，改用 260s 重跑成功。
- 執行檔判讀：`file` 顯示 Mach-O 64-bit arm64；`strings` 找到 `go1.x` 標記，判讀為 Go 編譯的原生程式。官方未公開實作語言，此為本機推斷。
- 輸出驗證：以 `render_intro.py` 重新產生 00_intro.html，`check_intro.py` 結果為 PASS，216 個舊錨點全部保留。agy_cli.html 以同一頁面外框產生，檢查結果：無重複 id、無斷裂的頁內連結。
- 未做事項：未在 Windows 實機安裝或執行 `agy`，PowerShell／CMD 指令依官方文件撰寫；未測試企業帳號、API 金鑰與 ADC 登入；未執行 Jev 外部 API 檢查。

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
