# 前導章內容搬移對照

Base: f7a957f。完整109個原標題的對應見 section-map.json；原稿保存在 inputs/。所有原小節都有去向，合併處保留實作內容與來源。

| 原標題 | 新主題錨點 |
|---|---|
| 前導章：讓 AI Agent 成為個人工作與學習助理 | `intro` |
| 0. 使用方式與學習目標 | `learning-route` |
| 0.1 完成後能做到什麼 | `learning-outcomes` |
| 0.2 課程安排與交付物 | `course-plan` |
| 0.3 指令閱讀約定 | `input-conventions` |
| 1. 為什麼需要一個 AI 工作環境（Why） | `agent-basics` |
| 1.1 從問答到完成任務 | `from-chat-to-work` |
| 1.2 環境建置解決的四個問題 | `environment-purpose` |
| 2. LLM 與 Agent 的六層關係（What） | `agent-basics` |
| 2.1 引用的分層圖 | `agent-layer-diagram` |
| 2.2 各層如何對應本課任務 | `layers-in-practice` |
| 2.3 模型、CLI 與執行環境有何不同 | `model-cli-environment` |
| 2.4 Prompt、Context、Tools、Skills 與 MCP | `context-tools-skills` |
| 2.5 軟限制與硬限制 | `guidance-and-permissions` |
| 2.6 Agent 迴圈：圖中的各層如何合作 | `agent-loop` |
| 2.7 Workflow 與 Agent：誰決定下一步 | `workflow-and-agent` |
| 3. 工具地圖與安裝需求 | `minimal-environment` |
| 3.1 每個工具負責什麼 | `tool-roles` |
| 3.2 CLI 還需要 Node.js 嗎？ | `appendix-installation` |
| 3.2.1 四種安裝方式比較 | `installation-methods` |
| 3.2.2 建議與結論 | `installation-decisions` |
| 3.2.3 先分清楚四種檔案與工具 | `binary-script-manager` |
| 3.2.4 「原生版」「standalone」「npm 版」指的是什麼 | `distribution-terms` |
| 3.2.5 安裝時、執行時、任務時：三個時間點各需要什麼 | `dependency-stages` |
| 3.2.6 三款 CLI 逐一對照 | `cli-dependency-comparison` |
| 3.2.7 CLI 改用 Rust 撰寫，就不需要 Node.js 了嗎？ | `implementation-language` |
| 3.2.8 官方安裝指令一覽 | `alternative-installation` |
| 3.3 選讀比較：Antigravity CLI（agy） | `antigravity-overview` |
| 3.4 作業系統、帳號與資源 | `platform-account-requirements` |
| 4. Windows 基礎環境安裝（How） | `workspace-setup` |
| 4.1 安裝順序 | `setup-order` |
| 4.2 安裝 VS Code | `windows-vscode` |
| 4.3 安裝 PowerShell 7 | `windows-powershell` |
| 4.4 安裝 Git | `windows-git` |
| 4.5 先學會五個終端機操作 | `terminal-basics` |
| 5. 安裝並啟動一款 Agent CLI | `cli-installation` |
| 5.1 選擇路線 | `installation-choice` |
| 5.2 路線 A：Claude Code | `install-claude` |
| 5.3 路線 B：Codex CLI | `install-codex` |
| 5.4 選讀路線 C：Antigravity CLI | `install-antigravity` |
| 5.5 選讀：舊 gemini 指令遷移到 agy | `gemini-migration` |
| 5.6 第一次對話的共同驗證 | `verify-first-session` |
| 5.7 記錄安裝方式與更新方式 | `update-uninstall` |
| 5.8 盤點既有安裝：這台電腦的 CLI 從哪裡來？ | `installation-inventory` |
| 5.9 啟動後，以自然語言完成任務 | `read-followup-save` |
| 5.10 常用會話內指令速查 | `slash-commands` |
| 5.11 進階操作：管理 session、context 與用量 | `session-context-usage` |
| 6. 用資料夾與 Git 管理專案 | `workspace-setup` |
| 6.1 建立一致的專案結構 | `project-folders` |
| 6.2 撰寫 README | `project-readme` |
| 6.3 設定 `.gitignore` | `gitignore` |
| 6.4 建立第一次 commit | `first-checkpoint` |
| 6.5 理解三個位置 | `git-states` |
| 6.6 撤回與回復的練習 | `git-recovery` |
| 6.7 Git、版本後綴與備份的分工 | `versions-and-backups` |
| 7. AGENTS.md 與第一個 AI 學習任務 | `first-task` |
| 7.1 專案規則要能直接執行 | `project-instructions` |
| 7.2 各工具是否會讀取 AGENTS.md | `instruction-loading` |
| 7.3 確認規則真的生效 | `verify-instructions` |
| 7.4 準備來源筆記 | `source-notes` |
| 7.5 第一個完整提示 | `complete-review` |
| 7.6 驗收，而不是只接受「完成了」 | `verify-deliverables` |
| 8. Python 與 uv：建立可重現的執行環境 | `python-practice` |
| 8.1 四個概念先分清楚 | `python-environment-concepts` |
| 8.2 安裝 uv，再由 uv 管理 Python | `install-python-uv` |
| 8.3 在既有專案加入 Python 設定 | `initialize-python` |
| 8.4 哪些檔案應該保存 | `python-project-files` |
| 8.5 安裝與移除套件 | `python-packages` |
| 8.6 是否需要手動 activate | `python-activation` |
| 9. 可執行實作：學習時間統計 | `python-practice` |
| 9.1 Node.js 的選修安裝 | `node-installation` |
| 9.2 在 VS Code 選對 Python | `select-python-interpreter` |
| 9.3 準備資料 | `study-data` |
| 9.4 先讀偽代碼 | `study-pseudocode` |
| 9.5 完整程式 | `study-program` |
| 9.6 執行與核對 | `run-study-report` |
| 9.7 用除錯器理解執行過程 | `debug-study-program` |
| 9.8 讓 AI 做一個有邊界的修改 | `agent-bounded-change` |
| 10. macOS 操作差異 | `workspace-setup` |
| 10.1 不必為了本課改用 PowerShell | `terminal-basics` |
| 10.2 最小安裝步驟 | `macos-setup` |
| 10.3 Python 路線 | `install-python-uv` |
| 11. 常見問題與解決方案（Q&A） | `reliable-work` |
| 11.1 先判斷錯誤在哪一層 | `diagnose-layer` |
| 11.2 問題對照表 | `troubleshooting-table` |
| 11.3 能直接貼給 AI 的除錯格式 | `debugging-prompt` |
| 11.4 費用與額度怎麼看 | `cost-and-quota` |
| 12. 實作練習與評量（Practice） | `practice-summary` |
| 12.1 練習 A：把任務放回六層模型 | `exercise-layers` |
| 12.2 練習 B：最小可用環境 | `exercise-minimal-setup` |
| 12.3 練習 C：資料錯誤能否被發現 | `exercise-data-errors` |
| 12.4 綜合任務：一週學習助理 | `weekly-assistant` |
| 12.5 評分規準 | `assessment-rubric` |
| 13. 學習總結（Summary） | `practice-summary` |
| 13.1 應獲得的知識 | `knowledge-summary` |
| 13.2 應獲得的技能 | `skills-checklist` |
| 13.3 每次工作的收尾清單 | `work-closeout` |
| 14. 延伸問題與應用（Extension & Application） | `practice-summary` |
| 14.1 反思性問題 | `reflection-questions` |
| 14.2 真實應用情境 | `application-scenarios` |
| 14.3 跨領域連結 | `cross-disciplinary` |
| 14.4 進階探索 | `further-exploration` |
| 15. 官方文件與維護方式 | `appendix-history` |
| 15.1 主要來源索引 | `official-sources` |
| 15.2 授課前重新確認 | `teaching-maintenance` |
| 15.3 版本記錄 | `version-history` |
| 15.4 原 b05 歷史驗證紀錄與本次限制 | `historical-verification` |
| Jev 合規檢查紀錄（原稿歷史紀錄） | `historical-jev-compliance` |
| Jev 圖表選型檢查紀錄（原稿歷史紀錄） | `historical-jev-diagrams` |

## 實質整併說明

- 首次任務先準備來源與指引，再建立 Git 檢查點；三重點摘要及自我檢核草稿接著擴成原四重點、三題測驗與五分鐘練習，保留 notes_summary.md 與 review_bXX.md 兩個里程碑。
- 原本三次建立資料夾與重複原生安裝指令集中到共同專案／各工具平台段落；替代方式與部署差異留在附錄 A。
- 原 macOS 章拆到基礎環境、CLI 安裝、uv 安裝及 Homebrew 附錄；各處接回同一主線。
- 完整 Python 程式與 CSV／偽代碼不改邏輯；Node 安裝移至附錄 A，rich 與activate練習移到統計實作後。
- 教師筆電盤點、版本與Jev紀錄保留於附錄 C，保留原日期且宣告歷史節號不代表新版。
- 主文交叉引用改為語意錨點；歷史敘述保留當時原稿的節號。
