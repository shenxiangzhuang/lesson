---
name: lesson
description: Learn debugging, API design, or architecture through a real project, or turn completed work into a lesson. Use for explicit invocation or learning intent such as "help me understand", "learn together", or "write a lesson". Creates self-contained Markdown in the project's top-level lesson/ folder. Routine fixes, reviews, and optimizations do not trigger it by default.
---

# Lesson

Help users learn engineering judgment and future agents find, verify, and reuse insights. Assume the user has not read 99% of the project's code, without assuming they lack programming knowledge.

## Two entry points

| Entry | Intent | Approach |
| --- | --- | --- |
| Active learning | Learn about a bug, API, or architecture in the current project, optionally improving it together | Follow the workflow below, narrowing from context to one issue; implement only within the user's request |
| Retrospective | Turn an existing fix, design discussion, or change into a lesson, or rebuild a lesson | Read the code, discussion, diff, and validation evidence; use the same narrative without repeating completed work |

Enter on explicit invocation or clear learning or documentation intent. Keywords such as "bug", "API", or "optimize" alone are insufficient: "fix this bug" and "review this API" are ordinary development requests. Looking up an existing lesson does not require creating or rebuilding one.

Continue the learning workflow through follow-up questions, comparisons, and changes on the same topic. Exit when the user ends it, switches topics, or asks for development only. Do not carry the mode across unrelated tasks or enable automatic retrospectives.

## When to write

- **Learn and improve:** After analysis, tradeoffs, implementation, and validation of one issue. Record results and limits if validation is blocked.
- **Understand existing design:** Once its mechanism, constraints, and boundaries are clear; no code change is required.
- **Retrospective:** After checking existing evidence; do not repeat implementation.
- **Explicit progress record:** Write a self-contained interim lesson, separating facts, hypotheses, proposals, and completed changes.

Write at a coherent learning checkpoint, not every turn. Follow the replacement rules when revising a lesson.

## Scope and types

- Focus on one small question that fits in a sentence. The main use case is finding an API design issue, comparing options, and improving it together.
- `bug`: Explain a concrete failure, its symptoms, cause, fix, and validation.
- `design`: Explain how and why a system works, including APIs, architecture, data models, algorithms, and responsibility boundaries.
- Choose one type by the lesson's main purpose. Weave concepts into the narrative; do not add types or duplicate articles for classification.
- Skip mechanical changes with no clear learning value unless the user asks to learn from them. Never invent problems or unnecessary changes to produce a lesson.

## Workflow: context → focus → improve → context

1. **Establish context.** Identify the target project root. Search existing `lesson/` files and related docs, then check the current implementation. Read the API definition, implementation, callers, and tests to trace the real path. Keep background relevant; do not expand into a repository audit.
2. **Focus on one issue.** Briefly summarize relevant findings, then choose one based on the user's goal. Show its trigger and impact through a real call, input, or operation sequence. Leave other findings in the conversation without expanding the change.
3. **Reason together.** Explain the cause or constraints and the smallest useful improvement. Compare alternatives where real tradeoffs exist, including cost and compatibility. For misuse or missed detection, inspect hidden call ordering, representable invalid states, and gaps between tests and real usage. Explain mechanisms and gaps without blaming people; mark unsupported causes as unknown. Give the user room to question assumptions and shape key choices, without turning learning into a quiz or approval checklist. Do not finish the entire refactor before explaining it.
4. **Implement and validate.** Stay within the user's request and existing authorization. Analysis alone does not authorize implementation. Reproduce bugs before fixing them where possible; use a small, meaningful test or runnable example for design changes. Check relevant callers and boundaries. State blocked validation and never report expected results as observed facts.
5. **Return to context.** Revisit the original scenario with a complete call or test. Explain changes to responsibilities, caller experience, and system behavior. Incorporate feedback into a reusable judgment: what signal to notice next time, what code or constraint to inspect, and how that informs the choice. Keep open questions when evidence is insufficient; do not force general rules. Then write the lesson.

Discuss and experiment in the conversation. Proceed when the available material is sufficient without repeated confirmation. For explanation-only requests, explain actual behavior and limits without forcing an improvement proposal.

