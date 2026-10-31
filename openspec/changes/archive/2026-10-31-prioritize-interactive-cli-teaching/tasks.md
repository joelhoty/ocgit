# Tasks: CLI 教材以互動對話為主線

> For agentic workers: Use sos-apply; apply TDD only where appropriate for editorial work.

**Goal:** 全課程包含進階任務均以 CLI 互動介面與自然語言為主。
**Architecture:** 保留現有靜態頁面，配對內容同步修改。兩款工具共用任務提示，區分 shell 與會話輸入。

### Task 1: 改寫操作約定與教學案例
**Covers:** `REQ-TEACH-003`, `REQ-TEACH-009`, `REQ-TEACH-010`, `REQ-TEACH-011`
**Risk:** Standard
**Expected Files:**
- Modify: `AI_Agent_CLi/00_intro.md`
- Modify: `AI_Agent_CLi/00_intro.html`
- Modify: `AI_Agent_CLi/04_workspace.md`
- Modify: `AI_Agent_CLi/04_workspace.html`
- Modify: `AI_Agent_CLi/04a_workflows.md`
- Modify: `AI_Agent_CLi/04a_workflows.html`
- Modify: `AI_Agent_CLi/06_lesson_plans.md`
- Modify: `AI_Agent_CLi/06_lesson_plans.html`
- Modify: `AI_Agent_CLi/06a_assessment.md`
- Modify: `AI_Agent_CLi/06a_assessment.html`
- Modify: `AI_Agent_CLi/07_agents_cli.html`
- Modify: `AI_Agent_CLi/09_cli_practice.html`

- [x] **Outcome:** 一般案例以同一會話自然語言串接，規則檔獨立說明，進階內容涵蓋會話管理與對話驅動的批次任務。

**Definition of Done:**
- 保留學科案例、來源、輸出檔名與驗收條件。
- 移除推薦操作中的 exec／-p 及啟動附帶 prompt；補充官方支援的 session、context、token 用量及模型選擇方式。
- 加入分工具的常用斜線指令速查與使用情境；逐項核對官方文件，明確標示在 CLI 會話內輸入。
- Markdown／HTML 同步；不改檔名與圖片。

**Verification Intent:**
- **Automated:** 靜態內容配對、連結及單次指令殘留掃描。
- **Representative:** 從啟動、摘要、追問到保存產物的教材閱讀演練；演練批次任務的對話流程；依官方文件核對會話、context、用量及模型操作。
- **High-risk:** Not applicable

### Task 2: 全課程一致性檢查與驗證紀錄
**Covers:** `REQ-TEACH-003`, `REQ-TEACH-009`, `REQ-TEACH-010`, `REQ-TEACH-011`
**Risk:** Standard
**Expected Files:**
- Create: `openspec/changes/archive/2026-10-31-prioritize-interactive-cli-teaching/verification-report.md`
- Modify: `AI_Agent_CLi/05_instructions.md`
- Modify: `AI_Agent_CLi/05_instructions.html`

一致性巡查發現單元五兩處推薦啟動附帶 prompt；依核准的全課程巡查範圍改為會話提示，保留原專案規則案例。

- [x] **Outcome:** 記錄跨章掃描、靜態檢查與代表性網頁驗證，無未解決的主線矛盾。

**Definition of Done:**
- 巡查全部 AI_Agent_CLi 教材與索引，確認進階操作也遵循互動主線；如其他頁需修正，先在本任務補記精確檔名及原因。
- 報告區分靜態／瀏覽驗證與未執行的真實 CLI 任務。

**Verification Intent:**
- **Automated:** 執行既有 check_course.py，核對配對內容與本機連結。
- **Representative:** 入門與長實作頁桌面、手機閱讀驗證。
- **High-risk:** Not applicable
