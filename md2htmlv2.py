#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Markdown to HTML 轉換器 (支援 Mermaid 圖表與多種 CSS 主題)

程式功能：
    將 Markdown 文件轉換為美觀的 HTML 頁面，並支援：
    - Mermaid 流程圖、時序圖等圖表自動渲染
    - 16 種流行的 CSS 框架主題（亮色/深色）
    - 代碼語法高亮（基於 Highlight.js）
    - 響應式設計，適配移動設備
    - 深色主題優化的對比度配色

主要特色：
    - 極簡使用：單一命令即可轉換
    - 主題豐富：支援 GitHub、Bootstrap、Water.css、Pico.css 等 16 種主題
    - 深色友好：所有深色主題均已優化代碼塊和引用區域的對比度
    - Mermaid 支援：自動識別並渲染 Mermaid 圖表
    - 預設主題：Water.css Dark（可自由切換）

版本資訊：
    版本：v2.0
    更新日期：2025-10-16
    Python 版本：3.6+

支援的主題：
    亮色主題：
        - github: GitHub Markdown 風格
        - bootstrap: Bootstrap 5 現代化設計
        - water: Water.css 極簡風格
        - pico: Pico.css 語義化設計
        - mvp: MVP.css 最小可行產品風格
        - sakura: Sakura 日式風格
        - latex: LaTeX.css 學術論文風格
        - tufte: Tufte CSS 經典排版
        - modest: Modest 簡約風格
        - retro: 98.css 復古 Windows 98 風格
        - nes: NES.css 像素風格

    深色主題（已優化對比度）：
        - water-dark: Water.css Dark（預設主題）
        - github-dark: GitHub Dark
        - bootstrap-dark: Bootstrap Dark
        - pico-dark: Pico.css Dark
        - sakura-dark: Sakura Dark

使用範例：
    # 使用預設主題 (water-dark)
    python3 md2htmlv2.py input.md output.html

    # 指定主題
    python3 md2htmlv2.py input.md output.html github-dark

    # 交互式模式
    python3 md2htmlv2.py interactive

    # 列出所有主題
    python3 md2htmlv2.py list

    # 生成主題展示
    python3 md2htmlv2.py demo

依賴套件：
    - markdown: Markdown 解析器
    - Python 標準庫: re, pathlib, typing, json

