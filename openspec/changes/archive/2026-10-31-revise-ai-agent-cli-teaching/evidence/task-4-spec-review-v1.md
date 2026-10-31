# Task 4 independent specification review — v1

Reviewer: task1_intro acting independently of Task4 author. Date: 2026-10-31.

Scope: completed new course/root indices and README/git_index/CONTRIBUTING edits. Old redirects and final target existence intentionally deferred until all targets exist; this is not the final High-risk gate review.

Result: **FAIL — one correctable index/content consistency issue**.

## Finding

1. `AI_Agent_CLi/index_content.html:172` and `:176` still make Google AI Studio the named Unit1 tool. The approved course is dual Codex CLI/Claude Code, and the target Unit1 is being updated accordingly. Replace this card description/bullet with the dual-route task wording (or explicitly mark web UI as optional if retained in the final unit). Otherwise the new entry point tells learners to start a different mandatory tool than the approved course. Covers REQ-TEACH-006 (index/sections consistency), with REQ-TEACH-005 context.

## Passing observations

- Front matter HTML and Markdown are first, before Unit1.
- All 15 content pages appear in course index; root index includes all 16 pages including index.
- New internal course links are target-relative; no old-folder navigation.
- Root #gemini anchor remains intentionally compatible while visible title and folder change.
- Original dark cards and six-unit ordering retained; mobile minimum-width grid revised without framework change.
- Root README/git_index/CONTRIBUTING point to new folder and canonical renamed Unit5/CLI pages.
- Existing repository historical changelog references do not count as active old instructions.

## Deferred scope

- Redirects, fragment handling, all-target existence and JavaScript-disabled behavior need a later review after Task4 completes.
- Final visual browser proof belongs to integration verification.

## Mechanical observations

{
  "front_matter_first": true,
  "all_15_content_pages_listed": true,
  "no_old_course_navigation": true,
  "root_16_cards": true,
  "root_anchor_compatibility": true
}

## Subject digests

- `AI_Agent_CLi/index_content.html`: `684c2b798c906f74662b030259802f3dd0400ad0d007acd37b0f6f9656eee2aa`
- `index.html`: `a2b90a8257fdcda72255b003f315fb306673764da80c1d95a5d6a7133440b0c6`
- `README.md`: `7f37a3273c0c2626446a4dc32d54d367b4a95136d647ce82bda3fa4f94125404`
- `git_index.md`: `21c4cb8888bf705730c954315d16360ecdf8dc94d703c935fb1bdb54d1f01e63`
- `CONTRIBUTING.md`: `a6f0f41fd4309e04220255729ccc55cef7252b618f7644c25358497e63a9e6f2`
