---
name: sos-verify
description: "Use when implementation is complete, before claiming work is done, or before archiving research findings — verifies against specs or evidence across three dimensions and writes a persistent verification report"
---

# Spec Verify

Verify that implementation or research output is complete, correct, and coherent. Write a persistent verification report.

**Core principle:** No work is "done" until verified against its spec or evidence. Evidence before claims, always.

## When to Use

- After all tasks in `sos-apply` are complete
- Before running `sos-archive`
- When user asks "is it done?", "verify", "check implementation"
- Anytime you're about to claim work is complete
- When verifying research output, conclusions, or factual claims

## Operating Modes

Choose the correct mode based on what you're verifying:

### Mode 1 — Spec Mode (default)

Verifying a code or documentation change against `openspec/changes/<change>/` specs.

**When:** After `sos-apply` completes, before `sos-archive`.
**Evidence items:** Test command output, linter output, build exit code, spec coverage checklist.

### Mode 2 — Research Mode (`sos-verify --mode=research`)

Verifying research conclusions, factual claims, or analysis outputs.

**When:** After producing research notes, analysis reports, literature reviews, or factual summaries.
**Evidence items:** Source URLs, citations, data file paths, reproduction steps. Shell commands are not required — any traceable evidence item qualifies.

**Decision tree:**
```
Are you verifying an implementation (code/docs)?  → Spec Mode
Are you verifying research conclusions or facts?  → Research Mode
```

## The Iron Law

```
NO COMPLETION CLAIMS WITHOUT VALID, SUFFICIENT VERIFICATION EVIDENCE
```

In Spec Mode, identity-valid structured evidence can be fresh enough for a
**Standard focused automated check**. It is reusable only after independent
matrix classification, manifest validation, and explicit requirement mapping.
An unstructured statement such as
"passed earlier," a prior message, or an agent success report is never evidence.

The verifier itself MUST freshly run the complete regression suite and every
High-risk check before PASS. Destructive behavior, user-state changes,
migrations, and atomic failure paths are High-risk; prior apply evidence and
representative sampling cannot satisfy them.

This refinement permits safe, narrow reuse. It does not relax completion-claim
rigor: invalid, insufficient, missing, malformed, stale, incompatible, or
unmapped evidence cannot support PASS.

**For Research Mode:** An "unverified claim" is any conclusion stated without at least one traceable evidence item. Such claims must be labeled `[UNVERIFIED]` in the report and cannot be archived.

**Violating the letter of this rule is violating the spirit of this rule.**

## The Gate Function

```
BEFORE claiming any status or expressing satisfaction:

1. IDENTIFY: What command / evidence item proves this claim?
2. VALIDATE: In Spec Mode, independently validate any structured evidence and
             its requirement mapping; invalidate it when identity or policy
             checks fail
3. RUN:     Execute the FULL regression suite and all High-risk checks (fresh)
            Execute invalidated or uncovered Standard-risk checks as needed
            OR: Cite the source / URL / data path for the claim
4. READ:    Full output, check exit code, count failures
            OR: Read the cited source and confirm it supports the claim
5. VERIFY:  Does the complete requirement-to-evidence matrix and output/source
            confirm the claim?
            - If NO: State actual status with evidence
            - If YES: State claim WITH evidence
6. ONLY THEN: Make the claim

Skip any step = lying, not verifying
```

## The Three Dimensions

### 1. Completeness — Is everything built / covered?

| Check | Spec Mode Method | Research Mode Method |
|-------|-----------------|----------------------|
| All task groups done | Every task group in tasks.md is complete, with no unchecked task | All research sub-questions have conclusions |
| Explicit requirement coverage | Independently map every requirement and scenario to sufficient evidence | Every stated research topic has findings |
| Minimal sufficient scenario evidence | Parameterized, invariant, or integration evidence may cover multiple scenarios when the mapping and sufficiency are explicit; a unique test function per scenario is not required | Every major claim has an evidence item |
| No missing edge cases | Boundary conditions from specs are handled | Counter-arguments addressed or noted |

