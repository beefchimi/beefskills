---
name: frontend-react
description: React-specific performance and best-practices guidelines for web applications and component libraries. Use when writing, reviewing, or refactoring React code, optimizing re-renders, implementing code-splitting with React.lazy/Suspense, client-side data fetching with SWR, or React rendering patterns.
license: MIT
metadata:
  version: "1.0.0"
---

# React Best Practices

React-specific performance and best-practices guide. Contains rules across 5 categories, prioritized by impact for refactoring and code generation.

For framework-agnostic patterns (async, JS performance, conventions, general bundle/rendering/DOM), see the `frontend-general` skill.

## Code snippet style

Code in rule files follows this style for consistency. **In a real project, local ESLint/oxlint, Prettier/oxfmt, and tsconfig override these defaults** (see `frontend-general` skill's `conventions-respect-local-config`).

- **Braces:** No spaces inside `{}` for imports, destructuring, and object literals (e.g. `import {x} from 'y';`, `const {a, b} = obj;`, `{passive: true}`).
- **Semicolons:** Statement-ending semicolons used.
- **Trailing commas:** Used in multiline objects and arrays.
- **Arrow parameters:** Wrap single parameters in parentheses: `(x) =>` not `x =>`.

## When to Apply

Reference these guidelines when:

- Writing new React components or hooks.
- Implementing client-side data fetching with SWR.
- Reviewing React code for re-render or rendering performance issues.
- Refactoring existing React code.
- Implementing code-splitting with React.lazy and Suspense.
- Working with SSR hydration patterns.

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Bundle Size Optimization | CRITICAL | `bundle-` |
| 2 | Client-Side Data Fetching | MEDIUM-HIGH | `client-` |
| 3 | Re-render Optimization | MEDIUM | `rerender-` |
| 4 | Rendering Performance | MEDIUM | `rendering-` |
| 5 | Advanced Patterns | LOW | `advanced-` |

## Quick Reference

### 1. Bundle Size Optimization (CRITICAL)

- `bundle-dynamic-imports`: Use React.lazy() + Suspense for heavy components.
- `bundle-defer-third-party`: Load analytics/logging after hydration via dynamic import.
- `bundle-conditional`: Load modules only when feature is activated.
- `bundle-preload`: Preload on hover/focus for perceived speed.

### 2. Client-Side Data Fetching (MEDIUM-HIGH)

- `client-swr-dedup`: Use SWR for automatic request deduplication.
- `client-event-listeners`: Deduplicate global event listeners.

### 3. Re-render Optimization (MEDIUM)

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

### 4. Rendering Performance (MEDIUM)

- `rendering-hydration-no-flicker`: Use inline script for client-only data (SSR).
- `rendering-hydration-suppress-warning`: Suppress expected mismatches (SSR).
- `rendering-activity`: Use Activity component for show/hide.
- `rendering-hoist-jsx`: Extract static JSX outside components.
- `rendering-conditional-render`: Use ternary, not && for conditionals.
- `rendering-usetransition-loading`: Prefer useTransition for loading state.

### 5. Advanced Patterns (LOW)

- `advanced-event-handler-refs`: Store event handlers in refs.
- `advanced-init-once`: Initialize app once per app load.
- `advanced-use-latest`: useLatest for stable callback refs.

## How to Use

Read individual rule files for detailed explanations and code examples:

```
rules/rerender-memo.md
rules/bundle-dynamic-imports.md
```

Each rule file contains:

- Brief explanation of why it matters.
- Incorrect code example with explanation.
- Correct code example with explanation.
- Additional context and references.

## Full Compiled Document

For the complete guide with all rules expanded: `AGENTS.md`
