# Verification report: prioritize-interactive-cli-teaching

Date: 2026-10-31
Mode: Spec Mode
Status: PASS

## Results

- Both Standard task groups complete. Four requirements, six scenarios mapped below.
- Fresh complete static regression: `python3 validation/check_course.py` (from this change directory), exit 0; 16 HTML, 280 local links, 15 legacy redirects, 10 Markdown pairs.
- Fresh final browser regression: `python3 validation/browser_check.py`, exit 0; evidence/browser-results-2.json, 47/47 cases (16 desktop, 16 mobile, 15 old URLs with JavaScript disabled).
- `git diff --check`: exit 0. No separate linter/build is configured for these static editorial files; generated HTML checked directly.
- Whole-course scan: no CLI command-plus-prompt recommendations remain.
- High-risk changed behavior: none. Existing redirect behavior was unmodified and additionally exercised exhaustively.

## Independent requirement-to-evidence matrix

Risk, coverage and execution classifications below derive from the requirements and editorial scope, not manifest kind. No prior suite result is reused as the final regression gate.

| Requirement / scenario | Risk | Coverage | Execution | Evidence | Status | Result / gaps |
|---|---|---|---|---|---|---|
| REQ-TEACH-003 / 官方安裝與操作依據驗收 | standard | representative | manual | spec-policy-review.md; sources.md; installation unchanged and first task now interactive | fresh | PASS / none |
| REQ-TEACH-009 / 讀檔並追問 | standard | exhaustive + representative | automated + manual | all-course scan; spec-review-v2.md; intro 5.9 read/follow-up/save exercise | fresh | PASS / none |
| REQ-TEACH-010 / 初學者閱讀操作約定 | standard | representative | manual | spec-review-v2.md; quality-review-v1.md; chapter introductions | fresh | PASS / none |
| REQ-TEACH-010 / 進階批次處理 | standard | representative | manual | complete workflow/assessment diffs reviewed; planning, trial run, failure and empty-output handling | fresh | PASS / none |
| REQ-TEACH-011 / 閱讀兩種格式 | standard | exhaustive + representative | automated + manual | static regression, browser-results-2.json, visual-review.md | rerun | PASS / none |
| REQ-TEACH-011 / 會話內常用指令速查 | standard | focused + representative | manual | sources.md; intro5.10/5.11; spec/quality and desktop/mobile table inspection | fresh | PASS / none |

Automated records in the manifest prove the bounded source/render/link checks; representative records refer to the independently reviewed content and visible samples. Their kind labels are not substitutes for the coverage mapping above.

## Evidence identity and task reconciliation

Schema sos-evidence/v1: valid. Four check records cover both tasks, each with nonempty exact requirement IDs, command or procedure, producer/actor, subject constituents/hash, four anchored policy-input kinds, policy hash and immutable payload digest. Python version recorded; no TTL. `validation/evidence_identity.py` recomputes and validates all records. The verification-policy snapshot is byte-identical to the sos-verify skill read for this run. No project overrides or legacy-ID requirements apply.

All task groups have one Standard risk and one outcome. Requirement headings resolve uniquely. The approved interaction direction required synchronizing old REQ-TEACH-003; this invalidated earlier policy identities, so checks and review bindings were refreshed. Chapter05 consistency fixes are recorded in Task2. No unresolved evidence or manual gaps remain.

## Coherence and per-requirement conclusions

- REQ-TEACH-003: PASS. Retains official installation/account references and removes the obsolete requirement to teach single-shot commands; independent policy review confirms user authorization.
- REQ-TEACH-009: PASS. Natural-language prompts carry inputs, follow-ups, output paths and verification. Session startup is separate.
- REQ-TEACH-010: PASS. Advanced examples stay conversational, project instruction files are separate, and session/context/token/model controls have usage scenarios.
- REQ-TEACH-011: PASS. Six edited Markdown/HTML pairs and two HTML-only pages retain filenames, design, navigation and prior anchors; global paired checks cover all ten pairs. Representative mobile tables/code use preserved horizontal scrolling.

No blocking issues. Earlier findings (chapter05 old commands and a transient source/render mismatch during parallel editing) were fixed and reviewed in v2. Complete regression was rerun after final content edits.

## Limits

No paid model tasks, live account operations, installer commands or example batch scripts were executed. Product command behavior is based on fetched official documents dated 2026-10-31; visibility depends on installed version/account. Screenshots establish page presentation, not live CLI account behavior. Main checkout's unrelated repo.log is preserved. External styling/Mermaid resources still require network as before.

Conclusion: PASS; ready for spec synchronization and archival.
