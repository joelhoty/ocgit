"""Reorder 00_intro.md for the beginner, VS Code-centred reading path.

Every block is moved by anchor id and every text edit asserts that its target
exists, so a stale string fails loudly instead of being skipped silently.
"""
import re
import shutil
import sys
from pathlib import Path

ROOT = Path("/Users/joelho/Library/Mobile Documents/com~apple~CloudDocs/vscode_project/OCgithub/AI_Agent_CLi")
SRC = ROOT / "00_intro.md"
BACKUP = Path(__file__).resolve().parents[1] / "inputs/00_intro.before.md"
if not BACKUP.exists():
    shutil.copy(SRC, BACKUP)
lines = BACKUP.read_text(encoding="utf-8").split("\n")

HEAD = re.compile(r"^(#{2,3}) (.+?) \{#([\w-]+)\}$")
blocks = {}
current = None
fence = False
for line in lines:
    if line.startswith("```"):
        fence = not fence
    m = None if fence else HEAD.match(line)
    if m:
        current = m.group(3)
        blocks[current] = [line]
    elif current:
        blocks[current].append(line)
blocks = {k: "\n".join(v).rstrip() for k, v in blocks.items()}
used = set()


def take(key):
    used.add(key)
    return blocks[key]


def sub(key, old, new, count=1):
    assert old in blocks[key], (key, old)
    blocks[key] = blocks[key].replace(old, new) if count == 0 else blocks[key].replace(old, new, count)


def retitle(key, title):
    blocks[key] = re.sub(r"^(#{2,3}) .+? \{#", lambda m: f"{m.group(1)} {title} {{#", blocks[key], count=1)


def demote(key):
    blocks[key] = "#" + blocks[key]


STUCK = "\n\n**卡住了？**先查[排錯索引](#troubleshooting)。"
VERIFIED = "2026-10-31"

# ---- 開頭與路線 -----------------------------------------------------------
HEADER = """# 前導章：讓 AI Agent 成為個人工作與學習助理 {#intro}

**VS Code ＋ 終端機 Agent（Codex CLI／Claude Code）入門教材**

> 對象：想學習 AI 應用的入門使用者。具備基本電腦操作能力即可，不需要程式背景。
> 工作方式：用 VS Code 管理檔案，在 VS Code 的整合終端機使用 Agent 產生與管理內容。Windows 使用 PowerShell 7，macOS 使用 zsh。
> 建議時數：基礎路線 6 節課，每節 50 分鐘；安裝與帳號準備可先完成。Python 延伸另需約 2 節。
> 官方文件查核日期：2026-10-31。CLI 從 Codex CLI／Claude Code 選一款即可；Antigravity 為附錄選讀。"""

ROUTE = """## 學習路線與閱讀約定 {#learning-route}

本課以「整理一份課堂筆記，交付有來源的複習資料」作為第一個完整任務。先認識 Agent 並搭好工作台，做完一次任務後，再回頭看懂系統架構，最後才學會話管理與程式自動化。"""
OUTCOMES = """### 完成後能做到什麼 {#learning-outcomes}

1. 在 VS Code 組好工作台：用檔案總管管理檔案，在整合終端機分開使用 Agent 與 shell。
2. 分辨安裝 CLI 所需環境、CLI 本身的執行依賴，以及工作專案的依賴。
3. 在正確資料夾啟動 AI Agent，讓它依資料與規則產生可檢查的文件。
4. 使用 Git 記錄修改，辨識未追蹤、未暫存與已暫存的變更。
5. 依據實際輸出與測試證據驗收 AI 工作，而不是只看它的完成宣告。
6. 用 L0–L5 六層架構說明 LLM、Context、Tools 與 Harness 的關係。
7. 【Python 延伸】透過 `uv` 管理 Python 版本、虛擬環境與套件，並在 VS Code 選對直譯器。"""
PLAN = """### 課程安排與交付物 {#course-plan}

| 節次 | 主題與對應章節 | 學習者交付物 |
|---|---|---|
| 1 | 認識 Agent、搭工作台（1–2） | 開好的專案資料夾、README 與工具版本 |
| 2 | 安裝登入 CLI 與第一次對話（3） | CLI 版本、登入驗證與權限觀察 |
| 3 | 第一個有來源的任務（4） | 來源筆記、摘要草稿與 Git 檢查點 |
| 4 | 專案規則與系統架構（5–6） | 專案指引、複習資料與六層對照表 |
| 5 | 管理會話與穩定工作（7–8） | 會話進度、用量觀察與收尾紀錄 |
| 6 | 練習、評量與總結（9） | 驗收證據、修正說明與版本紀錄 |
| 延伸 | Python 實作（10，選讀，約 2 節） | 可執行的學習時間統計程式 |

**基礎路線：**依序完成第 1–9 章；不需要先裝 Python 或 Node.js。
**Python 延伸：**完成基礎路線後再進入第 10 章，評分規準見第 9 章。
**卡住時：**查[排錯索引](#troubleshooting)。
**查閱：**更新、移除、原生／npm 差別與安裝盤點查附錄 A；Google 工具與舊 Gemini 遷移查附錄 B；官方來源查附錄 C。

每個階段都先完成前置檔案，再輸入任務。主線只安裝一款 CLI，無須同時購買多家服務。"""

