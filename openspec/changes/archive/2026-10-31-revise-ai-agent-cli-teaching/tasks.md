# Tasks：AI Agent CLI 教材改版

> For agentic workers: 使用 sos-apply 執行；依技能規定分派工作與審閱。文件與導航使用適當自動檢查，不為純文字改寫建立模仿內容的單元測試。

**Goal:** 完成保留原結構與設計的雙 CLI 教材，前導章前置，新版導航完整。
**Architecture:** 靜態 HTML 與既有 Markdown 配對；以 AI_Agent_CLi 為正式目錄，使用現有 assets。原 HTML 作為相容入口。

### Task 1: 官方來源與前導章

**Covers:** `REQ-TEACH-001`, `REQ-TEACH-003`, `REQ-TEACH-008`
**Risk:** Standard

**Expected Files:**
- `Modify: AI_Agent_CLi/AI_working_env_b05.md`
- `Create: AI_Agent_CLi/AI_working_env_b05.html`
- `Read: AI_Agent_CLi/assets/agent_layers_b01.svg`
- `Create: openspec/changes/revise-ai-agent-cli-teaching/sources.md`

- [x] **Outcome:** 完整前導教材成為雙 CLI 課程起點，概念、平台建議及來源已核對。

**Definition of Done:**
- 圖片與來源連結可用；雙 CLI 安裝依據、查核日期及原選讀路線清楚。

**Verification Intent:**
- **Automated:** 檢查該組檔案結構、相對連結、程式碼區塊與來源紀錄。
- **Representative:** 依學習者路線閱讀代表頁面，核對版面、步驟、預期產物與證據。
- **High-risk:** Not applicable

### Task 2: 雙 CLI 主指南與規則單元

**Covers:** `REQ-TEACH-002`, `REQ-TEACH-003`, `REQ-TEACH-004`, `REQ-TEACH-008`
**Risk:** Standard

**Expected Files:**
- `Create: AI_Agent_CLi/AI_Agent_Cli_b13.html`
- `Create: AI_Agent_CLi/Environment_Setup_Guide_b06.html`
- `Create: AI_Agent_CLi/AI_CLI_Tutorial_b03.html`
- `Create: AI_Agent_CLi/unit05_agent_instructions_b02.html`
- `Create: AI_Agent_CLi/unit05_agent_instructions_b02.md`

- [x] **Outcome:** CLI 主指南、環境指南、實戰指南與單元五提供一致且可追蹤的雙工具說明。

**Definition of Done:**
- 平台與命令介面分清；指引支援依最新官方條件寫明；模板與 HTML/Markdown 一致。

**Verification Intent:**
- **Automated:** 檢查該組檔案結構、相對連結、程式碼區塊與來源紀錄。
- **Representative:** 依學習者路線閱讀代表頁面，核對版面、步驟、預期產物與證據。
- **High-risk:** Not applicable

### Task 3: 漸進單元與補充教材

**Covers:** `REQ-TEACH-002`, `REQ-TEACH-005`, `REQ-TEACH-008`
**Risk:** Standard

**Expected Files:**
- `Create: AI_Agent_CLi/literacy_b02.html`
- `Create: AI_Agent_CLi/literacy_chatgpt_revise_b06.html`
- `Create: AI_Agent_CLi/literacy_research.html`
- `Create: AI_Agent_CLi/literacy_research.md`
- `Create: AI_Agent_CLi/unit01_first_ai_material_b02.html`
- `Create: AI_Agent_CLi/unit01_first_ai_material_b02.md`
- `Create: AI_Agent_CLi/unit02_ai_image_generation_b02.html`
- `Create: AI_Agent_CLi/unit02_ai_image_generation_b02.md`
- `Create: AI_Agent_CLi/unit03_notebooklm_b02.html`
- `Create: AI_Agent_CLi/unit03_notebooklm_b02.md`
- `Create: AI_Agent_CLi/unit04_local_ai_setup_b02.html`
- `Create: AI_Agent_CLi/unit04_local_ai_setup_b02.md`
- `Create: AI_Agent_CLi/unit04_supplement_additions.html`
- `Create: AI_Agent_CLi/unit04_supplement_additions.md`
- `Create: AI_Agent_CLi/unit06_practical_lesson_plan_b02.html`
- `Create: AI_Agent_CLi/unit06_practical_lesson_plan_b02.md`
- `Create: AI_Agent_CLi/unit06_supplement_additions.html`
- `Create: AI_Agent_CLi/unit06_supplement_additions.md`

