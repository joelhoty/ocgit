# Task 1 editorial self-review

- Base: `f7a957f`.
- Scope: complete Markdown reordering and source-heading mapping only. HTML, legacy aliases, index, independent reviews and lifecycle evidence are parent-owned.
- Markdown SHA-256: `fd6a7961434a5ef0a8213742159e3d7493df4029d82dc0f5e0adc53998e7fbb8`.

## Observed checks

- Original 109 rendered heading texts mapped uniquely to existing semantic heading IDs. Mapping records retain raw Markdown heading, canonical original HTML text, original ID and destination ID.
- Every actual Markdown heading (excluding fenced examples) has a semantic ID; no duplicate semantic IDs or dangling local anchor links.
- All original external HTTPS URL strings retained (set comparison); SVG path retained.
- Full Python fenced program blocks compare byte-for-byte with original. CSV, pseudocode, expected 170-minute total, Git examples and bounded-change exercise remain.
- Main order is 0–9, then appendices A–C. Node installation is in A.9; Python exercise runs consecutively in 8.1–8.13.
- Windows and macOS setup branches rejoin at the common project. Python installation and project initialization provide both platform paths. Shared git/uv command blocks use `shell`; platform-specific commands retain `powershell` or `bash`.
- First task order: create source notes → write rules → configure/init Git and save initial checkpoint → restart/check rule loading → read/follow up/save three-point draft → expand coverage to four source sections → verify and commit actual outputs.
- Three-point `notes_summary.md` is explicitly a draft milestone; four-point `review_b01.md` completes all P1–P4 source sections in the same session, with three quizzes and a five-minute practice.
- All main-text chapter references checked including Mermaid, README, rules and task prompts. The remaining external-source §1.2 is intentionally the cited source's section. Historical chapter numbers remain under a visible original-numbering notice.
- Preserved current interactive-first flow and slash-command table. Installation/account facts were retained rather than researched or recharacterized in this editorial task.

## Consolidation and variation

- Repeated project creation and platform-specific install demonstrations are consolidated at the first applicable step; alternative install channels, maintenance and dependency internals remain fully available in Appendix A.
- Google-specific requirements/rules/installation and migration remain in Appendix B, outside the two-tool beginner path.
- Historical inventory, version entries, Python tests and Jev results remain dated in Appendix C; they are not presented as tests rerun by this change.
- Added platform bridges, explicit optional-Python assessment scope and a combined pre-task Git checkpoint. Corrected the historical-version table's row continuity and macOS interpreter-picker shortcut.
- No substantive source topic intentionally omitted. Detailed original-to-new mapping is in content-map.md and section-map.json.

This is an editorial self-check, not the independent specification/quality review or final rendered-site verification.