sub("input-conventions", "- 標成 `powershell` 的區塊在 PowerShell 執行；標成 `bash` 的區塊在 macOS Terminal 的 zsh／bash 執行。",
    "- 除非另有說明，所有指令都在 VS Code 的整合終端機操作；Agent 與 shell 分開用兩個終端機，見[工作台](#vscode-workbench)。\n- 標成 `powershell` 的區塊在 PowerShell 執行；標成 `bash` 的區塊在 macOS 的 zsh 執行。")

# ---- 第 1 章：短版概念 ----------------------------------------------------
BASICS = """## 認識 AI Agent {#agent-basics}

**本章目的：**先知道 Agent 和聊天問答差在哪裡。這裡只講做第一個任務需要的概念；完整架構等親手做過一次再看（第 6 章）。這一章不需要安裝軟體。"""
sub("model-cli-environment", "這不是可代入數值的數學公式，也不是每個產品的實作規格。",
    "這不是可代入數值的數學公式，也不是每個產品的實作規格。\n\n**先記住三個詞：**Prompt 是你交代的任務；Context 是模型這一次實際看到的資訊；Tool 是實際讀檔、寫檔或執行命令的能力。檔案存在硬碟上，不等於模型已經讀過。")

# ---- 第 2 章：工作台 ------------------------------------------------------
WORKSPACE = """## 在 VS Code 搭好工作台 {#workspace-setup}

**本章目的：**把 VS Code 變成唯一的工作台，並決定平台與 CLI 路線。先看懂工作台，再準備編輯器、Git 與專案資料夾。Windows 讀 2.7，macOS 讀 2.8，再一起完成 2.9–2.12。此時還不需要啟動 Agent。"""
WORKBENCH = """### 工作台長什麼樣 {#vscode-workbench}

本課的操作都在同一個 VS Code 視窗完成：VS Code 負責檔案管理與審閱，終端機裡的 Agent 負責產生與管理內容。

| 區域 | 你在這裡做什麼 | 怎麼開啟 |
|---|---|---|
| 檔案總管（左側） | 建立、移動、開啟專案檔案 | `File → Open Folder` 開啟專案 |
| 編輯區（中央） | 閱讀與修改檔案，預覽 Markdown | 點選檔案；預覽按 `Ctrl+Shift+V`（macOS：`Cmd+Shift+V`） |
| Source Control（左側） | 查看 Agent 改了什麼、暫存與提交 | 活動列的分支圖示，或 `Ctrl+Shift+G` |
| Agent 終端機（下方） | 啟動 `codex` 或 `claude`，用自然語言交代任務 | `Terminal → New Terminal` |
| Shell 終端機（下方） | 執行安裝、Git、uv 等指令 | 終端機面板右上角的 `+` |

```mermaid
flowchart LR
    A["在 Agent 終端機交代任務"] --> B["Agent 讀寫專案檔案"]
    B --> C["在編輯區開啟產物"]
    C --> D["在 Source Control 看差異"]
    D -->|要修改| A
    D -->|通過| E["提交版本"]
```

**兩個終端機分開用。**Agent 終端機啟動 CLI 後，輸入的文字都交給 AI；shell 終端機輸入的文字由作業系統執行。把 Git 指令貼進 Agent 會話，或把中文任務貼進 shell，都是常見的混淆。

本課不需要安裝 Codex 或 Claude 的 VS Code 擴充功能，CLI 在整合終端機就能運作。新版 VS Code 已內建 Mermaid 預覽；若只看到圖表原始碼，先更新 VS Code。"""

sub("minimal-environment", "**本章目的：**決定自己的平台與 CLI 路線。先看必備工具與帳號條件，安裝時再照下一章操作；暫時不需要研究每種套件發行方式。",
    "先決定自己的平台與 CLI 路線，看必備工具與帳號條件；暫時不需要研究每種套件發行方式。")
sub("tool-roles", "| Windows Terminal | 容納不同 shell 的終端機介面 | 可選；VS Code 終端機也能操作 |",
    "| Windows Terminal | 容納不同 shell 的終端機介面 | 可選；本課使用 VS Code 整合終端機 |")
sub("choose-cli", "| Node.js | ", "| Node.js | ") if False else None
sub("platform-account-requirements", "| Codex CLI | 安裝腳本支援 macOS（Apple Silicon、Intel）、Linux（x86_64、arm64）與原生 Windows；官方未另列記憶體門檻 |",
    "| Codex CLI | 安裝腳本支援 macOS（Apple Silicon、Intel）、Linux（x86_64、arm64）與原生 Windows；GitHub 安裝文件列最低 4 GB、建議 8 GB 記憶體 |")
sub("platform-account-requirements", "授課前先在一台與教室相同的電腦測試登入與基本任務。課堂不需要同時購買多家服務；使用可用的一種即可。",
    """**年齡與帳號條件：**Claude 消費者方案須年滿 18 歲；OpenAI 服務須年滿 13 歲，未滿 18 歲需家長或監護人同意。未成年學習者，或由機構提供帳號時，依當下條款與機構政策確認。[Anthropic 條款](https://anthropic.com/terms)、[OpenAI 條款](https://openai.com/en-GB/policies/row-terms-of-use/)

**沒有可用帳號時：**可先讀第 3–6 章的流程，或觀看他人示範，等有帳號再補做。CLI 不需要同時購買多家服務，使用可用的一種即可。若用於課堂，先在一台與教室相同的電腦測試登入與基本任務。""")