### 2. Correctness — Is it built / claimed right?

| Check | Spec Mode Method | Research Mode Method |
|-------|-----------------|----------------------|
| Evidence is valid | Reuse only identity-valid Standard focused automated evidence after independent matrix classification; rerun invalidated or uncovered checks | Each conclusion has a verifiable source |
| Final gates pass | Freshly run the full regression suite and every High-risk check, and inspect exit codes/results | Each conclusion has a verifiable source |
| Behavior matches spec | Compare actual behavior against spec scenarios | Claims match what the cited source actually says |
| Error handling works | Test failure modes described in design.md | Contradictory evidence is acknowledged |
| No regressions | Fresh complete regression result passes | Consistent with previously accepted facts |

### 3. Coherence — Does it fit together?

| Check | Spec Mode Method | Research Mode Method |
|-------|-----------------|----------------------|
| Design reflected in code | Architecture from design.md matches implementation | Conclusions are internally consistent |
| Naming consistent | Terms from specs used consistently in code | Terminology used consistently throughout |
| Interfaces match | APIs match contracts in design.md | References cited consistently across sections |
| Evidence identity coherent | Subject and policy identities match the verified change; tool versions are compatible | References cited consistently across sections |
| Gaps agree with verdict | Evidence gaps and manual gaps are explicit and cannot be hidden by an aggregate PASS | No unsupported side-claims in conclusions |
| No orphaned code | Every new file/function serves a spec requirement | No unsupported side-claims in conclusions |

## Spec Mode Evidence Policy

### Independent matrix properties

For every evidence need, verify independently derives three separate matrix
properties from the **current spec, design, and task contract**:

- `risk: standard | high` — consequence and safety exposure;
- `coverage_mode: exhaustive | representative | focused` — what portion of the
  required behavior the evidence must cover; and
- `execution_mode: automated | manual` — how the check is performed.

Do not copy any of these properties from the evidence manifest. In particular,
manifest `kind` is not the matrix classification:

- After its schema, tool, and identity checks pass, `kind: automated` proves
  only `execution_mode: automated`; it never proves exhaustive coverage.
- `kind: representative` is only candidate representative evidence. Verify
  independently validates the sampling rule, selected cases, observations, and
  limitations before assigning representative coverage.
- `kind: high-risk` is only a candidate evidence record. It cannot establish or
  downgrade risk and cannot override independently assigned risk.

The named evidence policies are derived combinations of the separate fields:

- **Exhaustive automated** = `coverage_mode: exhaustive` plus
  `execution_mode: automated`; it proves a bounded property across the full
  subject, such as a full suite, schema check, link check, uniqueness invariant,
  or parser pass.
- **Representative manual** = `coverage_mode: representative` plus
  `execution_mode: manual`; record and validate the sampling rule, selected
  cases, observations, and limitations.
- **High-risk focused** = `risk: high` plus `coverage_mode: focused`; execution
  may be automated or manual, but verify must run/reproduce it freshly.

Only evidence independently classified as `risk: standard`,
`coverage_mode: focused`, and `execution_mode: automated` is eligible for
selective reuse, and only after all identity and mapping checks pass.

Every requirement and scenario MUST map to sufficient evidence. One evidence
item may cover multiple scenarios when a parameterized test, invariant, or
integration check actually proves them and the matrix lists every mapping.
Never require a distinct test function merely to make scenario counts match.

### Deterministic generated output

For deterministic generated output, the minimal sufficient coverage is:

1. exhaustive automated invariants over all generated artifacts, including
   schema validity, internal links, uniqueness, and parseability; and
2. representative manual samples covering normal, complex, and
   missing/ambiguous/unmapped inputs.

Record the sample selection and result. Do not manually inspect every generated
page. If any generated behavior is High-risk, the High-risk rule overrides this
sampling rule and requires a fresh focused execution or reproduction.

### Evidence manifest contract

When an apply-stage evidence manifest exists, treat it as an input to verify,
not as a verdict. Validate at least:

