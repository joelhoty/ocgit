# Task 2 independent specification review — v1

Reviewer: task1_intro (not Task2 author). Date: 2026-10-31.

Result: **PASS** against REQ-TEACH-002/003/004/008 and approved-amendment.md final filenames. No blocking findings.

## Scope and comparison

Read all five final Task2 files and compared original structure with git show HEAD:GeminiForDesignTeaching/<original>.html (live old files are now redirect pages).

- 07_agents_cli retains Agent/CLI concepts, relation, local workflow/refactoring scenario, detailed installation/use, six advanced examples, three instruction examples, and Python/C++ appendix. Text is shorter (13,369 to 10,354 extracted characters including navigation), but removed repetitions/obsolete Gemini-specific mechanics are replaced with substantive dual-tool tasks, not a summary. Original teaching functions remain.
- 08_environment retains four parts: CLI installation/troubleshooting, VS Code, Python/uv, project collaboration. Adds reproducible dependency/run checks; sample average is 80.0. Python dependencies are correctly separate from native CLI installation.
- 09_cli_practice retains six sections and four progressive levels, including all three research/life-use subscenarios. Each now has input, task, expected artifact and acceptance criteria; selected tool can complete the route without requiring the other.
- 05_instructions retains full role/workflow explanation, six subject templates, advanced practices, extensions, exercises and FAQ. Both tools have an explicit effective instruction path, tested loading and artifact checks.

## Correctness checks

Installation is platform- and package-manager-specific; version/login checks, update route, PATH/error diagnosis, interactive prompts and shell commands are distinct. Codex exec and Claude -p are not conflated; write permissions and noninteractive caveats are explained. Piped stdin with a separate Codex prompt is supported by the current official page.

Claude direct AGENTS support is qualified by version and file precedence; portable CLAUDE.md importing @AGENTS.md is the teaching route. /context is explicitly used for loaded Memory files. Text instructions, tool permissions and sandbox are separated; no claim that a role template enforces isolation.

The 05_instructions Markdown and HTML contain 22 corresponding code/diagram blocks; every decoded block is exact, including nested Markdown templates. H1/H2 pairs pass the course validator. Original subject templates remain full length.

## Official sources rechecked during independent review

- https://learn.chatgpt.com/docs/codex/cli — native install/update and first launch.
- https://learn.chatgpt.com/docs/non-interactive-mode — exec interface and prompt-plus-stdin context.
- https://code.claude.com/docs/en/setup — npm Node 22 requirement, optional Git on native Windows, native Windows versus WSL2 sandbox difference.
- https://code.claude.com/docs/en/memory — v2.1.277 direct AGENTS support, CLAUDE precedence, imports, /config and /context.

These checks occurred 2026-10-31 and agree with the cited teaching claims. Review did not run paid CLI requests or install on all platforms; those limitations are explicit in delivery evidence. Full visual evidence is handled by integration verification.

## Subject digests

- `AI_Agent_CLi/07_agents_cli.html`: `41871e933e502889d92bb65dd012e86be88c646593f0403f9f83580191da950e`
- `AI_Agent_CLi/08_environment.html`: `5925bc2783e7011b8535b756041bc67fee58b0d9c52d3923bd3a382f845d060b`
- `AI_Agent_CLi/09_cli_practice.html`: `97d7153e55c7173283ef2944f8b51d3d85063895c21512ad3f75fc3ae224808f`
- `AI_Agent_CLi/05_instructions.md`: `9d87eec81c23d130106009f764d9723eb0c9d1d2d762e775bc7e0e8d9248a4ca`
- `AI_Agent_CLi/05_instructions.html`: `7eef27074176fed45b8c485e33f8b3e6038168481186129e1d8d2178199d7d9e`