sub("windows-vscode", "x", "x") if False else None
sub("windows-setup", "Markdown 預覽可使用 `Ctrl+Shift+V`。Mermaid 是否顯示，取決於閱讀器與擴充功能；圖表不顯示時仍可閱讀相鄰文字與表格，或在支援 Mermaid 的 Obsidian 閱讀模式開啟。\n\n", "") if "windows-vscode" not in blocks else None
sub("macos-setup", "macOS 直接使用 Terminal 的 zsh，或 VS Code 的整合終端機，不必為本課另外安裝 PowerShell。完成後接著看下方對照，再建立共同專案。",
    "macOS 使用 VS Code 整合終端機內的 zsh 即可，不必為本課另外安裝 PowerShell。完成後接著看下方對照，再建立共同專案。")
sub("terminal-basics", "macOS 可直接使用 Terminal 的 zsh，或 VS Code 整合終端機。PowerShell 是 Windows 主線選擇，不是 Agent 的通用必要條件。",
    "以下指令都在 VS Code 的整合終端機輸入。PowerShell 是 Windows 主線選擇，不是 Agent 的通用必要條件。")
sub("project-folders", "依自己的平台執行一組指令，建立本課的 `study-assistant`。如果已有同名專案，先確認內容，不要把陌生資料夾當成空白練習。",
    "在整合終端機依自己的平台執行一組指令，建立本課的 `study-assistant`。最後的 `code .` 會用 VS Code 開啟這個專案，之後都在這個視窗工作；若 `code` 不可用，改用 `File → Open Folder`。如果已有同名專案，先確認內容，不要把陌生資料夾當成空白練習。")
sub("project-folders", "在 VS Code 檔案總管建立 `README.md`、`AGENTS.md`、`.gitignore`。先完成本章的 README 與忽略規則；指引內容會在[首次任務](#project-instructions)填入，Claude 路線另建立 CLAUDE.md。",
    "在 VS Code 檔案總管建立 `README.md` 與 `.gitignore`。專案指引 `AGENTS.md` 等做完第一個任務再建立，見[第 5 章](#project-rules)。")
sub("project-folders", "├── AGENTS.md              <- 給 Agent 的專案指引", "├── AGENTS.md              <- 給 Agent 的專案指引（第 5 章建立）")

# ---- 第 3 章：安裝 --------------------------------------------------------
sub("installation-choice", "以下只選 Claude Code 或 Codex CLI **其中一款**，再執行對應平台的指令。",
    "以下只選 Claude Code 或 Codex CLI **其中一款**，在 VS Code 的整合終端機執行對應平台的指令。")
sub("installation-choice", "完成登入後，兩條路線都回到 4.4 驗證工作目錄。", "完成登入後，兩條路線都回到[第一次對話的共同驗證](#verify-first-session)。")
sub("installation-choice", "本節保留最短原生安裝路線；", "本節只列最短的原生安裝路線；")
RESTART = "安裝後完全關閉並重新開啟 VS Code，讓整合終端機取得新的 PATH。確認仍在 `study-assistant`（Windows：`Get-Location`；macOS：`pwd`）後，"
sub("install-claude", "安裝後開新終端機，再回到上一章建立的專案：Windows 用 `Set-Location \"$env:USERPROFILE\\AI-Lab\\study-assistant\"`；macOS 用 `cd \"$HOME/AI-Lab/study-assistant\"`。兩平台接著執行：",
    RESTART + "兩平台接著執行：")
sub("install-codex", "安裝後開新終端機，再回到上一章建立的專案：Windows 用 `Set-Location \"$env:USERPROFILE\\AI-Lab\\study-assistant\"`；macOS 用 `cd \"$HOME/AI-Lab/study-assistant\"`。兩平台接著在 shell 執行：",
    RESTART + "兩平台接著在 shell 執行：")
sub("install-codex", "官方未提供 CLI 的 WinGet 或 CMD 安裝指令。", "OpenAI 官方文件未列 CLI 的 WinGet 或 CMD 安裝方式。")
sub("verify-first-session", "下一章準備來源與規則時，可在 VS Code 編輯檔案；需要執行 Git 時另開 shell 終端機，避免把命令貼進 AI 會話。",
    "從下一章開始同時使用兩個終端機：Agent 會話留在原本的終端機，Git 指令在另一個 shell 終端機執行。")
blocks["install-claude"] += STUCK
blocks["install-codex"] += STUCK
PERMISSIONS = """### 看懂權限提示 {#permission-prompts}

Agent 要寫檔、執行命令或連網時，工具可能先停下來問你。這個提示是實際的控制點，比寫在文字裡的要求更有效，不要習慣性全部同意。

| 看到什麼 | 先問自己 | 做法 |
|---|---|---|
| 讀取專案內的檔案 | 這個檔案與任務有關嗎？ | 有關就允許 |
| 寫入或修改檔案 | 路徑是我交代的位置嗎？ | 路徑正確才允許，完成後到 Source Control 看差異 |
| 執行命令 | 我看得懂它要做什麼嗎？ | 看不懂就拒絕，請它先說明用途與影響 |
| 安裝套件、連網、刪除、對外發送 | 這次任務真的需要嗎？ | 先拒絕，確認需要才只允許這一次 |

拒絕不會弄壞任務：Agent 會收到拒絕結果，你可以再說明限制。在會話內輸入 `/permissions` 可查看目前的權限設定。兩款工具的預設不同，有些操作可能不會先詢問，所以事後仍要看差異。本課不開啟自動核准。第 6 章會再說明文字規則與權限的差別。[Claude Code 權限](https://code.claude.com/docs/en/permissions)、[Codex CLI 指令](https://learn.chatgpt.com/docs/cli/slash-commands)"""

