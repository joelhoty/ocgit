# Design：雙 CLI 教材改版

## Architecture
靜態 HTML 課程維持原有呈現，已有 Markdown 的章節以 Markdown 為內容來源、沿用原頁模板生成 HTML；HTML-only 頁面沿原結構修訂，不引入網站框架。新版集中 AI_Agent_CLi，原目錄只提供歷史 Markdown 與 HTML 入口相容頁。

## Components
| 章節 | 改版重點 |
|---|---|
| 前導章 | 完整 AI_working_env_b05，先教 Agent／Harness／Context，再選環境；雙 CLI 為主要路線，原有 Antigravity 資訊保留為經查核的選讀比較，不成為課程必備 |
| 單元一 | 提示結構、第一份教材與人工核對；採雙工具可用的教學情境 |
| 單元二 | 圖片提示與教材視覺；CLI 協助撰寫提示與管理素材，圖像產生標明外部工具 |
| 單元三 | 保留 NotebookLM 來源導向學習；說明與 CLI 檔案工作流程銜接 |
| 單元四及補充 | 教學專案、VS Code、Markdown、Mermaid、環境檢查與雙 CLI 操作 |
| 單元五 | AGENTS.md／CLAUDE.md 規則、作用範圍、驗證與模板 |
| 單元六及補充 | 指定來源讀檔、教案產出、格式轉換、匿名成績實作及驗收 |
| CLI 主教材與指南 | Agent/CLI 概念、雙工具命令對照與最新安裝；連往前導章避免互相矛盾 |
| 素養教材 | 保留研究論述與引用；只校訂與本課工具變更直接相關內容 |

## Interfaces
使用目標目錄內相對路徑；根索引連向 AI_Agent_CLi；舊 HTML 以相對新版 URL 導向並提供手動連結。保留可對應的舊 fragment，改名的標題以相容 anchor 承接或明示新版章節。
前導章來源引用缺少 AI_working_env.md；不捏造原檔，改為來源註記。SVG 已由使用者提供，原檔保留，驗證尺寸、對比與載入。

### 檔案對照
| 舊來源 | 新版目標 |
|---|---|
| `GeminiForDesignTeaching/AI_Agent_Cli_b13.html` | `AI_Agent_CLi/AI_Agent_Cli_b13.html` |
| `GeminiForDesignTeaching/Environment_Setup_Guide_b06.html` | `AI_Agent_CLi/Environment_Setup_Guide_b06.html` |
| `GeminiForDesignTeaching/Gemini_CLI_Tutorial_b02.html` | `AI_Agent_CLi/AI_CLI_Tutorial_b03.html` |
| `GeminiForDesignTeaching/index_content.html` | `AI_Agent_CLi/index_content.html` |
| `GeminiForDesignTeaching/literacy_b02.html` | `AI_Agent_CLi/literacy_b02.html` |
| `GeminiForDesignTeaching/literacy_chatgpt_revise_b06.html` | `AI_Agent_CLi/literacy_chatgpt_revise_b06.html` |
| `GeminiForDesignTeaching/literacy_research.html` | `AI_Agent_CLi/literacy_research.html` |
| `GeminiForDesignTeaching/literacy_research.md` | `AI_Agent_CLi/literacy_research.md` |
| `GeminiForDesignTeaching/unit01_first_ai_material_b02.html` | `AI_Agent_CLi/unit01_first_ai_material_b02.html` |
| `GeminiForDesignTeaching/unit01_first_ai_material_b02.md` | `AI_Agent_CLi/unit01_first_ai_material_b02.md` |
| `GeminiForDesignTeaching/unit02_ai_image_generation_b02.html` | `AI_Agent_CLi/unit02_ai_image_generation_b02.html` |
| `GeminiForDesignTeaching/unit02_ai_image_generation_b02.md` | `AI_Agent_CLi/unit02_ai_image_generation_b02.md` |
| `GeminiForDesignTeaching/unit03_notebooklm_b02.html` | `AI_Agent_CLi/unit03_notebooklm_b02.html` |
| `GeminiForDesignTeaching/unit03_notebooklm_b02.md` | `AI_Agent_CLi/unit03_notebooklm_b02.md` |
| `GeminiForDesignTeaching/unit04_local_ai_setup_b02.html` | `AI_Agent_CLi/unit04_local_ai_setup_b02.html` |
| `GeminiForDesignTeaching/unit04_local_ai_setup_b02.md` | `AI_Agent_CLi/unit04_local_ai_setup_b02.md` |
| `GeminiForDesignTeaching/unit04_supplement_additions.html` | `AI_Agent_CLi/unit04_supplement_additions.html` |
| `GeminiForDesignTeaching/unit04_supplement_additions.md` | `AI_Agent_CLi/unit04_supplement_additions.md` |
| `GeminiForDesignTeaching/unit05_gemini_md_customization_b01.html` | `AI_Agent_CLi/unit05_agent_instructions_b02.html` |
| `GeminiForDesignTeaching/unit05_gemini_md_customization_b01.md` | `AI_Agent_CLi/unit05_agent_instructions_b02.md` |
| `GeminiForDesignTeaching/unit06_practical_lesson_plan_b02.html` | `AI_Agent_CLi/unit06_practical_lesson_plan_b02.html` |
| `GeminiForDesignTeaching/unit06_practical_lesson_plan_b02.md` | `AI_Agent_CLi/unit06_practical_lesson_plan_b02.md` |
| `GeminiForDesignTeaching/unit06_supplement_additions.html` | `AI_Agent_CLi/unit06_supplement_additions.html` |
| `GeminiForDesignTeaching/unit06_supplement_additions.md` | `AI_Agent_CLi/unit06_supplement_additions.md` |

### 其他檔案
- 修改 `AI_Agent_CLi/AI_working_env_b05.md`；新增 `AI_Agent_CLi/AI_working_env_b05.html`。
- 使用 `AI_Agent_CLi/assets/agent_layers_b01.svg`，不覆寫原圖內容。
- 修改 `index.html`、`README.md`、`git_index.md`、`CONTRIBUTING.md` 的相關入口／分類。
- 新增本變更目錄 `sources.md`、`verification.md` 與驗證證據。

## Error Handling
外部來源無法查核時記錄限制並避免確定性主張；本地資源遺失需修復或移除失效引用。導向保留手動連結，不依賴 JavaScript；不進行永久 HTTP 伺服器設定。轉換流程不可吞掉程式碼、表格、引用與 Mermaid。

## Testing Strategy
掃描全部 HTML/Markdown 本地連結、anchor、圖片與舊產品操作殘留；配對核對標題及 code blocks；對照官方指令，不執行教材中的安裝或付費命令。桌面與手機檢查目錄、前導章、安裝表格、單元五、單元六、Mermaid 與 SVG；記錄不可驗證項目。需求 ID 綁定驗證報告，由 sos-verify 完成，通過後 sos-archive。

## Decision Log
| Decision | Options Considered | Chosen | Reason |
|---|---|---|---|
| 新目錄 | 原址改名／新目錄 | AI_Agent_CLi | 使用者指定且已有前導教材與 assets |
| 呈現 | 新框架／沿用模板 | 沿用模板 | 使用者要求保留設計 |
| 課程序列 | 重編／保留加前導 | 保留六單元加前導 | 延續漸進結構 |
| 舊網址 | 移除／保留原內容／導向 | 提案建議導向 | 既有書籤可進入新版，待核准 |
| 安裝指令 | 記憶／官方查核 | 官方文件與日期 | 避免沿用過時行為 |