作者：Claude Code
最後修改：2025-10-16
"""

import markdown
import re
from pathlib import Path
from typing import Optional, Dict, Any

class MermaidMarkdownConverter:
    """
    Markdown to HTML 轉換器主類

    功能：
        - 將 Markdown 文件轉換為完整的 HTML 頁面
        - 支援 16 種流行的 CSS 框架主題
        - 自動處理 Mermaid 圖表代碼塊
        - 提供代碼語法高亮
        - 自動適配深色/亮色主題的 Mermaid 配色

    屬性：
        HTML_THEMES (dict): 所有可用的 HTML 主題配置
        MERMAID_THEMES (dict): 所有可用的 Mermaid 主題
        html_theme (dict): 當前選擇的 HTML 主題配置
        mermaid_theme (str): 當前選擇的 Mermaid 主題名稱
        container_width (int): 容器寬度（像素）
        mermaid_config (dict): Mermaid 自定義配置
        extra_css (str): 額外的自定義 CSS

    使用範例：
        >>> converter = MermaidMarkdownConverter(html_theme='water-dark')
        >>> converter.convert_file('input.md', 'output.html')
    """

    # 流行的CSS框架主題（通過CDN）
    HTML_THEMES = {
        'github': {
            'name': 'GitHub Markdown',
            'css': 'https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/5.2.0/github-markdown.min.css',
            'body_class': 'markdown-body',
            'is_dark': False,
            'highlight_css': 'https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.8.0/styles/github.min.css',
            'custom_css': '''
                body { 
                    background: #ffffff;
                    padding: 20px;
                }
                .markdown-body {
                    box-sizing: border-box;
                    min-width: 200px;
                    max-width: 980px;
                    margin: 0 auto;
                    padding: 45px;
                }
            '''
        },
        'github-dark': {
            'name': 'GitHub Dark',
            'css': 'https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/5.2.0/github-markdown-dark.min.css',
            'body_class': 'markdown-body',
            'is_dark': True,
            'highlight_css': 'https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.8.0/styles/github-dark.min.css',
            'custom_css': '''
                body {
                    background: #0d1117;
                    padding: 20px;
                }
                .markdown-body {
                    box-sizing: border-box;
                    min-width: 200px;
                    max-width: 980px;
                    margin: 0 auto;
                    padding: 45px;
                    background: #0d1117;
                    color: #c9d1d9;
                }
                /* 提升代码块对比度 */
                .markdown-body pre {
                    background: #161b22 !important;
                    border: 1px solid #30363d;
                }
                .markdown-body pre code {
                    background: #161b22 !important;
                    color: #e6edf3;
                }
                .markdown-body code:not(pre code) {
                    background: #343941 !important;
                    color: #e6edf3;
                    padding: 0.2em 0.4em;
                    border-radius: 6px;
                }
                /* 提升引用块对比度 */
                .markdown-body blockquote {
                    background: #161b22;
                    border-left: 4px solid #58a6ff;
                    padding: 12px 16px;
                    color: #c9d1d9;
                }
                /* 表格对比度 */
                .markdown-body table tr {
                    background: #0d1117;
                    border-top: 1px solid #30363d;
                }
                .markdown-body table tr:nth-child(2n) {
                    background: #161b22;
                }
                .markdown-body table th,
                .markdown-body table td {
                    border: 1px solid #30363d;
                }
            '''
        },
        'bootstrap': {
            'name': 'Bootstrap 5',
            'css': 'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css',
            'body_class': '',
            'is_dark': False,
            'highlight_css': 'https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.8.0/styles/stackoverflow-light.min.css',
            'custom_css': '''
                body {
                    background: #f8f9fa;
                    padding: 20px;
                }
                .container {
                    background: white;
                    padding: 40px;
                    border-radius: 8px;
                    box-shadow: 0 0 10px rgba(0,0,0,0.1);
                }
            '''
        },
        'bootstrap-dark': {
            'name': 'Bootstrap Dark',
            'css': 'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css',
            'body_class': '',
            'is_dark': True,
            'highlight_css': 'https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.8.0/styles/stackoverflow-dark.min.css',
            'custom_css': '''
                body {
                    background: #212529;
                    color: #dee2e6;
                    padding: 20px;
                }
                .container {
                    background: #343a40;
                    padding: 40px;
                    border-radius: 8px;
                    box-shadow: 0 0 10px rgba(0,0,0,0.3);
                }
                h1, h2, h3, h4, h5, h6 {
                    color: #f8f9fa;
                }
                /* 提升代码块对比度 */
                pre {
                    background: #1e2125 !important;
                    border: 1px solid #495057;
                }
                pre code {
                    background: #1e2125 !important;
                    color: #e9ecef;
                }
                code:not(pre code) {
                    background: #495057 !important;
                    color: #f8f9fa;
                    padding: .2em .4em;
                    border-radius: 6px;
                }
                /* 提升引用块对比度 */
                blockquote {
                    background: #2b3035;
                    border-left: 4px solid #0d6efd;
                    padding: 12px 20px;
                    margin: 1em 0;
                    color: #dee2e6;
                }
                /* 表格对比度 */
                table {
                    color: #dee2e6;
                }
                table thead {
                    background: #2b3035;
                }
                table tbody tr:nth-child(odd) {
                    background: #343a40;
                }
                table tbody tr:nth-child(even) {
                    background: #2b3035;
                }
                table td, table th {
                    border-color: #495057;
                }
            '''
        },
        'water': {
            'name': 'Water.css Light',
            'css': 'https://cdn.jsdelivr.net/npm/water.css@2/out/water.min.css',
            'body_class': '',
            'is_dark': False,
            'highlight_css': 'https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.8.0/styles/default.min.css',
            'custom_css': '''
                body {
                    max-width: 900px;
                    margin: 0 auto;
                    padding: 20px;
                }
            '''
        },
        'water-dark': {
            'name': 'Water.css Dark',
            'css': 'https://cdn.jsdelivr.net/npm/water.css@2/out/dark.min.css',
            'body_class': '',
            'is_dark': True,
            'highlight_css': 'https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.8.0/styles/base16/darcula.min.css',
            'custom_css': '''
                body {
                    max-width: 900px;
                    margin: 0 auto;
                    padding: 20px;
                }
                /* 提升代码块对比度 */
                pre {
                    background: #1e1e1e !important;
                    border: 1px solid #3e3e3e;
                }
                pre code {
                    background: #1e1e1e !important;
                }
                code {
                    background: #2d2d2d !important;
                }
                /* 引用块对比度 */
                blockquote {
                    background: #2d2d2d;
                    border-left: 4px solid #4a9eff;
                }
            '''
        },
        'pico': {
            'name': 'Pico.css',
            'css': 'https://cdn.jsdelivr.net/npm/@picocss/pico@1/css/pico.min.css',
            'body_class': '',
            'is_dark': False,
            'highlight_css': 'https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.8.0/styles/a11y-light.min.css',
            'custom_css': '''
                body {
                    padding: 20px;
                }
                main.container {
                    max-width: 980px;
                    margin: 0 auto;
                }
            '''
        },
        'pico-dark': {
            'name': 'Pico.css Dark',
            'css': 'https://cdn.jsdelivr.net/npm/@picocss/pico@1/css/pico.classless.min.css',
            'body_class': '',
            'is_dark': True,
            'highlight_css': 'https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.8.0/styles/base16/material-darker.min.css',
            'custom_css': '''
                html {
                    color-scheme: dark;
                }
                body {
                    padding: 20px;
                }
                main.container {
                    max-width: 980px;
                    margin: 0 auto;
                }
                /* 提升代码块对比度 */
                pre {
                    background: #1a1f29 !important;
                    border: 1px solid #2e3440;
                }
                pre code {
                    background: #1a1f29 !important;
                }
                code {
                    background: #2e3440 !important;
                }
                /* 引用块对比度 */
                blockquote {
                    background: #2e3440;
                    border-left: 4px solid #5294e2;
                }
            '''
        },
        'mvp': {
            'name': 'MVP.css',
            'css': 'https://unpkg.com/mvp.css',
            'body_class': '',
            'is_dark': False,
            'highlight_css': 'https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.8.0/styles/atom-one-light.min.css',
            'custom_css': '''
                body {
                    padding: 20px;
                }
            '''
        },
        'sakura': {
            'name': 'Sakura',
            'css': 'https://cdn.jsdelivr.net/npm/sakura.css@1.4.1/css/sakura.css',
            'body_class': '',
            'is_dark': False,
            'highlight_css': 'https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.8.0/styles/default.min.css',
            'custom_css': '''
                body {
                    max-width: 900px;
                    margin: 0 auto;
                    padding: 20px;
                }
            '''
        },
        'sakura-dark': {
            'name': 'Sakura Dark',
            'css': 'https://cdn.jsdelivr.net/npm/sakura.css@1.4.1/css/sakura-dark.css',
            'body_class': '',
            'is_dark': True,
            'highlight_css': 'https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.8.0/styles/base16/solarized-dark.min.css',
            'custom_css': '''
                body {
                    max-width: 900px;
                    margin: 0 auto;
                    padding: 20px;
                }
                /* 提升代码块对比度 */
                pre {
                    background: #002b36 !important;
                    border: 1px solid #073642;
                }
                pre code {
                    background: #002b36 !important;
                }
                code {
                    background: #073642 !important;
                }
                /* 引用块对比度 */
                blockquote {
                    background: #073642;
                    border-left: 4px solid #268bd2;
                }
            '''
        },
        'latex': {
            'name': 'LaTeX.css',
            'css': 'https://cdn.jsdelivr.net/npm/latex.css@1.10.0/style.min.css',
            'body_class': 'latex-body',
            'is_dark': False,
            'highlight_css': 'https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.8.0/styles/default.min.css',
            'custom_css': '''
                .latex-body {
                    max-width: 900px;
                    margin: 0 auto;
                    padding: 20px;
                }
            '''
        },
        'tufte': {
            'name': 'Tufte CSS',
            'css': 'https://cdnjs.cloudflare.com/ajax/libs/tufte-css/1.8.0/tufte.min.css',
            'body_class': '',
            'is_dark': False,
            'highlight_css': 'https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.8.0/styles/default.min.css',
            'custom_css': '''
                body {
                    padding: 20px;
                }
            '''
        },
        'modest': {
            'name': 'Modest',
            'css': 'https://cdn.jsdelivr.net/gh/markdowncss/modest/css/modest.css',
            'body_class': '',
            'is_dark': False,
            'highlight_css': 'https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.8.0/styles/default.min.css',
            'custom_css': ''
        },
        'retro': {
            'name': 'Retro (98.css)',
            'css': 'https://unpkg.com/98.css',
            'body_class': 'window-body',
            'is_dark': False,
            'highlight_css': 'https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.8.0/styles/a11y-light.min.css',
            'custom_css': '''
                body {
                    padding: 20px;
                }
                .window-body {
                    max-width: 900px;
                    margin: 0 auto;
                }
            '''
        },
        'nes': {
            'name': 'NES.css (像素風)',
            'css': 'https://unpkg.com/nes.css@latest/css/nes.min.css',
            'body_class': 'nes-container is-rounded',
            'is_dark': False,
            'highlight_css': 'https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.8.0/styles/a11y-light.min.css',
            'custom_css': '''
                body {
                    padding: 20px;
                }
                .nes-container.is-rounded {
                    max-width: 980px;
                    margin: 0 auto;
                }
                .mermaid {
                    background: white;
                    padding: 20px;
                    border-image-source: url('data:image/svg+xml;charset=UTF-8,<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M3 3V21H21V3H3Z" fill="white"/><path d="M0 0V24H24V0H0ZM3 3V21H21V3H3Z" fill="black"/></svg>');
                    border-image-slice: 3;
                    border-image-repeat: repeat;
                    border-style: solid;
                    border-width: 3px;
                }
            '''
        }
    }
    
    # Mermaid 主題
    MERMAID_THEMES = {
        'default': '預設主題',
        'forest': '森林主題',
        'dark': '深色主題',
        'neutral': '中性主題',
        'base': '基礎主題'
    }
    
    def __init__(
        self,
        html_theme: str = 'water-dark',
        mermaid_theme: str = 'default',
        container_width: int = 900,
        mermaid_config: Optional[Dict[str, Any]] = None,
        extra_css: str = ""
    ):
        """
        初始化 Markdown 轉換器

        Args:
            html_theme (str): HTML 主題名稱，預設為 'water-dark'
                可選值：github, github-dark, bootstrap, bootstrap-dark,
                       water, water-dark, pico, pico-dark, mvp,
                       sakura, sakura-dark, latex, tufte, modest, retro, nes
            mermaid_theme (str): Mermaid 圖表主題，預設為 'default'（自動選擇）
                可選值：default, forest, dark, neutral, base
                若設為 'default'，將根據 HTML 主題自動選擇深色或亮色
            container_width (int): 容器最大寬度（像素），預設 900
            mermaid_config (dict): Mermaid 自定義配置，可覆蓋預設配置
            extra_css (str): 額外的自定義 CSS 樣式

        範例：
            >>> # 使用預設主題
            >>> converter = MermaidMarkdownConverter()
            >>>
            >>> # 自定義主題與配置
            >>> converter = MermaidMarkdownConverter(
            ...     html_theme='github-dark',
            ...     mermaid_theme='dark',
            ...     container_width=1200
            ... )
        """
        self.html_theme = self.HTML_THEMES.get(html_theme, self.HTML_THEMES['github'])
        
        # 如果未指定Mermaid主題，根據HTML主題自動選擇
        if mermaid_theme == 'default':
            self.mermaid_theme = 'dark' if self.html_theme.get('is_dark', False) else 'default'
        else:
            self.mermaid_theme = mermaid_theme
            
        self.container_width = container_width
        self.mermaid_config = mermaid_config or {}
        self.extra_css = extra_css
        
    def convert(self, markdown_text: str, title: str = "Markdown文檔") -> str:
        """
        將 Markdown 文本轉換為完整的 HTML 頁面

        Args:
            markdown_text (str): Markdown 格式的文本內容
            title (str): HTML 頁面標題，預設為 "Markdown文檔"

        Returns:
            str: 完整的 HTML 頁面內容（包含 <html>, <head>, <body> 標籤）

        處理流程：
            1. 使用 Python-Markdown 解析 Markdown 語法
            2. 識別並轉換 Mermaid 代碼塊為可渲染格式
            3. 生成包含 CSS 和 JavaScript 的完整 HTML 頁面

        支援的 Markdown 擴展：
            - fenced_code: 圍欄式代碼塊（```）
            - tables: 表格
            - nl2br: 換行轉為 <br>
            - codehilite: 代碼語法高亮

        範例：
            >>> converter = MermaidMarkdownConverter()
            >>> markdown_text = "# 標題\\n\\n這是內容"
            >>> html = converter.convert(markdown_text, title="我的文檔")
        """
        md = markdown.Markdown(extensions=[
            'fenced_code',
            'tables',
            'nl2br',
            'codehilite'
        ])
        
        html_content = md.convert(markdown_text)
        html_content = self._process_mermaid_blocks(html_content)
        full_html = self._generate_full_html(html_content, title)
        
        return full_html
    
    def _process_mermaid_blocks(self, html_content: str) -> str:
        """
        處理 HTML 中的 Mermaid 代碼塊

        將 Markdown 轉換後的 Mermaid 代碼塊（<pre><code>）
        轉換為 Mermaid 可渲染的 <div class="mermaid"> 格式

        Args:
            html_content (str): Markdown 轉換後的 HTML 內容

        Returns:
            str: 處理後的 HTML 內容，Mermaid 代碼塊已轉換為可渲染格式

        處理邏輯：
            1. 使用正則表達式匹配 <pre><code class="language-mermaid">
            2. 提取 Mermaid 代碼內容並解碼 HTML 實體
            3. 轉換為 <div class="mermaid"> 格式供 Mermaid.js 渲染

        支援格式：
            - <pre><code class="language-mermaid">...</code></pre>
            - <pre class="codehilite"><code class="language-mermaid">...</code></pre>
        """
        # 匹配兩種可能的格式：
        # 1. <pre><code class="language-mermaid">...</code></pre>
        # 2. <pre class="codehilite"><code class="language-mermaid">...</code></pre>
        pattern = r'<pre(?:\s+class="[^"]*")?\s*><code class="language-mermaid">(.*?)</code></pre>'

        def replace_mermaid(match):
            mermaid_code = match.group(1)
            # 解碼HTML實體
            import html
            mermaid_code = html.unescape(mermaid_code)
            return f'<div class="mermaid">\n{mermaid_code}\n</div>'

        html_content = re.sub(pattern, replace_mermaid, html_content, flags=re.DOTALL)
        return html_content
    
    def _generate_mermaid_config(self) -> str:
        """生成Mermaid配置"""
        import json
        base_config = {
            'startOnLoad': True,
            'theme': self.mermaid_theme,
            'securityLevel': 'loose'
        }
        base_config.update(self.mermaid_config)
        return json.dumps(base_config, indent=12)
    
    def _generate_full_html(self, body_content: str, title: str) -> str:
        """生成完整HTML"""
        theme = self.html_theme
        mermaid_config = self._generate_mermaid_config()
        
        # 判斷容器包裝邏輯
        container_tag = 'main' if theme['name'] in ['Pico.css', 'Pico.css Dark'] else 'div'
        
        if theme['body_class']:
            # 對於github, nes, latex等主題，class直接放在body_content的包裝元素上
            container_html = f'<{container_tag} class="{theme["body_class"]}">{body_content}</{container_tag}>'
        else:
            # 對於bootstrap, water等，使用一個標準的container class
            container_html = f'<{container_tag} class="container">{body_content}</{container_tag}>'

        # 根據主題決定Mermaid背景
        mermaid_style = '''
        .mermaid {
            margin: 2em 0;
            padding: 1.5em;
            text-align: center;
            border-radius: 8px;
        }
        '''
        if theme.get('is_dark', False):
            mermaid_style += '''
        .mermaid {
            background: #2c3034;
            border: 1px solid #444;
        }
            '''
        else:
            mermaid_style += '''
        .mermaid {
            background: #f9f9f9;
            border: 1px solid #ddd;
        }
            '''

        html_template = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    
    <!-- CSS 框架 -->
    <link rel="stylesheet" href="{theme['css']}">
    
    <!-- 代碼高亮 -->
    <link rel="stylesheet" href="{theme['highlight_css']}">
    
    <!-- 自定義樣式 -->
    <style>
        {theme['custom_css']}
        
        /* 通用代碼塊樣式 */
        pre code {{
            display: block;
            padding: 1.5em;
            border-radius: 8px;
            overflow-x: auto;
            line-height: 1.6;
        }}

        /* Mermaid 圖表樣式 */
        {mermaid_style}
        
        /* 響應式調整 */
        @media (max-width: 768px) {{
            body {{
                padding: 10px;
            }}
            .container, .markdown-body, .latex-body, .window-body, .nes-container {{
                padding: 15px;
            }}
            pre code {{
                padding: 1em;
            }}
        }}
        
        {self.extra_css}
    </style>
</head>
<body>
    {container_html}
    
    <!-- Highlight.js -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.8.0/highlight.min.js"></script>
    <script>hljs.highlightAll();</script>
    
    <!-- Mermaid -->
    <script type="module">
        import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
        mermaid.initialize({mermaid_config});
    </script>
</body>
</html>"""
        return html_template
    
    def convert_file(self, input_file: str, output_file: str, title: Optional[str] = None):
        """
        將 Markdown 文件轉換為 HTML 文件

        Args:
            input_file (str): 輸入的 Markdown 文件路徑（絕對或相對路徑）
            output_file (str): 輸出的 HTML 文件路徑
            title (str, optional): HTML 頁面標題
                若未指定，將使用輸入文件名（不含副檔名）作為標題

        Returns:
            None: 直接將結果寫入輸出文件

        異常處理：
            - FileNotFoundError: 輸入文件不存在時顯示錯誤訊息
            - 其他例外: 讀取或寫入文件時的錯誤

        輸出資訊：
            轉換成功後會顯示：
            - ✅ 轉換成功
            - HTML 主題名稱
            - Mermaid 主題名稱
            - 輸出文件路徑

        範例：
            >>> converter = MermaidMarkdownConverter(html_theme='water-dark')
            >>> converter.convert_file('input.md', 'output.html')
            ✅ 轉換成功！
               HTML 主題：Water.css Dark
               Mermaid 主題：dark
               輸出檔案：output.html
        """
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                markdown_text = f.read()
        except FileNotFoundError:
            print(f"❌ 錯誤：找不到文件 {input_file}")
            return
        except Exception as e:
            print(f"❌ 讀取文件時發生錯誤：{e}")
            return

        if title is None:
            title = Path(input_file).stem
        
        html_content = self.convert(markdown_text, title)
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
        except Exception as e:
            print(f"❌ 寫入文件時發生錯誤：{e}")
            return

        print(f"✅ 轉換成功！")
        print(f"   HTML 主題：{self.html_theme['name']}")
        print(f"   Mermaid 主題：{self.mermaid_theme}")
        print(f"   輸出檔案：{output_file}")
    
    @classmethod
    def list_themes(cls):
        """
        列出所有可用的 HTML 主題

        顯示所有支援的 HTML 主題列表，包含：
        - 主題編號（供交互式模式使用）
        - 主題鍵名（供命令行參數使用）
        - 主題完整名稱
        - 深色/亮色標註

        範例輸出：
            ============================================================
            📚 可用的 HTML 主題：
            ============================================================
             1. github               - GitHub Markdown
             2. github-dark          - GitHub Dark (Dark)
             3. bootstrap            - Bootstrap 5
            ...
            ============================================================
        """
        print("=" * 60)
        print("📚 可用的 HTML 主題：")
        print("=" * 60)
        for i, (key, theme) in enumerate(cls.HTML_THEMES.items(), 1):
            dark_label = " (Dark)" if theme.get('is_dark') else ""
            print(f"{i:2d}. {key:20s} - {theme['name']}{dark_label}")
        print("=" * 60)


def interactive_convert():
    """
    交互式轉換模式

    提供友善的交互式介面，逐步引導使用者：
    1. 選擇 HTML 主題（顯示所有可用主題）
    2. 選擇 Mermaid 主題（可選，預設自動）
    3. 輸入 Markdown 文件路徑
    4. 輸入輸出 HTML 文件路徑（可選）
    5. 執行轉換

    特色：
        - 友善的提示訊息
        - 預設值設定（water-dark 主題）
        - 錯誤處理與提示
        - 自動計算預設輸出文件名

    使用方式：
        python3 md2htmlv2.py interactive
    """
    print("=" * 70)
    print("📝 Markdown to HTML 轉換器（支援流行CSS框架主題）")
    print("=" * 70)
    
    # 顯示所有主題
    MermaidMarkdownConverter.list_themes()
    
    themes = list(MermaidMarkdownConverter.HTML_THEMES.items())
    # 找出 water-dark 的編號
    default_index = next((i for i, (key, _) in enumerate(themes, 1) if key == 'water-dark'), 6)
    html_choice = input(f"\n請選擇主題編號 (預設{default_index} 'water-dark'): ").strip() or str(default_index)
    try:
        html_theme_key = themes[int(html_choice) - 1][0]
    except (ValueError, IndexError):
        print("無效選擇，使用預設主題 'water-dark'")
        html_theme_key = 'water-dark'

    # 選擇 Mermaid 主題
    print("\n🎨 請選擇 Mermaid 主題 (Enter 使用自動模式)：")
    mermaid_themes = list(MermaidMarkdownConverter.MERMAID_THEMES.items())
    for i, (key, desc) in enumerate(mermaid_themes, 1):
        print(f"  {i}. {key} - {desc}")
    
    mermaid_choice = input(f"\n請選擇 (預設: 自動): ").strip()
    if not mermaid_choice:
        mermaid_theme_key = 'default' # 'default'觸發自動選擇
    else:
        try:
            mermaid_theme_key = mermaid_themes[int(mermaid_choice) - 1][0]
        except (ValueError, IndexError):
            print("無效選擇，使用自動模式")
            mermaid_theme_key = 'default'

    # 輸入輸出文件
    input_file = input("\n📄 輸入 Markdown 文件路徑: ").strip()
    if not input_file:
        print("❌ 錯誤：必須提供輸入文件。")
        return
        
    default_output = f"{Path(input_file).stem}.html"
    output_file = input(f"💾 輸出 HTML 文件路徑 (預設: {default_output}): ").strip() or default_output
    
    # 轉換
    main_convert(input_file, output_file, html_theme_key, mermaid_theme_key)


def demo():
    """
    生成所有主題的展示文件

    功能：
        自動生成包含以下內容的測試 Markdown 文件：
        - 標題與段落
        - Mermaid 流程圖與時序圖
        - 代碼區塊（Python）
        - 表格
        - 列表
        - 引用區塊

    然後將測試文件轉換為多個主題的 HTML 文件：
        - github, github-dark
        - bootstrap, bootstrap-dark
        - water-dark
        - pico, pico-dark
        - mvp
        - sakura-dark
        - latex
        - nes

    輸出：
        在當前目錄生成 demo_*.html 文件（共 11 個）
        每個文件使用不同的 CSS 主題

    使用方式：
        python3 md2htmlv2.py demo

    清理：
        自動清理臨時的 demo_temp.md 文件
    """
    
    test_markdown = """
# Markdown 主題展示

這是一個展示各種 HTML 主題的文檔。

## 流程圖
```mermaid
graph TD
    A[開始] --> B{條件判斷}
    B -->|是| C[處理A]
    B -->|否| D[處理B]
    C --> E[結束]
    D --> E