# ---- 第 4 章：第一個任務 --------------------------------------------------
FIRST_TASK = """## 完成第一個有來源的任務 {#first-task}

**本章目的：**用同一份筆記完成一次可驗收的對話工作。依序準備來源、建立 Git 檢查點，讓 Agent 讀檔、追問與保存，再回到 VS Code 驗收。筆記內容談 Python，但本章只處理文字，**不需要先安裝或操作 Python**。"""
sub("source-notes", "來源快照會在 5.4 與專案文件一起提交。", "來源快照會在下一節與專案文件一起提交。")
sub("first-checkpoint", "在 **shell 終端機**執行，不貼到 AI 會話。先用 Windows `Get-Location` 或 macOS `pwd` 確認位於自己的 `study-assistant`。",
    "在 **shell 終端機**執行，不貼到 AI 會話；Agent 會話留在原本的終端機即可。先用 Windows `Get-Location` 或 macOS `pwd` 確認位於自己的 `study-assistant`。")
sub("first-checkpoint", "git add README.md .gitignore AGENTS.md inputs/notes.md", "git add README.md .gitignore inputs/notes.md")
sub("first-checkpoint", "Claude 路線若已建立 `CLAUDE.md`，另外執行 `git add CLAUDE.md`。接著檢查暫存內容並提交：", "接著檢查暫存內容並提交：")
sub("first-checkpoint", 'git commit -m "建立學習助理專案、工作規則與來源筆記"', 'git commit -m "建立學習助理專案與來源筆記"')
sub("first-checkpoint", "**成功判準：**能看到提交代碼與訊息，且提交內包含正確來源與規則。這是讓你知道任務開始前檔案長什麼樣子的檢查點；`git add` 與 diff 的關係會在第 7 章進一步說明。",
    "**成功判準：**能看到提交代碼與訊息，且提交內包含正確來源。這是讓你知道任務開始前檔案長什麼樣子的檢查點；VS Code 的 Source Control 也會顯示同樣的狀態，暫存與差異的意思在本章最後說明。")
sub("read-followup-save", "沿用上一節確認指引的會話，日常與進階任務都在同一會話中逐輪溝通；不用每次回到 shell 重新啟動。安裝與環境設定指令才依標示在 shell 執行。",
    "回到 Agent 終端機的會話。日常與進階任務都在同一會話中逐輪溝通，不用每次回到 shell 重新啟動；安裝與環境設定指令才依標示在 shell 執行。")
sub("read-followup-save", "這次先將摘要草稿存成 outputs/notes_summary.md；這是本練習指定的草稿檔名。", "這次先將摘要草稿存成 outputs/notes_summary.md。")
sub("read-followup-save", "**驗收：**逐點對回筆記，開啟實際檔案檢查，再查看 Git 變更；原先已有的修改不能算成本次成果。這是學習者實作設計，編寫教材時未代替學習者呼叫模型。",
    "**驗收：**見下一節；原先已有的修改不能算成本次成果。")
sub("read-followup-save", "文字要求「不要修改」不是檔案系統唯讀設定。開始前用會話內的 `/permissions` 檢查工具權限，收到操作授權時看清楚路徑與用途。專案長期指引另放在 `AGENTS.md` 或 `CLAUDE.md`，詳見[單元五：專案指引](05_instructions.html)，它們是檔案，不是對話操作指令。",
    "文字要求「不要修改」不是檔案系統唯讀設定。收到操作授權時，依[權限提示](#permission-prompts)看清楚路徑與用途。" + STUCK.strip())
REVIEW = """### 在 VS Code 驗收 {#review-in-vscode}

Agent 說完成後，回到 VS Code 自己確認：

1. 在檔案總管開啟 `outputs/notes_summary.md`，逐點對回 `inputs/notes.md`。
2. 開啟 Source Control。新檔案會顯示為未追蹤，點開檢查內容；`inputs/notes.md` 不應出現在變更清單。
3. 確認後按檔案旁的 `+` 暫存，輸入訊息並提交。也可在 shell 終端機執行：

```shell
git add outputs/notes_summary.md
git diff --staged
git commit -m "加入摘要草稿"
```

下一節說明這幾個步驟背後的三個位置。"""
retitle("git-states", "理解 Git 的三個位置")

# ---- 第 5 章：規則 --------------------------------------------------------
RULES = """## 把要求寫成專案規則 {#project-rules}

**本章目的：**上一章每次都要重複交代「標示來源」「不改來源檔」。把這些要求寫成規則，再用規則完成一份完整的複習資料。"""
sub("project-instructions", "先把共用規則貼進 `AGENTS.md`；下一節說明 Claude 路線如何載入它。規則中的 Python 操作只在第 8 章延伸實作時使用：",
    "在專案根目錄新增 `AGENTS.md`，貼入共用規則；下一節說明 Claude 路線如何載入它：")
sub("project-instructions", "- 協助整理筆記、產生自我測驗與執行學習時間統計。", "- 協助整理筆記與產生自我測驗。")
sub("project-instructions", "- 程式放在 scripts；修改前說明用途。\n- Python 指令從專案根目錄使用 uv run 執行。\n", "")
sub("project-instructions", "這是文字規則範例，不會自動設定作業系統權限。課程使用的工作資料夾與 CLI 權限，仍需在工具中設定。",
    "這是文字規則範例，不會自動設定作業系統權限；實際限制由工具的權限與 sandbox 負責。規則可以再加深，見[單元五：專案指引](05_instructions.html)。")
