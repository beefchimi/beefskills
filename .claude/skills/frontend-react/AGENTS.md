# React Best Practices

**Version 1.0.0**
React

> **Note:**
> This document is for agents and LLMs when maintaining, generating, or refactoring
> React codebases. For framework-agnostic patterns, see the `frontend-general` skill.

---

## Abstract

React-specific performance and best-practices guide.
Rules across 5 categories: bundle optimization with React.lazy/Suspense, client-side
data fetching with SWR, re-render optimization, React rendering patterns, and advanced
hook patterns. Each rule includes incorrect vs. correct examples.

---

## Table of Contents

1. [Bundle Size Optimization](#1-bundle-size-optimization) — **CRITICAL**
   - 1.1 Conditional Module Loading
   - 1.2 Defer Non-Critical Third-Party Libraries
   - 1.3 Dynamic Imports for Heavy Components
   - 1.4 Preload Based on User Intent

2. [Client-Side Data Fetching](#2-client-side-data-fetching) — **MEDIUM-HIGH**
   - 2.1 Deduplicate Global Event Listeners
   - 2.2 Use SWR for Automatic Deduplication

3. [Re-render Optimization](#3-re-render-optimization) — **MEDIUM**
   - 3.1 Defer State Reads to Usage Point
   - 3.2 Narrow Effect Dependencies
   - 3.3 Calculate Derived State During Rendering
   - 3.4 Subscribe to Derived State
   - 3.5 Use Functional setState Updates
   - 3.6 Use Lazy State Initialization
   - 3.7 Extract Default Non-primitive Parameter Value from Memoized Component to Constant
   - 3.8 Extract to Memoized Components
   - 3.9 Put Interaction Logic in Event Handlers
   - 3.10 Do not wrap a simple expression with a primitive result type in useMemo
   - 3.11 Use Transitions for Non-Urgent Updates
   - 3.12 Use useRef for Transient Values

4. [Rendering Performance](#4-rendering-performance) — **MEDIUM**
   - 4.1 Use Activity Component for Show/Hide
   - 4.2 Use Explicit Conditional Rendering
   - 4.3 Hoist Static JSX Elements
   - 4.4 Prevent Hydration Mismatch Without Flickering
   - 4.5 Suppress Expected Hydration Mismatches
   - 4.6 Use useTransition Over Manual Loading States

5. [Advanced Patterns](#5-advanced-patterns) — **LOW**
   - 5.1 Store Event Handlers in Refs
   - 5.2 Initialize App Once, Not Per Mount
   - 5.3 useEffectEvent for Stable Callback Refs

---

## 1. Bundle Size Optimization

### 1.1 Conditional Module Loading

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

### 1.2 Defer Non-Critical Third-Party Libraries

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

### 1.3 Dynamic Imports for Heavy Components

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

### 1.4 Preload Based on User Intent

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


## 2. Client-Side Data Fetching

### 2.1 Deduplicate Global Event Listeners

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

### 2.2 Use SWR for Automatic Deduplication

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


## 3. Re-render Optimization

### 3.1 Defer State Reads to Usage Point

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

### 3.2 Narrow Effect Dependencies

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

### 3.3 Calculate Derived State During Rendering

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

### 3.4 Subscribe to Derived State

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

### 3.5 Use Functional setState Updates

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

### 3.6 Use Lazy State Initialization

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

### 3.7 Extract Default Non-primitive Parameter Value from Memoized Component to Constant

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

### 3.8 Extract to Memoized Components

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

### 3.9 Put Interaction Logic in Event Handlers

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

### 3.10 Do not wrap a simple expression with a primitive result type in useMemo

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

### 3.11 Use Transitions for Non-Urgent Updates

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

### 3.12 Use useRef for Transient Values

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


## 4. Rendering Performance

### 4.1 Use Activity Component for Show/Hide

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

### 4.2 Use Explicit Conditional Rendering

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

### 4.3 Hoist Static JSX Elements

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

### 4.4 Prevent Hydration Mismatch Without Flickering

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

### 4.5 Suppress Expected Hydration Mismatches

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

### 4.6 Use useTransition Over Manual Loading States

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


## 5. Advanced Patterns

### 5.1 Store Event Handlers in Refs

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

### 5.2 Initialize App Once, Not Per Mount

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

### 5.3 useEffectEvent for Stable Callback Refs

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

