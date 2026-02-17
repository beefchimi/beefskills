---
name: frontend-general
description: Frontend and TypeScript performance and best-practices guidelines for web applications. Use when writing, reviewing, or refactoring frontend/TypeScript code, async patterns, bundle optimization, DOM performance, or JavaScript micro-optimizations. Framework-agnostic — applies to React, Vue, Svelte, vanilla JS, etc.
license: MIT
metadata:
  version: '1.0.0'
---

# Frontend / TypeScript Best Practices

Performance and best-practices guide for frontend and TypeScript applications. Contains framework-agnostic rules across 6 categories, prioritized by impact for refactoring and code generation.

For React-specific patterns (hooks, re-renders, hydration, Suspense, etc.), see the `frontend-react` skill. For accessibility (ARIA, keyboard navigation, WCAG compliance), see the `frontend-a11y` skill if available.

## Code snippet style

Code in rule files follows this style for consistency. **In a real project, local ESLint/oxlint, Prettier/oxfmt, and tsconfig override these defaults** (see `conventions-respect-local-config`).

- **Braces:** No spaces inside `{}` for imports, destructuring, and object literals (e.g. `import {x} from 'y';`, `const {a, b} = obj;`, `{passive: true}`).
- **Semicolons:** Statement-ending semicolons used.
- **Trailing commas:** Used in multiline objects and arrays.
- **Arrow parameters:** Wrap single parameters in parentheses: `(x) =>` not `x =>`.

## When to Apply

Reference these guidelines when:

- Writing new frontend or TypeScript code.
- Reviewing code for performance issues.
- Refactoring existing frontend/TypeScript code.
- Optimizing bundle size or load times.
- Working with async patterns, DOM APIs, or event listeners.
- Writing or editing markdown documentation (`.md` files); see the `docs-` rules.

## Rule Categories by Priority

| Priority | Category                      | Impact      | Prefix         |
| -------- | ----------------------------- | ----------- | -------------- |
| 1        | Project & tooling conventions | HIGH        | `conventions-` |
| 2        | Eliminating Waterfalls        | CRITICAL    | `async-`       |
| 3        | Bundle Size Optimization      | CRITICAL    | `bundle-`      |
| 4        | Client-Side Data Handling     | MEDIUM-HIGH | `client-`      |
| 5        | Rendering Performance         | MEDIUM      | `rendering-`   |
| 6        | JavaScript Performance        | LOW-MEDIUM  | `js-`          |
| 7        | Documentation                 | MEDIUM      | `docs-`        |

## Quick Reference

### 1. Project & tooling conventions (HIGH)

- `conventions-respect-local-config`: Read project lint/format/TS configs before writing code; let them guide every code decision. Local configs override this skill's formatting defaults.
- `conventions-inline-type-exports`: Prefer inline `type` specifiers in mixed value + type re-exports (`export {Foo, type FooProps}`) over separate `export` / `export type` lines.
- `conventions-use-beeftools`: In projects that depend on beeftools, import and use its utilities and types (e.g. `classNames`, `arrayShuffle`) instead of reimplementing or adding other libs.
- `conventions-avoid-circular-dependencies`: Structure modules with a clear dependency direction; extract shared code to break cycles; use `import type` for type-only references.

### 2. Eliminating Waterfalls (CRITICAL)

- `async-defer-await`: Move await into branches where actually used.
- `async-parallel`: Use Promise.all() for independent operations.
- `async-dependencies`: Use better-all for partial dependencies.

### 3. Bundle Size Optimization (CRITICAL)

- `bundle-barrel-imports`: Prefer barrel imports; avoid over-optimizing with direct/dist subpath imports (tooling e.g. Vite/Rolldown improves barrel performance).

### 4. Client-Side Data Handling (MEDIUM-HIGH)

- `client-passive-event-listeners`: Use passive listeners for scroll.
- `client-localstorage-schema`: Version and minimize localStorage data.

### 5. Rendering Performance (MEDIUM)

- `rendering-animate-svg-wrapper`: Animate div wrapper, not SVG element.
- `rendering-content-visibility`: Use content-visibility for long lists.
- `rendering-svg-precision`: Reduce SVG coordinate precision.

### 6. JavaScript Performance (LOW-MEDIUM)

- `js-batch-dom-css`: Group CSS changes via classes or cssText.
- `js-index-maps`: Build Map for repeated lookups.
- `js-cache-property-access`: Cache object properties in loops.
- `js-cache-function-results`: Cache function results in module-level Map.
- `js-cache-storage`: Cache localStorage/sessionStorage reads.
- `js-combine-iterations`: Combine multiple filter/map into one loop.
- `js-length-check-first`: Check array length before expensive comparison.
- `js-early-exit`: Return early from functions.
- `js-hoist-regexp`: Hoist RegExp creation outside loops.
- `js-min-max-loop`: Use loop for min/max instead of sort.
- `js-set-map-lookups`: Use Set/Map for O(1) lookups.
- `js-tosorted-immutable`: Use toSorted() for immutability.

### 7. Documentation (MEDIUM)

- `docs-fancy-quotes`: Use “fancy” quotes and apostrophes in markdown prose; keep straight quotes in code snippets (inline or fenced). Do not replace existing fancy quotes when editing.

## How to Use

Read individual rule files for detailed explanations and code examples:

```
rules/async-parallel.md
rules/bundle-barrel-imports.md
```

Each rule file contains:

- Brief explanation of why it matters.
- Incorrect code example with explanation.
- Correct code example with explanation.
- Additional context and references.

## Full Compiled Document

For the complete guide with all rules expanded: `AGENTS.md`
