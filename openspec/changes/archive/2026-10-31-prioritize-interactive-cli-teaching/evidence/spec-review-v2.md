# Independent spec compliance review v2

Date: 2026-10-31
Reviewer: /root/spec_review
Workspace: /private/tmp/ocgithub-interactive-cli
Base: 26553d4
Verdict: PASS — editorial implementation meets REQ-TEACH-009, REQ-TEACH-010, REQ-TEACH-011. Final browser verification and manifest publication remain parent-owned.

## Recheck of v1 findings

1. Chapter 05 now uses natural-language text prompts inside an already-open session for the rewriting and custom quick-mode cases. Its explanation distinguishes custom quick-mode formatting from actual CLI model/speed settings. Exact 05 Markdown/HTML paths were added to Task 2 under the existing approved cross-course consistency provision. PASS.
2. All final paired pages were regenerated. Fresh full `check_course.py` returned exit 0: 16 HTML, 280 local links, 15 legacy redirects, 10 Markdown pairs, no errors. PASS.
3. Whole-course search for `codex exec`, `claude -p`, or startup commands with quoted prompts returned no matches. `git diff --check` returned exit 0. PASS.

## Requirement/scenario review

- REQ-TEACH-009 / 讀檔並追問: Intro 5.9 demonstrates one CLI launch, read sources, follow-up in the same session, named output file and physical-file verification. Workspace, workflow, lessons and assessment chapter examples consistently use shared natural-language prompts. PASS.
- REQ-TEACH-010 / 初學者閱讀操作約定: Chapter introductions separate shell startup from conversation input and describe AGENTS.md/CLAUDE.md as files linked to chapter 05. PASS.
- REQ-TEACH-010 / 進階批次處理: Weekly reports, three-unit lesson generation, Pandoc batches and grading scripts use dialogue to plan, create, inspect, authorize and verify scripts. Source/output names and missing/empty/conflicting-file checks remain. Intro 5.11 teaches session continuation, context compaction, model selection and consumption checks, without claiming infinite memory or token count equals billing. PASS.
- REQ-TEACH-011 / 閱讀兩種格式: Static full-course invariants pass; diff preserves filenames, images, visual shell/navigation and teaching cases. Original duplicated CLI syntax was removed without loss of subject examples or scoring rules. PASS for content/static scope; browser visual observation is delegated to final verification.
- REQ-TEACH-011 / 會話內常用指令速查: Intro 5.10 and HTML-only CLI chapters distinguish Codex status/statusline from Claude usage/context/help. Both tools model/compact/resume/permissions are represented with intended use and input location; account/version availability is explicit. Matches the official-source findings recorded in sources.md. PASS.

## Limits

This review inspected artifacts and diffs; it does not claim execution of live model prompts, billing measurements, installation commands or batch scripts. Task 2 final browser evidence and lifecycle/identity validation must still be completed before whole-change completion. No unresolved spec findings remain in the editorial implementation.
