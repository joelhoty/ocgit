# Tasks: 前導章閱讀順序重整

> Use sos-apply after approval; documentation-adapted verification.

**Goal:** 前導章可按前置依賴連續閱讀與操作，詳細內容保留於附錄。
**Architecture:** 保留單一Markdown／HTML，按內容對照重排並更新錨點與索引。

### Task 1: 重排與銜接完整教材
**Covers:** `REQ-TEACH-012`, `REQ-TEACH-013`
**Risk:** Standard
**Expected Files:**
- Modify: `AI_Agent_CLi/00_intro.md`
- Modify: `AI_Agent_CLi/00_intro.html`
- Modify: `AI_Agent_CLi/index.html`
- Create: `openspec/changes/archive/2026-10-31-reorder-agent-introduction/content-map.md`

- [x] **Outcome:** 主線依前置條件連續排列，細節進附錄，實作與來源完整保留。

**Definition of Done:**
- 依proposed-outline逐節對照，修正所有主文節號與閱讀路線。
- 首次任務在準備筆記與專案後；Python實作不插入Node安裝。
- 互動CLI與斜線指令教學保持，Markdown／HTML同步。

**Verification Intent:**
- **Automated:** 全課程配對、連結與圖檔檢查。
- **Representative:** 以Windows與macOS基礎讀者順讀，核對首次任務與Python前置條件。
- **High-risk:** Not applicable

### Task 2: 驗證重排與舊錨點相容
**Covers:** `REQ-TEACH-012`, `REQ-TEACH-013`
**Risk:** High
**Expected Files:**
- Modify: `AI_Agent_CLi/00_intro.html`
- Create: `openspec/changes/archive/2026-10-31-reorder-agent-introduction/verification-report.md`
- Create: `openspec/changes/archive/2026-10-31-reorder-agent-introduction/anchor-map.json`

- [x] **Outcome:** 全部舊錨點仍對應原主題，桌面與手機閱讀及教材內容驗證通過。
- [x] **High-risk safety gate:** 以重排前HTML擷取完整ID清單，建立每個舊錨點的主題映射，不刪除舊入口。
- [x] **High-risk failure-path gate:** 停用JavaScript驗證舊深層連結仍可到達對應主題；檢查遺漏或重複ID會被驗證拒絕。

**Definition of Done:**
- 所有已存在錨點有唯一目的位置，尤其跨章已引用的510。
- 內容對照、連結、配對、視覺與前置依賴審查無阻擋問題。

**Verification Intent:**
- **Automated:** 全部舊ID與新映射逐一驗證，重複／缺失檢查，全課程靜態回歸。
- **Representative:** 正常主線、寬表、長程式、附錄的桌面／手機閱讀。
- **High-risk:** 重排前完整ID備份及全量映射；停用JS驗證相容位置並拒絕缺失／重複映射。
