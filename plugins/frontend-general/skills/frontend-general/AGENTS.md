# Frontend / TypeScript Best Practices

**Version 1.0.0**
Frontend/TypeScript

> **Note:**
> This document is for agents and LLMs when maintaining, generating, or refactoring
> frontend and TypeScript codebases. These rules are framework-agnostic.

---

## Abstract

Performance and best-practices guide for frontend and TypeScript applications.
Rules across 7 categories: project conventions, eliminating async waterfalls, bundle
optimization, client-side data handling, rendering performance, and JavaScript
micro-optimizations. Each rule includes incorrect vs. correct examples.

---

## Table of Contents

1. [Project & tooling conventions](#1-project-&-tooling-conventions) — **HIGH**
   - 1.1 Identify and Avoid Circular Dependencies
   - 1.2 Prefer Inline `type` Specifiers in Re-exports
   - 1.3 Read and Respect Local ESLint, Prettier/oxfmt, and tsconfig
   - 1.4 Use beeftools When Available

2. [Eliminating Waterfalls](#2-eliminating-waterfalls) — **CRITICAL**
   - 2.1 Defer Await Until Needed
   - 2.2 Dependency-Based Parallelization
   - 2.3 Promise.all() for Independent Operations

3. [Bundle Size Optimization](#3-bundle-size-optimization) — **CRITICAL**
   - 3.1 Prefer Barrel Imports; Avoid Over-Optimizing

4. [Client-Side Data Handling](#4-client-side-data-handling) — **MEDIUM-HIGH**
   - 4.1 Version and Minimize localStorage Data
   - 4.2 Use Passive Event Listeners for Scrolling Performance

5. [Rendering Performance](#5-rendering-performance) — **MEDIUM**
   - 5.1 Animate SVG Wrapper Instead of SVG Element
   - 5.2 CSS content-visibility for Long Lists
   - 5.3 Optimize SVG Precision

6. [JavaScript Performance](#6-javascript-performance) — **LOW-MEDIUM**
   - 6.1 Avoid Layout Thrashing
   - 6.2 Cache Repeated Function Calls
   - 6.3 Cache Property Access in Loops
   - 6.4 Cache Storage API Calls
   - 6.5 Combine Multiple Array Iterations
   - 6.6 Early Return from Functions
   - 6.7 Hoist RegExp Creation
   - 6.8 Build Index Maps for Repeated Lookups
   - 6.9 Early Length Check for Array Comparisons
   - 6.10 Use Loop for Min/Max Instead of Sort
   - 6.11 Use Set/Map for O(1) Lookups
   - 6.12 Use toSorted() Instead of sort() for Immutability

7. [Documentation](#7-documentation) — **MEDIUM**
   - 7.1 Use Fancy Quotes in Documentation Prose, Not in Code

---

## 1. Project & tooling conventions

### 1.1 Identify and Avoid Circular Dependencies

Circular dependencies occur when module A imports from module B, and module B (directly or transitively) imports from module A. This causes partially-initialized modules at runtime — imports resolve to `undefined`, classes are used before they're defined, and bugs surface far from their cause.

Linters like oxlint and ESLint can catch circular imports (`import/no-cycle`), but the linter only flags the symptom. This rule covers the structural patterns that **prevent** cycles from forming in the first place.

### How cycles happen

**Direct cycle — two modules import each other:**

```ts
// user.ts
import {formatEmail} from './email';
export function getUser() {
  /* ... */
}

// email.ts
import {getUser} from './user';
export function formatEmail() {
  /* ... */
}
```

**Transitive cycle — three or more modules form a chain:**

```ts
// a.ts → imports from b.ts → imports from c.ts → imports from a.ts
```

**Barrel file cycle — `index.ts` re-exports create hidden loops:**

```ts
// components/index.ts
export {Button} from './Button';
export {Modal} from './Modal';

// components/Modal.tsx — imports from its own barrel
import {Button} from '.'; // cycle: index → Modal → index
```

### Pattern 1: Enforce a dependency direction

Organize modules into layers with a clear dependency direction. Lower layers never import from higher layers.

```
shared/       ← pure utilities, types, constants (imports from nothing)
  └─ types.ts
  └─ utils.ts
domain/       ← business logic (imports from shared/)
  └─ user.ts
  └─ email.ts
features/     ← UI features (imports from domain/ and shared/)
  └─ profile/
  └─ settings/
```

**Incorrect (lower layer imports from higher layer):**

```ts
// shared/format.ts
import {getUserLocale} from '../domain/user'; // shared/ → domain/ = wrong direction
```

**Correct (extract the shared dependency):**

```ts
// shared/locale.ts
export function getLocale() {
  /* ... */
}

// domain/user.ts
import {getLocale} from '../shared/locale';
```

### Pattern 2: Extract shared code into a third module

When two modules need each other, the shared dependency belongs in a separate module that both import from.

**Incorrect (mutual dependency):**

```ts
// order.ts
import {getCustomer} from './customer';
export function getOrder() {
  /* ... */
}
export function formatOrderId(id: string) {
  return `ORD-${id}`;
}

// customer.ts
import {formatOrderId} from './order';
export function getCustomer() {
  /* ... */
}
```

**Correct (extract shared utility):**

```ts
// format.ts
export function formatOrderId(id: string) {
  return `ORD-${id}`;
}

// order.ts
import {getCustomer} from './customer';
import {formatOrderId} from './format';
export function getOrder() {
  /* ... */
}

// customer.ts
import {formatOrderId} from './format';
export function getCustomer() {
  /* ... */
}
```

### Pattern 3: Use type-only imports to break runtime cycles

If the cycle exists only because of type references, use `import type` to eliminate the runtime dependency. Type-only imports are erased at compile time and do not create module edges.

```ts
// user.ts
import type {Order} from './order'; // no runtime import — cycle broken
export interface User {
  recentOrders: Order[];
}
```

This only works when the import is used purely for type annotations. If you need the value at runtime, use Pattern 2 instead.

### Pattern 4: Avoid importing from your own barrel

Never import from a directory's `index.ts` within that same directory. Use direct relative imports instead.

**Incorrect:**

```ts
// components/Modal.tsx
import {Button} from '.'; // imports from components/index.ts — cycle
```

**Correct:**

```ts
// components/Modal.tsx
import {Button} from './Button'; // direct sibling import — no cycle
```

### When adding a new import

Before adding an import, consider: does the target module (or anything it imports) already depend on the current module? If unsure, trace the import chain or rely on the linter's `import/no-cycle` rule to catch it. Structuring code with a clear dependency direction (Pattern 1) makes this question easy to answer.

### 1.2 Prefer Inline `type` Specifiers in Re-exports

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

### 1.3 Read and Respect Local ESLint, Prettier/oxfmt, and tsconfig

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

### 1.4 Use beeftools When Available

In projects where **[beeftools](https://www.npmjs.com/package/beeftools)** is installed (listed in `package.json` dependencies or devDependencies), **import and use its functions, types, and utilities** instead of reimplementing logic or adding other packages for the same purpose.

**beeftools** provides common front-end utilities and types. Examples include:

- **`classNames`** — conditional class name composition (e.g. for React `className` props).
- **`arrayShuffle`** — shuffle arrays (e.g. for randomizing order).
- Plus many other utilities and shared types; check the package API when you need array, string, object, or type helpers.

**In practice:**

- If the project has `beeftools` as a dependency, prefer it for utility needs (class names, array helpers, etc.) before reaching for ad-hoc code or another library.
- Import from `'beeftools'` (or the subpath the package documents) and use the exported functions and types.
- Do not duplicate logic that beeftools already provides.

**References:**

- [npm: beeftools](https://www.npmjs.com/package/beeftools)
- [GitHub: beefchimi/beeftools](https://github.com/beefchimi/beeftools)


## 2. Eliminating Waterfalls

### 2.1 Defer Await Until Needed

Move `await` operations into the branches where they're actually used to avoid blocking code paths that don't need them.

**Incorrect (blocks both branches):**

```ts
async function handleRequest(userId: string, skipProcessing: boolean) {
  const userData = await fetchUserData(userId);

  if (skipProcessing) {
    // Returns immediately but still waited for userData
    return {skipped: true};
  }

  // Only this branch uses userData
  return processUserData(userData);
}
```

**Correct (only blocks when needed):**

```ts
async function handleRequest(userId: string, skipProcessing: boolean) {
  if (skipProcessing) {
    // Returns immediately without waiting
    return {skipped: true};
  }

  // Fetch only when needed
  const userData = await fetchUserData(userId);
  return processUserData(userData);
}
```

**Another example (early return optimization):**

```ts
// Incorrect: always fetches permissions
async function updateResource(resourceId: string, userId: string) {
  const permissions = await fetchPermissions(userId);
  const resource = await getResource(resourceId);

  if (!resource) {
    return {error: 'Not found'};
  }

  if (!permissions.canEdit) {
    return {error: 'Forbidden'};
  }

  return await updateResourceData(resource, permissions);
}

// Correct: fetches only when needed
async function updateResource(resourceId: string, userId: string) {
  const resource = await getResource(resourceId);

  if (!resource) {
    return {error: 'Not found'};
  }

  const permissions = await fetchPermissions(userId);

  if (!permissions.canEdit) {
    return {error: 'Forbidden'};
  }

  return await updateResourceData(resource, permissions);
}
```

This optimization is especially valuable when the skipped branch is frequently taken, or when the deferred operation is expensive.

### 2.2 Dependency-Based Parallelization

For operations with partial dependencies, use `better-all` to maximize parallelism. It automatically starts each task at the earliest possible moment.

**Incorrect (profile waits for config unnecessarily):**

```ts
const [user, config] = await Promise.all([fetchUser(), fetchConfig()]);
const profile = await fetchProfile(user.id);
```

**Correct (config and profile run in parallel):**

```ts
import {all} from 'better-all';

const {user, config, profile} = await all({
  async user() {
    return fetchUser();
  },
  async config() {
    return fetchConfig();
  },
  async profile() {
    return fetchProfile((await this.$.user).id);
  },
});
```

**Alternative without extra dependencies:**

We can also create all the promises first, and do `Promise.all()` at the end.

```ts
const userPromise = fetchUser();
const profilePromise = userPromise.then((user) => fetchProfile(user.id));

const [user, config, profile] = await Promise.all([userPromise, fetchConfig(), profilePromise]);
```

Reference: [https://github.com/shuding/better-all](https://github.com/shuding/better-all)

### 2.3 Promise.all() for Independent Operations

When async operations have no interdependencies, execute them concurrently using `Promise.all()`.

**Incorrect (sequential execution, 3 round trips):**

```ts
const user = await fetchUser();
const posts = await fetchPosts();
const comments = await fetchComments();
```

**Correct (parallel execution, 1 round trip):**

```ts
const [user, posts, comments] = await Promise.all([fetchUser(), fetchPosts(), fetchComments()]);
```


## 3. Bundle Size Optimization

### 3.1 Prefer Barrel Imports; Avoid Over-Optimizing

**Barrel files are fine.** Using an `index.ts` (or similar) that re-exports from your components is recommended for component libraries and internal packages. It gives a single entry point and a clear public API. For third-party libraries, prefer the package’s public barrel import over fragile subpath or dist imports.

**Avoid over-optimizing.** Do not use direct/dist subpath imports just to shave bytes or speed up cold starts. They are brittle (tied to package internals), harder to read, and often unnecessary. Upcoming improvements in tooling (e.g. Vite with Rolldown) greatly improve barrel file performance, so the historical downsides of barrel imports matter less and less.

**Preferred (single-line barrel import):**

```tsx
import {Check, X, Menu} from 'lucide-react';

import {Button, TextField} from '@mui/material';
```

**Avoid (over-optimized, brittle subpath imports):**

```tsx
import Check from 'lucide-react/dist/esm/icons/check';
import X from 'lucide-react/dist/esm/icons/x';
import Menu from 'lucide-react/dist/esm/icons/menu';

import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
```

Use the package’s documented public API. Let the bundler and future tooling (e.g. Vite/Rolldown) handle tree-shaking and performance. For your own libraries, keep using barrel files (e.g. `export * from './Button'`) for a clean public API.


## 4. Client-Side Data Handling

### 4.1 Version and Minimize localStorage Data

Add version prefix to keys and store only needed fields. Prevents schema conflicts and accidental storage of sensitive data.

**Incorrect:**

```ts
// No version, stores everything, no error handling
localStorage.setItem('userConfig', JSON.stringify(fullUserObject));
const data = localStorage.getItem('userConfig');
```

**Correct:**

```ts
const VERSION = 'v2';

function saveConfig(config: {theme: string; language: string}) {
  try {
    localStorage.setItem(`userConfig:${VERSION}`, JSON.stringify(config));
  } catch {
    // Throws in incognito/private browsing, quota exceeded, or disabled
  }
}

function loadConfig() {
  try {
    const data = localStorage.getItem(`userConfig:${VERSION}`);
    return data ? JSON.parse(data) : null;
  } catch {
    return null;
  }
}

// Migration from v1 to v2
function migrate() {
  try {
    const v1 = localStorage.getItem('userConfig:v1');
    if (v1) {
      const old = JSON.parse(v1);
      saveConfig({theme: old.darkMode ? 'dark' : 'light', language: old.lang});
      localStorage.removeItem('userConfig:v1');
    }
  } catch {}
}
```

**Store minimal fields from server responses:**

```ts
// User object has 20+ fields, only store what UI needs
function cachePrefs(user: FullUser) {
  try {
    localStorage.setItem(
      'prefs:v1',
      JSON.stringify({
        theme: user.preferences.theme,
        notifications: user.preferences.notifications,
      }),
    );
  } catch {}
}
```

**Always wrap in try-catch:** `getItem()` and `setItem()` throw in incognito/private browsing (Safari, Firefox), when quota exceeded, or when disabled.

**Benefits:** Schema evolution via versioning, reduced storage size, prevents storing tokens/PII/internal flags.

### 4.2 Use Passive Event Listeners for Scrolling Performance

Add `{passive: true}` to touch and wheel event listeners to enable immediate scrolling. Browsers normally wait for listeners to finish to check if `preventDefault()` is called, causing scroll delay.

**Incorrect:**

```ts
useEffect(() => {
  const handleTouch = (e: TouchEvent) => console.log(e.touches[0].clientX);
  const handleWheel = (e: WheelEvent) => console.log(e.deltaY);

  document.addEventListener('touchstart', handleTouch);
  document.addEventListener('wheel', handleWheel);

  return () => {
    document.removeEventListener('touchstart', handleTouch);
    document.removeEventListener('wheel', handleWheel);
  };
}, []);
```

**Correct:**

```ts
useEffect(() => {
  const handleTouch = (e: TouchEvent) => console.log(e.touches[0].clientX);
  const handleWheel = (e: WheelEvent) => console.log(e.deltaY);

  document.addEventListener('touchstart', handleTouch, {passive: true});
  document.addEventListener('wheel', handleWheel, {passive: true});

  return () => {
    document.removeEventListener('touchstart', handleTouch);
    document.removeEventListener('wheel', handleWheel);
  };
}, []);
```

**Use passive when:** tracking/analytics, logging, any listener that doesn't call `preventDefault()`.

**Don't use passive when:** implementing custom swipe gestures, custom zoom controls, or any listener that needs `preventDefault()`.


## 5. Rendering Performance

### 5.1 Animate SVG Wrapper Instead of SVG Element

Many browsers don't have hardware acceleration for CSS3 animations on SVG elements. Wrap SVG in a `<div>` and animate the wrapper instead.

**Incorrect (animating SVG directly - no hardware acceleration):**

```tsx
function LoadingSpinner() {
  return (
    <svg className="animate-spin" width="24" height="24" viewBox="0 0 24 24">
      <circle cx="12" cy="12" r="10" stroke="currentColor" />
    </svg>
  );
}
```

**Correct (animating wrapper div - hardware accelerated):**

```tsx
function LoadingSpinner() {
  return (
    <div className="animate-spin">
      <svg width="24" height="24" viewBox="0 0 24 24">
        <circle cx="12" cy="12" r="10" stroke="currentColor" />
      </svg>
    </div>
  );
}
```

This applies to all CSS transforms and transitions (`transform`, `opacity`, `translate`, `scale`, `rotate`). The wrapper div allows browsers to use GPU acceleration for smoother animations.

### 5.2 CSS content-visibility for Long Lists

Apply `content-visibility: auto` to defer off-screen rendering.

**CSS:**

```css
.message-item {
  content-visibility: auto;
  contain-intrinsic-size: 0 80px;
}
```

**Example:**

```tsx
function MessageList({messages}: {messages: Message[]}) {
  return (
    <div className="overflow-y-auto h-screen">
      {messages.map((msg) => (
        <div key={msg.id} className="message-item">
          <Avatar user={msg.author} />
          <div>{msg.content}</div>
        </div>
      ))}
    </div>
  );
}
```

For 1000 messages, browser skips layout/paint for ~990 off-screen items (10× faster initial render).

### 5.3 Optimize SVG Precision

Reduce SVG coordinate precision to decrease file size. The optimal precision depends on the viewBox size, but in general reducing precision should be considered.

**Incorrect (excessive precision):**

```svg
<path d="M 10.293847 20.847362 L 30.938472 40.192837" />
```

**Correct (1 decimal place):**

```svg
<path d="M 10.3 20.8 L 30.9 40.2" />
```

**Automate with SVGO:**

```bash
npx svgo --precision=1 --multipass icon.svg
```


## 6. JavaScript Performance

### 6.1 Avoid Layout Thrashing

Avoid interleaving style writes with layout reads. When you read a layout property (like `offsetWidth`, `getBoundingClientRect()`, or `getComputedStyle()`) between style changes, the browser is forced to trigger a synchronous reflow.

**This is OK (browser batches style changes):**

```ts
function updateElementStyles(element: HTMLElement) {
  // Each line invalidates style, but browser batches the recalculation
  element.style.width = '100px';
  element.style.height = '200px';
  element.style.backgroundColor = 'blue';
  element.style.border = '1px solid black';
}
```

**Incorrect (interleaved reads and writes force reflows):**

```ts
function layoutThrashing(element: HTMLElement) {
  element.style.width = '100px';
  const width = element.offsetWidth; // Forces reflow
  element.style.height = '200px';
  const height = element.offsetHeight; // Forces another reflow
}
```

**Correct (batch writes, then read once):**

```ts
function updateElementStyles(element: HTMLElement) {
  // Batch all writes together
  element.style.width = '100px';
  element.style.height = '200px';
  element.style.backgroundColor = 'blue';
  element.style.border = '1px solid black';

  // Read after all writes are done (single reflow)
  const {width, height} = element.getBoundingClientRect();
}
```

**Correct (batch reads, then writes):**

```ts
function avoidThrashing(element: HTMLElement) {
  // Read phase - all layout queries first
  const rect1 = element.getBoundingClientRect();
  const offsetWidth = element.offsetWidth;
  const offsetHeight = element.offsetHeight;

  // Write phase - all style changes after
  element.style.width = '100px';
  element.style.height = '200px';
}
```

**Better (use CSS classes):**

```css
.highlighted-box {
  width: 100px;
  height: 200px;
  background-color: blue;
  border: 1px solid black;
}
```

```ts
function updateElementStyles(element: HTMLElement) {
  element.classList.add('highlighted-box');

  const {width, height} = element.getBoundingClientRect();
}
```

**React example:**

```tsx
// Incorrect: interleaving style changes with layout queries
function Box({isHighlighted}: {isHighlighted: boolean}) {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (ref.current && isHighlighted) {
      ref.current.style.width = '100px';
      const width = ref.current.offsetWidth; // Forces layout
      ref.current.style.height = '200px';
    }
  }, [isHighlighted]);

  return <div ref={ref}>Content</div>;
}

// Correct: toggle class
function Box({isHighlighted}: {isHighlighted: boolean}) {
  return <div className={isHighlighted ? 'highlighted-box' : ''}>Content</div>;
}
```

Prefer CSS classes over inline styles when possible. See [this gist](https://gist.github.com/paulirish/5d52fb081b3570c81e3a) and [CSS Triggers](https://csstriggers.com/) for more on layout-forcing operations.

### 6.2 Cache Repeated Function Calls

Use a module-level Map to cache function results when the same function is called repeatedly with the same inputs during render.

**Incorrect (redundant computation):**

```tsx
function ProjectList({projects}: {projects: Project[]}) {
  return (
    <div>
      {projects.map((project) => {
        // slugify() called 100+ times for same project names
        const slug = slugify(project.name);

        return <ProjectCard key={project.id} slug={slug} />;
      })}
    </div>
  );
}
```

**Correct (cached results):**

```tsx
// Module-level cache
const slugifyCache = new Map<string, string>();

function cachedSlugify(text: string): string {
  if (slugifyCache.has(text)) {
    return slugifyCache.get(text)!;
  }

  const result = slugify(text);
  slugifyCache.set(text, result);

  return result;
}

function ProjectList({projects}: {projects: Project[]}) {
  return (
    <div>
      {projects.map((project) => {
        // Computed only once per unique project name
        const slug = cachedSlugify(project.name);

        return <ProjectCard key={project.id} slug={slug} />;
      })}
    </div>
  );
}
```

**Simpler pattern for single-value functions:**

```ts
let isLoggedInCache: boolean | null = null;

function isLoggedIn(): boolean {
  if (isLoggedInCache !== null) {
    return isLoggedInCache;
  }

  isLoggedInCache = document.cookie.includes('auth=');
  return isLoggedInCache;
}

// Clear cache when auth changes
function onAuthChange() {
  isLoggedInCache = null;
}
```

Use a Map (not a hook) so it works everywhere: utilities, event handlers, not just React components.

### 6.3 Cache Property Access in Loops

Cache object property lookups in hot paths.

**Incorrect (3 lookups × N iterations):**

```ts
for (let i = 0; i < arr.length; i++) {
  process(obj.config.settings.value);
}
```

**Correct (1 lookup total):**

```ts
const value = obj.config.settings.value;
const len = arr.length;
for (let i = 0; i < len; i++) {
  process(value);
}
```

### 6.4 Cache Storage API Calls

`localStorage`, `sessionStorage`, and `document.cookie` are synchronous and expensive. Cache reads in memory.

**Incorrect (reads storage on every call):**

```ts
function getTheme() {
  return localStorage.getItem('theme') ?? 'light';
}
// Called 10 times = 10 storage reads
```

**Correct (Map cache):**

```ts
const storageCache = new Map<string, string | null>();

function getLocalStorage(key: string) {
  if (!storageCache.has(key)) {
    storageCache.set(key, localStorage.getItem(key));
  }
  return storageCache.get(key);
}

function setLocalStorage(key: string, value: string) {
  localStorage.setItem(key, value);
  storageCache.set(key, value); // keep cache in sync
}
```

Use a Map (not a hook) so it works everywhere: utilities, event handlers, not just React components.

**Cookie caching:**

```ts
let cookieCache: Record<string, string> | null = null;

function getCookie(name: string) {
  if (!cookieCache) {
    cookieCache = Object.fromEntries(document.cookie.split('; ').map((c) => c.split('=')));
  }
  return cookieCache[name];
}
```

**Important (invalidate on external changes):**

If storage can change externally (another tab, server-set cookies), invalidate cache:

```ts
window.addEventListener('storage', (e) => {
  if (e.key) storageCache.delete(e.key);
});

document.addEventListener('visibilitychange', () => {
  if (document.visibilityState === 'visible') {
    storageCache.clear();
  }
});
```

### 6.5 Combine Multiple Array Iterations

Multiple `.filter()` or `.map()` calls iterate the array multiple times. Combine into one loop.

**Incorrect (3 iterations):**

```ts
const admins = users.filter((u) => u.isAdmin);
const testers = users.filter((u) => u.isTester);
const inactive = users.filter((u) => !u.isActive);
```

**Correct (1 iteration):**

```ts
const admins: User[] = [];
const testers: User[] = [];
const inactive: User[] = [];

for (const user of users) {
  if (user.isAdmin) admins.push(user);
  if (user.isTester) testers.push(user);
  if (!user.isActive) inactive.push(user);
}
```

### 6.6 Early Return from Functions

Return early when result is determined to skip unnecessary processing.

**Incorrect (processes all items even after finding answer):**

```ts
function validateUsers(users: User[]) {
  let hasError = false;
  let errorMessage = '';

  for (const user of users) {
    if (!user.email) {
      hasError = true;
      errorMessage = 'Email required';
    }
    if (!user.name) {
      hasError = true;
      errorMessage = 'Name required';
    }
    // Continues checking all users even after error found
  }

  return hasError ? {valid: false, error: errorMessage} : {valid: true};
}
```

**Correct (returns immediately on first error):**

```ts
function validateUsers(users: User[]) {
  for (const user of users) {
    if (!user.email) {
      return {valid: false, error: 'Email required'};
    }
    if (!user.name) {
      return {valid: false, error: 'Name required'};
    }
  }

  return {valid: true};
}
```

### 6.7 Hoist RegExp Creation

Don't create RegExp inside render. Hoist to module scope or memoize with `useMemo()`.

**Incorrect (new RegExp every render):**

```tsx
function Highlighter({text, query}: Props) {
  const regex = new RegExp(`(${query})`, 'gi');
  const parts = text.split(regex);
  return <>{parts.map((part, i) => ...)}</>;
}
```

**Correct (memoize or hoist):**

```tsx
const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

function Highlighter({text, query}: Props) {
  const regex = useMemo(
    () => new RegExp(`(${escapeRegex(query)})`, 'gi'),
    [query],
  );
  const parts = text.split(regex);
  return <>{parts.map((part, i) => ...)}</>;
}
```

**Warning (global regex has mutable state):**

Global regex (`/g`) has mutable `lastIndex` state:

```ts
const regex = /foo/g;
regex.test('foo'); // true, lastIndex = 3
regex.test('foo'); // false, lastIndex = 0
```

### 6.8 Build Index Maps for Repeated Lookups

Multiple `.find()` calls by the same key should use a Map.

**Incorrect (O(n) per lookup):**

```ts
function processOrders(orders: Order[], users: User[]) {
  return orders.map((order) => ({
    ...order,
    user: users.find((u) => u.id === order.userId),
  }));
}
```

**Correct (O(1) per lookup):**

```ts
function processOrders(orders: Order[], users: User[]) {
  const userById = new Map(users.map((u) => [u.id, u]));

  return orders.map((order) => ({
    ...order,
    user: userById.get(order.userId),
  }));
}
```

Build map once (O(n)), then all lookups are O(1).
For 1000 orders × 1000 users: 1M ops → 2K ops.

### 6.9 Early Length Check for Array Comparisons

When comparing arrays with expensive operations (sorting, deep equality, serialization), check lengths first. If lengths differ, the arrays cannot be equal.

In real-world applications, this optimization is especially valuable when the comparison runs in hot paths (event handlers, render loops).

**Incorrect (always runs expensive comparison):**

```ts
function hasChanges(current: string[], original: string[]) {
  // Always sorts and joins, even when lengths differ
  return current.sort().join() !== original.sort().join();
}
```

Two O(n log n) sorts run even when `current.length` is 5 and `original.length` is 100. There is also overhead of joining the arrays and comparing the strings.

**Correct (O(1) length check first):**

```ts
function hasChanges(current: string[], original: string[]) {
  // Early return if lengths differ
  if (current.length !== original.length) {
    return true;
  }
  // Only sort when lengths match
  const currentSorted = current.toSorted();
  const originalSorted = original.toSorted();
  for (let i = 0; i < currentSorted.length; i++) {
    if (currentSorted[i] !== originalSorted[i]) {
      return true;
    }
  }
  return false;
}
```

This approach is more efficient because:

- It avoids the overhead of sorting and joining the arrays when lengths differ
- It avoids consuming memory for the joined strings (especially important for large arrays)
- It avoids mutating the original arrays
- It returns early when a difference is found

### 6.10 Use Loop for Min/Max Instead of Sort

Finding the smallest or largest element only requires a single pass through the array. Sorting is wasteful and slower.

**Incorrect (O(n log n) - sort to find latest):**

```ts
interface Project {
  id: string;
  name: string;
  updatedAt: number;
}

function getLatestProject(projects: Project[]) {
  const sorted = [...projects].sort((a, b) => b.updatedAt - a.updatedAt);
  return sorted[0];
}
```

Sorts the entire array just to find the maximum value.

**Incorrect (O(n log n) - sort for oldest and newest):**

```ts
function getOldestAndNewest(projects: Project[]) {
  const sorted = [...projects].sort((a, b) => a.updatedAt - b.updatedAt);
  return {oldest: sorted[0], newest: sorted[sorted.length - 1]};
}
```

Still sorts unnecessarily when only min/max are needed.

**Correct (O(n) - single loop):**

```ts
function getLatestProject(projects: Project[]) {
  if (projects.length === 0) return null;

  let latest = projects[0];

  for (let i = 1; i < projects.length; i++) {
    if (projects[i].updatedAt > latest.updatedAt) {
      latest = projects[i];
    }
  }

  return latest;
}

function getOldestAndNewest(projects: Project[]) {
  if (projects.length === 0) return {oldest: null, newest: null};

  let oldest = projects[0];
  let newest = projects[0];

  for (let i = 1; i < projects.length; i++) {
    if (projects[i].updatedAt < oldest.updatedAt) oldest = projects[i];
    if (projects[i].updatedAt > newest.updatedAt) newest = projects[i];
  }

  return {oldest, newest};
}
```

Single pass through the array, no copying, no sorting.

**Alternative (Math.min/Math.max for small arrays):**

```ts
const numbers = [5, 2, 8, 1, 9];
const min = Math.min(...numbers);
const max = Math.max(...numbers);
```

This works for small arrays, but can be slower or throw for very large arrays due to spread operator limitations. Use the loop approach for reliability.

### 6.11 Use Set/Map for O(1) Lookups

Convert arrays to Set/Map for repeated membership checks.

**Incorrect (O(n) per check):**

```ts
const allowedIds = ['a', 'b', 'c', ...];
items.filter((item) => allowedIds.includes(item.id));
```

**Correct (O(1) per check):**

```ts
const allowedIds = new Set(['a', 'b', 'c', ...]);
items.filter((item) => allowedIds.has(item.id));
```

### 6.12 Use toSorted() Instead of sort() for Immutability

`.sort()` mutates the array in place, which can cause bugs with React state and props. Use `.toSorted()` to create a new sorted array without mutation.

**Incorrect (mutates original array):**

```ts
function UserList({users}: {users: User[]}) {
  // Mutates the users prop array!
  const sorted = useMemo(
    () => users.sort((a, b) => a.name.localeCompare(b.name)),
    [users],
  );
  return <div>{sorted.map(renderUser)}</div>;
}
```

**Correct (creates new array):**

```ts
function UserList({users}: {users: User[]}) {
  // Creates new sorted array, original unchanged
  const sorted = useMemo(
    () => users.toSorted((a, b) => a.name.localeCompare(b.name)),
    [users],
  );
  return <div>{sorted.map(renderUser)}</div>;
}
```

**Why this matters in React:**

1. Props/state mutations break React's immutability model - React expects props and state to be treated as read-only
2. Causes stale closure bugs - Mutating arrays inside closures (callbacks, effects) can lead to unexpected behavior

**Browser support (fallback for older browsers):**

`.toSorted()` is available in all modern browsers (Chrome 110+, Safari 16+, Firefox 115+, Node.js 20+). For older environments, use spread operator:

```ts
// Fallback for older browsers
const sorted = [...items].sort((a, b) => a.value - b.value);
```

**Other immutable array methods:**

- `.toSorted()` - immutable sort
- `.toReversed()` - immutable reverse
- `.toSpliced()` - immutable splice
- `.with()` - immutable element replacement


## 7. Documentation

### 7.1 Use Fancy Quotes in Documentation Prose, Not in Code

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

