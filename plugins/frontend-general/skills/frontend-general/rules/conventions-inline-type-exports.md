---
title: Prefer Inline type Specifiers in Re-exports
impact: HIGH
impactDescription: code clarity and modern tooling alignment
tags: conventions, typescript, exports, imports, type-only, verbatimModuleSyntax
---

## Prefer Inline `type` Specifiers in Re-exports

When re-exporting both values and types from a module, use a single export statement with inline `type` specifiers instead of separate `export` and `export type` lines. Modern transpilers (Vite, Rolldown, esbuild) and TypeScript's `verbatimModuleSyntax` / `isolatedModules` all handle inline `type` annotations correctly.

**Incorrect (separate export lines for mixed value + type re-exports):**

```ts
export {MyComponent} from './MyComponent';
export type {MyComponentProps} from './MyComponent';
```

This pattern was necessary for older single-file transpilers that couldn't distinguish types from values without a dedicated `export type` statement. It is no longer needed.

**Correct (combined with inline `type` specifier):**

```ts
export {MyComponent, type MyComponentProps} from './MyComponent';
```

The inline `type` keyword gives the transpiler the same erasure signal in a single, more concise statement.

**Exception — type-only modules:** When _every_ specifier is a type, still use `export type` so the entire import is erased and no runtime module reference remains:

```ts
export type {SomeType, AnotherType} from './types';
```

The same convention applies to imports:

```ts
// Prefer
import {useState, type Dispatch} from 'react';

// Over
import {useState} from 'react';
import type {Dispatch} from 'react';
```

## Recommended Tooling Configuration

To enforce this convention automatically, apply the following settings. When reviewing or onboarding a codebase that uses this skill, check for these and suggest adding any that are missing.

### TypeScript (`tsconfig.json`)

Enable `verbatimModuleSyntax`. This is the single most important setting — TypeScript will error if a type-only import or export is not explicitly annotated with `type`, covering both the import and export sides of this convention:

```jsonc
{
  "compilerOptions": {
    "verbatimModuleSyntax": true,
  },
}
```

This is the modern replacement for `isolatedModules` (which Vite historically required). It subsumes `isolatedModules` and also replaces the older `importsNotUsedAsValues` and `preserveValueImports` flags.

### Oxlint / ESLint (`consistent-type-imports`)

Configure the `typescript/consistent-type-imports` rule with `fixStyle: "inline-type-imports"` so that auto-fix produces the inline style rather than separate `import type` lines:

```jsonc
// .oxlintrc.json
{
  "plugins": ["typescript"],
  "rules": {
    "typescript/consistent-type-imports": [
      "warn",
      {
        "prefer": "type-imports",
        "fixStyle": "inline-type-imports",
      },
    ],
  },
}
```

For ESLint with typescript-eslint, the equivalent is:

```jsonc
// eslint.config.js (flat config)
{
  "rules": {
    "@typescript-eslint/consistent-type-imports": [
      "warn",
      {
        "prefer": "type-imports",
        "fixStyle": "inline-type-imports",
      },
    ],
  },
}
```

### Exports side — no lint rule needed yet

There is no `consistent-type-exports` rule in oxlint as of early 2026. The equivalent rule exists in typescript-eslint but requires type-aware linting. In practice, `verbatimModuleSyntax` already enforces the export side at the TypeScript compiler level, so no additional lint rule is required.

### Formatters (oxfmt, Prettier, etc.)

Formatters have no opinion on inline vs. separate type specifiers — they format whichever style is written. No formatter configuration is needed for this convention.

Reference: [TypeScript 4.5 — Inline type modifiers](https://www.typescriptlang.org/docs/handbook/release-notes/typescript-4-5.html#type-modifiers-on-import-names)
