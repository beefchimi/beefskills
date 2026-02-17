---
title: Use Fancy Quotes in Documentation Prose, Not in Code
impact: MEDIUM
impactDescription: consistent typography in markdown documentation
tags: docs, markdown, typography, prose, code-snippets
---

## Use Fancy Quotes in Documentation Prose, Not in Code

When authoring or editing **documentation** (`.md` files), use typographic (curly) quotes and apostrophes in **prose**, and keep straight quotes in **code snippets**. This applies to any markdown file: READMEs, guides, skill docs, and comments that are documentation.

### When authoring documentation

- **Prose (outside code):** Prefer opening and closing “fancy” double quotes (`“` and `”`) instead of straight `"`. Prefer “fancy” apostrophes (`‘` and `’`) instead of straight `'`.
- **Code (inside backticks):** Use straight quotes only. Inline code (single backticks) and fenced code blocks (triple backticks) must follow the syntax of the language being documented. Do not use fancy quotes or apostrophes inside code.

### When editing documentation

- **Do not replace** existing fancy quotes or apostrophes with straight ones in prose. Leave typographic punctuation as-is.
- **Do not introduce** fancy quotes or apostrophes inside code snippets; code must keep straight quotes so it remains valid and copy-pasteable.

### Examples

**Prose — use fancy quotes:**

- Prefer: The feature is “experimental” and may change.
- Avoid: The feature is "experimental" and may change.

**Prose — use fancy apostrophes:**

- Prefer: It’s important to check the project’s config.
- Avoid: It's important to check the project's config.

**Code — keep straight quotes (HTML/JS/TS, etc.):**

- In HTML snippets use straight double quotes: `<button type="button" />`.
- In JavaScript/TypeScript use straight quotes for strings: `const thing = 'some string';` or `const other = "double";`.
- Fenced blocks must stay valid for the language: use `"` and `'` as the language requires.

**Summary:** Fancy quotes and apostrophes belong in the explanatory text; backtick-delimited and fenced code must use only straight quotes so the snippet stays syntactically correct and copy-pasteable.
