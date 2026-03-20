/* Path: Network/Git/v1/assets | Timestamp: 2026-03-19 20:12:48 | Version: b03 */
const pages = [
  { id: "index", title: "課程首頁", subtitle: "Git 版本管理與 GitHub 協作", href: "index_b03.html" },
  { id: "repo", title: "01 Repository 概念與原理", subtitle: "Repo 定義、ID 與物件資料庫", href: "pages/01-repo-concept.html" },
  { id: "init", title: "02 Git Init 指令", subtitle: "初始化倉庫與 .git 目錄結構", href: "pages/02-git-init.html" },
  { id: "commit", title: "03 Commit 提交", subtitle: "快照、SHA-1、歷史紀錄與回溯", href: "pages/03-commit.html" },
  { id: "github", title: "04 GitHub 協作平台", subtitle: "帳號設定、遠端 Repo 與協作功能", href: "pages/04-github-collaboration.html" },
  { id: "pr-issue-branch", title: "05 PR、Issue 與 Branch", subtitle: "分支開發、議題追蹤與合併流程", href: "pages/05-pr-issue-branch.html" },
  { id: "advanced", title: "06 進階操作", subtitle: "rebase、revert、reset 與 stash", href: "pages/06-advanced-usage.html" },
  { id: "github-advanced", title: "07 GitHub Pages 與 Actions", subtitle: "靜態網站部署與自動化工作流程", href: "pages/07-github-pages-actions_b03.html" },
  { id: "runner-advanced", title: "08 Runner 進階應用", subtitle: "Docker、Self-hosted、快取與除錯", href: "pages/08-runner-advanced.html" }
];

function withRoot(path) {
  const rawRoot = document.body.dataset.root || ".";
  const root = rawRoot.endsWith("/") ? rawRoot : `${rawRoot}/`;
  return `${root}${path}`;
}

function renderSidebar() {
  const nav = document.getElementById("site-nav");
  if (!nav) return;

  const currentPage = document.body.dataset.page;

  nav.className = "sidebar-nav";
  nav.innerHTML = pages
    .map((page) => {
      const active = page.id === currentPage ? "active" : "";
      return `
        <a class="sidebar-link ${active}" href="${withRoot(page.href)}">
          ${page.title}
          <small>${page.subtitle}</small>
        </a>
      `;
    })
    .join("");
}

function renderPageNav() {
  const host = document.getElementById("page-nav");
  if (!host) return;

  const currentPage = document.body.dataset.page;
  const currentIndex = pages.findIndex((page) => page.id === currentPage);
  if (currentIndex < 0) return;

  const previous = pages[currentIndex - 1];
  const next = pages[currentIndex + 1];
  host.className = "page-nav";

  host.innerHTML = `
    ${
      previous
        ? `<a href="${withRoot(previous.href)}"><span>上一頁</span>${previous.title}</a>`
        : `<div></div>`
    }
    ${
      next
        ? `<a href="${withRoot(next.href)}"><span>下一頁</span>${next.title}</a>`
        : `<div></div>`
    }
  `;
}

function initTabs() {
  document.querySelectorAll("[data-example]").forEach((example) => {
    const buttons = example.querySelectorAll("[data-tab-target]");
    const panels = example.querySelectorAll("[data-tab-panel]");

    buttons.forEach((button) => {
      button.addEventListener("click", () => {
        const target = button.dataset.tabTarget;

        buttons.forEach((item) => {
          const active = item === button;
          item.classList.toggle("is-active", active);
          item.setAttribute("aria-selected", String(active));
        });

        panels.forEach((panel) => {
          panel.classList.toggle("is-active", panel.dataset.tabPanel === target);
        });
      });
    });
  });
}

function initMermaid() {
  if (!window.mermaid) return;
  window.mermaid.initialize({
    startOnLoad: true,
    securityLevel: "loose",
    theme: "neutral",
    flowchart: {
      curve: "basis"
    }
  });
}

document.addEventListener("DOMContentLoaded", () => {
  renderSidebar();
  renderPageNav();
  initTabs();
  initMermaid();
});
