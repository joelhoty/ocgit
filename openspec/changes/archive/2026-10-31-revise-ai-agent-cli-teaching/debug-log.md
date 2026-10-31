# Debug log

## Browser verification environment
- Reproduction: Playwright default chromium launch failed because bundled browser executable is absent.
- Comparison: locally installed Google Chrome exists; channel=chrome launched but sandboxed process exited SIGABRT.
- Hypothesis: host process sandbox prevents Chrome startup, independent of curriculum files.
- Minimal test: same isolated headless Chrome call under approved execution escalation succeeded (`Browser check`).
- Resolution: use installed Chrome with temporary Playwright profile for visual tests; no personal profile or accounts.

## Index first-unit wording
- Independent spec review found two old AI Studio references in first card.
- Root cause: initial replacement map covered Gemini CLI only; first unit used a separate web product name.
- Fix: first-unit card now names Codex CLI／Claude Code, consistent with updated first-unit content.
- Verification: search for AI Studio in new index has no match; final reviewer will reconfirm.

## Mermaid HTML break escaping
- Independent spec review compared code fences with generated DOM, finding literal br children inside three Mermaid containers.
- Root cause: converter unescapes all HTML entities before inserting diagram source; HTML parser consumes Mermaid label markup.
- Resolution in final navigation integration: rebuild every Mermaid container from its matching Markdown fence as a text node.
- Verification: full browser run checks diagram count equals rendered SVG count and no syntax errors; final paired-source check confirms literal source.

## Browser checker callback API
- Actual run failed at remove_all_listeners: Python Playwright exposes remove_listener(event, handler).
- Fix: retain callback identity and remove that callback after each page. No course changes.
- Full browser check is rerun; prior incomplete attempt does not count as verification.

## Task3: CLI consumes report-loop stdin

- Root cause: `done < student_list.txt` supplies stdin to both `read` and the child CLI; an stdin-consuming child drains remaining student IDs.
- Reproduction: task-3-stdin-red-v2.json executes the actual extracted script with model calls replaced by a stdin-consuming shell function; only student_A report exists in both routes. Earlier red-v1 fed the script over stdin and is an invalid harness result, retained for diagnosis, superseded by red-v2 using a script file.
- Pattern/hypothesis: isolate the child stdin while preserving loop stdin. A single `</dev/null` on each inner CLI prevents it consuming student_list.txt.
- Fix: applied to Markdown and HTML surgically, preserving navigation.
- Verification: task-3-stdin-green-v1.json has all three reports for both routes. No paid CLI calls were executed.
- Additional document quality fixes: Google Docs Open→Upload path and Markdown mode distinction, plus removed residual browser-save-as-DOCX claim; official sources cited in both artifacts.
