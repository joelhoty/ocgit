# Verification report

Status: PASS
Date: 2026-10-31

## Scope and independent coverage

Two tasks, two requirements, four scenarios verified against the approved outline.

| Requirement / scenario | Risk | Evidence and result |
| --- | --- | --- |
| REQ-TEACH-012 basic reader | Standard | Independent spec and quality reviews trace Windows/macOS setup, source preparation, rules and Git before first read/follow-up/save/verify task. PASS |
| REQ-TEACH-012 Python extension | Standard | uv/interpreter precede the complete exercise; optional Node installation is in Appendix A. PASS |
| REQ-TEACH-013 old topic links | High | Exact 111-ID inventory, 110 topic fragments navigated with page JavaScript disabled, topic-local destination comparisons; missing, duplicate and misplaced alias negative controls rejected. PASS |
| REQ-TEACH-013 complete content | Standard | 109-heading content map independently reviewed; Python blocks byte-identical, all original external sources and images retained; paired Markdown/HTML validated. PASS |

## Fresh execution

- check_course.py: PASS, 16 HTML pages, 304 local links, 15 legacy redirects, 10 Markdown/HTML pairs.
- check_intro.py: PASS, exact expected section order, 111 legacy IDs, all three negative controls.
- browser_intro.py final browser-intro-2.json: PASS, 114 cases, zero errors. Includes desktop/mobile index and intro, images and Mermaid.
- git diff --check: PASS.
- Independent spec-review-final.md, quality-review-final.md and quality-harness-followup.md: PASS.
- visual-review.md: PASS after inspecting actual desktop opening, mobile slash-command table and full Python program screenshots. Wide content scrolls within preserved containers.
- evidence-manifest.yaml: five checks with matching subject, anchored policy, requirement bindings and immutable payload digests, no manual gaps.

The initial browser harness stalled at add_style_tag with JavaScript disabled. A controlled diagnostic isolated this operation; synchronous inline scroll-behavior assignment retains disabled page scripts and enabled exhaustive fragment verification. See debug-log.md. Both corrected complete runs passed.

## Limits

This is a teaching-content reorganization. CLI installers, account login and paid model calls were not executed. Product facts were preserved from the previously verified curriculum. Archive relocation requires refreshed identity evidence; historical run payloads are retained.

Archive relocation: capture_evidence.py and evidence_identity.py rerun successfully at the archived location; all five checks match the final archived paths.