sub("instruction-loading", "用 `/memory` 核對 |", "用 `/context` 的 Memory files 核對 |")
sub("instruction-loading", "可在 `/config` 的 Project instructions 選擇同時載入兩種規則，並以 `/memory` 檢查。本課為了讓不同教室版本共用內容，在同一資料夾的 `CLAUDE.md` 使用：",
    "可在 `/config` 的 Project instructions 選擇同時載入兩種規則，並以 `/context` 的 Memory files 檢查。`/memory` 也會列出不存在的檔案，且要到 v2.1.280 才能確認直接讀取的 AGENTS.md。本課為了讓不同版本共用內容，Claude 路線在同一資料夾建立 `CLAUDE.md`，內容為：")
sub("verify-instructions", "請比較 AI 回答與檔案內容。主動要求讀檔可以確認文字內容，但不等於證明它在啟動時就自動載入；有指引清單或日誌時一起核對。",
    """請比較 AI 回答與檔案內容。主動要求讀檔可以確認文字內容，但不等於證明它在啟動時就自動載入；有指引清單或日誌時一起核對。

確認後在 shell 終端機提交規則；Claude 路線另外加上 `CLAUDE.md`：

```shell
git add AGENTS.md
git commit -m "加入專案工作規則"
```""")
sub("complete-review", "摘要草稿驗收後，繼續在同一會話要求完整複習資料。這一步檢查三重點草稿是否漏掉來源段落，補齊為一一對應 P1–P4 的四個核心重點，另加測驗與操作練習。草稿與完整版是同一任務的兩個階段，並非改變原草稿的驗收條件：",
    "規則確認後，在同一會話要求完整複習資料。這一步檢查三重點草稿是否漏掉來源段落，補齊為一一對應 P1–P4 的四個核心重點，另加測驗與操作練習，並觀察規則是否讓你少交代幾句：")
sub("complete-review", "目標：把 inputs/notes.md 整理成高中生可閱讀的課後複習資料。", "目標：把 inputs/notes.md 整理成入門者可閱讀的課後複習資料。")
sub("complete-review", "請先讀 AGENTS.md 與 inputs/notes.md，再建立 outputs/review_b01.md。", "請先讀 AGENTS.md、inputs/notes.md 與 outputs/notes_summary.md，再建立 outputs/review_b01.md。")
sub("read-followup-save", "把剛才的三個重點改寫成適合高中生複習的版本。", "把剛才的三個重點改寫成適合入門者複習的版本。")
sub("verify-deliverables", "git add outputs/notes_summary.md outputs/review_b01.md", "git add outputs/review_b01.md")
sub("verify-deliverables", "若產出的是其他版本，請替換檔名。這個流程把 L1 的來源、L3 的寫檔與 L4 的驗收連在一起。",
    "若產出的是其他版本，請替換檔名。下一章會用這個流程說明系統各層如何合作。")

# ---- 第 6 章：回頭看懂系統 ------------------------------------------------
SYSTEM = """## 回頭看懂 Agent 系統 {#understand-system}

**本章目的：**用剛完成的任務理解完整架構。知道系統怎麼分層，出問題時才知道該查哪裡。這一章不需要操作。"""
retitle("agent-layer-diagram", "六層分層圖")
sub("agent-layer-diagram", "本地 SVG 保留原圖內容與布局，補白色背景以適應深色閱讀介面。", "本地 SVG 補白色背景以適應深色介面。")
sub("layers-in-practice", "以「讀取學習筆記，產生重點與自我測驗」為例：", "用你剛完成的「讀取筆記，產生重點與自我測驗」對照：")
sub("guidance-and-permissions", "把「不要改原始檔」寫在 AGENTS.md，是給模型的行為指引。", "第 5 章把「不直接修改 inputs」寫在 AGENTS.md，是給模型的行為指引。")

# ---- 第 7 章：會話 --------------------------------------------------------
sub("slash-commands", "| 看用量 | `/status`；可用 `/statusline` 顯示 token 等資訊 | `/usage`（現行文件的 `/cost`、`/stats` 為其別名） |",
    "| 看用量 | `/usage`；可用 `/statusline` 顯示 token 等資訊 | `/usage`（現行文件的 `/cost`、`/stats` 為其別名） |")
sub("slash-commands", "Codex 本表以 `/status` 查用量，不將 Claude 的 `/usage` 當成兩款共通指令。模型清單以實際選單為準，無須背誦固定模型名稱。",
    "兩款都有 `/usage`，但顯示內容不同；Codex 未以其服務帳號登入時，會提示需要登入。模型清單以實際選單為準，無須背誦固定模型名稱。")
sub("slash-commands", "依據：[Codex CLI 會話指令](https://learn.chatgpt.com/docs/developer-commands?surface=cli)、", "依據：[Codex CLI 斜線指令](https://learn.chatgpt.com/docs/cli/slash-commands)、[Codex CLI 指令](https://learn.chatgpt.com/docs/developer-commands?surface=cli)、")
sub("session-context-usage", "一個階段完成後查看用量；Codex 用 `/status`，Claude 用 `/usage`。", "一個階段完成後用 `/usage` 查看用量。")

# ---- 第 8 章：穩定工作 ----------------------------------------------------
RELIABLE = """## 穩定工作與收尾 {#reliable-work}

**本章目的：**在每次任務後保留成果、能回復錯誤，並知道怎麼向 AI 求助。Git 命令仍在 shell 終端機執行；要請 Agent 協助時，再把目標與錯誤訊息貼進 Agent 會話。遇到問題先查[排錯索引](#troubleshooting)。"""

