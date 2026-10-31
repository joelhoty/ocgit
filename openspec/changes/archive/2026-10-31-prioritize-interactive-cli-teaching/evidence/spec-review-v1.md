# Independent spec compliance review v1

Date: 2026-10-31
Reviewer: /root/spec_review
Workspace: /private/tmp/ocgithub-interactive-cli
Base: 26553d4
Verdict: FAIL — two current blockers; no task completion claimed.

## Requirement coverage

- REQ-TEACH-009: Changed examples start the CLI once and use shared natural-language prompts. Intro 5.9 provides read, follow-up, save and verification. Workspaces, lessons and assessment retain the original substantive teaching cases and named inputs/outputs.
- REQ-TEACH-010: Changed chapter introductions separate project instruction files from commands. Intro 5.10/5.11 distinguishes session/context/token/account usage/model selection. Batch workflows now use conversation to plan, create, review and execute scripts with failure checks. However, unchanged chapter 05 still recommends startup-with-prompt commands (finding 1).
- REQ-TEACH-011: Names, image assets, design shell and navigation are retained in diff. Slash menu guidance distinguishes Claude /usage, /context and /help from Codex /status, /statusline and slash menu. Current static pairing has one mismatch (finding 2).

## Blocking findings

1. REQ-TEACH-009/010: `AI_Agent_CLi/05_instructions.md:409` still recommends `codex "改寫這段關於光合作用的說明"`; lines 492/494 still recommend Codex/Claude startup-with-prompt for quick mode. Paired HTML lines 453/519/521 also retain these. Convert to already-open session prompts and update surrounding explanation. Task 2 permits adding exact consistency-fix paths before editing.
2. REQ-TEACH-011: Fresh `python3 openspec/changes/archive/2026-10-31-revise-ai-agent-cli-teaching/validation/check_course.py` returned exit 1, reporting `04_workspace.html: Markdown/HTML fenced content mismatch`. Likely a concurrent final edit after render; regenerate final pairs and rerun.

## Review scope and observations

Read approved specs, design, task contract; inspected complete Markdown diffs for 04_workspace, 04a_workflows, 06_lesson_plans, 06a_assessment, intro changes and HTML-only replacements, plus whole-course CLI command scans and unchanged 01/02/03/05/08 pages. No substantive case/input/output/grading-logic loss found in reviewed changes. Long duplicated CLI prompts were consolidated without deleting the educational content. Pandoc/Git/install commands remain separately labeled shell/reference operations, consistent with scope.

Source interpretation uses parent-fetched official Codex CLI and Claude commands documentation recorded in sources.md; this review does not claim a live model session or paid CLI operation was executed. Browser/manual visual coverage and final evidence-manifest review remain parent verification responsibilities.

## Commands

- `rg -n 'codex exec|claude -p|codex "|claude "|codex &quot;|claude &quot;|非互動|單次輸出|單次任務' AI_Agent_CLi`: found chapter 05 remnants.
- `git diff --check`: no reported whitespace errors.
- `python3 .../validation/check_course.py`: FAIL as above, 16 HTML / 279 links / 15 redirects / 10 Markdown pairs.
