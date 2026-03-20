# 📚 OC 教學資料共享平台

> **Open Course Learning Hub** — 以 GitHub Pages 為基礎的多元課程開放學習資源

🌐 **線上瀏覽：** [https://joelhoty.github.io/ocgit/](https://joelhoty.github.io/ocgit/)

---

## 關於本專案

本專案由 **joel.tw@gmail.com** 提供教學構想與課程規劃，並與多種 AI CLI 工具（GitHub Copilot CLI、Gemini CLI 等）共同設計、撰寫與維護。所有教材內容皆以 HTML 靜態頁面呈現，透過 GitHub Pages 自動部署，提供任何人隨時隨地存取的開放學習環境。

### 🤝 人機協作模式

| 角色 | 負責內容 |
|------|----------|
| 👨‍🏫 **Joel**（joel.tw@gmail.com） | 課程規劃、教學目標設定、內容審核、主題發想 |
| 🤖 **AI CLI 工具** | 教材內容生成、HTML 頁面建構、程式碼範例、索引自動化 |

---

## 📂 課程分類總覽

本平台目前收錄 **101 份 HTML 教材**，涵蓋以下主題：

### 🎨 Gemini AI 設計教學
`GeminiForDesignTeaching/` — 15 篇

以 Google Gemini 為核心的設計教學系列，涵蓋 AI 圖像生成、NotebookLM 應用、本地 AI 環境建置、Markdown 客製化、實務教案設計，以及 AI 素養探討。

### 🤖 AI 導論
`AI_intro/` — 15 篇

AI 基礎概念與完整的 AI 發展史系列（9 章），從早期基礎、古典時期、AI 寒冬，到深度學習與生成式 AI 的全面回顧。

### 🔀 Git 版本管理與 GitHub 協作
`Git/` — 12 篇

從 Repository 概念、Git 初始化、Commit 提交，到 GitHub 協作、PR/Issue/Branch、GitHub Pages & Actions 的完整教學。

### 🌐 網頁開發技術
`WEB_HTML_JAVACCRIPT/b11/` — 12 篇

TCP/IP 基礎、HTTP 協定、HTML/CSS、JavaScript DOM、Web Server、現代前端框架、全端架構、jQuery、AJAX 等系統性網頁開發教材。

### 🧠 CNN 卷積神經網路
`CNN/` — 7 篇

CNN 入門介紹到進階應用，包含多部分拆解教學與完整實作範例。

### 👁️ OpenCV 影像處理
`OpenCV/` — 8 篇

影像分類任務系列（Task 1-4）、物件偵測、Kernel 與形態學運算等電腦視覺教材。

### 🤖 機器人程式設計
`Robots/` — 5 篇

LEGO Mindstorm（超音波感測器、顏色感測器）與 Arduino 馬達控制教學。

### ⚡ 工程設計（Arduino / NodeMCU）
`104A_EngeeringDesign/` — 3 篇

Arduino IDE 入門到進階，以及 NodeMCU-32S IoT 開發入門。

### 🔒 LLM 網頁安全代理
`LLM_web_security_agent/` — 7 篇

網頁安全基礎教學與 LLM 安全代理系統提案（架構、工作流程、互動模式）。

### 📦 其他資源
- `Coreldraw/` — CorelDraw 形狀繪製（1 篇）
- `VideCoding/` — Vibe Coding Python 教學（1 篇）
- `TaigiSpeaking/` — 台語語音應用（1 篇）
- `anaQ/` — 問卷分析互動 Dashboard（6 篇）
- `Youtube_sub/` — YouTube 字幕與 WhisperUI 計畫（2 篇）

---

## 🏗️ 專案結構

```
OCgithub/
├── index.html                  # 🏠 入口首頁（GitHub Pages 首頁）
├── git_index.md                # 📋 Markdown 格式完整索引
├── update_index.py             # 🔧 自動化索引產生腳本
├── CONTRIBUTING.md             # 📝 貢獻指南
├── README.md                   # 📖 本文件
│
├── GeminiForDesignTeaching/    # 🎨 Gemini AI 設計教學
├── AI_intro/                   # 🤖 AI 導論
│   └── History/                #     AI 發展史系列
├── Git/                        # 🔀 Git 版本管理
│   └── v1/                     #     V1 版教材
├── WEB_HTML_JAVACCRIPT/        # 🌐 網頁開發技術
│   └── b11/                    #     B11 課程系列
├── CNN/                        # 🧠 CNN 深度學習
├── OpenCV/                     # 👁️ 影像處理
├── Robots/                     # 🤖 機器人
├── 104A_EngeeringDesign/       # ⚡ 工程設計
├── LLM_web_security_agent/     # 🔒 網頁安全
├── Coreldraw/                  # 🎨 CorelDraw
├── VideCoding/                 # 💻 Vibe Coding
├── TaigiSpeaking/              # 🗣️ 台語語音
├── anaQ/                       # 📊 問卷分析
├── Youtube_sub/                # 🎬 YouTube 字幕
│
└── .github/workflows/          # ⚙️ GitHub Actions（自動部署）
```

---

## 🚀 部署方式

本專案使用 **GitHub Pages + GitHub Actions** 自動部署：

1. 推送至 `main` 分支
2. GitHub Actions 自動觸發 `static.yml` workflow
3. 靜態內容部署至 [https://joelhoty.github.io/ocgit/](https://joelhoty.github.io/ocgit/)

---

## 📝 更新紀錄

| 日期 | 說明 |
|------|------|
| 2026-03-20 | 建立根目錄 `index.html` 入口頁面，整合 11 大分類約 90 份教材 |
| 2026-03-20 | 加入未追蹤資料夾（Coreldraw、Git、b11），共 34 檔 |
| 2026-03-20 | 重構 `b11/` → `WEB_HTML_JAVACCRIPT/b11/`，重建所有索引 |
| 2026-03-19 | 新增 Git 版本管理完整課程（8 單元） |
| 2026-03-19 | 新增網頁開發技術教材（11 篇） |
| 2026-03-01 | 新增 CorelDraw 形狀繪製教材 |
| 2026-02-23 | 新增 AI 基礎概念教材 |
| 2025-12-30 | 新增 Gemini CLI 教學與課程索引 |
| 2025-12-15 | 新增 CNN 教學系列與 NodeMCU 教材 |
| 2025-12-14 | 新增 Vibe Coding Python 教學 |

---

## 📄 授權

本專案教學資料由 **joel.tw@gmail.com** 與 AI 工具共同創作，僅供教學用途。

---

<p align="center">
  <sub>由 <strong>Joel</strong> 發想 ✕ <strong>AI CLI</strong> 共同打造 — 持續更新中 🚧</sub>
</p>