# ---- 第 9 章：基礎評量 ----------------------------------------------------
PRACTICE = """## 基礎練習、評量與總結 {#practice-summary}

**基礎路線：**完成兩個練習，再用本章其餘小節自評。完成第 10 章 Python 延伸的讀者，再加上該章的資料測試與綜合任務。"""
sub("exercise-minimal-setup", "完成第 5 章文件整理。", "完成第 4–5 章文件整理。")

# ---- 第 10 章：Python ------------------------------------------------------
sub("python-practice", "只整理文件的讀者可先跳到第 9 章基礎評量。", "只整理文件的讀者不需要本章。")
sub("python-practice", "## 8. 延伸實作：Python 學習時間統計", "## 延伸實作：Python 學習時間統計")
sub("initialize-python", "**成功判準：**Python 版本為 3.13 系列；", """接著在 `AGENTS.md` 的「執行與驗收」補上兩條規則：

```markdown
- 程式放在 scripts；修改前說明用途。
- Python 指令從專案根目錄使用 uv run 執行。
```

**成功判準：**Python 版本為 3.13 系列；""")
sub("exercise-data-errors", "### 9.3 Python 延伸：資料錯誤能否被發現", "### 9.3 資料錯誤能否被發現")
sub("weekly-assistant", "### 9.4 Python 綜合任務：一週學習助理", "### 9.4 綜合任務：一週學習助理")

# ---- 排錯索引 --------------------------------------------------------------
TROUBLE = """## 排錯索引 {#troubleshooting}

這一章不用依序閱讀，操作卡住時再回來查。先判斷錯誤在哪一層，再用對照表找處理方式。"""
sub("diagnose-layer", "### 7.5 先判斷錯誤在哪一層", "### 先判斷錯誤在哪一層")
sub("troubleshooting-table", "### 7.6 問題對照表", "### 問題對照表")
sub("troubleshooting-table", "| 仍在使用 `gemini` 指令 | Gemini CLI 已由 Antigravity CLI 取代 |", "| 仍在使用 `gemini` 指令 | 個人方案的 Gemini CLI 服務已轉移至 Antigravity CLI；企業授權與付費 API 金鑰不在此限 |")
sub("troubleshooting-table", "| 外部 PowerShell 可用，VS Code 內不可用 | VS Code 保留舊環境變數 | 完全關閉後重新開啟 VS Code |",
    "| 外部 PowerShell 可用，VS Code 內不可用 | VS Code 保留舊環境變數 | 完全關閉後重新開啟 VS Code |\n| 工具一直要求核准，或拒絕執行 | 權限設定或 sandbox 限制 | 依[權限提示](#permission-prompts)閱讀它要的路徑與命令，只核准本次必要操作 |\n| 安裝時下載失敗 | 網路、代理或官方網址 | 保存錯誤訊息，勿以關閉安全工具作為通用解法 |")
sub("troubleshooting-table", "| 圖表只顯示 Mermaid 原始碼 | 閱讀器不支援 Mermaid | 用支援的閱讀模式；SVG 分層圖可獨立開啟 |",
    "| 圖表只顯示 Mermaid 原始碼 | VS Code 版本較舊，或閱讀器不支援 | 更新 VS Code 或改用支援的閱讀器；SVG 分層圖可獨立開啟 |")

# ---- 附錄 A：事實修正與改順序 ----------------------------------------------
sub("appendix-installation", "查完可回到[CLI 安裝](#cli-installation)或[穩定工作](#reliable-work)。", "前四節是常用查閱項目，後面說明安裝原理。查完可回到[CLI 安裝](#cli-installation)或[穩定工作](#reliable-work)。")
sub("installation-methods", "**基本資料（原稿套件盤點日 2026-10-29；2026-10-31 複核官方安裝文件）：**", "**基本資料（2026-10-31 查核官方安裝文件）：**")
sub("installation-methods", "| WinGet | Windows | 只有 Claude Code（`Anthropic.ClaudeCode`）；Codex 官方頁未列 CLI 的 WinGet，agy 官方未列 |",
    "| WinGet | Windows | 官方文件只列 Claude Code（`Anthropic.ClaudeCode`）；WinGet 另有 `OpenAI.Codex`，但 OpenAI 文件未列；agy 官方未列 |")
sub("installation-methods", "| **是**（Claude Code 要 22+） | Claude Code：否；Codex：**是** | 手動 `npm install -g <套件>` |",
    "| **是**（Claude Code 要 22+） | Claude Code：否；Codex：**是** | Claude Code 會自動更新；Codex 手動 `npm install -g <套件>` |")
sub("installation-methods", "三款中只有 Claude Code 有官方套件；", "官方文件只列 Claude Code；")
sub("installation-decisions", "（見附錄 A.8）", "（見附錄 A.4）")
sub("installation-decisions", "（見附錄 A.9）", "（見附錄 A.3）")
sub("installation-decisions", "那時再依附錄 A.9 安裝 Node.js LTS", "那時再依附錄 A.3 安裝 Node.js LTS")
sub("installation-decisions", "附錄 A.3 以後說明這個結論的根據：", "附錄 A.7 以後說明這個結論的根據：")
sub("alternative-installation", "下表保留原官方安裝總表的選擇資訊，原生指令改用章節連結，避免同一指令多處維護。\n\n", "")
sub("alternative-installation", "| 無官方 CMD／WinGet CLI 路線；Homebrew `codex`；npm `@openai/codex` |", "| 官方文件未列 CMD／WinGet；Homebrew `codex`；npm `@openai/codex` |")
sub("alternative-installation", "| Git for Windows | 選用；有安裝時 Bash 與 Monitor 工具使用 Git Bash，沒有時改用 PowerShell 工具；本課已安裝 Git |",
    "| Git for Windows | 選用；有安裝時 Bash 工具使用 Git Bash，沒有時改用 PowerShell 工具；Monitor 工具在 Windows 僅於有 Git Bash 時可用；本課已安裝 Git |")