- supported manifest schema and required fields;
- subject identity and digest (change, source, inputs, and relevant artifacts);
- verification-policy identity and digest;
- evidence item identity and evidence-payload digest, manifest `kind`, command
  or procedure, result, artifact digest, declared TTL/expiry, and
  requirement/scenario mappings;
- producer/tool version compatibility;
- declared manual gaps and other coverage gaps; and
- complete, sufficient coverage of the independently derived matrix.

Require the manifest's stable check/task/requirement IDs, subject constituents
and hash, command/procedure, automated tool or manual actor identity, policy
inputs and aggregate hash, result, immutable evidence path/digest, capture time,
and manual-gap records to agree internally. Recompute canonical subject, policy,
and evidence digests rather than trusting recorded hash strings.

For every check, independently reconstruct and validate the four separate,
anchored `policy_inputs` kinds defined by apply:

1. **`task_contract`** — require exactly one selected task-contract entry for
   this task/check. Re-select the exact recorded task-group or legacy-unit
   anchor; an omitted task identity or an entry for a different task is invalid.
2. **`spec_requirement`** — require one exact applicable entry for every
   requirement reference mapped to the check. Resolve canonical IDs by the
   exact unique canonical heading prefix and ID boundary
   `### Requirement: <ID> — <requirement name>`, not by comparing a heading to
   the bare ID. Permit the read-only legacy separate-`**ID:**` fallback only
   under the rule below. Reproduce conservative all-requirements or
   `LEGACY-<hash>` mappings from their anchors; reject missing, duplicate,
   ambiguous, extra-substitution, or cross-requirement matches.
3. **`design_constraint`** — require every applicable design entry using its
   exact recorded heading anchor. When apply recorded its conservative
   whole-file fallback, require the exact recorded path with
   `source_anchor: "<whole-file>"`; never infer a narrower replacement or allow
   omitted design identity.
4. **`verification_policy`** — require every active verification-policy file,
   including this skill, every loaded verification configuration/policy, and
   every active project override. Reject a newly active override or policy file
   that is absent from the recorded path inventory.

For all four kinds, normalize and validate repo-relative POSIX `source_path`
values, exact `source_anchor` values, and the complete recorded path inventory.
Apply each entry's recorded canonicalization name/version to the re-selected
bytes, then recompute and compare every individual digest. Reject unsupported
canonicalization versions and duplicate `(kind, source_path, source_anchor)`
tuples. Finally, bytewise-sort the validated tuples by
`(kind, source_path, source_anchor)`, reproduce the recorded canonical aggregate
listing, recompute `policy_hash`, and require an exact match.

Unknown schema versions, malformed fields, missing digests, incompatible tools,
expired evidence, digest mismatches, or mappings that cannot be reproduced are
invalid. Any missing or mismatched policy kind, path, anchor, individual digest,
or aggregate `policy_hash` invalidates each governed check and forces its rerun;
task or design identity may never be omitted to obtain PASS. Changed or missing
subject, policy, or evidence identity—and expiry under a declared non-null
TTL—likewise invalidate every affected item. A policy change invalidates all
checks governed by that policy. Do not silently broaden a valid item's scope.

Only valid evidence independently classified as **Standard focused automated**
may be reused. Full regression results and High-risk checks are never reused for
the final gate: verify runs them freshly regardless of apply-stage evidence. The
requirement coverage review is also always performed independently.

Read the change metadata's `evidence_schema` marker before handling a missing
manifest. If it declares `sos-evidence/v1`, a missing manifest is CRITICAL and
PASS-blocking. A missing marker does not make a change legacy.

The absent-manifest legacy path requires positive immutable provenance that the
change's initial artifacts predate project/schema adoption. In a VCS project,
compare the immutable initial artifact commit with a recorded adoption
commit/tag/release marker. In a non-git (non-VCS) project, require a pre-existing
project adoption/legacy registry or another immutable approved/archive record.
Record the provenance type, identifiers, comparison, and conclusion in the
verification report. A change's own assertion that it is "legacy" is never
sufficient.