## Writing: code first, self-contained

- Tell a complete story about one question. Readers should not need prior conversation, other lessons, or project source to understand it.
- Start with the smallest useful call chain. Explain responsibilities, essential terms, data flow, and control flow needed for the conclusion.
- Prefer real code. Label simplified code or pseudocode, preserving relevant errors, ordering, concurrency, state, and lifetimes.
- Include the types, inputs, outputs, and behavior needed to read each snippet. Ground important claims in code, scenarios, or results, and explain the causal links.
- Preserve useful hypotheses, reasons for rejecting them, and decisive evidence. For design choices, show which real call or constraint changed the decision. Skip full activity logs; never invent experiments or comparisons.
- Separate a working change from a proven explanation. Symptom disappearance or shorter code alone proves neither cause nor design benefit. Trace the mechanism through code. Use a minimal test or observation to distinguish plausible alternatives; retain hypotheses and suggested checks when evidence is insufficient.
- For actual changes, show the API and callers before and after. Explain the difference with concrete inputs or execution steps, then return to the whole scenario. Never invent a before/after for unchanged code.
- Separate code facts, historical rationale, and inference. Mark unknown motives. Check current code and constraints before reusing old lessons; past conclusions are not permanent rules.
- When KISS, DRY, or another principle fits naturally, explain: code change → benefits and costs → principle → limits. Labels never replace evidence. For DRY, ask whether similar code represents the same business knowledge, not just repeated syntax.
- Use the user's language and exact code identifiers. Cite repository-relative paths and key symbols, adding a version or commit where useful. Links support deeper reading; they cannot replace the explanation.

## Files and metadata

Keep articles flat under `lesson/` at the **target project root**, not the skill installation directory or an arbitrary subdirectory. Use plain Markdown, code blocks, tables, and text flows; no HTML, images, attachments, or special renderer.

Name files `YYYY-MM-DD-{bug|design}-topic.md`, using the user's local creation date and a short, searchable kebab-case topic. Example: `2026-09-14-design-cursor-pagination.md`.

Start with YAML frontmatter; keep the title in the body:

```markdown
---
type: design
created: "2026-09-14"
verified: "2026-09-14"
scope: Pagination API v2
---

# Why the pagination API returns a next-page cursor
```

- Require `type` and `created`, matching the filename. Types are limited to `bug` and `design`.
- Include `verified` only after checking the implementation or evidence. It records the latest check date, not a claim that all tests passed; describe methods and results in the body.
- Add `scope` for a relevant module, interface, or version. Omit `updated`, duplicate title metadata, and empty fields.
- Maintain `lesson/README.md` as a small index grouped by the two types, with links and one-sentence descriptions.

## Delete and rebuild

Do not edit, append to, or patch an existing lesson in place. Replace it to correct, extend, or reflect a changed implementation:

1. Read the old article and its references. Check current code and evidence to identify the exact article to replace.
2. Prepare a complete replacement separately. Preserve useful context and tradeoffs, then run the delivery checks below. Set `created` to the rebuild date; set `verified` only to an actual check date.
3. Once ready, delete the old article and create the new file. Keep a recoverable copy until replacement succeeds, including same-day replacements at the same path.
4. Update the index and repository references to the replaced article. Keep history in Git, without old copies or redirect pages in `lesson/`. Do not commit automatically.

Replace only the affected article, preserving lessons about different questions on the same topic. The index and links may be edited normally.

## Delivery checks

Before delivery, confirm:

- A reader unfamiliar with the source can explain the API's role, problem, change, mechanism, costs, and wider impact. Explanation-only lessons cover behavior and boundaries.
- The article answers one question with self-contained code, faithful simplification, and evidence for important claims.
- Validation steps and observed results are distinct. Causal claims have mechanisms and evidence; useful exploration and misuse or detection gaps are explained without inventing missing facts.
- Supported insights name signals, checks, and conditions for future decisions. Relevant principles have concrete examples and limits; rules are not forced.
- Paths, dates, types, frontmatter, index, and references agree. Replacements leave only the new article.

Provide the article link, main takeaway, and a brief account of actual changes and validation. Do not report proposals as completed work or promise that every future agent will read the lesson automatically.