sub("alternative-installation", "**Codex：官方四個安裝分頁**（原稿查核 2026-10-29，課程版複核 2026-10-31）：", "**Codex：官方四個安裝分頁**（查核 2026-10-31）：")
sub("update-uninstall", "| Claude Code Homebrew | `brew upgrade claude-code`（或 `claude-code@latest`） | `brew uninstall --cask claude-code` |",
    "| Claude Code Homebrew | `brew upgrade claude-code`（或 `claude-code@latest`） | `brew uninstall --cask claude-code`（`@latest` 版用 `brew uninstall --cask claude-code@latest`） |")
sub("update-uninstall", "| Claude Code npm | `npm install -g @anthropic-ai/claude-code@latest`（不要用 `npm update -g`） |", "| Claude Code npm | 會自動更新；手動用 `npm install -g @anthropic-ai/claude-code@latest`（不要用 `npm update -g`） |")
sub("update-uninstall", "Windows 上 npm 指令請用 `npm.cmd`。", """登入狀態與診斷在 shell 終端機執行：

| 檢查 | Codex CLI | Claude Code |
|---|---|---|
| 登入狀態 | `codex login status` | `claude auth status --text` |
| 重新登入 | `codex login` | `claude auth login` |
| 安裝診斷 | `codex doctor` | `claude doctor` |

Windows 上 npm 指令請用 `npm.cmd`。""")
sub("installation-inventory", "同名指令有多個版本時，先確認目前使用哪份，再處理舊安裝。原稿教師筆電的實際盤點已移至[歷史紀錄](#historical-inventory)，不能視為你的電腦狀態。",
    "同名指令有多個版本時，先確認目前使用哪份，再處理舊安裝。")
sub("antigravity-overview", "Google 的 Agent CLI 已由 Gemini CLI（`gemini`）改為 Antigravity CLI（`agy`），本教材的 Google 路線只使用 `agy`。",
    "Google 的個人方案已由 Gemini CLI（`gemini`）轉移至 Antigravity CLI（`agy`），企業授權與付費 API 金鑰仍可使用 Gemini CLI；本教材的 Google 路線只使用 `agy`。")
sub("cli-installation", "## 4. 安裝並登入一款 CLI", "## 安裝並登入一款 CLI")

# ---- 附錄 C：只留來源與維護 ------------------------------------------------
APPENDIX_C = """## 附錄 C. 官方來源與維護 {#appendix-history}

本附錄列出維護教材時查閱的來源與課前檢查項目。版本與歷史驗證紀錄另存於 [00_intro_history.md](00_intro_history.md)，僅供維護參考。"""
sub("teaching-maintenance", "### C.2 授課前重新確認", "### C.2 授課前重新確認")


sub("tool-roles", "| Python | 執行 Python 程式 | 第 8 章開始 |", "| Python | 執行 Python 程式 | 第 10 章延伸時才需要 |")
sub("tool-roles", "| uv | 管理 Python、依賴與專案環境 | Python 主線 |", "| uv | 管理 Python、依賴與專案環境 | 第 10 章延伸時才需要 |")
sub("choose-cli", "| 第 8 章 Python 統計 |", "| 第 10 章 Python 統計 |")
sub("platform-account-requirements", "| 記憶體 | 課堂建議 8 GB 以上，16 GB 較充裕 | 是同時開編輯器、瀏覽器與 CLI 的教學建議，不是所有工具官方最低需求 |", "| 記憶體 | 建議 8 GB 以上，16 GB 較充裕 | 是同時開編輯器、瀏覽器與 CLI 的建議，不是所有工具官方最低需求 |")
sub("layers-in-practice", "| 學生、教師、作業要求、電腦與檔案 |", "| 你的目標、任務要求、電腦與檔案 |")
sub("context-tools-skills", "課堂上應要求 AI 說明", "應要求 AI 說明")
sub("workflow-and-agent", "**課堂小練習：**", "**小練習：**")
sub("session-context-usage", "教師依任務決定何時讓 Agent 繼續", "你依任務決定何時讓 Agent 繼續")
sub("cross-disciplinary", "將同學的學習紀錄交給雲端模型前", "將他人的學習紀錄交給雲端模型前")
sub("install-python-uv", "若教室已統一另一個受支援版本，可整班調整，但必須同步修改文件並重跑範例。", "若想改用另一個受支援版本，須同步修改文件並重跑範例。")
sub("weekly-assistant", "不要用真實同學的個資", "不要用他人的真實個資")
sub("installation-inventory", "（例如教師自己的筆電）", "（例如自己用了一段時間的筆電）")
sub("select-python-interpreter", "先完成 8.3 的 `uv sync`", "先完成 10.3 的 `uv sync`")

HISTORY_KEYS = ["historical-inventory", "version-history", "historical-verification", "historical-jev-compliance", "historical-jev-diagrams"]