If positive provenance is established, use the safe legacy path: derive the
matrix independently and obtain all required evidence freshly. If provenance
cannot be established, fail closed and require manifest reconciliation; never
infer legacy from an absent marker or missing file. If a manifest is expected
but missing, or if a present manifest is malformed or stale, preserve and report
the invalid record, create a valid replacement from rerun evidence, and do not
PASS while its status remains missing, malformed, or stale.

## Common Failures

| Claim | Requires | Not Sufficient |
|-------|----------|----------------|
| Tests pass | Test command output: 0 failures | Unstructured, stale, or identity-invalid previous run; "should pass" |
| Linter clean | Linter output: 0 errors | Partial check, extrapolation |
| Build succeeds | Build command: exit 0 | Linter passing, logs look good |
| Bug fixed | Test original symptom: passes | Code changed, assumed fixed |
| Regression test works | Red-green cycle verified | Test passes once |
| Agent completed | VCS diff shows changes | Agent reports "success" |
| Requirements met | Independent requirement-to-evidence matrix with sufficient coverage | Tests passing or an apply-stage verdict |
| Standard focused automated check passes | Independently classified, identity-valid structured evidence, or a fresh rerun | Unstructured "passed earlier" or manifest `kind` alone |
| Evidence is reusable | Valid schema, identities/digests, compatibility, freshness, and explicit mapping | Manifest exists |
| High-risk path works | Fresh independent execution/reproduction by verify | Prior evidence or representative sampling |
| Research conclusion valid | Source URL / citation that confirms claim | "Everyone knows", "it's obvious" |
| Data fact accurate | Original data file path + value quoted | Summarized by a secondary source |

Valid structured selective reuse is allowed only for independently classified
Standard focused automated evidence under the rules above. This exception never
permits reuse of the final regression suite or a High-risk check.

## The Process

### Step 1: Read All Artifacts

**Spec Mode:**
- `tasks.md` — check all tasks marked complete
- `specs/<domain>/spec.md` — requirements to verify against
- `design.md` — architecture to verify against
- `review-report.md` — any prior issues to re-check

**Research Mode:**
- Research document or notes to verify
- List of conclusions / claims to check

Verification is called while the change lifecycle status is `verifying`. A PASS
allows `sos-apply` to set the status to `completed`; verify does not set that
status itself. FAIL or PASS-blocking gaps leave the status `verifying` for fixes
and another verification run.

Before building the matrix, independently parse task groups and requirement
references using the apply contract. A new outcome group has exactly one Risk
line and one primary outcome. When `Risk: High`, it must also contain exactly
one `High-risk safety gate:` and exactly one `High-risk failure-path gate:`;
missing or duplicate gates are a parse/reconciliation blocker and cannot be
repaired by Standard evidence. A Standard task cannot claim High-risk evidence
using absent gates. Legacy tasks are not forced to migrate or add these
persistent checkboxes, but independently classified High-risk legacy behavior
still requires fresh High-risk verification.

For each `Covers` ID, resolve an exact unique canonical heading prefix plus ID
boundary: `### Requirement: <ID> — <requirement name>`. The ID must be followed
by the space/em-dash/space boundary and a non-empty name; a bare-ID heading,
partial prefix, or body occurrence is not a canonical match. Missing,
duplicate, or ambiguous matches fail closed. An old requirement section with a
separate `**ID:**` may be read only as legacy input when there is no canonical
match; verify never generates that form.

For a legacy task without `Covers`, reproduce apply's binding: prefer exact
unique ID, exact name, or exact heading/source-anchor references already in the
unit; otherwise bind conservatively to all delta requirements. With no delta
requirements, recompute the deterministic `LEGACY-<hash>` from normalized spec,
proposal, design, and task anchors and independently review the binding. Any
all-delta binding must be reproduced from the original, non-deduplicated
canonical headings: each ID must occur exactly once before bytewise sorting.
Malformed headings or duplicate IDs fail closed. Any missing or ambiguous
claimed reference fails closed. Keep manifest requirement
references non-empty and deterministic. Report legacy requirement references explicitly,
including the binding strategy and anchors.

