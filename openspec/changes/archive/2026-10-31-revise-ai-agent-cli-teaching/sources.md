# 官方來源查核紀錄

查核日期：2026-10-31。用途：本次教材改版的安裝、登入、使用、指引與平台建議。來源均已實際開啟；以下記錄核對重點，不代表已執行安裝或登入。原前導教材 2026-10-29 的 npm、Bun、Python、uv 與 Jev 數據保留為歷史紀錄，本次不冒稱重新測試。

## Task 1：前導教材

| 官方來源 | 本次核對項目 | 教材處理 |
|---|---|---|
| [Codex CLI](https://learn.chatgpt.com/docs/codex/cli) | standalone 安裝、啟動與登入、互動功能 | 主線使用原生安裝，依來源更新 |
| [Codex Windows 部署](https://learn.chatgpt.com/docs/enterprise/windows-deployment) | PowerShell installer、-Release、使用者 PATH 與安裝路徑 | 保留 Windows 版本固定與新終端機檢查 |
| [Codex 指令](https://learn.chatgpt.com/docs/developer-commands?surface=cli) | exec、resume、login status、sandbox、update | update 只對支援 self-update 的發行版；新增雙 CLI 最小操作 |
| [Codex AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md) | 全域／專案指引發現與優先次序 | 指引載入與工具權限分開說明 |
| [Claude Code setup](https://code.claude.com/docs/en/setup) | OS/RAM、原生／Homebrew／WinGet、Node 22+ npm、doctor、update | 原生主線；npm 安裝需求不混同執行依賴 |
| [Claude Code quickstart](https://code.claude.com/docs/en/quickstart) | 訂閱／Console／雲端、首次登入 | 不宣稱一般聊天帳號即可使用 CLI |
| [Claude Code memory](https://code.claude.com/docs/en/memory) | CLAUDE.md、AGENTS.md v2.1.277 起的條件與匯入 | /memory 核對；教室兼容做法為 CLAUDE.md 匯入共用 AGENTS.md |
| [Claude Code CLI reference](https://code.claude.com/docs/en/cli-reference) | -p、-c、-r | 單次與互動指令分開 |
| [Claude Code interactive mode](https://code.claude.com/docs/en/interactive-mode) | /status、/login、/permissions | 會話命令不貼入 shell |
| [Antigravity 入門](https://antigravity.google/docs/getting-started?tab=cli) | 三平台腳本、agy 啟動與工作區 | 保留為選讀，課程不必安裝 |
| [Antigravity 遷移](https://antigravity.google/docs/cli/gcli-migration) | GEMINI.md／AGENTS.md、plugins、skills、MCP 欄位 | 舊工具遷移保留作選讀 |
| [Antigravity troubleshooting](https://antigravity.google/docs/cli/troubleshooting) | background updater、PATH | 更新失敗先診斷，不直接要求刪除 binary |
| [Codex cask](https://formulae.brew.sh/cask/codex)、[Claude Code cask](https://formulae.brew.sh/cask/claude-code)、[Antigravity cask](https://formulae.brew.sh/cask/antigravity-cli) | 原生 binary、平台清單；目前列有 Linux x86_64/ARM64 | 不套用歷史的「cask 一律只有 macOS」說法 |
| [Node.js 發行狀態](https://nodejs.org/en/about/previous-releases) | Current／Active LTS／Maintenance LTS | 不綁死當前最新主版本，選仍受支援 LTS |
| [PowerShell chain operators](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_pipeline_chain_operators?view=powershell-7.5) | PowerShell 7 起支援 && | 原稿錯誤訊息限定 Windows PowerShell 5.1，不混同 PowerShell 7 |

## 查核限制與內容來源

- 前導章的原概念、Python 範例、uv 操作、評量與歷史實測紀錄保留；這次新增的文件／HTML 檢查不能推論原歷史測試已重跑。
- 未呼叫付費模型、未登入服務、未實際安裝或移除 CLI、未執行原稿 Jev API。
- 已有使用者提供的 `AI_Agent_CLi/assets/agent_layers_b01.svg`，保持原檔。原稿提到但未提供的 `AI_working_env.md` 改成來源註記。
- 課堂提示、輸出與驗收是教材設計，不冒稱模型已產生指定結果。

# Task 3 source checks — 2026-10-31

Opened primary sources:
- https://learn.chatgpt.com/docs/non-interactive-mode — Codex exec, read-only default, automation; discovered via developers.openai.com/codex/noninteractive redirect.
- https://code.claude.com/docs/en/cli-reference — interactive vs print and separate session semantics.
- https://learn.chatgpt.com/docs/image-generation — ChatGPT images and current optional Codex imagegen capability; shared class route uses external service so Claude does not require image integration.
- https://support.google.com/gemininotebook/answer/16164461 — original NotebookLM help redirected to Gemini Notebook, source-grounded answers and fallibility; lesson identity/path preserved with current-name notice.
- https://pandoc.org/installing.html — Windows WinGet and macOS brew install, separate PDF engine prerequisites.
- https://pandoc.org/MANUAL.html — format conversion limitations and standalone HTML/output.
- https://marketplace.visualstudio.com/items?itemName=yzane.markdown-pdf — corrected obsolete limits: now PDF/HTML/PNG/JPEG, Mermaid, PlantUML, KaTeX and CSS; Chromium prerequisite.
- https://code.visualstudio.com/docs/languages/markdown — Markdown preview/editor context.
- https://developers.google.com/apps-script/reference/document/document-app — minimal Google Docs script; explicitly limited to h1/h2/text and needs authorization.

No CLI sessions, installation, paid image generation, Pandoc conversions or Google document writes were run. Bash -n and shell failure-path surrogates were run only. Grade numeric examples were independently recalculated with Python standard-library statistics; all five weighted totals and population standard deviations corrected. Original research prose/citations retained rather than represented as newly reverified research.

# Official research notes

Checked: 2026-10-31. Read-only documentation research; no CLI installation, authentication, model request or payment performed.

## Codex
- CLI landing: https://learn.chatgpt.com/docs/codex/cli . Standalone install/update macOS/Linux: `curl -fsSL https://chatgpt.com/codex/install.sh | sh`; Windows/npm/Homebrew tabs exist. Startup `codex`, then browser sign-in. `/status`, `/permissions`, `/model`, `/review`, `/init` are session commands.
- Windows installer: https://learn.chatgpt.com/docs/enterprise/windows-deployment . Download `https://chatgpt.com/codex/install.ps1`, execute in a new PowerShell window. `-Release` pins a release; omitted defaults latest. Per-user runtime/PATH; installation as SYSTEM does not magically become all-users.
- Reference: https://learn.chatgpt.com/docs/developer-commands?surface=cli . `codex resume --last` resumes latest chat scoped to cwd; `--all` broadens it. `codex update` depends on installed release supporting self-update. `codex exec --skip-git-repo-check` allows non-Git directories. `--sandbox read-only|workspace-write` controls model-generated shell operations; `-p` means profile, not print.
- Automation: https://learn.chatgpt.com/docs/non-interactive-mode . `codex exec "task"` final response stdout, progress stderr; `-o path` stores final response. `--json` is JSONL events. By default read-only; explicit `--sandbox workspace-write` permits scoped edits. `--full-auto` is no longer supported. Piped stdin can accompany a prompt argument.
- Auth: https://learn.chatgpt.com/docs/auth . `codex login`, `codex login status`, `codex logout`; subscription versus usage-billed API authentication differ. API key login via stdin `printenv OPENAI_API_KEY | codex login --with-api-key`. Do not insert literal keys in examples.
- Windows: https://learn.chatgpt.com/docs/windows/windows-sandbox . Native Windows is supported. MXC preferred on compatible systems, legacy elevated fallback requires admin setup; unelevated has weaker isolation. Avoid claiming WSL mandatory or native Windows experimental universally.

## Claude Code
- Install: https://code.claude.com/docs/en/setup . Native recommended; macOS/Linux/WSL `curl -fsSL https://claude.ai/install.sh | bash`; PowerShell `irm https://claude.ai/install.ps1 | iex`; native updates automatically. `claude --version`, `claude doctor`. Homebrew `brew install --cask claude-code` stable versus `claude-code@latest`; manual package-manager upgrades. WinGet `winget install Anthropic.ClaudeCode`. Windows Git for Windows is optional/recommended; without it Claude uses PowerShell. Native Windows has no Claude sandbox; WSL2 does. npm requires Node22+ at installation, downloads native binary not Node at runtime.
- CLI: https://code.claude.com/docs/en/cli-reference . `claude` interactive; `claude -p "task"` print then exit; `claude -c` continues most recent cwd conversation; `claude -r` selector or session argument. `claude auth login`, `claude auth status --text`, `claude auth logout`; `claude update`. `--output-format text|json|stream-json`; `--permission-mode plan` for planning; do not invent `claude chat` or `config set api_key`.
- Instructions: https://code.claude.com/docs/en/memory . AGENTS.md native support v2.1.277+. Default loads AGENTS.md only if no CLAUDE.md/.claude/CLAUDE.md/CLAUDE.local.md in cwd or ancestor. Global user/managed CLAUDE.md does not suppress it. `/config` Project instructions can load both. Built-in plugin disabled/older versions/first upgrade session can prevent support. Portable course pattern: CLAUDE.md containing `@AGENTS.md`. `/context` verifies memory files. AGENTS.override.md is not read by Claude. Text instructions are context, not enforced permissions.
- Permissions: https://code.claude.com/docs/en/permissions . `/permissions` shows rules; deny before ask before allow. Manual/default, acceptEdits, plan, auto, dontAsk, bypass modes differ. Plan reads/explores without source edits; not a guarantee of zero actions. Avoid teaching bypass flags as setup.

## Supporting toolchains
- https://code.visualstudio.com/docs/cpp/config-mingw : C/C++ extension does not install compiler; use documented MSYS2 UCRT64 toolchain; PATH and g++/gdb version checks.
- https://code.visualstudio.com/docs/python/python-tutorial : Python extension and interpreter separate; select project interpreter.
- https://docs.astral.sh/uv/getting-started/installation/ : standalone uv independent of preinstalled Python.
- https://docs.astral.sh/uv/guides/projects/ : uv init/add/run with pyproject and lockfile; do not replace project dependency declaration with global pip freeze.
