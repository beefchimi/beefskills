---
title: Read and Respect Local ESLint, Prettier/oxfmt, and tsconfig
impact: HIGH
impactDescription: project consistency and tooling compatibility
tags: conventions, eslint, oxlint, prettier, oxfmt, tsconfig, formatting
---

## Read and Respect Local ESLint, Prettier/oxfmt, and tsconfig

When starting work in a project, **actively read the project's tooling configuration before writing code.** These files are the source of truth for that codebase and inform every code decision — style, strictness, module resolution, and enforced rules.

### Step 1: Read the config files

At the beginning of a task (or when first encountering an unfamiliar project), read the following config files in the repo root (or monorepo package root):

- **Lint:** `.eslintrc*`, `eslint.config.*`, `.oxlintrc*`, or equivalent (ESLint, Oxlint, etc.)
- **Format:** `.prettierrc*`, `.editorconfig`, `.oxfmtrc*`, or equivalent (Prettier, Oxfmt, etc.)
- **TypeScript:** `tsconfig.json` (strictness, paths, module resolution, etc.)

Pay attention to:

- Which lint rules are enabled, warned, or errored — these represent the project's enforced standards.
- Formatting preferences (quotes, semicolons, trailing commas, print width, etc.).
- TypeScript strictness flags (`strict`, `noUncheckedIndexedAccess`, `verbatimModuleSyntax`, etc.).
- Path aliases and module resolution strategy.

### Step 2: Let configs guide your code

**Local preferences override this skill's own formatting conventions.** The rules in this skill (including the style described in `_formatting.md`) are defaults for documentation and for projects that do not already define their own. If the project has an `.oxlintrc.json`, use its rules. If it uses Prettier with a different quote or semicolon style, follow that. If `tsconfig` enables stricter options, respect them.

**In practice:**

- Before applying formatting or style changes, check for existing config files in the repo root (or monorepo package root).
- Prefer running the project's formatter (e.g. `oxfmt`, `prettier --write`) over hand-editing to match a different style.
- When in doubt, match existing file style in the same directory or package.
- If a lint rule already enforces a pattern (e.g. `import/no-cycle` for circular dependencies), trust the linter as the enforcement layer — focus on writing code that satisfies the rule rather than re-documenting what the linter already checks.

This keeps the codebase consistent with the team's tools and avoids churn from introducing a different style than the one the linter and formatter enforce.
