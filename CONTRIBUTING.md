# 📚 教學資料共享平台 — 貢獻指南

## 索引更新規則

本專案有兩份索引檔案，**每次新增或搬移 HTML 檔案時必須同步更新**：

| 檔案 | 用途 | 更新方式 |
|------|------|----------|
| `git_index.md` | Markdown 格式索引（依資料夾分組 + 表格） | 執行 `python3 update_index.py` 自動產生 |
| `index.html` | GitHub Pages 入口頁面（卡片式 UI） | **手動編輯**，將新檔案加入對應分類區塊 |

---

## 新增檔案的標準流程

### Step 1：加入檔案並確認追蹤

```bash
git add <新檔案或資料夾>
```

### Step 2：更新 `git_index.md`（自動）

```bash
python3 update_index.py
```

此腳本會掃描所有 `.html` 檔案，依資料夾分組，產生 Markdown 表格索引。

### Step 3：更新 `index.html`（手動）

開啟 `index.html`，找到對應的分類區塊（`<section id="...">`），新增一張卡片：

```html
<a class="card" href="資料夾/檔名.html">
  <span class="title">教材標題</span>
  <span class="meta">更新：YYYY-MM-DD</span>
</a>
```

**若新增的是全新資料夾**，需要：
1. 在導航列 `<nav class="nav-bar">` 中新增連結
2. 在 `<main>` 中新增完整的 `<section>` 區塊（參考現有區塊格式）
3. 更新對應 `<span class="count">` 的數量

### Step 4：提交並推送

```bash
git add git_index.md index.html <新檔案>
git commit -m "feat: 新增 XXX 教材"
git push
```

> ⚠️ **pre-push hook** 會自動檢查 `git_index.md` 是否為最新，並驗證 `index.html` 是否涵蓋所有 HTML 檔案所在的資料夾。若未通過將阻擋推送。

---

## 資料夾分類對照表

以下是 `index.html` 中的分類 ID 與對應的資料夾：

| Section ID | 資料夾 | 說明 |
|------------|--------|------|
| `#gemini` | `GeminiForDesignTeaching/` | Gemini AI 設計教學 |
| `#ai-intro` | `AI_intro/`, `AI_intro/History/` | AI 導論 |
| `#git` | `Git/`, `Git/v1/` | Git 版本管理 |
| `#b11` | `WEB_HTML_JAVACCRIPT/b11/` | 網頁開發技術 |
| `#cnn` | `CNN/` | CNN 卷積神經網路 |
| `#opencv` | `OpenCV/` | OpenCV 影像處理 |
| `#robots` | `Robots/` | 機器人程式設計 |
| `#engineering` | `104A_EngeeringDesign/` | 工程設計 |
| `#security` | `LLM_web_security_agent/` | LLM 網頁安全 |
| `#others` | `Coreldraw/`, `VideCoding/`, `TaigiSpeaking/`, `anaQ/`, `Youtube_sub/` | 其他資源 |

---

## 驗證指令

手動執行檢查（與 pre-push hook 相同邏輯）：

```bash
python3 update_index.py --check
```

此命令會：
1. 重新產生 `git_index.md` 並比對是否有差異
2. 檢查 `index.html` 是否涵蓋所有 HTML 檔案所在的資料夾
3. 列出 `index.html` 中缺少的檔案（若有）
