/* Path: Network/WEB Service/Content/b11/assets | Timestamp: 2026-03-19 20:18:24 | Version: b11 */
const pages = [
  { id: "index", title: "課程首頁", subtitle: "從基礎到框架的學習地圖", href: "index_b11.html" },
  { id: "tcp-ip", title: "01 TCP/IP 與 Client-Server", subtitle: "IP、Port、Socket、Daemon", href: "pages/01-tcp-ip-foundation_b11.html" },
  { id: "lifecycle", title: "02 Web 服務流程", subtitle: "網址輸入到頁面呈現的完整旅程", href: "pages/02-web-service-lifecycle_b11.html" },
  { id: "http", title: "03 HTTP 協定", subtitle: "Request、Response、DevTools、curl、HTTPS", href: "pages/03-http-protocol_b11.html" },
  { id: "html-css", title: "04 HTML 與 CSS 基礎", subtitle: "先學 5 個標籤，再展開 CSS 版型", href: "pages/04-html-css-foundation_b11.html" },
  { id: "js-dom", title: "05 JavaScript、DOM 與 CSS", subtitle: "HTML 原始碼、DOM 樹與互動實驗", href: "pages/05-javascript-dom-css_b11.html" },
  { id: "server", title: "06 Web Server 範例", subtitle: "初學者與傳統管理者的雙路徑理解", href: "pages/06-web-server-examples_b11.html" },
  { id: "frameworks", title: "07 現代框架", subtitle: "不用框架會卡在哪與分層理解", href: "pages/07-modern-frameworks_b11.html" },
  { id: "js-architecture", title: "08 JavaScript 全貌", subtitle: "從發展歷史到前後端整體架構", href: "pages/08-javascript-fullstack-architecture_b11.html" },
  { id: "jquery-guide", title: "09 jQuery 詳解", subtitle: "選取器、事件、AJAX 與經典寫法", href: "pages/09-jquery-detailed-guide_b11.html" },
  { id: "ajax-guide", title: "10 AJAX 原理", subtitle: "非同步請求、局部更新與運作流程", href: "pages/10-ajax-fundamentals_b11.html" },
  { id: "stack-case", title: "11 實務技術堆疊", subtitle: "解讀 Laravel、Vue、SEO 與 AI 可讀內容", href: "pages/11-practical-stack-case_b11.html" }
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