```

## 時序圖
```mermaid
sequenceDiagram
    participant 用戶
    participant 前端
    participant 後端
    
    用戶->>前端: 點擊按鈕
    前端->>後端: API請求
    後端-->>前端: 返回數據
    前端-->>用戶: 顯示結果
```

## 代碼示例
```python
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

print(fibonacci(10))
```

## 表格

| 主題 | 類型 | 特色 |
|------|------|------|
| GitHub | 經典 | 簡潔明了 |
| Bootstrap | 現代 | 響應式 |
| Water.css | 極簡 | 無類名 |

## 列表

- 支持 Markdown 語法
- 整合 Mermaid 圖表
- 多種主題選擇
- 響應式設計

> 這是一段引用文字，用來測試主題的引用樣式。
"""
    
    # 創建測試文件
    demo_md_file = 'demo_temp.md'
    with open(demo_md_file, 'w', encoding='utf-8') as f:
        f.write(test_markdown)
    
    # 生成多個主題示例
    themes_to_demo = [
        'github',
        'github-dark',
        'bootstrap',
        'bootstrap-dark',
        'water-dark',
        'pico',
        'pico-dark',
        'mvp',
        'sakura-dark',
        'latex',
        'nes'
    ]
    
    print("\n🚀 開始生成所有主題的展示文件...")
    for theme in themes_to_demo:
        output_filename = f'demo_{theme}.html'
        print(f"\n🎨 正在生成 {theme} 主題...")
        main_convert(demo_md_file, output_filename, theme)
    
    # 清理臨時文件
    import os
    os.remove(demo_md_file)
    
    print("\n\n✅ 所有主題示例生成完成！")
    print("請在瀏覽器中打開 demo_*.html 文件查看效果。")


def main_convert(input_file: str, output_file: str, html_theme: str = 'water-dark', mermaid_theme: str = 'default'):
    """
    主要的轉換函數（命令行入口）

    Args:
        input_file (str): 輸入的 Markdown 文件路徑
        output_file (str): 輸出的 HTML 文件路徑
        html_theme (str): HTML 主題名稱，預設為 'water-dark'
        mermaid_theme (str): Mermaid 主題名稱，預設為 'default'（自動選擇）

    功能：
        1. 創建 MermaidMarkdownConverter 實例
        2. 調用 convert_file 方法執行轉換
        3. 顯示轉換結果（成功/失敗訊息）

    使用方式：
        # Python 函數調用
        >>> main_convert('input.md', 'output.html', 'github-dark')

        # 命令行調用（由 __main__ 塊處理）
        $ python3 md2htmlv2.py input.md output.html github-dark

    注意：
        此函數是所有轉換模式的統一入口
        包括：直接轉換、交互式轉換、demo 模式
    """
    converter = MermaidMarkdownConverter(
        html_theme=html_theme,
        mermaid_theme=mermaid_theme
    )
    converter.convert_file(input_file, output_file)


if __name__ == "__main__":
    """
    命令行入口點

    支援的使用模式：

    1. 直接轉換模式（預設）：
        python3 md2htmlv2.py <input.md> [output.html] [theme]
        - input.md: 必需，輸入的 Markdown 文件
        - output.html: 可選，輸出文件（預設為 input.html）
        - theme: 可選，主題名稱（預設為 water-dark）

    2. 交互式模式：
        python3 md2htmlv2.py interactive
        - 提供友善的交互式介面

    3. 列出主題：
        python3 md2htmlv2.py list
        - 顯示所有可用的 HTML 主題

    4. 展示模式：
        python3 md2htmlv2.py demo
        - 生成所有主題的展示文件

    5. 無參數模式：
        python3 md2htmlv2.py
        - 自動進入交互式模式
    """
    import sys

    if len(sys.argv) > 1:
        if sys.argv[1] == 'demo':
            # 展示模式：生成所有主題的範例 HTML
            demo()
        elif sys.argv[1] == 'interactive':
            # 交互式模式：逐步引導用戶輸入參數
            interactive_convert()
        elif sys.argv[1] == 'list':
            # 列出所有可用主題
            MermaidMarkdownConverter.list_themes()
        else:
            # 直接轉換模式：從命令行參數讀取文件路徑和主題
            input_file = sys.argv[1]
            output_file = sys.argv[2] if len(sys.argv) > 2 else f"{Path(input_file).stem}.html"
            theme = sys.argv[3] if len(sys.argv) > 3 else 'water-dark'
            main_convert(input_file, output_file, theme)
    else:
        # 無參數時進入交互式模式
        interactive_convert()