# 延伸章：Antigravity CLI（agy）安裝、啟動與 AGENTS.md 實作 {#agy-cli}

**VS Code ＋ Antigravity CLI（agy）專題工作流程教材**

> 對象：已讀過[前導章](00_intro.html)第 1–3 章，知道「終端機 Agent」與「工作資料夾」的意思；不需要程式背景。
> 工作方式：用 VS Code 管理專題資料夾，在整合終端機啟動 `agy`，所有檔案與 Git 操作都交給 `agy` 完成。
> 建議時數：3 節課，每節 50 分鐘（安裝登入 1 節、啟動與會話操作 1 節、AGENTS.md 1 節）。
> 查核依據：Antigravity 官方文件（查核日期 2026-11-17）、本機 `agy` 1.5.10 的 `--help` 與 `agy changelog`、本機實測。來源列表見[附錄 B](#agy-sources)。

## 0. 學習路線與閱讀約定 {#agy-route}

### 0.1 為什麼要單獨學 agy {#why-agy}

前導章以 Codex CLI／Claude Code 為主線，把 Antigravity 放在附錄選讀。若你的學校或個人帳號是 Google 方案（Google 帳號、Gemini 付費方案、Google Cloud 專案），`agy` 是 Google 目前提供給個人使用的終端機 Agent；原本的 Gemini CLI（`gemini`）個人方案服務已轉移到 `agy`。

本章用一個「專題資料夾」貫穿全部操作：建立資料夾、啟動 `agy`、讓 `agy` 建立專題結構，最後為專題設計一份 `AGENTS.md`，讓之後每次啟動都依同一套規則工作。

### 0.2 完成後能做到什麼 {#agy-outcomes}

1. 在 Windows 或 macOS 安裝 `agy`，完成登入，並用 `agy` 自己的指令確認版本、模型與用量。
2. 分辨「在獨立終端機啟動」與「在 VS Code 以專題資料夾啟動」，並說明工作區（workspace）由啟動位置決定。
3. 在 `agy` 會話內使用斜線指令、`@` 檔案提及、`!` 指令列與模式切換，看懂權限提示。
4. 用 `agy` 訪談、規劃、產生並驗證專案的 `AGENTS.md`，必要時拆成 `.agents/rules/` 規則檔。
5. 分析一份實際使用中的 `AGENTS.md`，找出可沿用的設計與需要修正的地方。

### 0.3 課程安排與交付物 {#agy-plan}

| 節次 | 主題與對應章節 | 學習者交付物 |
|---|---|---|
| 1 | 安裝與登入（1） | `agy --version` 結果、登入成功畫面、`/usage` 截圖 |
| 2 | 啟動方式與會話操作（2–3） | 專題資料夾結構、README、第一個 Git 檢查點 |
| 3 | AGENTS.md 設計與驗證（4–5） | 專題 `AGENTS.md`、規則生效驗證紀錄、練習答案 |

### 0.4 指令閱讀約定：一律以 agy 操作 {#agy-conventions}

本章的原則是**所有操作都以 `agy` 的指令示範**，不直接在終端機打 `mkdir`、`git` 等指令。操作分成四種輸入，區塊標籤如下：

| 區塊標籤 | 在哪裡輸入 | 內容 | 範例 |
|---|---|---|---|
| `shell` | 終端機提示字元（PowerShell 或 zsh） | 只有 `agy` 開頭的啟動指令與子指令 | `agy --version` |
| `text`（標示「會話內」） | 已啟動的 `agy` 輸入區 | 斜線指令、`@` 提及、`!` 指令列 | `/model` |
| `transcript` | 已啟動的 `agy` 輸入區 | 用自然語言交代的任務 | 「請建立 outputs 資料夾……」 |
| `markdown` | VS Code 編輯器 | 檔案內容範例 | `AGENTS.md` 內容 |

只有兩個例外：

- **安裝**：安裝前電腦上還沒有 `agy`，只能用作業系統的 PowerShell、CMD 或 zsh 執行官方安裝指令（第 1 章）。
- **VS Code 與檔案總管的圖形介面**：開啟資料夾、開新終端機等用滑鼠操作。

其他動作，例如建立資料夾、寫 README、看 Git 狀態、提交檔案，都在 `agy` 會話內用自然語言交代，由 `agy` 提出指令、你核准後執行。這樣每一步都會經過 `agy` 的權限提示，你可以看到 Agent 實際做了什麼。

> 每次只輸入一小段，確認結果後再往下做。斜線指令與功能會隨版本更新；畫面與本章不同時，先在會話內輸入 `/help` 查看目前版本的說明。

## 1. 安裝與登入 {#agy-install}

**本章目的：**在自己的電腦裝好 `agy`，登入帳號，並用 `agy` 的指令確認「程式能執行」「帳號能用」「模型能選」。

### 1.1 安裝前確認 {#agy-prerequisites}

| 項目 | 條件 |
|---|---|
| 作業系統 | 官方安裝腳本支援 64 位元 Windows、macOS、Linux；Homebrew cask 標示 macOS 12 以上 |
| Node.js | **不需要**。`agy` 是原生執行檔，不經 npm 安裝 |
| 帳號 | 個人 Google 帳號（免費、Pro、Ultra）、Google Cloud／Gemini Enterprise 專案，或 Gemini API 金鑰擇一 |
| 權限 | 原生安裝放在使用者目錄，不需要系統管理員權限 |
| 學校電腦 | 若資訊組限制執行下載的腳本，依學校核准方式安裝，不要自行繞過 |

同一台電腦只保留**一種**安裝來源（原生腳本或 Homebrew 擇一），避免兩個 `agy` 互相搶 PATH。

### 1.2 Windows 安裝 {#agy-install-windows}

在 VS Code 開一個整合終端機（PowerShell），執行官方安裝指令：

```powershell
irm https://antigravity.google/cli/install.ps1 | iex
```

`irm` 下載安裝腳本，`iex` 執行它。若你使用的是「命令提示字元」（CMD），改用：

```batch
curl -fsSL https://antigravity.google/cli/install.cmd -o install.cmd && install.cmd && del install.cmd
```

預設安裝位置是 `C:\Users\<使用者名稱>\AppData\Local\agy\bin`。安裝完成後**完全關閉並重新開啟 VS Code**，讓終端機讀到新的 PATH。

### 1.3 macOS 安裝 {#agy-install-macos}

**原生安裝（本章主線）：**在 VS Code 整合終端機（zsh）執行：

```bash
curl -fsSL https://antigravity.google/cli/install.sh | bash
```

執行檔會放在 `~/.local/bin/agy`。完成後完全關閉並重新開啟 VS Code。

**Homebrew（替代方式）：**已經用 Homebrew 管理軟體的人可以改用：

```bash
brew install --cask antigravity-cli
```

注意 Homebrew 版會**關閉 `agy` 的自動更新**，改由 Homebrew 管理；更新時用 `brew upgrade --cask antigravity-cli`，不要用 `agy update`。

### 1.4 用 agy 指令驗證安裝 {#agy-verify}

從這一節開始，只輸入 `agy` 開頭的指令。重開 VS Code 後，在整合終端機執行：

```shell
agy --version
agy changelog
```

**成功判準：**第一行顯示版本號（本章查核時為 `1.5.10`）；第二行顯示各版更新說明，按 `q` 或捲到底即可離開。

若出現 `agy: command not found`（Windows 為「無法辨識 agy」），表示終端機找不到執行檔，依序檢查：

1. 是否已完全關閉 VS Code 再重開（只關終端機分頁不夠）。
2. 用完整路徑執行 `agy` 內建的 PATH 設定子指令，讓它把安裝目錄加回 shell 設定：

```bash
~/.local/bin/agy install
```

```powershell
& "$env:LOCALAPPDATA\agy\bin\agy.exe" install
```

`agy install` 會設定 PATH 並清理舊的 `agy`／`antigravity` 別名；執行後再重開 VS Code。

### 1.5 第一次啟動與登入 {#agy-first-run}

先決定專題資料夾的位置，第 2 章會正式建立；第一次啟動**不要**在使用者主目錄（`C:\Users\<名稱>` 或 `~`）啟動，因為 `agy` 會詢問是否信任目前資料夾，信任整個主目錄等於讓 Agent 能讀取你所有個人檔案。

建議先用 VS Code「檔案 → 開啟資料夾」，在對話框中按「新增資料夾」，建立 `文件/AI-Lab/agy-project`（Windows 可放在 `C:\Users\<名稱>\AI-Lab\agy-project`），開啟後從「終端機 → 新增終端機」開一個終端機，再執行：

```shell
agy
```

第一次啟動會依序出現：

| 步驟 | 畫面內容 | 建議選擇 |
|---|---|---|
| 1. 配色 | Dark、Solarized Dark、Solarized Light、終端機預設 | 選看得清楚的即可，之後可在 `/config` 修改 |
| 2. 顯示模式 | Alt-Screen（全螢幕）或 Inline（接在終端機輸出後面） | 初學者選 Inline，捲動與複製較直覺 |
| 3. 工作區信任 | 確認是否信任目前資料夾，信任後才開始建立檔案索引 | 確認路徑是 `agy-project` 才信任 |
| 4. 登入 | 自動開啟瀏覽器進行 Google 登入 | 依帳號類型選擇，見下表 |

| 帳號類型 | 登入方式 |
|---|---|
| 個人 Google 帳號（免費、Pro、Ultra） | 瀏覽器中選 Google 帳號完成 OAuth 登入 |
| 學校或公司的 Gemini Enterprise／Google Cloud | 選「Use a Google Cloud project」，再依管理員指示選 Continue with Google Cloud 或 SSO 設定 |
| Gemini API 金鑰 | 由教師或管理員設定，需在 `agy` 設定檔指定 `modelProvider` 並提供 `GEMINI_API_KEY` 環境變數；只設環境變數不會生效 |

登入憑證存在作業系統的鑰匙圈（macOS 鑰匙圈、Windows 認證管理員），不會寫進專題資料夾。用 SSH 連到遠端電腦時，`agy` 會改為顯示一個網址，貼到本機瀏覽器登入後再把代碼貼回終端機。

### 1.6 登入後用會話指令確認帳號 {#agy-check-account}

進入 `agy` 後，在輸入區依序輸入：

```text
/model
/usage
/credits
```

| 指令 | 確認什麼 |
|---|---|
| `/model` | 帳號能用哪些模型；選定後會記住，下次啟動沿用 |
| `/usage`（別名 `/quota`） | 目前模型額度用了多少 |
| `/credits` | AI 點數與購買連結；免費帳號可確認是否有額度限制 |

也可以不進會話，直接在終端機列出可用模型：

```shell
agy models
```

**成功判準：**`/model` 能列出模型，`/usage` 能顯示額度。只看到版本號不代表能工作；能列出模型才代表登入與帳號權限都正常。

### 1.7 更新、切換帳號與移除 {#agy-maintenance}

| 想做什麼 | agy 的做法 | 說明 |
|---|---|---|
| 更新 | 自動；需要時執行 `agy update` | 原生版在背景每 15 分鐘內檢查一次更新；Homebrew 版改用 `brew upgrade --cask antigravity-cli` |
| 看更新內容 | `agy changelog` 或會話內 `/changelog` | 遇到行為改變時先查這裡 |
| 換帳號 | 會話內 `/logout`，結束後重新執行 `agy` 登入 | `/logout` 會清除鑰匙圈中保存的登入資料；使用 API 金鑰時無效 |
| 從舊 Gemini CLI 遷移 | `agy plugin import gemini` | 第一次啟動偵測到舊設定時也會出現遷移清單；詳見[前導章附錄 B.3](00_intro.html#gemini-migration) |
| 移除 | 刪除 `agy` 執行檔 | 官方文件未提供移除指令；位置見 1.2、1.3 |

## 2. 啟動 agy：工作區由啟動位置決定 {#agy-launch}

**本章目的：**理解「在哪裡啟動，`agy` 就在哪裡工作」，並練習兩種啟動方式。

### 2.1 工作區是什麼 {#agy-workspace}

`agy` 的工作區（workspace）是**你執行 `agy` 時所在的資料夾**，加上用 `--add-dir` 或 `/add-dir` 額外加入的資料夾。Agent 預設只讀寫工作區內的檔案，專案規則（`AGENTS.md`）也從這個資料夾往上找。

```text
啟動位置錯了 → 讀不到你的資料、寫到錯的地方、載入不到你的 AGENTS.md
啟動位置對了 → 只看得到這個專題，規則自動生效
```

所以每次啟動前先確認：**終端機目前的位置就是專題資料夾**。

### 2.2 方式 A：在獨立終端機啟動 {#agy-launch-terminal}

不開 VS Code、只想快速問問題或處理單一資料夾時使用。重點是「讓終端機直接開在專題資料夾」，不必手打切換目錄的指令：

| 平台 | 操作 |
|---|---|
| Windows 11 | 在檔案總管對 `agy-project` 資料夾按右鍵 → 「在終端機中開啟」 |
| macOS | 把 Finder 中的 `agy-project` 資料夾拖到 Dock 上的「終端機」圖示；或在「系統設定 → 鍵盤 → 鍵盤快速鍵 → 服務」啟用「新增位於檔案夾位置的終端機視窗」，之後在資料夾按右鍵 → 服務 |

終端機開好後執行：

```shell
agy
```

進入會話後先請 `agy` 回報位置，確認啟動在正確資料夾：

```transcript
請只回報目前的工作區路徑與裡面的檔案清單，不要建立或修改任何檔案。
```

### 2.3 方式 B：在 VS Code 以專題資料夾啟動（本章主線） {#agy-launch-vscode}

做專題時用這個方式：左邊看檔案、中間看內容、下方讓 `agy` 工作。

1. VS Code 選「檔案 → 開啟資料夾」，選 `agy-project`。視窗標題列與檔案總管最上方會顯示 `AGY-PROJECT`。
2. 若跳出「是否信任此資料夾的作者」，確認是自己的資料夾後選信任。
3. 選「終端機 → 新增終端機」（Windows／macOS 皆可用 <kbd>Ctrl</kbd>+<kbd>`</kbd>）。VS Code 會把新終端機開在**目前開啟的資料夾**，這就是能用專題資料夾啟動的原因。
4. 在終端機執行：

```shell
agy
```

5. 建議再按終端機面板右上角的「分割」按鈕，開第二個終端機。左邊留給 `agy` 會話，右邊留著備用（例如再開一個 `agy -p` 單次查詢）。

```text
┌──────────────┬────────────────────────────┐
│ 檔案總管      │ 編輯器：README.md / AGENTS.md │
│ agy-project  │                            │
│  ├ inputs    ├──────────────┬─────────────┤
│  ├ outputs   │ 終端機 1：agy │ 終端機 2：備用 │
│  └ AGENTS.md │ 會話          │              │
└──────────────┴──────────────┴─────────────┘
```

> **VS Code 擴充功能是另一個介面。** Marketplace 上的「Antigravity for Visual Studio Code」（`Google.google-antigravity`，需 VS Code 1.90 以上）提供編輯器內的聊天面板，與本章在終端機使用的 `agy` CLI 是不同介面。本章不需要安裝它；若已安裝，兩者的專案規則（`AGENTS.md`）可共用。

### 2.4 讓 agy 建立專題骨架 {#agy-scaffold}

在 VS Code 中啟動的 `agy` 會話輸入：

```transcript
這是一個新的專題資料夾。請幫我建立以下結構，每一步先說明要做什麼：
1. 建立 inputs、outputs、docs 三個資料夾。
2. 建立 README.md，包含：專題名稱（先寫「待定專題」）、目的、資料位置、操作方式四個段落。
3. 建立 .gitignore，排除作業系統暫存檔（.DS_Store、Thumbs.db）與 .env。
4. 初始化 Git，並把以上檔案做第一次提交，訊息為「建立專題骨架」。
完成後列出實際建立的檔案，以及 git status 的結果。
```

這時 `agy` 會在建立檔案、執行 `git init`、`git commit` 前停下來請你核准（見 3.3）。每次核准前看清楚它要執行的指令與路徑。

**成功判準：**VS Code 左側出現 `inputs`、`outputs`、`docs`、`README.md`、`.gitignore`；`agy` 回報的 `git status` 顯示工作區乾淨（nothing to commit）。

### 2.5 常用啟動參數 {#agy-launch-flags}

以下都在終端機提示字元輸入，作用只限這一次啟動，不會改到設定檔：

| 指令 | 用途 | 使用時機 |
|---|---|---|
| `agy` | 開新會話 | 一般情況 |
| `agy -c` | 接續這個資料夾最近一次的會話 | 昨天沒做完，今天繼續 |
| `agy --mode plan` | 以規劃模式啟動，先產生計畫再動手 | 大改動之前 |
| `agy -i "請先讀 README.md 並摘要專題目標"` | 帶著第一句話啟動，之後繼續對話 | 固定的開場檢查 |
| `agy --add-dir ../共用資料` | 把另一個資料夾也加入工作區 | 專題需要讀取資料夾外的資料 |
| `agy --sandbox` | 讓終端機指令在沙箱內執行 | 讓 Agent 執行不熟悉的指令時 |
| `agy -p "列出 outputs 內的檔案"` | 單次執行，印出結果就結束 | 快速查詢、寫進腳本 |
| `agy --model "<模型名稱>"` | 這次啟動改用指定模型 | 名稱以 `agy models` 列出的為準 |

## 3. 在 agy 會話內工作 {#agy-session}

**本章目的：**熟悉 `agy` 輸入區的四種輸入，並學會在核准前判斷、在完成後檢查。

### 3.1 輸入區的四種輸入 {#agy-input-types}

| 開頭 | 意義 | 範例 |
|---|---|---|
| 一般文字 | 交代任務，`agy` 會規劃並使用工具完成 | 「請把 inputs/notes.md 摘要成三點」 |
| `/` | 斜線指令，操作 `agy` 本身（模型、會話、權限……） | `/model` |
| `@` | 提及檔案或資料夾路徑，支援模糊比對 | `@notes`（會找到 `inputs/notes.md`） |
| `!` | 讓 `agy` 直接執行一行指令並顯示結果 | `! git status` |

`@` 只是把**路徑**交給 Agent，不會自動貼上內容，也不會額外給它讀取權限。`!` 適合快速看一眼狀態；要修改檔案或提交時，仍建議用自然語言交代，讓 `agy` 說明每一步。

### 3.2 常用斜線指令速查 {#agy-slash-commands}

在輸入區打 `/` 會出現選單，可用方向鍵選擇；按 <kbd>Tab</kbd> 補完反白的選項。

| 想做什麼 | 指令 | 說明 |
|---|---|---|
| 看所有指令與快捷鍵 | `/help` | 忘記指令名稱時先用這個 |
| 選模型 | `/model` | 選定後跨會話保存 |
| 調整推理強度 | `/effort` | `low` 到 `max`；越高越慢、越耗額度 |
| 看額度 | `/usage` | 每完成一個階段看一次 |
| 看 context 使用量 | `/context` | 對話或讀入檔案變多時檢查 |
| 開新對話 | `/clear`（別名 `/new`） | 換主題時使用，避免沿用不相關內容 |
| 接續舊對話 | `/resume` | 從清單選擇；也可接 ID 前綴 |
| 回到之前的對話點 | `/rewind`（別名 `/undo`） | 回復對話歷史；檔案是否回復依畫面選項確認 |
| 看這輪改了什麼 | `/diff` | 互動式差異檢視 |
| 先規劃再執行 | `/plan <任務>` | 產生實作計畫，確認後再動手 |
| 讓 agy 先訪問你 | `/grill-me <任務>` | 開始前由 Agent 提問，釐清需求（第 4 章使用） |
| 把修正記成規則 | `/learn <說明>` | 把你的糾正寫入規則檔或技能 |
| 管理權限 | `/permissions` | 查看、修改允許／詢問／拒絕規則 |
| 修改設定 | `/config`（別名 `/settings`） | 配色、顯示模式、預設 Agent 模式等 |
| 加入資料夾 | `/add-dir <路徑>` | 會話中途擴大工作區 |
| 用編輯器開檔 | `/open <路徑>` | 用系統預設編輯器開啟 |
| 看技能 | `/skills` | 列出已載入的技能；修改後用 `/skills reload` |
| 問 agy 本身的用法 | `/antigravity-guide <問題>` | 依官方文件回答 |
| 登出 | `/logout` | 換帳號時使用 |
| 結束 | `/exit`（別名 `/quit`） | 也可在輸入區為空時按 <kbd>Ctrl</kbd>+<kbd>D</kbd> |

前導章介紹的 `/compact`、`/memory`、`/init`、`/ide` 是其他 CLI 的指令，`agy` 目前**沒有**這些指令。不要把別款工具的指令名稱直接套用到 `agy`。

### 3.3 權限提示與 Agent 模式 {#agy-permissions}

`agy` 要寫檔或執行指令時會停下來詢問：

| 提示 | 選項 | 判斷方式 |
|---|---|---|
| `Accept this file edit?`／`Allow creation of this file?` | `1` 接受、`2` 拒絕、`f` 看完整差異 | 路徑是你交代的位置才接受；不確定就按 `f` |
| `Do you want to proceed?`（執行指令） | Yes／Yes, and always allow…／No | 看不懂指令就選 No，請它先解釋 |

拒絕不會弄壞任務，`agy` 會收到拒絕結果，你可以補充限制後再讓它繼續。

按 <kbd>Shift</kbd>+<kbd>Tab</kbd> 可以在四種模式間切換，畫面下方會顯示目前模式：

| 模式 | 寫檔 | 執行指令 | 適合誰 |
|---|---|---|---|
| `default` | 先讓你看差異 | 先詢問 | **初學者建議使用** |
| `accept-edits` | 自動接受工作區內的修改 | 先詢問 | 已熟悉任務，只想審核指令 |
| `auto` | 自動 | 在沙箱內自動執行，離開沙箱前由審查機制判斷 | 個人帳號且系統支援沙箱時才出現 |
| `plan` | 不直接修改，先產生計畫 | 不直接執行 | 大改動、還在想做法時 |

自 1.5.7 版起，沒有保存模式的會話預設為 `auto`（在支援的帳號與系統上）。本課希望你看到每一步，所以先進入 `/config`，把 `Agent Mode` 改為 `Default`。請勿在課堂中使用 `--dangerously-skip-permissions`，它會自動核准所有工具請求。

### 3.4 第一次有來源的小任務 {#agy-first-task}

在 VS Code 中把一份課堂筆記存成 `inputs/notes.md`（內容可沿用[前導章 4.1](00_intro.html#source-notes) 的範例），然後在 `agy` 輸入：

```transcript
請讀取 @inputs/notes.md，整理成三個重點，每點標示來源段落（例如 P1）。
結果寫入 outputs/summary_b01.md，不要修改 inputs 內的檔案。
完成後告訴我：產出的檔案、你實際讀了哪些檔案、還有哪些內容來源沒有提供。
```

完成後檢查：

```text
/diff
! git status --short
```

**成功判準：**`/diff` 只顯示 `outputs/summary_b01.md` 的新增；`git status` 中 `inputs/notes.md` 若是新加入的檔案顯示為未追蹤（`??`），而不是被修改（`M`）。

確認無誤後，請 `agy` 建立檢查點：

```transcript
請把 inputs/notes.md 與 outputs/summary_b01.md 加入 Git 並提交，訊息為「新增第一份摘要」。
提交後顯示最近一筆紀錄。
```

### 3.5 會話管理：接續、換題與單次執行 {#agy-session-control}

1. **今天做完，明天接著做：**在同一個專題資料夾執行 `agy -c`，或啟動後輸入 `/resume` 選擇會話。接續後先請 `agy` 讀 README 與最近的提交紀錄，再確認下一步。
2. **換一個不相關的任務：**先確認成果已提交，再輸入 `/clear` 開新對話。
3. **對話很長：**輸入 `/context` 看使用量。`agy` 沒有 `/compact`，比較穩定的做法是請它把已確認的決策與待辦寫進 `docs/progress.md`，提交後再 `/clear`，新對話開頭請它先讀 `docs/progress.md`。
4. **只想問一件事：**在備用終端機使用單次執行，結果印出就結束，不進入互動畫面：

```shell
agy -p "依 README.md，用一句話說明這個專題的目的。不要修改任何檔案。" --mode plan
```

`--mode plan` 讓這次執行只規劃、不修改檔案，適合查詢類問題。單次執行預設會等到回答完成；回答很長時可加 `--print-timeout 300s` 設定上限。

## 4. 用 agy 設計並生成 AGENTS.md {#agy-agents-md}

**本章目的：**把每次都要重複交代的要求寫成專案規則，並用 `agy` 自己來訪談、起草、驗證這份規則。

### 4.1 為什麼需要 AGENTS.md {#agy-why-rules}

第 3 章每次都要說「標示來源」「不要改 inputs」「用 _b01 版本號」。這些要求寫進 `AGENTS.md` 後，`agy` 每次啟動都會自動帶入，不必重講，換成其他支援 `AGENTS.md` 的 CLI（如 Codex CLI）也能沿用。

`AGENTS.md` 是**文字規則**：它影響 Agent 的判斷，但不是安全機制。真正禁止某些操作要靠 3.3 的權限設定（`/permissions`）與沙箱。

### 4.2 agy 會載入哪些規則檔 {#agy-rule-loading}

`agy` 從**啟動資料夾往上找到 Git 儲存庫根目錄**，每一層都會檢查下列檔案；全域檔案則對所有專案生效：

| 範圍 | 檔案位置 | 是否需要前置設定（frontmatter） |
|---|---|---|
| 專案（每一層資料夾） | `AGENTS.md` 或 `GEMINI.md` | 不需要，永遠生效 |
| 專案（每一層資料夾） | `.agents/AGENTS.md` 或 `.agents/GEMINI.md` | 不需要，永遠生效 |
| 專案（每一層資料夾） | `.agents/rules/*.md` | **需要** `trigger` 欄位，否則會被忽略 |
| 全域 | `~/.gemini/AGENTS.md`、`~/.gemini/GEMINI.md`、`~/.gemini/config/rules/*.md` 等 | 同上 |

幾個要注意的規則：

- **累加，不是取代**：找到的規則全部合併使用，沒有「近的蓋掉遠的」。同一件事不要在兩個檔案寫出互相矛盾的規定。
- **只往上，不往下**：子資料夾裡的 `AGENTS.md` 不會因為你在上層啟動而載入。
- **大小限制**：單一規則檔上限 24,000 bytes；全域與 `always_on` 規則合計約 20,000 tokens，超過的部分會被改成只留指標。規則要精簡。
- **`AGENTS.md` 與 `GEMINI.md` 擇一**：兩者都會載入。新專題建議統一用 `AGENTS.md`，方便與其他 CLI 共用。
- **引用其他檔案**：在規則中寫 `@[說明文字](路徑)` 會把該檔內容一起帶入；只寫 `@檔名` 則只是提到路徑。
- `.agents/rules/*.md` 的 `trigger` 可為 `always_on`（永遠生效）、`model_decision`（由模型判斷何時套用）、`glob`（依檔案路徑套用）；CLI 不支援 `manual`。

> **本機實測（agy 1.5.10，2026-11-17）：**在測試資料夾放入 `AGENTS.md`、含 `trigger: always_on` 的 `.agents/rules/output.md`，以及由 `AGENTS.md` 用 `@[寫作風格](docs/style.md)` 引用的檔案，三份檔案中的規則在 `agy -p` 不讀檔的情況下都能正確回答，表示啟動時已自動載入。

### 4.3 好規則的五個條件 {#agy-rule-design}

| 條件 | 不好的寫法 | 可操作的寫法 |
|---|---|---|
| 可檢查 | 「內容要詳細」 | 「每個重點標示來源段落（P1、P2…）；來源沒有的內容列入『待查』」 |
| 有位置 | 「好好管理檔案」 | 「inputs 是來源，不修改；成果寫入 outputs，檔名加 _b01、_b02」 |
| 有順序 | 「記得驗收」 | 「完成時依序回報：產出檔案、檢查方式、實際結果、未確認事項」 |
| 有邊界 | 「注意安全」 | 「刪除檔案、對外發送、安裝套件前先取得我的同意」 |
| 不重複工具本身的設定 | 寫「不准執行 rm」 | 用 `/permissions` 設定拒絕規則；`AGENTS.md` 只說明原因 |

### 4.4 生成流程：訪談 → 規劃 → 寫入 → 驗證 {#agy-generate-rules}

`agy` 沒有自動產生規則檔的 `/init` 指令。我們用它現有的指令完成同樣的事，而且更能貼合你的專題。

**步驟 1：讓 agy 訪問你。**在專題資料夾的 `agy` 會話輸入：

```text
/grill-me 為這個專題資料夾設計一份 AGENTS.md
```

`agy` 會先提問，例如專題主題、讀者是誰、資料放哪裡、輸出格式、哪些事情一定要先問你。逐題回答；不確定的就說「先列為待定」。

**步驟 2：先規劃，不寫入。**

```transcript
/plan 根據剛才的訪談，起草 AGENTS.md。
要求：
1. 先讀 README.md 與目前的資料夾結構，規則要和實際資料夾一致。
2. 分成：專題目標、資料夾與檔名、工作流程、寫作規範、驗收回報、需要先詢問的事項。
3. 每條規則都要能檢查；寫不出檢查方式的規則先列在「待定」。
4. 全文控制在 80 行以內，使用繁體中文。
先把草稿顯示給我，不要寫入檔案。
```

**步驟 3：修改後寫入。**對草稿提出修改意見，例如「把檔名規則改成 主題_日期_b01.md」。滿意後：

```transcript
請把確認後的草稿寫入專題根目錄的 AGENTS.md。
如果 AGENTS.md 已存在，先顯示差異讓我確認，不要直接覆蓋。
```

**步驟 4：重新啟動並驗證。**規則檔在啟動時載入，所以先輸入 `/exit` 結束會話，再於同一資料夾執行 `agy`，然後輸入：

```transcript
不要使用任何工具讀檔，只根據你啟動時已載入的規則回答：
1. 這次自動載入了哪些規則檔（列出路徑）？
2. 成果檔要放在哪裡、檔名規則是什麼？
3. 哪些事情你必須先問我？
```

把回答與 `AGENTS.md` 對照。要求「不使用工具讀檔」是為了確認規則是**啟動時自動載入**，而不是它臨時去讀檔。

**步驟 5：提交規則。**

```transcript
請把 AGENTS.md 加入 Git 並提交，訊息為「加入專題規則 AGENTS.md」。
```

### 4.5 範例一：專題用 AGENTS.md {#agy-example-project}

以下是一份「主題探究專題」的規則範例，可直接放在專題根目錄後依需求修改：

````markdown
# 專題工作規則

## 專題目標
- 本專題探究「＿＿＿」，產出可給同學閱讀的研究摘要與簡報大綱。
- 讀者是同班同學；使用繁體中文，專有名詞第一次出現附英文。

## 資料夾與檔名
- inputs/：來源資料（訪談、文章、筆記），只讀不改。
- outputs/：成果，檔名為「主題_YYYYMMDD_b01.md」，修改時遞增為 b02、b03，不覆蓋舊版。
- docs/progress.md：已確認的決策與待辦，每次工作結束前更新。

## 工作流程
1. 開始任務前，先說明你要讀哪些檔案、要產出什麼。
2. 超過三個檔案的修改，先用條列提出計畫，等我同意再做。
3. 執行失敗時保留錯誤訊息，先說明原因再修改。

## 寫作規範
- 每個論點標示來源，格式為（來源：inputs/檔名 段落）。
- 來源沒有提供的事實，不寫成結論，列在文末「待查」。
- 數字、日期、人名要和來源一致；無法確認時標註「待確認」。

## 驗收回報
完成時依序回報：
1. 產出或修改的檔案路徑。
2. 你做了哪些檢查（例如逐條核對來源）。
3. 實際結果與還沒確認的事項。

## 需要先詢問的事項
- 刪除或搬移任何檔案。
- 安裝套件、連網查詢、對外發送內容。
- 修改本檔（AGENTS.md）。
````

### 4.6 範例二：把規則拆成主檔與規則資料夾 {#agy-example-split}

規則變多時，把「每次都要遵守的」留在 `AGENTS.md`，把「特定情境才需要的」拆出去，讓主檔保持精簡：

```text
agy-project/
├── AGENTS.md                  ← 目標、資料夾、流程（每次都載入）
├── docs/
│   └── style.md               ← 寫作風格細節（由 AGENTS.md 引用）
└── .agents/
    └── rules/
        └── slides.md          ← 製作簡報時才需要的規則
```

`AGENTS.md` 中用引用語法帶入寫作風格：

```markdown
## 寫作規範
- 詳細寫作風格見 @[寫作風格](docs/style.md)
```

`.agents/rules/slides.md` 必須有 `trigger`，這裡用 `model_decision` 讓模型在處理簡報任務時套用：

```markdown
---
trigger: model_decision
description: 製作或修改簡報大綱時套用
---

# 簡報規則
- 每張投影片標題不超過 15 字，內容不超過 5 行。
- 每張投影片附講者備註，說明要講的重點。
- 圖表需註明資料來源。
```

> 若某條規則一定要每次生效，`trigger` 改為 `always_on`。拆檔後同樣依 4.4 步驟 4 重新啟動並驗證。

### 4.7 範例三：分析一份實際使用中的 AGENTS.md {#agy-example-onclass}

[onclassbyJoel 的 AGENTS.md](https://joelhoty.github.io/onclassbyJoel/AGENTS.md) 是一份實際用於課堂筆記工作區、讓多個 Agent 共用的規則（約 3,900 bytes，在 `agy` 的 24,000 bytes 單檔上限內）。以下摘錄其結構並分析：

| 段落 | 規定內容 | 值得沿用的設計 |
|---|---|---|
| 1. Metadata Header | 每份文件標題下方記錄「最後更新時間（UTC+8）」「使用模型」「執行 Agent」 | 讓讀者知道內容由哪個模型、何時產生，方便追查 |
| 2. 關鍵字自動擴充 | 遇到核心關鍵字，展開為核心概念、實作範例、延伸思考三層 | 把「寫詳細一點」變成可檢查的三層結構 |
| 3. Prompt Archive | 文件底部用「增補」方式記錄每次的提示詞原文與變更摘要；索引檔例外 | 保留產生過程，且明確寫出例外 |
| 4–5. 儲存格式與內容 | 同時存 md 與 html；html 加匯出 PDF 按鈕；程式碼要有註解與流程圖 | 輸出格式寫成可勾選的清單 |
| 6. 索引自動更新 | 索引由 `tools/build_index.py` 產生，不得手改；提交前後各執行一次 | 指定「用哪支腳本做」而不是「記得更新索引」 |
| 目錄分類 | `AI/`、`ec/`、`ev3/`、`math/`… 依主題歸檔，不放根目錄 | 用明確清單避免 Agent 自創資料夾 |

其中第 1 段的 Metadata 格式如下：

```markdown
> **最後更新時間**: YYYY-MM-DD HH:mm:ss (UTC+8)
> **使用模型**: [Model Name]
> **執行 Agent**: [Agent/Subagent Name]
```

**改寫給 agy 使用時，建議修正四處：**

1. **程式碼區塊沒有關閉。**原檔第 3 段的 Prompt Archive 範例以 ```` ```markdown ```` 開頭，結尾的 ```` ``` ```` 直到第 5 段後才出現，結果第 4、5 段在顯示時被當成程式碼內容。規則檔裡要放含程式碼區塊的範例時，外層改用四個反引號（````` ```` `````）或 `~~~`，並在 VS Code 預覽中確認段落標題有正常顯示。
2. **路徑寫死在特定電腦。**原檔寫明 `D:\CLASS_NOTE`。`agy` 的工作區就是啟動資料夾，規則中改寫為「本工作區」即可，同一份規則在 macOS 與其他電腦也適用。
3. **模型名稱要有來源。**要求記錄「使用模型」時，模型不一定能正確說出自己的名稱。可在規則補一句：「使用模型一欄填寫 `/model` 目前選定的名稱；無法確認時寫『未確認』」，或由使用者在提示中直接告訴它。
4. **累加內容會讓檔案變大。**Prompt Archive 會越來越長；`agy` 讀檔時會消耗 context。可規定每份文件只保留最近 N 筆，其餘移到 `docs/prompt_archive.md`。同理，用 `/learn` 增補規則時，注意不要超過單檔大小限制。

用 `agy` 實際套用這份範例：

```transcript
請參考 https://joelhoty.github.io/onclassbyJoel/AGENTS.md 的設計，
為本專題草擬 AGENTS.md，保留「Metadata Header」與「Prompt Archive」兩項規範，
並依下列要求調整：
1. 不寫死磁碟路徑，以本工作區為範圍。
2. 目錄分類改為本專題實際的 inputs、outputs、docs。
3. 檔案中的範例程式碼區塊外層用四個反引號，確保不會吃掉後面的段落。
4. 「使用模型」填寫 /model 目前選定的名稱，無法確認時寫「未確認」。
先顯示草稿與你的修改理由，不要寫入檔案。
```

這個任務需要連網讀取網頁，`agy` 會請你核准；確認網址正確再同意。

### 4.8 用 /learn 持續維護規則 {#agy-learn}

工作中發現 `agy` 反覆犯同一個錯，例如忘了加版本號，可以直接把糾正寫回規則：

```text
/learn 成果檔一律加 _bNN 版本號，不可覆蓋舊檔
```

`/learn` 會提議要寫入哪個規則檔或技能；接近大小上限時，它會建議精簡現有內容或拆成分範圍的規則。**寫入前先看它提議的位置與內容**，接受後一樣用 4.4 步驟 4 的方式驗證，再請 `agy` 提交。

### 4.9 AGENTS.md 驗收清單 {#agy-rules-checklist}

- [ ] 放在專題根目錄，且在專題根目錄啟動 `agy`。
- [ ] 每條規則都能說出檢查方式。
- [ ] 資料夾名稱、檔名規則和實際結構一致。
- [ ] 沒有和全域規則（`~/.gemini/AGENTS.md` 等）互相矛盾。
- [ ] 範例程式碼區塊有正確關閉，VS Code 預覽中段落標題正常。
- [ ] 重新啟動後，`agy` 能在不讀檔的情況下正確說出規則。
- [ ] 已提交到 Git，修改時看得到差異。

## 5. 練習、問答與總結 {#agy-practice}

### 5.1 練習 {#agy-exercises}

**練習 A：找出啟動位置錯誤。**同學在使用者主目錄執行 `agy`，再要求「整理 agy-project/inputs 的筆記」。請說明會發生什麼問題，以及正確做法。

**練習 B：為規則寫檢查方式。**把下列三條改寫成可檢查的規則：「內容要正確」「格式要整齊」「不要亂改檔案」。

**練習 C：設計規則分層。**你的專題有「研究報告」與「簡報」兩種產出。請規劃哪些規則放 `AGENTS.md`、哪些放 `.agents/rules/`，並寫出 `trigger`。

**練習 D：完整流程。**依 4.4 完成自己專題的 `AGENTS.md`，交付：規則檔、步驟 4 的驗證回答截圖、Git 提交紀錄（請 `agy` 顯示）。

### 5.2 評分規準 {#agy-rubric}

| 項目 | 達成 | 部分達成 | 未達成 |
|---|---|---|---|
| 安裝與登入 | 版本、模型清單、額度都能顯示 | 只能顯示版本 | 無法啟動 |
| 啟動位置 | 能說明工作區由啟動位置決定，並在 VS Code 正確啟動 | 能啟動但說不出原因 | 在主目錄啟動 |
| 會話操作 | 能用 `/diff`、`!`、`/resume` 檢查與接續 | 只會輸入自然語言 | 未檢查即接受所有修改 |
| AGENTS.md | 規則可檢查、結構一致、有重啟驗證證據 | 有規則但無驗證 | 沒有規則檔 |

### 5.3 常見問題與排錯 {#agy-faq}

| 症狀 | 可能原因 | 處理方式 |
|---|---|---|
| `agy: command not found` | PATH 尚未更新 | 完全重開 VS Code；仍不行則以完整路徑執行 `agy install`（1.4） |
| 瀏覽器沒有跳出登入頁 | 預設瀏覽器設定或遠端連線 | 複製終端機顯示的網址到瀏覽器開啟 |
| `secret keyring is locked` | 系統鑰匙圈被鎖定 | 解鎖系統鑰匙圈後重新啟動 `agy` |
| 規則好像沒生效 | 啟動位置不對、規則在子資料夾、`rules/*.md` 缺 `trigger` | 確認啟動資料夾；檢查 frontmatter；`/exit` 後重新啟動驗證 |
| `/compact`、`/init` 找不到 | 那是其他 CLI 的指令 | `agy` 用 `/clear`＋`docs/progress.md` 接續；規則用 4.4 流程產生 |
| 沒有出現 `auto` 模式 | 企業帳號、或系統不支援沙箱（如 Windows 10） | 本課使用 `default` 模式即可 |
| Agent 不經詢問就改檔 | 目前是 `auto` 或 `accept-edits` 模式 | 按 <kbd>Shift</kbd>+<kbd>Tab</kbd> 切回 `default`，或在 `/config` 修改預設 |
| 更新卡住，提示 `update.lock` | 另一個更新程序執行中 | 等待完成；參考官方排錯頁處理 |
| 用了 Homebrew 卻執行 `agy update` | Homebrew 版停用自動更新 | 改用 `brew upgrade --cask antigravity-cli` |

### 5.4 總結 {#agy-summary}

- `agy` 是原生執行檔，安裝不需 Node.js；裝完後用 `agy --version`、`/model`、`/usage` 確認「能執行、能登入、能用模型」。
- **在哪裡啟動，就在哪裡工作。**在 VS Code 開啟專題資料夾再開終端機，是最不容易出錯的啟動方式。
- 會話內有四種輸入：自然語言、`/`、`@`、`!`。修改前看權限提示，修改後用 `/diff` 與 Git 檢查。
- `AGENTS.md` 從啟動資料夾往上載入、累加生效；`.agents/rules/*.md` 必須有 `trigger`。
- 沒有 `/init`，就用 `/grill-me` → `/plan` → 寫入 → 重啟驗證，產生更貼合專題的規則，再用 `/learn` 持續維護。

### 5.5 延伸探索 {#agy-extension}

- **技能（Skills）：**把重複的多步驟流程寫成 `.agents/skills/<名稱>/SKILL.md`，它會自動變成斜線指令。規則說「要遵守什麼」，技能說「某件事怎麼做」。
- **MCP 伺服器：**用 `agy mcp list`、`agy mcp add` 管理外部工具連線；會話內用 `/mcp` 檢查狀態。
- **權限規則：**在 `/permissions` 為專題加入拒絕規則（例如禁止刪除 `inputs/`），體會「文字規則」與「實際權限」的差別。
- **與其他 CLI 共用規則：**同一份 `AGENTS.md` 交給 Codex CLI 使用，比較兩者對規則的理解差異；Claude Code 的載入方式見[前導章 5.2](00_intro.html#instruction-loading)。

## 附錄 A. agy 指令速查 {#agy-cheatsheet}

**終端機提示字元（只用 `agy` 開頭）：**

| 指令 | 用途 |
|---|---|
| `agy` | 啟動互動會話 |
| `agy -c` | 接續最近一次會話 |
| `agy -i "<提示>"` | 帶著第一句話啟動互動會話 |
| `agy -p "<提示>"` | 單次執行後結束 |
| `agy --mode <模式>` | 指定本次 Agent 模式：`default`、`accept-edits`、`auto`、`plan` |
| `agy --add-dir <路徑>` | 加入額外資料夾到工作區 |
| `agy --sandbox` | 在沙箱中執行終端機指令 |
| `agy --model "<名稱>"`、`agy --effort <等級>` | 本次使用的模型與推理強度 |
| `agy --version`、`agy changelog`、`agy update` | 版本、更新說明、手動更新 |
| `agy models`、`agy agents` | 列出可用模型、可用 Agent |
| `agy install` | 設定 PATH 與 shell 環境 |
| `agy mcp <子指令>` | 管理 MCP 伺服器：`list`、`add`、`remove`、`enable`、`disable` |
| `agy plugin <子指令>` | 管理外掛：`list`、`install`、`import`、`enable`、`disable`；`agy plugin import gemini` 匯入舊 Gemini CLI 擴充 |

**會話內快捷鍵：**

| 按鍵 | 作用 |
|---|---|
| <kbd>Shift</kbd>+<kbd>Tab</kbd> | 切換 `default` → `accept-edits` → `auto` → `plan` |
| <kbd>Esc</kbd> | 關閉面板、停止輸出，或清除空白提示 |
| <kbd>Ctrl</kbd>+<kbd>C</kbd> | 中斷目前回合；閒置時連按兩次離開 |
| <kbd>Shift</kbd>+<kbd>Enter</kbd> 或 <kbd>Ctrl</kbd>+<kbd>J</kbd> | 換行但不送出 |
| <kbd>Ctrl</kbd>+<kbd>O</kbd> | 展開或收合工具執行細節 |
| <kbd>Ctrl</kbd>+<kbd>G</kbd> | 用外部編輯器撰寫較長的提示 |
| <kbd>Ctrl</kbd>+<kbd>L</kbd> | 清除畫面 |
| `y`／`n` | 核准或拒絕工具請求 |

## 附錄 B. 查詢資料列表 {#agy-sources}

撰寫本章時查閱的資料如下，依用途分類。官方頁面查核日期均為 2026-11-17。

**Antigravity 官方文件**

| 主題 | 來源 | 本章用途 |
|---|---|---|
| CLI 入門 | [Getting started（CLI）](https://antigravity.google/docs/getting-started?tab=cli) | 安裝指令、安裝位置、首次啟動設定 |
| 登入驗證 | [Install & Authenticate（CLI）](https://antigravity.google/docs/install?tab=cli) | 帳號類型、鑰匙圈、API 金鑰、`/logout`、安裝旗標 |
| 指令參考 | [CLI reference](https://antigravity.google/docs/cli/reference) | 斜線指令、快捷鍵、啟動參數、設定鍵 |
| 執行模式 | [Modes](https://antigravity.google/docs/cli/modes) | `default`／`accept-edits`／`auto`／`plan` |
| 權限 | [Permissions](https://antigravity.google/docs/permissions) | 權限提示、規則語法、優先順序 |
| 設定 | [Settings（CLI）](https://antigravity.google/docs/settings?tab=cli) | `settings.json` 位置與鍵值 |
| 沙箱 | [Sandbox（CLI）](https://antigravity.google/docs/sandbox?tab=cli) | `--sandbox` 與各平台機制 |
| 規則 | [Rules](https://antigravity.google/docs/rules) | AGENTS.md／GEMINI.md 載入位置、`trigger`、引用語法、大小限制 |
| 自訂項目探索 | [Customization discovery](https://antigravity.google/docs/customization-discovery) | 規則、技能、外掛的搜尋路徑 |
| 技能 | [Skills](https://antigravity.google/docs/skills) | `.agents/skills/` 結構 |
| 提及 | [At-mentions](https://antigravity.google/docs/at-mentions) | `@` 檔案提及行為 |
| VS Code 擴充 | [VS Code extension](https://antigravity.google/docs/ide/extensions/vscode) | 擴充功能 ID 與版本需求 |
| 排錯 | [CLI troubleshooting](https://antigravity.google/docs/cli/troubleshooting) | PATH、鑰匙圈、自動更新鎖定 |
| 遷移 | [Gemini CLI migration](https://antigravity.google/docs/cli/gcli-migration) | `agy plugin import gemini`、GEMINI.md 相容 |

**本機查核（macOS，agy 1.5.10）**

| 查核項目 | 方法 | 結果摘要 |
|---|---|---|
| 啟動參數與子指令 | `agy --help`、`agy help install／mcp／plugin／models` | 附錄 A 的指令與說明 |
| 版本變更 | `agy changelog`（1.5.5–1.5.9） | 1.5.7 起預設模式為 `auto`；`!` 指令列於 Windows PowerShell 的修正（1.5.9）；`/learn` 大小限制檢查（1.5.8） |
| Homebrew | `brew info --cask antigravity-cli` | cask 版本 1.5.9，需 macOS 12 以上；Homebrew 版停用自動更新 |
| 規則自動載入 | 在測試資料夾以 `agy -p ... --mode plan` 詢問規則內容 | `AGENTS.md`、`.agents/rules/*.md`（`trigger: always_on`）、`@[說明](路徑)` 引用的檔案皆自動載入 |

**範例與相關教材**

| 主題 | 來源 | 本章用途 |
|---|---|---|
| 實例 AGENTS.md | [onclassbyJoel AGENTS.md](https://joelhoty.github.io/onclassbyJoel/AGENTS.md)（檔內最後更新 2026-10-30） | 4.7 範例分析 |
| 前導章 | [00_intro.html](00_intro.html) | 工作台、Git 觀念、其他 CLI 對照、Gemini 遷移 |
| 專案指引單元 | [05_instructions.html](05_instructions.html) | 規則撰寫的延伸閱讀 |

**未能在官方文件確認的項目：**`agy` 的移除指令、`/rewind` 對檔案的回復範圍、`.agents/rules/*.md` 中 `glob` 觸發的欄位名稱、可列出已載入規則的專用指令。本章對這些項目只寫已確認的部分，授課前請以 `/help` 與最新文件再確認。

## 附錄 C. 檔案資訊 {#agy-file-info}

> **最後更新時間**：2026-11-17 21:51:46 (UTC+8)
> **使用模型**：Claude Opus 5.5（模型代號 `claude-opus-5-5`）
> **執行 Agent**：Claude Code
> **查核環境**：macOS（Darwin 27.2.0）、agy 1.5.10、Homebrew cask antigravity-cli 1.5.9

| 版本 | 日期 | 變更摘要 |
|---|---|---|
| b01 | 2026-11-17 | 初版：agy 安裝（Windows、macOS）與登入、終端機與 VS Code 專題資料夾啟動、會話內操作、AGENTS.md 生成流程與三個範例（含 onclassbyJoel AGENTS.md 分析）、查詢資料列表 |