### Step 2: Build the Independent Requirement-to-Evidence Matrix

**Spec Mode only:**

1. Derive the complete list of requirements and scenarios directly from the
   current specs. Do not copy coverage conclusions from apply output.
2. Add task-group completion, relevant design interfaces, failure paths, and
   generated-output invariants/samples.
3. Independently assign `risk: standard | high`,
   `coverage_mode: exhaustive | representative | focused`, and
   `execution_mode: automated | manual` from the current spec, design, and task
   contract. Do not derive them from manifest `kind`.
4. Map proposed evidence to every requirement and scenario. Shared evidence is
   allowed only when its parameterization, invariant, or integration scope is
   explicit and sufficient.
5. Mark evidence gaps and manual gaps before considering reuse.

The matrix is the coverage authority for this verification run.

### Step 3: Validate, Reuse, or Invalidate Structured Evidence

**Spec Mode only:**

For each manifest and evidence item, apply this algorithm in order:

1. **Validate structure** — schema/version and all required fields parse.
2. **Validate identity** — subject and inputs/artifacts match; independently
   reconstruct all four anchored policy-input kinds, apply their recorded
   canonicalization versions, compare individual digests, and compare the
   bytewise-sorted aggregate `policy_hash` to the current verification target.
3. **Validate compatibility and time** — producer/tool versions are compatible
   and the evidence has not expired.
4. **Validate result and mapping** — commands/procedures, artifacts, outcome,
   independently assigned matrix properties, manifest-`kind` candidate semantics,
   and explicit requirement/scenario coverage agree. `kind: automated` proves
   `execution_mode: automated` only; representative samples require independent
   validation; `kind: high-risk` cannot establish or downgrade risk.
5. **Invalidate affected evidence** — any missing, changed, stale, expired,
   incompatible, or malformed identity forces the affected check to rerun.
6. **Reuse narrowly** — only a still-valid item independently classified as
   `risk: standard`, `coverage_mode: focused`, and
   `execution_mode: automated` may be marked `reused`; never reuse it for
   requirements outside its mapping.

Record an evidence status for each matrix row:

- `reused` — valid structured Standard focused automated evidence was accepted;
- `rerun` — prior evidence existed but was invalidated or a mandatory fresh
  gate applied, so verify executed it again; or
- `fresh` — verify obtained new evidence where no reusable item existed.

A malformed, stale, or expected-but-missing manifest is a blocking validation
failure until every affected item is rerun and valid replacement evidence is
recorded. An absent manifest takes the fully fresh legacy path only after the
positive immutable provenance check above passes.

### Step 4: Run Verification Commands / Gather Evidence

**Spec Mode:**
```
1. IDENTIFY: What commands/procedures satisfy uncovered or invalidated rows?
2. RUN:      Execute the FULL regression suite (fresh, complete)
3. RUN:      Execute/reproduce EVERY High-risk path (fresh, independent)
4. RUN:      Execute remaining Standard checks needed for complete coverage
5. READ:     Full output, check exit codes, count failures, inspect manual results
6. VERIFY:   Does the matrix confirm every requirement and scenario?
```

**Mandatory checks (Spec Mode):**
- Run full regression suite freshly → record command, exit code, and result
- Run every High-risk check freshly and independently → record reproduction and result
- Run linter (if configured) → record result
- Run build (if applicable) → record result
- Complete representative manual samples where required → record selection,
  observations, and manual gaps

**Research Mode:**
- For each conclusion: identify source URL / citation / data path
- Open / read the source and confirm it supports the claim
- Mark unsupported conclusions as `[UNVERIFIED]`

### Step 5: Spec-by-Spec / Claim-by-Claim Verification

For EACH requirement (Spec Mode) or conclusion (Research Mode):

1. Read the requirement / claim
2. Find the corresponding implementation / evidence item
3. Verify coverage and sufficiency / source support
4. In Spec Mode, confirm evidence status, independently assigned risk,
   coverage mode, execution mode, manifest-`kind` interpretation, and gaps
5. Record: ✅ PASS, ⚠️ WARNING, or ❌ FAIL

