# React / TypeScript Best Practices

**Version 1.0.0**
React/TypeScript

> **Note:**
> This document is for agents and LLMs when maintaining, generating, or refactoring
> React and TypeScript codebases.

---

## Abstract

Performance and best-practices guide for React and TypeScript applications.
Rules across 8 categories: project conventions, eliminating async waterfalls, bundle
optimization, client-side data fetching, re-render optimization, rendering, JavaScript
micro-optimizations, and advanced patterns. Each rule includes incorrect vs. correct examples.

---

## Table of Contents

1. [Project & tooling conventions](#1-project-&-tooling-conventions) — **HIGH**
   - 1.1 Prefer Inline `type` Specifiers in Re-exports
   - 1.2 Respect Local ESLint, Prettier/oxfmt, and tsconfig
   - 1.3 Use beeftools When Available

2. [Eliminating Waterfalls](#2-eliminating-waterfalls) — **CRITICAL**
   - 2.1 Defer Await Until Needed
   - 2.2 Dependency-Based Parallelization
   - 2.3 Promise.all() for Independent Operations

3. [Bundle Size Optimization](#3-bundle-size-optimization) — **CRITICAL**
   - 3.1 Prefer Barrel Imports; Avoid Over-Optimizing
   - 3.2 Conditional Module Loading
   - 3.3 Defer Non-Critical Third-Party Libraries
   - 3.4 Dynamic Imports for Heavy Components
   - 3.5 Preload Based on User Intent

4. [Client-Side Data Fetching](#4-client-side-data-fetching) — **MEDIUM-HIGH**
   - 4.1 Deduplicate Global Event Listeners
   - 4.2 Version and Minimize localStorage Data
   - 4.3 Use Passive Event Listeners for Scrolling Performance
   - 4.4 Use SWR for Automatic Deduplication

5. [Re-render Optimization](#5-re-render-optimization) — **MEDIUM**
   - 5.1 Defer State Reads to Usage Point
   - 5.2 Narrow Effect Dependencies
   - 5.3 Calculate Derived State During Rendering
   - 5.4 Subscribe to Derived State
   - 5.5 Use Functional setState Updates
   - 5.6 Use Lazy State Initialization
   - 5.7 Extract Default Non-primitive Parameter Value from Memoized Component to Constant
   - 5.8 Extract to Memoized Components
   - 5.9 Put Interaction Logic in Event Handlers
   - 5.10 Do not wrap a simple expression with a primitive result type in useMemo
   - 5.11 Use Transitions for Non-Urgent Updates
   - 5.12 Use useRef for Transient Values

6. [Rendering Performance](#6-rendering-performance) — **MEDIUM**
   - 6.1 Use Activity Component for Show/Hide
   - 6.2 Animate SVG Wrapper Instead of SVG Element
   - 6.3 Use Explicit Conditional Rendering
   - 6.4 CSS content-visibility for Long Lists
   - 6.5 Hoist Static JSX Elements
   - 6.6 Prevent Hydration Mismatch Without Flickering
   - 6.7 Suppress Expected Hydration Mismatches
   - 6.8 Optimize SVG Precision
   - 6.9 Use useTransition Over Manual Loading States

7. [JavaScript Performance](#7-javascript-performance) — **LOW-MEDIUM**
   - 7.1 Avoid Layout Thrashing
   - 7.2 Cache Repeated Function Calls
   - 7.3 Cache Property Access in Loops
   - 7.4 Cache Storage API Calls
   - 7.5 Combine Multiple Array Iterations
   - 7.6 Early Return from Functions
   - 7.7 Hoist RegExp Creation
   - 7.8 Build Index Maps for Repeated Lookups
   - 7.9 Early Length Check for Array Comparisons
   - 7.10 Use Loop for Min/Max Instead of Sort
   - 7.11 Use Set/Map for O(1) Lookups
   - 7.12 Use toSorted() Instead of sort() for Immutability

8. [Advanced Patterns](#8-advanced-patterns) — **LOW**
   - 8.1 Store Event Handlers in Refs
   - 8.2 Initialize App Once, Not Per Mount
   - 8.3 useEffectEvent for Stable Callback Refs

---

## 1. Project & tooling conventions

### 1.1 Prefer Inline `type` Specifiers in Re-exports

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

**Exception — type-only modules:** When *every* specifier is a type, still use `export type` so the entire import is erased and no runtime module reference remains:

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
    "verbatimModuleSyntax": true
  }
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
    "typescript/consistent-type-imports": ["warn", {
      "prefer": "type-imports",
      "fixStyle": "inline-type-imports"
    }]
  }
}
```

For ESLint with typescript-eslint, the equivalent is:

```jsonc
// eslint.config.js (flat config)
{
  "rules": {
    "@typescript-eslint/consistent-type-imports": ["warn", {
      "prefer": "type-imports",
      "fixStyle": "inline-type-imports"
    }]
  }
}
```

### Exports side — no lint rule needed yet

There is no `consistent-type-exports` rule in oxlint as of early 2026. The equivalent rule exists in typescript-eslint but requires type-aware linting. In practice, `verbatimModuleSyntax` already enforces the export side at the TypeScript compiler level, so no additional lint rule is required.

### Formatters (oxfmt, Prettier, etc.)

Formatters have no opinion on inline vs. separate type specifiers — they format whichever style is written. No formatter configuration is needed for this convention.

Reference: [TypeScript 4.5 — Inline type modifiers](https://www.typescriptlang.org/docs/handbook/release-notes/typescript-4-5.html#type-modifiers-on-import-names)

### 1.2 Respect Local ESLint, Prettier/oxfmt, and tsconfig

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

### 1.3 Use beeftools When Available

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
const [user, config] = await Promise.all([
  fetchUser(),
  fetchConfig(),
]);
const profile = await fetchProfile(user.id);
```

**Correct (config and profile run in parallel):**

```ts
import {all} from 'better-all';

const {user, config, profile} = await all({
  async user() { return fetchUser() },
  async config() { return fetchConfig() },
  async profile() {
    return fetchProfile((await this.$.user).id)
  },
});
```

**Alternative without extra dependencies:**

We can also create all the promises first, and do `Promise.all()` at the end.

```ts
const userPromise = fetchUser();
const profilePromise = userPromise.then((user) => fetchProfile(user.id));

const [user, config, profile] = await Promise.all([
  userPromise,
  fetchConfig(),
  profilePromise,
]);
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
const [user, posts, comments] = await Promise.all([
  fetchUser(),
  fetchPosts(),
  fetchComments(),
]);
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

### 3.2 Conditional Module Loading

Load large data or modules only when a feature is activated.

**Example (lazy-load animation frames):**

```tsx
function AnimationPlayer({enabled, setEnabled}: {enabled: boolean; setEnabled: React.Dispatch<React.SetStateAction<boolean>>}) {
  const [frames, setFrames] = useState<Frame[] | null>(null);

  useEffect(() => {
    if (enabled && !frames && typeof window !== 'undefined') {
      import('./animation-frames.js')
        .then((mod) => setFrames(mod.frames))
        .catch(() => setEnabled(false));
    }
  }, [enabled, frames, setEnabled]);

  if (!frames) return <Skeleton />;
  return <Canvas frames={frames} />;
}
```

The `typeof window !== 'undefined'` check avoids loading this module in SSR environments, optimizing server bundle size and build speed when applicable.

### 3.3 Defer Non-Critical Third-Party Libraries

Analytics, logging, and error tracking don't need to block initial render. Load them after the app has mounted or on first user interaction using dynamic `import()`.

**Incorrect (blocks initial bundle):**

```tsx
import {Analytics} from '@vercel/analytics/react';

export default function RootLayout({children}: {children: React.ReactNode}) {
  return (
    <>
      {children}
      <Analytics />
    </>
  );
}
```

**Correct (loads after mount):**

```tsx
import {useEffect, useState} from 'react';

function AnalyticsLoader({children}: {children: React.ReactNode}) {
  const [Analytics, setAnalytics] = useState<React.ComponentType | null>(null);

  useEffect(() => {
    import('@vercel/analytics/react').then((mod) => setAnalytics(() => mod.Analytics));
  }, []);

  return (
    <>
      {children}
      {Analytics ? <Analytics /> : null}
    </>
  );
}
```

Alternatively, load on first interaction (e.g. first click or route change) with `import()` inside the handler so the analytics script never blocks the initial bundle.

### 3.4 Dynamic Imports for Heavy Components

Use `React.lazy()` and `<Suspense>` to lazy-load large components not needed on initial render. This keeps the main bundle smaller and improves Time to Interactive.

**Incorrect (Monaco bundles with main chunk):**

```tsx
import {MonacoEditor} from './monaco-editor';

function CodePanel({code}: {code: string}) {
  return <MonacoEditor value={code} />;
}
```

**Correct (Monaco loads on demand):**

```tsx
import {lazy, Suspense} from 'react';

const MonacoEditor = lazy(() =>
  import('./monaco-editor').then((m) => ({default: m.MonacoEditor})),
);

function CodePanel({code}: {code: string}) {
  return (
    <Suspense fallback={<div>Loading editor…</div>}>
      <MonacoEditor value={code} />
    </Suspense>
  );
}
```

Use the same pattern for route-level or heavy UI (charts, rich editors) so they load only when needed.

Reference: [React lazy](https://react.dev/reference/react/lazy)

### 3.5 Preload Based on User Intent

Preload heavy bundles before they're needed to reduce perceived latency.

**Example (preload on hover/focus):**

```tsx
function EditorButton({onClick}: {onClick: () => void}) {
  const preload = () => {
    if (typeof window !== 'undefined') {
      void import('./monaco-editor');
    }
  };

  return (
    <button
      onMouseEnter={preload}
      onFocus={preload}
      onClick={onClick}
    >
      Open Editor
    </button>
  );
}
```

**Example (preload when feature flag is enabled):**

```tsx
function FlagsProvider({children, flags}: Props) {
  useEffect(() => {
    if (flags.editorEnabled && typeof window !== 'undefined') {
      void import('./monaco-editor').then((mod) => mod.init());
    }
  }, [flags.editorEnabled]);

  return (
    <FlagsContext.Provider value={flags}>
      {children}
    </FlagsContext.Provider>
  );
}
```

The `typeof window !== 'undefined'` check avoids bundling preloaded modules in SSR builds when applicable.


## 4. Client-Side Data Fetching

### 4.1 Deduplicate Global Event Listeners

Use `useSWRSubscription()` to share global event listeners across component instances.

**Incorrect (N instances = N listeners):**

```tsx
function useKeyboardShortcut(key: string, callback: () => void) {
  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (e.metaKey && e.key === key) {
        callback();
      }
    };
    window.addEventListener('keydown', handler);
    return () => window.removeEventListener('keydown', handler);
  }, [key, callback]);
}
```

When using the `useKeyboardShortcut` hook multiple times, each instance will register a new listener.

**Correct (N instances = 1 listener):**

```tsx
import useSWRSubscription from 'swr/subscription';

// Module-level Map to track callbacks per key
const keyCallbacks = new Map<string, Set<() => void>>();

function useKeyboardShortcut(key: string, callback: () => void) {
  // Register this callback in the Map
  useEffect(() => {
    if (!keyCallbacks.has(key)) {
      keyCallbacks.set(key, new Set());
    }
    keyCallbacks.get(key)!.add(callback);

    return () => {
      const set = keyCallbacks.get(key);
      if (set) {
        set.delete(callback);
        if (set.size === 0) {
          keyCallbacks.delete(key);
        }
      }
    };
  }, [key, callback]);

  useSWRSubscription('global-keydown', () => {
    const handler = (e: KeyboardEvent) => {
      if (e.metaKey && keyCallbacks.has(e.key)) {
        keyCallbacks.get(e.key)!.forEach((cb) => cb());
      }
    };
    window.addEventListener('keydown', handler);
    return () => window.removeEventListener('keydown', handler);
  });
}

function Profile() {
  // Multiple shortcuts will share the same listener
  useKeyboardShortcut('p', () => { /* ... */ });
  useKeyboardShortcut('k', () => { /* ... */ });
  // ...
}
```

### 4.2 Version and Minimize localStorage Data

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
    localStorage.setItem('prefs:v1', JSON.stringify({
      theme: user.preferences.theme,
      notifications: user.preferences.notifications,
    }));
  } catch {}
}
```

**Always wrap in try-catch:** `getItem()` and `setItem()` throw in incognito/private browsing (Safari, Firefox), when quota exceeded, or when disabled.

**Benefits:** Schema evolution via versioning, reduced storage size, prevents storing tokens/PII/internal flags.

### 4.3 Use Passive Event Listeners for Scrolling Performance

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

### 4.4 Use SWR for Automatic Deduplication

SWR enables request deduplication, caching, and revalidation across component instances.

**Incorrect (no deduplication, each instance fetches):**

```tsx
function UserList() {
  const [users, setUsers] = useState([]);

  useEffect(() => {
    fetch('/api/users')
      .then((r) => r.json())
      .then(setUsers);
  }, []);
}
```

**Correct (multiple instances share one request):**

```tsx
import useSWR from 'swr';

function UserList() {
  const {data: users} = useSWR('/api/users', fetcher);
}
```

**For immutable data:**

```tsx
import {useImmutableSWR} from '@/lib/swr';

function StaticContent() {
  const {data} = useImmutableSWR('/api/config', fetcher);
}
```

**For mutations:**

```tsx
import {useSWRMutation} from 'swr/mutation';

function UpdateButton() {
  const {trigger} = useSWRMutation('/api/user', updateUser);
  return <button onClick={trigger}>Update</button>;
}
```

Reference: [https://swr.vercel.app](https://swr.vercel.app)


## 5. Re-render Optimization

### 5.1 Defer State Reads to Usage Point

Don't subscribe to dynamic state (e.g. URL params, localStorage) if you only read it inside callbacks. Subscribing causes re-renders whenever that state changes even though you don't render from it.

**Incorrect (subscribes to URL changes for use only in callback):**

```tsx
function ShareButton({chatId}: {chatId: string}) {
  const [params, setParams] = useState(() => new URLSearchParams(window.location.search));

  useEffect(() => {
    const onPopState = () => setParams(new URLSearchParams(window.location.search));
    window.addEventListener('popstate', onPopState);
    return () => window.removeEventListener('popstate', onPopState);
  }, []);

  const handleShare = () => {
    const ref = params.get('ref');
    shareChat(chatId, {ref});
  };

  return <button onClick={handleShare}>Share</button>;
}
```

**Correct (reads on demand in callback, no subscription):**

```tsx
function ShareButton({chatId}: {chatId: string}) {
  const handleShare = () => {
    const params = new URLSearchParams(window.location.search);
    const ref = params.get('ref');
    shareChat(chatId, {ref});
  };

  return <button onClick={handleShare}>Share</button>;
}
```

Same idea applies to any reactive value you only use inside event handlers or effects: read it at the point of use instead of subscribing.

### 5.2 Narrow Effect Dependencies

Specify primitive dependencies instead of objects to minimize effect re-runs.

**Incorrect (re-runs on any user field change):**

```tsx
useEffect(() => {
  console.log(user.id);
}, [user]);
```

**Correct (re-runs only when id changes):**

```tsx
useEffect(() => {
  console.log(user.id);
}, [user.id]);
```

**For derived state, compute outside effect:**

```tsx
// Incorrect: runs on width=767, 766, 765...
useEffect(() => {
  if (width < 768) {
    enableMobileMode();
  }
}, [width]);

// Correct: runs only on boolean transition
const isMobile = width < 768;
useEffect(() => {
  if (isMobile) {
    enableMobileMode();
  }
}, [isMobile]);
```

### 5.3 Calculate Derived State During Rendering

If a value can be computed from current props/state, do not store it in state or update it in an effect. Derive it during render to avoid extra renders and state drift. Do not set state in effects solely in response to prop changes; prefer derived values or keyed resets instead.

**Incorrect (redundant state and effect):**

```tsx
function Form() {
  const [firstName, setFirstName] = useState('First');
  const [lastName, setLastName] = useState('Last');
  const [fullName, setFullName] = useState('');

  useEffect(() => {
    setFullName(firstName + ' ' + lastName);
  }, [firstName, lastName]);

  return <p>{fullName}</p>;
}
```

**Correct (derive during render):**

```tsx
function Form() {
  const [firstName, setFirstName] = useState('First');
  const [lastName, setLastName] = useState('Last');
  const fullName = firstName + ' ' + lastName;

  return <p>{fullName}</p>;
}
```

References: [You Might Not Need an Effect](https://react.dev/learn/you-might-not-need-an-effect)

### 5.4 Subscribe to Derived State

Subscribe to derived boolean state instead of continuous values to reduce re-render frequency.

**Incorrect (re-renders on every pixel change):**

```tsx
function Sidebar() {
  const width = useWindowWidth();  // updates continuously
  const isMobile = width < 768;
  return <nav className={isMobile ? 'mobile' : 'desktop'} />;
}
```

**Correct (re-renders only when boolean changes):**

```tsx
function Sidebar() {
  const isMobile = useMediaQuery('(max-width: 767px)');
  return <nav className={isMobile ? 'mobile' : 'desktop'} />;
}
```

### 5.5 Use Functional setState Updates

When updating state based on the current state value, use the functional update form of setState instead of directly referencing the state variable. This prevents stale closures, eliminates unnecessary dependencies, and creates stable callback references.

**Incorrect (requires state as dependency):**

```tsx
function TodoList() {
  const [items, setItems] = useState(initialItems);

  // Callback must depend on items, recreated on every items change
  const addItems = useCallback((newItems: Item[]) => {
    setItems([...items, ...newItems]);
  }, [items]);  // ❌ items dependency causes recreations

  // Risk of stale closure if dependency is forgotten
  const removeItem = useCallback((id: string) => {
    setItems(items.filter((item) => item.id !== id));
  }, []);  // ❌ Missing items dependency - will use stale items!

  return <ItemsEditor items={items} onAdd={addItems} onRemove={removeItem} />;
}
```

The first callback is recreated every time `items` changes, which can cause child components to re-render unnecessarily. The second callback has a stale closure bug—it will always reference the initial `items` value.

**Correct (stable callbacks, no stale closures):**

```tsx
function TodoList() {
  const [items, setItems] = useState(initialItems);

  // Stable callback, never recreated
  const addItems = useCallback((newItems: Item[]) => {
    setItems((curr) => [...curr, ...newItems]);
  }, []);  // ✅ No dependencies needed

  // Always uses latest state, no stale closure risk
  const removeItem = useCallback((id: string) => {
    setItems((curr) => curr.filter((item) => item.id !== id));
  }, []);  // ✅ Safe and stable

  return <ItemsEditor items={items} onAdd={addItems} onRemove={removeItem} />;
}
```

**Benefits:**

1. **Stable callback references** - Callbacks don't need to be recreated when state changes
2. **No stale closures** - Always operates on the latest state value
3. **Fewer dependencies** - Simplifies dependency arrays and reduces memory leaks
4. **Prevents bugs** - Eliminates the most common source of React closure bugs

**When to use functional updates:**

- Any setState that depends on the current state value
- Inside useCallback/useMemo when state is needed
- Event handlers that reference state
- Async operations that update state

**When direct updates are fine:**

- Setting state to a static value: `setCount(0)`
- Setting state from props/arguments only: `setName(newName)`
- State doesn't depend on previous value

**Note:** If your project has [React Compiler](https://react.dev/learn/react-compiler) enabled, the compiler can automatically optimize some cases, but functional updates are still recommended for correctness and to prevent stale closure bugs.

### 5.6 Use Lazy State Initialization

Pass a function to `useState` for expensive initial values. Without the function form, the initializer runs on every render even though the value is only used once.

**Incorrect (runs on every render):**

```tsx
function FilteredList({items}: {items: Item[]}) {
  // buildSearchIndex() runs on EVERY render, even after initialization
  const [searchIndex, setSearchIndex] = useState(buildSearchIndex(items));
  const [query, setQuery] = useState('');

  // When query changes, buildSearchIndex runs again unnecessarily
  return <SearchResults index={searchIndex} query={query} />;
}

function UserProfile() {
  // JSON.parse runs on every render
  const [settings, setSettings] = useState(
    JSON.parse(localStorage.getItem('settings') || '{}'),
  );

  return <SettingsForm settings={settings} onChange={setSettings} />;
}
```

**Correct (runs only once):**

```tsx
function FilteredList({items}: {items: Item[]}) {
  // buildSearchIndex() runs ONLY on initial render
  const [searchIndex, setSearchIndex] = useState(() => buildSearchIndex(items));
  const [query, setQuery] = useState('');

  return <SearchResults index={searchIndex} query={query} />;
}

function UserProfile() {
  // JSON.parse runs only on initial render
  const [settings, setSettings] = useState(() => {
    const stored = localStorage.getItem('settings');
    return stored ? JSON.parse(stored) : {};
  });

  return <SettingsForm settings={settings} onChange={setSettings} />;
}
```

Use lazy initialization when computing initial values from localStorage/sessionStorage, building data structures (indexes, maps), reading from the DOM, or performing heavy transformations.

For simple primitives (`useState(0)`), direct references (`useState(props.value)`), or cheap literals (`useState({})`), the function form is unnecessary.

### 5.7 Extract Default Non-primitive Parameter Value from Memoized Component to Constant

When memoized component has a default value for some non-primitive optional parameter, such as an array, function, or object, calling the component without that parameter results in broken memoization. This is because new value instances are created on every rerender, and they do not pass strict equality comparison in `memo()`.

To address this issue, extract the default value into a constant.

**Incorrect (`onClick` has different values on every rerender):**

```tsx
const UserAvatar = memo(function UserAvatar({onClick = () => {}}: {onClick?: () => void}) {
  // ...
});

// Used without optional onClick
<UserAvatar />
```

**Correct (stable default value):**

```tsx
const NOOP = () => {};

const UserAvatar = memo(function UserAvatar({onClick = NOOP}: {onClick?: () => void}) {
  // ...
});

// Used without optional onClick
<UserAvatar />
```

### 5.8 Extract to Memoized Components

Extract expensive work into memoized components to enable early returns before computation.

**Incorrect (computes avatar even when loading):**

```tsx
function Profile({user, loading}: Props) {
  const avatar = useMemo(() => {
    const id = computeAvatarId(user);
    return <Avatar id={id} />;
  }, [user]);

  if (loading) return <Skeleton />;
  return <div>{avatar}</div>;
}
```

**Correct (skips computation when loading):**

```tsx
const UserAvatar = memo(function UserAvatar({user}: {user: User}) {
  const id = useMemo(() => computeAvatarId(user), [user]);
  return <Avatar id={id} />;
});

function Profile({user, loading}: Props) {
  if (loading) return <Skeleton />;
  return (
    <div>
      <UserAvatar user={user} />
    </div>
  );
}
```

**Note:** If your project has [React Compiler](https://react.dev/learn/react-compiler) enabled, manual memoization with `memo()` and `useMemo()` is not necessary. The compiler automatically optimizes re-renders.

### 5.9 Put Interaction Logic in Event Handlers

If a side effect is triggered by a specific user action (submit, click, drag), run it in that event handler. Do not model the action as state + effect; it makes effects re-run on unrelated changes and can duplicate the action.

**Incorrect (event modeled as state + effect):**

```tsx
function Form() {
  const [submitted, setSubmitted] = useState(false);
  const theme = useContext(ThemeContext);

  useEffect(() => {
    if (submitted) {
      post('/api/register');
      showToast('Registered', theme);
    }
  }, [submitted, theme]);

  return <button onClick={() => setSubmitted(true)}>Submit</button>;
}
```

**Correct (do it in the handler):**

```tsx
function Form() {
  const theme = useContext(ThemeContext);

  function handleSubmit() {
    post('/api/register');
    showToast('Registered', theme);
  }

  return <button onClick={handleSubmit}>Submit</button>;
}
```

Reference: [Should this code move to an event handler?](https://react.dev/learn/removing-effect-dependencies#should-this-code-move-to-an-event-handler)

### 5.10 Do not wrap a simple expression with a primitive result type in useMemo

When an expression is simple (few logical or arithmetical operators) and has a primitive result type (boolean, number, string), do not wrap it in `useMemo`.
Calling `useMemo` and comparing hook dependencies may consume more resources than the expression itself.

**Incorrect:**

```tsx
function Header({user, notifications}: Props) {
  const isLoading = useMemo(() => {
    return user.isLoading || notifications.isLoading;
  }, [user.isLoading, notifications.isLoading]);

  if (isLoading) return <Skeleton />;
  // return some markup
}
```

**Correct:**

```tsx
function Header({user, notifications}: Props) {
  const isLoading = user.isLoading || notifications.isLoading;

  if (isLoading) return <Skeleton />;
  // return some markup
}
```

### 5.11 Use Transitions for Non-Urgent Updates

Mark frequent, non-urgent state updates as transitions to maintain UI responsiveness.

**Incorrect (blocks UI on every scroll):**

```tsx
function ScrollTracker() {
  const [scrollY, setScrollY] = useState(0);
  useEffect(() => {
    const handler = () => setScrollY(window.scrollY);
    window.addEventListener('scroll', handler, {passive: true});
    return () => window.removeEventListener('scroll', handler);
  }, []);
}
```

**Correct (non-blocking updates):**

```tsx
import {startTransition} from 'react';

function ScrollTracker() {
  const [scrollY, setScrollY] = useState(0);
  useEffect(() => {
    const handler = () => {
      startTransition(() => setScrollY(window.scrollY));
    };
    window.addEventListener('scroll', handler, {passive: true});
    return () => window.removeEventListener('scroll', handler);
  }, []);
}
```

### 5.12 Use useRef for Transient Values

When a value changes frequently and you don't want a re-render on every update (e.g., mouse trackers, intervals, transient flags), store it in `useRef` instead of `useState`. Keep component state for UI; use refs for temporary DOM-adjacent values. Updating a ref does not trigger a re-render.

**Incorrect (renders every update):**

```tsx
function Tracker() {
  const [lastX, setLastX] = useState(0);

  useEffect(() => {
    const onMove = (e: MouseEvent) => setLastX(e.clientX);
    window.addEventListener('mousemove', onMove);
    return () => window.removeEventListener('mousemove', onMove);
  }, []);

  return (
    <div
      style={{
        position: 'fixed',
        top: 0,
        left: lastX,
        width: 8,
        height: 8,
        background: 'black',
      }}
    />
  );
}
```

**Correct (no re-render for tracking):**

```tsx
function Tracker() {
  const lastXRef = useRef(0);
  const dotRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const onMove = (e: MouseEvent) => {
      lastXRef.current = e.clientX;
      const node = dotRef.current;
      if (node) {
        node.style.transform = `translateX(${e.clientX}px)`;
      }
    };
    window.addEventListener('mousemove', onMove);
    return () => window.removeEventListener('mousemove', onMove);
  }, []);

  return (
    <div
      ref={dotRef}
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        width: 8,
        height: 8,
        background: 'black',
        transform: 'translateX(0px)',
      }}
    />
  );
}
```


## 6. Rendering Performance

### 6.1 Use Activity Component for Show/Hide

If working in project that is using the most recent version of React, you can use React's `<Activity>` to preserve state/DOM for expensive components that frequently toggle visibility.

**Usage:**

```tsx
import {Activity} from 'react';

function Dropdown({isOpen}: Props) {
  return (
    <Activity mode={isOpen ? 'visible' : 'hidden'}>
      <ExpensiveMenu />
    </Activity>
  );
}
```

Avoids expensive re-renders and state loss.

### 6.2 Animate SVG Wrapper Instead of SVG Element

Many browsers don't have hardware acceleration for CSS3 animations on SVG elements. Wrap SVG in a `<div>` and animate the wrapper instead.

**Incorrect (animating SVG directly - no hardware acceleration):**

```tsx
function LoadingSpinner() {
  return (
    <svg
      className="animate-spin"
      width="24"
      height="24"
      viewBox="0 0 24 24"
    >
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
      <svg
        width="24"
        height="24"
        viewBox="0 0 24 24"
      >
        <circle cx="12" cy="12" r="10" stroke="currentColor" />
      </svg>
    </div>
  );
}
```

This applies to all CSS transforms and transitions (`transform`, `opacity`, `translate`, `scale`, `rotate`). The wrapper div allows browsers to use GPU acceleration for smoother animations.

### 6.3 Use Explicit Conditional Rendering

Use explicit ternary operators (`? :`) instead of `&&` for conditional rendering when the condition can be `0`, `NaN`, or other falsy values that render.

**Incorrect (renders "0" when count is 0):**

```tsx
function Badge({count}: {count: number}) {
  return (
    <div>
      {count && <span className="badge">{count}</span>}
    </div>
  );
}

// When count = 0, renders: <div>0</div>
// When count = 5, renders: <div><span class="badge">5</span></div>
```

**Correct (renders nothing when count is 0):**

```tsx
function Badge({count}: {count: number}) {
  return (
    <div>
      {count > 0 ? <span className="badge">{count}</span> : null}
    </div>
  );
}

// When count = 0, renders: <div></div>
// When count = 5, renders: <div><span class="badge">5</span></div>
```

### 6.4 CSS content-visibility for Long Lists

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

### 6.5 Hoist Static JSX Elements

Extract static JSX outside components to avoid re-creation.

**Incorrect (recreates element every render):**

```tsx
function LoadingSkeleton() {
  return <div className="animate-pulse h-20 bg-gray-200" />;
}

function Container() {
  return (
    <div>
      {loading && <LoadingSkeleton />}
    </div>
  );
}
```

**Correct (reuses same element):**

```tsx
const loadingSkeleton = (
  <div className="animate-pulse h-20 bg-gray-200" />
);

function Container() {
  return (
    <div>
      {loading && loadingSkeleton}
    </div>
  );
}
```

This is especially helpful for large and static SVG nodes, which can be expensive to recreate on every render.

**Note:** If your project has [React Compiler](https://react.dev/learn/react-compiler) enabled, the compiler automatically hoists static JSX elements and optimizes component re-renders, making manual hoisting unnecessary.

### 6.6 Prevent Hydration Mismatch Without Flickering

When using SSR (e.g. Vite SSR, Remix, or any React SSR setup), content that depends on client-only APIs (localStorage, cookies) can cause breakage or flicker. Avoid both by injecting a synchronous script that updates the DOM before React hydrates.

**Incorrect (breaks SSR):**

```tsx
function ThemeWrapper({children}: {children: ReactNode}) {
  // localStorage is not available on server - throws error
  const theme = localStorage.getItem('theme') || 'light';

  return (
    <div className={theme}>
      {children}
    </div>
  );
}
```

In SSR applications the server has no `localStorage`, so this will throw.

**Incorrect (visual flickering):**

```tsx
function ThemeWrapper({children}: {children: ReactNode}) {
  const [theme, setTheme] = useState('light');

  useEffect(() => {
    // Runs after hydration - causes visible flash
    const stored = localStorage.getItem('theme');
    if (stored) {
      setTheme(stored);
    }
  }, []);

  return (
    <div className={theme}>
      {children}
    </div>
  );
}
```

Component first renders with default value (`light`), then updates after hydration, causing a visible flash.

**Correct (no flicker, no hydration mismatch):**

```tsx
function ThemeWrapper({children}: {children: ReactNode}) {
  return (
    <>
      <div id="theme-wrapper">
        {children}
      </div>
      <script
        dangerouslySetInnerHTML={{
          __html: `
            (function() {
              try {
                var theme = localStorage.getItem('theme') || 'light';
                var el = document.getElementById('theme-wrapper');
                if (el) el.className = theme;
              } catch (e) {}
            })();
          `,
        }}
      />
    </>
  );
}
```

The inline script runs before React hydrates, so the DOM already has the correct value. No flickering, no hydration mismatch.

Use this pattern for theme toggles, user preferences, and any client-only data that should appear immediately without flashing defaults.

### 6.7 Suppress Expected Hydration Mismatches

In SSR applications, some values are intentionally different on server vs client (random IDs, dates, locale/timezone formatting). For these *expected* mismatches, wrap the dynamic text in an element with `suppressHydrationWarning` to prevent noisy warnings. Do not use this to hide real bugs. Don't overuse it.

**Incorrect (known mismatch warnings):**

```tsx
function Timestamp() {
  return <span>{new Date().toLocaleString()}</span>;
}
```

**Correct (suppress expected mismatch only):**

```tsx
function Timestamp() {
  return (
    <span suppressHydrationWarning>
      {new Date().toLocaleString()}
    </span>
  );
}
```

### 6.8 Optimize SVG Precision

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

### 6.9 Use useTransition Over Manual Loading States

Use `useTransition` instead of manual `useState` for loading states. This provides built-in `isPending` state and automatically manages transitions.

**Incorrect (manual loading state):**

```tsx
function SearchResults() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleSearch = async (value: string) => {
    setIsLoading(true);
    setQuery(value);
    const data = await fetchResults(value);
    setResults(data);
    setIsLoading(false);
  };

  return (
    <>
      <input onChange={(e) => handleSearch(e.target.value)} />
      {isLoading && <Spinner />}
      <ResultsList results={results} />
    </>
  );
}
```

**Correct (useTransition with built-in pending state):**

```tsx
import {useTransition, useState} from 'react';

function SearchResults() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [isPending, startTransition] = useTransition();

  const handleSearch = (value: string) => {
    setQuery(value); // Update input immediately

    startTransition(async () => {
      // Fetch and update results
      const data = await fetchResults(value);
      setResults(data);
    });
  };

  return (
    <>
      <input onChange={(e) => handleSearch(e.target.value)} />
      {isPending && <Spinner />}
      <ResultsList results={results} />
    </>
  );
}
```

**Benefits:**

- **Automatic pending state**: No need to manually manage `setIsLoading(true/false)`
- **Error resilience**: Pending state correctly resets even if the transition throws
- **Better responsiveness**: Keeps the UI responsive during updates
- **Interrupt handling**: New transitions automatically cancel pending ones

Reference: [useTransition](https://react.dev/reference/react/useTransition)


## 7. JavaScript Performance

### 7.1 Avoid Layout Thrashing

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
  const width = element.offsetWidth;  // Forces reflow
  element.style.height = '200px';
  const height = element.offsetHeight;  // Forces another reflow
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
  return (
    <div className={isHighlighted ? 'highlighted-box' : ''}>
      Content
    </div>
  );
}
```

Prefer CSS classes over inline styles when possible. See [this gist](https://gist.github.com/paulirish/5d52fb081b3570c81e3a) and [CSS Triggers](https://csstriggers.com/) for more on layout-forcing operations.

### 7.2 Cache Repeated Function Calls

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

### 7.3 Cache Property Access in Loops

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

### 7.4 Cache Storage API Calls

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
  storageCache.set(key, value);  // keep cache in sync
}
```

Use a Map (not a hook) so it works everywhere: utilities, event handlers, not just React components.

**Cookie caching:**

```ts
let cookieCache: Record<string, string> | null = null;

function getCookie(name: string) {
  if (!cookieCache) {
    cookieCache = Object.fromEntries(
      document.cookie.split('; ').map((c) => c.split('=')),
    );
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

### 7.5 Combine Multiple Array Iterations

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

### 7.6 Early Return from Functions

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

### 7.7 Hoist RegExp Creation

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
regex.test('foo');  // true, lastIndex = 3
regex.test('foo');  // false, lastIndex = 0
```

### 7.8 Build Index Maps for Repeated Lookups

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

### 7.9 Early Length Check for Array Comparisons

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

### 7.10 Use Loop for Min/Max Instead of Sort

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

### 7.11 Use Set/Map for O(1) Lookups

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

### 7.12 Use toSorted() Instead of sort() for Immutability

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


## 8. Advanced Patterns

### 8.1 Store Event Handlers in Refs

Store callbacks in refs when used in effects that shouldn't re-subscribe on callback changes.

**Incorrect (re-subscribes on every render):**

```tsx
function useWindowEvent(event: string, handler: (e) => void) {
  useEffect(() => {
    window.addEventListener(event, handler);
    return () => window.removeEventListener(event, handler);
  }, [event, handler]);
}
```

**Correct (stable subscription):**

```tsx
function useWindowEvent(event: string, handler: (e) => void) {
  const handlerRef = useRef(handler);
  useEffect(() => {
    handlerRef.current = handler;
  }, [handler]);

  useEffect(() => {
    const listener = (e) => handlerRef.current(e);
    window.addEventListener(event, listener);
    return () => window.removeEventListener(event, listener);
  }, [event]);
}
```

**Alternative: use `useEffectEvent` if you're on latest React:**

```tsx
import {useEffectEvent} from 'react';

function useWindowEvent(event: string, handler: (e) => void) {
  const onEvent = useEffectEvent(handler);

  useEffect(() => {
    window.addEventListener(event, onEvent);
    return () => window.removeEventListener(event, onEvent);
  }, [event]);
}
```

`useEffectEvent` provides a cleaner API for the same pattern: it creates a stable function reference that always calls the latest version of the handler.

### 8.2 Initialize App Once, Not Per Mount

Do not put app-wide initialization that must run once per app load inside `useEffect([])` of a component. Components can remount and effects will re-run. Use a module-level guard or top-level init in the entry module instead.

**Incorrect (runs twice in dev, re-runs on remount):**

```tsx
function Comp() {
  useEffect(() => {
    loadFromStorage();
    checkAuthToken();
  }, []);

  // ...
}
```

**Correct (once per app load):**

```tsx
let didInit = false;

function Comp() {
  useEffect(() => {
    if (didInit) return;
    didInit = true;
    loadFromStorage();
    checkAuthToken();
  }, []);

  // ...
}
```

Reference: [Initializing the application](https://react.dev/learn/you-might-not-need-an-effect#initializing-the-application)

### 8.3 useEffectEvent for Stable Callback Refs

Access latest values in callbacks without adding them to dependency arrays. Prevents effect re-runs while avoiding stale closures.

**Incorrect (effect re-runs on every callback change):**

```tsx
function SearchInput({onSearch}: {onSearch: (q: string) => void}) {
  const [query, setQuery] = useState('');

  useEffect(() => {
    const timeout = setTimeout(() => onSearch(query), 300);
    return () => clearTimeout(timeout);
  }, [query, onSearch]);
}
```

**Correct (using React's useEffectEvent):**

```tsx
import {useEffectEvent} from 'react';

function SearchInput({onSearch}: {onSearch: (q: string) => void}) {
  const [query, setQuery] = useState('');
  const onSearchEvent = useEffectEvent(onSearch);

  useEffect(() => {
    const timeout = setTimeout(() => onSearchEvent(query), 300);
    return () => clearTimeout(timeout);
  }, [query]);
}
```