- [x] **Outcome:** 所有漸進單元、補充與素養頁面納入新版並維持完整教學結構。

**Definition of Done:**
- 六單元教學目的保留；兩工具路線的輸入、產物與驗收清楚；圖片和 NotebookLM 能力描述正確。

**Verification Intent:**
- **Automated:** 檢查該組檔案結構、相對連結、程式碼區塊與來源紀錄。
- **Representative:** 依學習者路線閱讀代表頁面，核對版面、步驟、預期產物與證據。
- **High-risk:** Not applicable

### Task 4: 新版索引與舊入口相容

**Covers:** `REQ-TEACH-006`, `REQ-TEACH-007`
**Risk:** High

**Expected Files:**
- `Create: AI_Agent_CLi/index_content.html`
- `Modify: GeminiForDesignTeaching/AI_Agent_Cli_b13.html`
- `Modify: GeminiForDesignTeaching/Environment_Setup_Guide_b06.html`
- `Modify: GeminiForDesignTeaching/Gemini_CLI_Tutorial_b02.html`
- `Modify: GeminiForDesignTeaching/index_content.html`
- `Modify: GeminiForDesignTeaching/literacy_b02.html`
- `Modify: GeminiForDesignTeaching/literacy_chatgpt_revise_b06.html`
- `Modify: GeminiForDesignTeaching/literacy_research.html`
- `Modify: GeminiForDesignTeaching/unit01_first_ai_material_b02.html`
- `Modify: GeminiForDesignTeaching/unit02_ai_image_generation_b02.html`
- `Modify: GeminiForDesignTeaching/unit03_notebooklm_b02.html`
- `Modify: GeminiForDesignTeaching/unit04_local_ai_setup_b02.html`
- `Modify: GeminiForDesignTeaching/unit04_supplement_additions.html`
- `Modify: GeminiForDesignTeaching/unit05_gemini_md_customization_b01.html`
- `Modify: GeminiForDesignTeaching/unit06_practical_lesson_plan_b02.html`
- `Modify: GeminiForDesignTeaching/unit06_supplement_additions.html`
- `Modify: index.html`
- `Modify: README.md`
- `Modify: git_index.md`
- `Modify: CONTRIBUTING.md`

- [x] **Outcome:** 新版內部導航統一，根目錄入口與舊網址均可到達新版對應教材。
- [x] **High-risk safety gate:** 記錄所有舊頁至新版的對照，先確認目標存在再替換入口；保留 Git 原版與使用者未提交內容。
- [x] **High-risk failure-path gate:** 驗證 JavaScript 停用、舊 fragment 與無自動跳轉情況仍有正確可用的新版連結。

**Definition of Done:**
- 所有目標存在；舊頁提供手動連結；保留歷史 Markdown 與原有無關修改。

**Verification Intent:**
- **Automated:** 遍歷所有新舊本地連結與 anchor，確認無斷鏈。
- **Representative:** 以瀏覽器開啟原課程入口、單元五舊網址及新版手機目錄。
- **High-risk:** 對照舊頁清單、驗證目標存在與保留修改；模擬不自動導向的手動導航。

### Task 5: 整體驗證與封存

**Covers:** `REQ-TEACH-001`, `REQ-TEACH-002`, `REQ-TEACH-003`, `REQ-TEACH-004`, `REQ-TEACH-005`, `REQ-TEACH-006`, `REQ-TEACH-007`, `REQ-TEACH-008`
**Risk:** Standard

**Expected Files:**
- `Create: openspec/changes/revise-ai-agent-cli-teaching/verification.md`
- `Create: openspec/changes/revise-ai-agent-cli-teaching/evidence/`

- [x] **Outcome:** 完成具需求 ID 的驗證報告，通過 sos-verify 後依 sos-archive 同步規格與封存。

**Definition of Done:**
- 來源、結構、連結、視覺證據完整；未實測的安裝與帳號功能明確記錄，不誤報測試成功。

**Verification Intent:**
- **Automated:** 檢查該組檔案結構、相對連結、程式碼區塊與來源紀錄。
- **Representative:** 依學習者路線閱讀代表頁面，核對版面、步驟、預期產物與證據。
- **High-risk:** Not applicable