No aggregate suite result can replace this independent coverage review.

### Step 6: Issue Classification

| Level | Description | Action |
|-------|-------------|--------|
| **CRITICAL** | Any required scenario, specified boundary/edge case, required failure path, or required evidence is missing/failing; any required manual gap is unresolved; or a Research claim is unsupported | PASS-blocking; must fix or provide sufficient evidence before archive |
| **WARNING** | Non-required improvement, maintainability suggestion, or source/sample-quality concern that leaves no requirement uncovered; in Research Mode, a weak secondary source only when the claim remains adequately supported | May pass if explicitly reported and the matrix remains complete |
| **SUGGESTION** | Optional opportunity unrelated to required coverage | Note for future |

Never downgrade a required coverage or evidence gap to WARNING. An unsupported
Research Mode claim is CRITICAL, remains `[UNVERIFIED]`, and cannot be archived.

### Step 7: Write Verification Report

Write to `openspec/changes/<change-name>/verification-report.md`.

**Spec Mode report template:**

```markdown
# Verification Report: <Change Name>

**Date:** YYYY-MM-DD
**Mode:** Spec Mode
**Status:** ✅ PASS / ⚠️ PASS WITH WARNINGS / ❌ FAIL

## Test Results
- Full regression suite (fresh): [PASS/FAIL] — [command, exit code, N/N]
- High-risk checks (fresh): [PASS/FAIL] — [N/N]
- Linter: [PASS/FAIL/N/A]
- Build: [PASS/FAIL/N/A]

## Completeness
- Task groups: [N/N] complete
- Spec requirements: [N/N] implemented
- Requirements with sufficient evidence: [N/N]
- Scenarios with explicit sufficient mapping: [N/N]

## Evidence Manifest Validation
- Evidence schema marker: [sos-evidence/v1 / absent]
- Manifest: [valid / provenance-proven legacy fresh path / invalid]
- Legacy provenance: [N/A or immutable source, identifiers, comparison, conclusion]
- Schema and tool compatibility: [result]
- Subject digest: [result]
- Policy digest: [result]
- Invalidations and forced reruns: [list]

## Requirement-to-Evidence Matrix
| Requirement / Scenario | Risk | Coverage Mode | Execution Mode | Manifest Kind | Evidence / Command | Status | Result | Gaps |
|------------------------|------|---------------|----------------|---------------|--------------------|--------|--------|------|
| REQ-... / Scenario ... | standard/high | exhaustive/representative/focused | automated/manual | automated/representative/high-risk/N/A | ID or command | reused/rerun/fresh | PASS/FAIL | none or detail |

## Per-Requirement Verification

### Requirement: REQ-<DOMAIN>-NNN — <Name>
- Implementation: `path/to/file.ts:L42`
- Evidence: [IDs, commands, procedures, artifacts]
- Evidence status: [reused/rerun/fresh]
- Risk: [standard/high]
- Coverage mode: [exhaustive/representative/focused]
- Execution mode: [automated/manual]
- Manifest kind and interpretation: [value and candidate-only validation]
- Scenarios: [explicit mappings and sufficiency]
- Gaps/manual gaps: [none or details]
- Status: ✅ PASS

## Coherence Check
- Design alignment: ✅
- Naming consistency: ✅
- Interface contracts: ✅
- Evidence identity and policy alignment: ✅
- Gaps consistent with verdict: ✅

## Commands and Results
| Command / Procedure | Purpose | Freshness | Exit / Observation | Result |
|---------------------|---------|-----------|--------------------|--------|

## Risks and Gaps
- High-risk paths: [list and fresh results]
- Evidence gaps: [none or list]
- Manual gaps: [none or list]

## Issues Summary
| # | Severity | Requirement | Issue |
|---|----------|-------------|-------|

## Conclusion
[Overall assessment and recommendation: archive-ready or needs fixes]
```

The Spec Mode report is archive-ready only when it exposes the independent
matrix, all evidence statuses (`reused`, `rerun`, or `fresh`), independently
assigned risk/coverage/execution properties, manifest-kind interpretation,
legacy provenance when used, evidence and manual gaps, per-requirement results,
commands/results, and a verdict that agrees with those details.

