# Delta for Teaching

## ADDED Requirements

### Requirement: REQ-TEACH-012 — 前導章依學習前置條件排序
前導章 MUST 依概念、最小環境、專案準備、CLI登入、首次對話任務、會話管理、維護與延伸實作排列。首次操作使用的來源檔與環境 MUST 已先介紹建立方式；技術細節與歷史紀錄 SHOULD 集中附錄，不中斷主線。

#### Scenario: 基礎讀者順讀
- GIVEN 學習者尚未建立工作環境
- WHEN 依所選平台完成主線至第一次任務
- THEN 可連續完成讀檔、追問、保存與驗收，不需往後尋找尚未建立的筆記或資料夾。

#### Scenario: Python延伸讀者
- GIVEN 已完成基礎對話任務
- WHEN 選讀Python實作
- THEN 先完成uv與直譯器準備，再操作資料、程式與驗收，不被Node選修安裝打斷。

### Requirement: REQ-TEACH-013 — 前導章重排內容與連結相容
教材 MUST 保留原有效案例、程式、圖形、引用、驗收與歷史標籤，合併重複敘述後以對照紀錄追蹤。Markdown與HTML MUST 同步，原檔名及已存在的錨點仍能到達相應主題。

#### Scenario: 舊主題連結
- GIVEN 原有指向前導章小節的連結
- WHEN 開啟連結（包含停用JavaScript）
- THEN 仍到達相應主題位置，目錄與新章節一致。

#### Scenario: 完整教材保留
- GIVEN 原教材內容清單
- WHEN 對照新版主文與附錄
- THEN 有效實作及歷史資料均有去向，兩種格式一致且圖片正常。
