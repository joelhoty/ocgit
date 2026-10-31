# Task 4 independent specification review — v3 final static review

Reviewer: task1_intro (not Task4 author). Date: 2026-10-31.

Result: **PASS** for final implementation against REQ-TEACH-006/007 and approved filename amendment. No blocking specification findings. Browser execution/visual acceptance remains a distinct integration evidence gate; this is source/static review, not a claim that this reviewer executed a browser.

## Navigation and naming

The approved 16-name mapping is applied: 00_intro through numbered topic names and index.html; HTML/Markdown pairs share basenames. Front matter HTML and source link precede six ordered units. New pages link inside AI_Agent_CLi, all chapter paths and fragments resolve, and root index/git_index list all 16 final pages. README and CONTRIBUTING use the new course directory. The formerly inconsistent Unit1 card now names both CLI products.

Independently executed check_course.py: PASS, 16 HTML pages, 262 local references, 15 old redirects, 10 Markdown pairs, zero errors. Additionally checked each old page's manual href, meta-refresh URL and script target against the approved mapping; all 15 agree and destinations exist. Root index/git_index references independently resolve to the final files.

## Compatibility failure paths and preservation

All 15 old HTML files remain at original URLs. Each includes a visible ordinary anchor to the corresponding final chapter, so navigation does not require JavaScript or automatic redirection. A meta refresh provides a no-JavaScript automatic route; script redirects preserve location.hash. If an old fragment no longer exists, chapter arrival still works and the page directs readers to the new chapter contents. Retaining every obsolete heading ID was not required by the approved contract. When both script and refresh are unavailable, the ordinary anchor remains usable by standard HTML semantics.

All historical Markdown files were compared byte-for-byte with git show HEAD and are unchanged. Original HTML remains recoverable from Git, and no legacy target is replaced with a redirect to a nonexistent destination. Earlier implementation evidence records pre-replacement target existence; this review confirms final state.

## Task3 rendering closure under final filenames

Re-ran independent line-based fenced-block comparison for every paired source. All exact: 00_intro 72, 01_materials 32, 02_images 28, 03_notebooklm 45, 04_workspace 47, 04a_workflows 45, 05_instructions 22, 06_lesson_plans 40, 06a_assessment 46, 12_literacy_research 0. Source and rendered counts match in each pair. The three Mermaid br escaping follow-ups from task-3-spec-review-v1 are resolved: decoded div.mermaid now equals the source including literal line-break markup. Actual SVG layout remains covered by final browser evidence.

## Subject digests

- `AI_Agent_CLi/index.html`: `274a295274fa985bb878359b055a2b6c27ae68fa413dc0e6903d731e7df1960e`
- `index.html`: `64405d1930c64ab46136ebd17ce9de7d382b974f8ebc013f68d722fb1d117a39`
- `README.md`: `7f37a3273c0c2626446a4dc32d54d367b4a95136d647ce82bda3fa4f94125404`
- `git_index.md`: `e2badabdd16430f5519061a3c7502d382f219ca92b00b778e9db55fe1b204f24`
- `CONTRIBUTING.md`: `a6f0f41fd4309e04220255729ccc55cef7252b618f7644c25358497e63a9e6f2`
- `GeminiForDesignTeaching/AI_Agent_Cli_b13.html`: `d9db9ed30c09ff3ddd42c7513987c3a8e89d5b7d48cb4c479af070c8693795d9`
- `GeminiForDesignTeaching/Environment_Setup_Guide_b06.html`: `68c7e7e3bfbdf0d8009588b5f6a90a320a9730e24715a6f6a253c9fc07c2ef06`
- `GeminiForDesignTeaching/Gemini_CLI_Tutorial_b02.html`: `73dd5b1930ddc166c7d0d2f3bc527c8c7ce44132dc1390a08377b4d533319b3c`
- `GeminiForDesignTeaching/index_content.html`: `e8025b68b3f7a51d58af52d04d53976a61c46446a3564a8b33404c8d8d0d41a9`
- `GeminiForDesignTeaching/literacy_b02.html`: `df4082e8051f0b751c78a6dbf8ea7e0acfb6115868c87f3bf335b2bc3c78427e`
- `GeminiForDesignTeaching/literacy_chatgpt_revise_b06.html`: `4a781d95874a342104506dd97d4e51d9e5e62c08a522f8cd6797f1df58c8464c`
- `GeminiForDesignTeaching/literacy_research.html`: `eaecae58d92cd2502239abd8aaa9886770871f90a7062e2ce2e16cca1b0bb16e`
- `GeminiForDesignTeaching/unit01_first_ai_material_b02.html`: `20a8029b3648359338355c91a7fdd05f7a80d9a78c3a4d6494fcaecf141b8f55`
- `GeminiForDesignTeaching/unit02_ai_image_generation_b02.html`: `503edd9366fb5bd86afebfd3a1ac0be560d4570a8e0cce8a2b0dcd2798e840fd`
- `GeminiForDesignTeaching/unit03_notebooklm_b02.html`: `03e4bac34709fa55224cafdac621d1470e89c85fed049c2e5e008331b68b5c7b`
- `GeminiForDesignTeaching/unit04_local_ai_setup_b02.html`: `7f5750df33de63a7fc855f123d78b9cbdee679fb455533308ef861fcd34f0e40`
- `GeminiForDesignTeaching/unit04_supplement_additions.html`: `8736239f720d8f6bb7b512fc8acb799e15d111ddb80cdda02e8ceda59b9bb78a`
- `GeminiForDesignTeaching/unit05_gemini_md_customization_b01.html`: `6367e56350070154e10a2e4622990b47ef37997e5be01962613b47c66e181bda`
- `GeminiForDesignTeaching/unit06_practical_lesson_plan_b02.html`: `c3346f4c23d2d8450f452d27a2565e9bb9a90e3e8e387f68b668c3fec43bdd75`
- `GeminiForDesignTeaching/unit06_supplement_additions.html`: `56ee2bbc0859972c571d5020c6d180e3ae4ed4a815f9a7ad6680e5ce71b7b87b`
- `openspec/changes/revise-ai-agent-cli-teaching/approved-amendment.md`: `76a446ff343507226851c2d1e6d7d52509d30658189778c047bd8850071d363d`
- `openspec/changes/revise-ai-agent-cli-teaching/validation/filename-map.json`: `419239d83ed10476872d21593871752332d46756a37fd670f74da37bba59c247`
