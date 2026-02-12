---
title: Respect Local ESLint, Prettier/oxfmt, and tsconfig
impact: HIGH
impactDescription: project consistency and tooling compatibility
tags: conventions, eslint, oxlint, prettier, oxfmt, tsconfig, formatting
---

## Respect Local ESLint, Prettier/oxfmt, and tsconfig

When working in a project, **respect the project’s local tooling configuration**. Treat the following as the source of truth for that codebase:

- **Lint:** `.eslintrc*`, `eslint.config.*`, `.oxlintrc*`, or equivalent (ESLint, Oxlint, etc.)
- **Format:** `.prettierrc*`, `.editorconfig`, `.oxfmtrc*`, or equivalent (Prettier, Oxfmt, etc.)
- **TypeScript:** `tsconfig.json` (strictness, paths, module resolution, etc.)

**Local preferences override this skill’s own formatting conventions.** The rules in this skill (including the style described in `_formatting.md`) are defaults for documentation and for projects that do not already define their own. If the project has an `.oxlintrc.json`, use its rules. If it uses Prettier with a different quote or semicolon style, follow that. If `tsconfig` enables stricter options, respect them.

**In practice:**

- Before applying formatting or style changes, check for existing config files in the repo root (or monorepo package root).
- Prefer running the project’s formatter (e.g. `oxfmt`, `prettier --write`) over hand-editing to match a different style.
- When in doubt, match existing file style in the same directory or package.

This keeps the codebase consistent with the team’s tools and avoids churn from introducing a different style than the one the linter and formatter enforce.
