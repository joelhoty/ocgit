# Independent policy-alignment review

Date: 2026-10-31
Reviewer: /root/spec_review
Verdict: PASS

## Reviewed change

Reviewed the canonical main requirement, the newly added MODIFIED delta, updated task Covers, approved-scope-reconciliation.md, current teaching content and the explicit user direction in the conversation.

The exact canonical heading `REQ-TEACH-003 — 官方安裝與操作依據` is preserved. The modification removes the former obligation to teach single-shot execution and states interactive-session operation for beginner and advanced tasks. This is directly consistent with the user’s explicit rejection of command-plus-prompt at all levels, later approved with “ok”; it introduces no additional teaching scope. Retaining the old requirement unmodified would contradict that approved direction.

Installation, update, version check, authentication, project startup, troubleshooting, official citations/check date, shell/session distinction and runtime/project dependency distinction remain required by the delta. The success scenario is narrowed only to make the first task explicitly interactive, while retaining the ability to choose one tool.

## Current implementation evidence

- Intro sections 3–5 retain platform/install/dependency instructions and the 2026-10-31 official-source check date; the edited section 5.9 teaches first task read/follow-up/save/verify in a CLI session.
- The separate environment guide `08_environment.html` has no diff from the accepted baseline and retains install/update/version/login/troubleshooting material.
- Intro 0.3 and 5.10 distinguish shell from conversation/slash-command input. Tool alternatives and account/version differences remain explicit.
- Whole-course search found no `codex exec`, `claude -p` or startup-with-quoted-prompt examples.
- Fresh full course static check: PASS, exit 0, 16 HTML, 280 local links, 15 redirects, 10 Markdown pairs, no errors. `git diff --check`: exit 0.
- Both task groups now cover the exact REQ-TEACH-003 ID in addition to 009–011. Evidence identity must be refreshed for this changed policy input as the parent has planned; this review does not itself publish completion or validate the replacement manifest.

## Limits

No installers, live model tasks, authentication changes or paid CLI calls were executed by this review. Existing installation material was inspected for retained coverage, not independently rerun. No unresolved policy-alignment finding remains.
