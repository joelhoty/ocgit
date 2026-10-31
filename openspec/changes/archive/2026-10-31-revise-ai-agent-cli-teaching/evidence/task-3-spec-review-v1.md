# Task 3 independent specification review — v1

Reviewer: task1_intro, independent of Task3 author. Date: 2026-10-31.

Result: **PASS for substantive teaching-content scope**, after corrections during review. Common navigation, final topic-based English filenames, representative browser proof and final rendered Mermaid normalization remain integration checks, not declared complete here.

## Contract and coverage

Reviewed Task3 against approved design/tasks and REQ-TEACH-002/005/008. Compared original Markdown headings and teaching purpose, inspected new paired pages, practical inputs/prompts/outputs, code blocks and official feature claims. All 18 expected files exist. All original H2 teaching sections remain in the eight Markdown sources; new text is at least as long as the original in each case. Original exercise progression and literacy materials remain, not replaced with summaries.

- Unit1: dual interactive entry, concrete prompt/material/reflection outputs and acceptance criteria.
- Unit2: CLI produces image prompt; actual bitmap generation is an explicitly separate web tool, subject to account availability.
- Unit3: source-grounded notebook activity retained, exported source_notes.md explicitly prepared before CLI worksheet generation. Current Google official naming is explained without implying automatic CLI browser access.
- Unit4: shell versus session prompts, separate interactive/noninteractive interfaces, Git working-folder prerequisite and redirection overwrite behavior are distinguished.
- Unit6: guided source-to-lesson workflow, shared context across turns and project-instruction filenames distinguished. Source fidelity and human checks remain.
- Supplements: dual executable routes, dependency notes, document-export limitations, fake-data privacy boundaries, reproducible grading formula and arithmetic. Recalculation confirms totals 84.10/89.65/73.65/89.60/70.75 and published rounded means/standard deviations.

## Issues found and corrected before this report

1. weekly_report.sh could continue after failed cd/CLI and print success. Both routes now use set -euo pipefail, quote the working path, check nonempty output and label the result a draft. Paired HTML includes correction. task-3-script-failure-v1.txt additionally records failure-branch checks using a substituted failing command; this is not an actual CLI execution test.
2. Markdown PDF capabilities were stale. Current prose and comparison table now correctly list PDF/HTML/PNG/JPEG, Mermaid/PlantUML/KaTeX and required browser availability, with official Marketplace source and check date. Paired HTML includes correction.

## Independent code-fence inspection

Line-based fence parsing, including nested shorter fences, paired every source block with its rendered pre/code or div.mermaid in order:

| Pair | Source / rendered blocks |
|---|---:|
| unit01 | 32 / 32 |
| unit02 | 28 / 28 |
| unit03 | 45 / 45 |
| unit04 | 47 / 47 |
| unit04 supplement | 45 / 45 |
| unit06 | 40 / 40 |
| unit06 supplement | 46 / 46 |
| literacy research | 0 / 0 |

All non-Mermaid code text matches exactly. Three Mermaid blocks (unit04 main, unit04 supplement, unit06 supplement) have literal HTML br elements rather than escaped source text; parent informed to normalize during common rendering, as done for Task1. They retain the graph nodes/edges but line-break fidelity needs the final browser/render check. This is a known integration follow-up, not proof of final visual acceptance.

## Primary sources inspected

- https://support.google.com/gemininotebook/answer/16164461 — current Gemini Notebook naming and source-based capabilities.
- https://learn.chatgpt.com/docs/non-interactive-mode — codex exec default read-only and output behavior.
- https://marketplace.visualstudio.com/items?itemName=yzane.markdown-pdf — current exports, browser dependencies and diagram/math support.
- https://code.visualstudio.com/docs/languages/markdown — Markdown editor context.

No paid CLI calls or platform installation were executed by this reviewer. Final link/anchor, renamed-path and desktop/mobile evidence remains parent integration work under REQ-TEACH-008.

## Reviewed subject digests

- `AI_Agent_CLi/literacy_b02.html`: `55f68908032e48e3835c986cb4a1fad9279fb809f5740141626235e8b869d185`
- `AI_Agent_CLi/literacy_chatgpt_revise_b06.html`: `cf18b9fcd4de32f0c98b67d648bbaf163e03f56385e041be9c6a9018e737ba87`
- `AI_Agent_CLi/literacy_research.html`: `c3056032bfb6ab38c4b7a72e6b6330e539c3a03f7a561cec92b1f14c8b026eff`
- `AI_Agent_CLi/literacy_research.md`: `69b41783746956c57c8b2537d147e0779e5787e405b0ec32b26c46e26640927d`
- `AI_Agent_CLi/unit01_first_ai_material_b02.html`: `e66aeb7e839a0ca5a400a06428089d857c2bb57d7649996472529017d96cda04`
- `AI_Agent_CLi/unit01_first_ai_material_b02.md`: `2780652af13a62f369f0d16795a71784d2bb327aac62702ad12668a3119527a2`
- `AI_Agent_CLi/unit02_ai_image_generation_b02.html`: `73e9b594406610076bfff9a7ba90d85480176c109ebe539e669dbbab5251d103`
- `AI_Agent_CLi/unit02_ai_image_generation_b02.md`: `23cf2e602feac206a064e0b212caf02e866f2ec095f98ed06c8947e92f847642`
- `AI_Agent_CLi/unit03_notebooklm_b02.html`: `06200c7e4e72f85832a99dbcce593dd80c9c4e088ba21443a4231f2597488819`
- `AI_Agent_CLi/unit03_notebooklm_b02.md`: `55f83828a29d4d7af164e0983373556cf3f49f34e640d713585aea13550fdfc2`
- `AI_Agent_CLi/unit04_local_ai_setup_b02.html`: `2e7adef95270ac358e8dde713f8ade65e9a29a177fc92cdb58f2ebe35d8c56b6`
- `AI_Agent_CLi/unit04_local_ai_setup_b02.md`: `a46f2c39dfc6d5a6d7ad588054ac9cfbe1b3708c067cb3393a4d26878cf229a7`
- `AI_Agent_CLi/unit04_supplement_additions.html`: `c5138c5a2ec2953a1ca4a64d493feb93b6be72ad8c37116c3e5dc8fdd6ca4e56`
- `AI_Agent_CLi/unit04_supplement_additions.md`: `8046766398191f80d7a374a14da1fe6cd22896381b692969fedd9d7f4cec1960`
- `AI_Agent_CLi/unit06_practical_lesson_plan_b02.html`: `65088f542c3c0c86e8a46f703bcc47264f345e8c61f6dd6b659ffec6199a9347`
- `AI_Agent_CLi/unit06_practical_lesson_plan_b02.md`: `0eab60742d90fafcddfd7205563c0c5ec39a80896ef59e9db632bbbb2fa7c542`
- `AI_Agent_CLi/unit06_supplement_additions.html`: `06d19b94700693e61d3446f1980456af6ee4746d08e5f367fa5bb3ce5390861c`
- `AI_Agent_CLi/unit06_supplement_additions.md`: `e72a69b4668d7f03de608447e30c66c40dfbe5cbb668919ebab7488c88059970`
