---
title: Dynamic Imports for Heavy Components
impact: CRITICAL
impactDescription: directly affects TTI and LCP
tags: bundle, dynamic-import, code-splitting, React.lazy, Suspense
---

## Dynamic Imports for Heavy Components

Use `React.lazy()` and `<Suspense>` to lazy-load large components not needed on initial render. This keeps the main bundle smaller and improves Time to Interactive.

**Incorrect (Monaco bundles with main chunk):**

```tsx
import { MonacoEditor } from './monaco-editor'

function CodePanel({ code }: { code: string }) {
  return <MonacoEditor value={code} />
}
```

**Correct (Monaco loads on demand):**

```tsx
import { lazy, Suspense } from 'react'

const MonacoEditor = lazy(() =>
  import('./monaco-editor').then(m => ({ default: m.MonacoEditor }))
)

function CodePanel({ code }: { code: string }) {
  return (
    <Suspense fallback={<div>Loading editor…</div>}>
      <MonacoEditor value={code} />
    </Suspense>
  )
}
```

Use the same pattern for route-level or heavy UI (charts, rich editors) so they load only when needed.

Reference: [React lazy](https://react.dev/reference/react/lazy)