# ---- 組合 ------------------------------------------------------------------
ORDER = [
    ROUTE, OUTCOMES, PLAN, "input-conventions",
    BASICS, "from-chat-to-work", "environment-purpose", "model-cli-environment",
    WORKSPACE, WORKBENCH, "minimal-environment", "tool-roles", "choose-cli", "platform-account-requirements",
    "setup-order", "windows-setup", "macos-setup", "terminal-basics", "project-folders", "project-readme", "gitignore",
    "cli-installation", "installation-choice", "install-claude", "install-codex", "verify-first-session", PERMISSIONS,
    FIRST_TASK, "source-notes", "first-checkpoint", "read-followup-save", REVIEW, "git-states",
    RULES, "project-instructions", "instruction-loading", "verify-instructions", "complete-review", "verify-deliverables",
    SYSTEM, "agent-layer-diagram", "layers-in-practice", "context-tools-skills", "guidance-and-permissions", "agent-loop", "workflow-and-agent",
    "session-controls", "slash-commands", "session-context-usage",
    RELIABLE, "git-recovery", "versions-and-backups", "work-closeout", "debugging-prompt", "cost-and-quota",
    PRACTICE, "exercise-layers", "exercise-minimal-setup", "assessment-rubric", "knowledge-summary", "skills-checklist",
    "reflection-questions", "application-scenarios", "cross-disciplinary", "further-exploration",
    "python-practice", "python-environment-concepts", "install-python-uv", "initialize-python", "python-project-files",
    "select-python-interpreter", "study-data", "study-pseudocode", "study-program", "run-study-report", "debug-study-program",
    "agent-bounded-change", "python-packages", "python-activation", "exercise-data-errors", "weekly-assistant",
    TROUBLE, "diagnose-layer", "troubleshooting-table",
    "appendix-installation", "update-uninstall", "installation-inventory", "node-installation", "alternative-installation",
    "installation-methods", "installation-decisions", "binary-script-manager", "distribution-terms", "dependency-stages",
    "cli-dependency-comparison", "implementation-language",
    "appendix-antigravity", "antigravity-overview", "install-antigravity", "gemini-migration",
    APPENDIX_C, "official-sources", "teaching-maintenance",
]
REPLACED = {"learning-route", "learning-outcomes", "course-plan", "agent-basics", "workspace-setup", "first-task", "reliable-work", "practice-summary", "appendix-history"}
demote("minimal-environment")
sub("minimal-environment", "### 2. 選擇最小工作環境", "### 選擇最小工作環境")
sub("session-controls", "## 6. 管理會話、模型與用量", "## 管理會話、模型與用量")

parts = [HEADER]
for item in ORDER:
    if item in blocks:
        parts.append(take(item))
    else:
        parts.append(item)
missing = set(blocks) - used - REPLACED - set(HISTORY_KEYS)
assert not missing, missing
body = "\n\n".join(parts) + "\n"

# ---- 章節重新編號 ----------------------------------------------------------
out = []
fence = False
chapter = -1
section = 0
sub4 = 0
letter = None
for line in body.split("\n"):
    if line.startswith("```"):
        fence = not fence
    if fence:
        out.append(line)
        continue
    if line.startswith("## "):
        title = re.sub(r"^## (\d+\. )?", "", line)
        section, sub4 = 0, 0
        m = re.match(r"附錄 ([A-C])\.", title)
        if m:
            letter = m.group(1)
            out.append("## " + title)
        elif title.startswith("排錯索引"):
            letter = "T"
            out.append("## " + title)
        else:
            letter = None
            chapter += 1
            out.append(f"## {chapter}. {title}")
        continue
    if line.startswith("### ") and "{#" in line:
        section += 1
        sub4 = 0
        title = re.sub(r"^([A-C]\.\d+|\d+\.\d+) ", "", line[4:])
        prefix = (letter if letter else str(chapter)) + f".{section}"
        out.append(f"### {prefix} {title}")
        continue
    if line.startswith("#### ") and re.match(r"#### \d+\.\d+\.\d+ ", line):
        sub4 += 1
        title = re.sub(r"^#### \d+\.\d+\.\d+ ", "", line)
        out.append(f"#### {chapter}.{section}.{sub4} {title}")
        continue
    out.append(line)
body = "\n".join(out)
SRC.write_text(body, encoding="utf-8")

# ---- 歷史紀錄另存 ----------------------------------------------------------
history = ["# 前導章版本與歷史驗證紀錄", "",
           "本檔保存前導章的維護紀錄，不是學習內容。內文的節號指向當時版本；紀錄描述當時的狀態，不代表目前教材或讀者電腦已重新驗證。", ""]
for key in HISTORY_KEYS:
    used.add(key)
    text = re.sub(r" \{#[\w-]+\}$", "", blocks[key], count=1, flags=re.M)
    text = re.sub(r"^### C\.\d+ ", "## ", text, count=1)
    history.append(text.replace("\n---", "").rstrip())
    history.append("")
history_text = "\n".join(history)
row = "| 本次閱讀順序重整 | 2026-10-31 |"
assert row in history_text
marker = next(l for l in history_text.split("\n") if l.startswith(row))
history_text = history_text.replace(marker, marker + "\n| 入門概念版重整 | 2026-10-31 | 受眾改為入門使用者；以 VS Code 工作台為主場；主線改為短版概念 → 工作台 → CLI → 第一個任務 → 專案規則 → 回看系統架構；Python 改為基礎評量後的延伸；排錯集中為索引；附錄 A 依查閱頻率排序；歷史紀錄移至本檔 |")
(ROOT / "00_intro_history.md").write_text(history_text, encoding="utf-8")
print("ok chapters", chapter)
