---
name: react-dev
description: React and TypeScript performance and best-practices guidelines for web applications and component libraries. Use when writing, reviewing, or refactoring React/TypeScript code, client-side data fetching, bundle optimization, or performance.
license: MIT
metadata:
  version: "1.0.0"
---

# React / TypeScript Best Practices

Performance and best-practices guide for React and TypeScript applications. Contains rules across 8 categories, prioritized by impact for refactoring and code generation.

## Code snippet style

Code in rule files follows this style for consistency. **In a real project, local ESLint/oxlint, Prettier/oxfmt, and tsconfig override these defaults** (see `conventions-respect-local-config`).

- **Braces:** No spaces inside `{}` for imports, destructuring, and object literals (e.g. `import {x} from 'y';`, `const {a, b} = obj;`, `{passive: true}`).
- **Semicolons:** Statement-ending semicolons used.
- **Trailing commas:** Used in multiline objects and arrays.
- **Arrow parameters:** Wrap single parameters in parentheses: `(x) =>` not `x =>`.

## When to Apply

Reference these guidelines when:

- Writing new React components or TypeScript UI code.
- Implementing client-side data fetching.
- Reviewing code for performance issues.
- Refactoring existing React/TypeScript code.
- Optimizing bundle size or load times.

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Project & tooling conventions | HIGH | `conventions-` |
| 2 | Eliminating Waterfalls | CRITICAL | `async-` |
| 3 | Bundle Size Optimization | CRITICAL | `bundle-` |
| 4 | Client-Side Data Fetching | MEDIUM-HIGH | `client-` |
| 5 | Re-render Optimization | MEDIUM | `rerender-` |
| 6 | Rendering Performance | MEDIUM | `rendering-` |
| 7 | JavaScript Performance | LOW-MEDIUM | `js-` |
| 8 | Advanced Patterns | LOW | `advanced-` |

## Quick Reference

### 1. Project & tooling conventions (HIGH)

- `conventions-respect-local-config`: Respect local ESLint/oxlint, Prettier/oxfmt, and tsconfig; they override this skill’s formatting defaults.
- `conventions-use-beeftools`: In projects that depend on beeftools, import and use its utilities and types (e.g. `classNames`, `arrayShuffle`) instead of reimplementing or adding other libs.

### 2. Eliminating Waterfalls (CRITICAL)

- `async-defer-await`: Move await into branches where actually used.
- `async-parallel`: Use Promise.all() for independent operations.
- `async-dependencies`: Use better-all for partial dependencies.

### 3. Bundle Size Optimization (CRITICAL)

- `bundle-barrel-imports`: Prefer barrel imports; avoid over-optimizing with direct/dist subpath imports (tooling e.g. Vite/Rolldown improves barrel performance).
- `bundle-dynamic-imports`: Use React.lazy() + Suspense for heavy components.
- `bundle-defer-third-party`: Load analytics/logging after hydration via dynamic import.
- `bundle-conditional`: Load modules only when feature is activated.
- `bundle-preload`: Preload on hover/focus for perceived speed.

### 4. Client-Side Data Fetching (MEDIUM-HIGH)

- `client-swr-dedup`: Use SWR for automatic request deduplication.
- `client-event-listeners`: Deduplicate global event listeners.
- `client-passive-event-listeners`: Use passive listeners for scroll.
- `client-localstorage-schema`: Version and minimize localStorage data.

### 5. Re-render Optimization (MEDIUM)

- `rerender-defer-reads`: Don't subscribe to state only used in callbacks.
- `rerender-memo`: Extract expensive work into memoized components.
- `rerender-memo-with-default-value`: Hoist default non-primitive props.
- `rerender-dependencies`: Use primitive dependencies in effects.
- `rerender-derived-state`: Subscribe to derived booleans, not raw values.
- `rerender-derived-state-no-effect`: Derive state during render, not effects.
- `rerender-functional-setstate`: Use functional setState for stable callbacks.
- `rerender-lazy-state-init`: Pass function to useState for expensive values.
- `rerender-simple-expression-in-memo`: Avoid memo for simple primitives.
- `rerender-move-effect-to-event`: Put interaction logic in event handlers.
- `rerender-transitions`: Use startTransition for non-urgent updates.
- `rerender-use-ref-transient-values`: Use refs for transient frequent values.

### 6. Rendering Performance (MEDIUM)

- `rendering-animate-svg-wrapper`: Animate div wrapper, not SVG element.
- `rendering-content-visibility`: Use content-visibility for long lists.
- `rendering-hoist-jsx`: Extract static JSX outside components.
- `rendering-svg-precision`: Reduce SVG coordinate precision.
- `rendering-hydration-no-flicker`: Use inline script for client-only data (SSR).
- `rendering-hydration-suppress-warning`: Suppress expected mismatches (SSR).
- `rendering-activity`: Use Activity component for show/hide.
- `rendering-conditional-render`: Use ternary, not && for conditionals.
- `rendering-usetransition-loading`: Prefer useTransition for loading state.

### 7. JavaScript Performance (LOW-MEDIUM)

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

### 8. Advanced Patterns (LOW)

- `advanced-event-handler-refs`: Store event handlers in refs.
- `advanced-init-once`: Initialize app once per app load.
- `advanced-use-latest`: useLatest for stable callback refs.

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