**Research Mode report template (also append to `docs/project_notes/research.md` when memory is enabled):**

```markdown
# Verification Report: <Research Topic>

**Date:** YYYY-MM-DD
**Mode:** Research Mode
**Status:** ✅ VERIFIED / ⚠️ PARTIAL / ❌ UNVERIFIED CLAIMS PRESENT

## Claims Verification
| Claim | Evidence Item | Source | Status |
|-------|--------------|--------|--------|
| [conclusion 1] | [URL / citation] | [author/date] | ✅ |
| [conclusion 2] | — | — | [UNVERIFIED] |

## Unverified Claims
[List claims that could not be backed with evidence.
These cannot be archived as fact and must be labeled [UNVERIFIED] in any downstream document.]

## Conclusion
[Summary of verified findings and outstanding gaps]
```

### Step 8: Handle Results

**If all PASS:**
> "Verification complete — all specs verified. `sos-apply` may set the change
> to `completed`; it is then ready for `sos-archive`."

**If CRITICAL issues found:**
> "Verification found [N] critical issues. These must be fixed before archiving:
> 1. [issue description]
> The change remains `verifying`. Fix these and run `sos-verify` again."

**If only WARNINGS:**
> "Verification passed with [N] warnings. `sos-apply` may set the change to
> `completed`; then archive it, or fix the warnings first."

### Step 9: Sync to Project Memory

**Skip this step entirely if `docs/project_notes/` does not exist.**

**Spec Mode** — append verification outcome to `issues.md`:
```
sos_memory_add issues <<EOF
## YYYY-MM-DD HH:MM — <change-name> verification PASS

Result: PASS [WITH N WARNINGS]
Tests: <pass>/<total>
Report: openspec/changes/<change-name>/verification-report.md
EOF
```

**Research Mode** — append verified conclusions to `research.md`:
```
sos_memory_add research <<EOF
## YYYY-MM-DD HH:MM — <research-topic>

[Verified conclusions with source citations]
Report: openspec/changes/<change-name>/verification-report.md
EOF
```

## Integration with sos-memory

When `docs/project_notes/` exists, `sos-verify` writes to project memory at Step 9:

| Mode | Target File | Content |
|------|------------|---------|
| Spec Mode | `issues.md` | Verification outcome (PASS/FAIL, test counts, report link) |
| Research Mode | `research.md` | Verified conclusions with source citations |

**Rule:** Unverified claims (`[UNVERIFIED]`) are **never** written to memory — they stay only in the verification report until evidence is provided.

The integration point is Step 9. Do not write to memory before the verification report is written.

## Red Flags — STOP

- Claiming "done" without running verification commands or citing evidence
- Using "should pass", "probably works", "looks correct"
- Skipping spec-by-spec / claim-by-claim check
- Trusting subagent success reports without independent verification
- Partial verification ("tests pass so it's done")
- Reusing evidence without validating manifest schema, identities/digests,
  compatibility, mappings, and gaps
- Reusing full regression or High-risk evidence instead of running it freshly
- Treating representative samples as proof of a destructive or atomic failure path
- Research Mode: stating a conclusion without a traceable source
- Research Mode: treating secondary summaries as primary evidence

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "Should work now" | RUN the verification |
| "I'm confident" | Confidence ≠ evidence |
| "Just this once" | No exceptions |
| "Linter passed" | Linter ≠ compiler |
| "Agent said success" | Verify independently |
| "Partial check is enough" | Partial proves nothing |
| "The manifest says PASS" | Validate identities, payload, mapping, and gaps independently |
| "Apply already tested the risky path" | Verify reruns every High-risk path freshly |

## Integration

**Consumed by:**
- `sos-apply` — calls this after all tasks complete
- `sos-archive` — checks this report before archiving

**Produces:**
- `verification-report.md` (persistent, in change directory)
- `docs/project_notes/research.md` updates (Research Mode, when memory enabled)
