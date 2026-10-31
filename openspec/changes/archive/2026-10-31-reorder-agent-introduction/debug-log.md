# Debug log: browser navigation harness

2026-10-31, verification tooling only; no course-content defect found.

## Root cause investigation
Full no-JS browser run remained live without producing a case result. A four-fragment diagnostic printed initial navigation at0.692s, then stalled before the first fragment, locating the stall at add_style_tag. Removing only that operation completed four fragment navigations in milliseconds, proving navigation itself works. add_style_tag was awaiting style completion on a JS-disabled page.

## Pattern and controlled fix
The prior successful compatibility checks did not inject styles. Smooth scrolling still needs to be disabled to measure final positions reliably. Replace async style-tag insertion with synchronous inline style property assignment via the automation runtime; page JavaScript remains disabled. Controlled four-fragment run: initial0.697s; ai-agent/intro scroll112; 510 scroll18297 and slash-commands18305, an8px difference. Each navigation completed under0.01s.

## Execution
Stopped only the two identified stalled test processes (PIDs31286 and45888) after confirming the cause. Neither run produced passing evidence. No full run was restarted merely because an observation timed out. Run the corrected full harness and final verification to establish completion; reports are stored separately under evidence/.
