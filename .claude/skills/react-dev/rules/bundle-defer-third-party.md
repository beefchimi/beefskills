---
title: Defer Non-Critical Third-Party Libraries
impact: MEDIUM
impactDescription: loads after hydration or on interaction
tags: bundle, third-party, analytics, defer
---

## Defer Non-Critical Third-Party Libraries

Analytics, logging, and error tracking don't need to block initial render. Load them after the app has mounted or on first user interaction using dynamic `import()`.

**Incorrect (blocks initial bundle):**

```tsx
import { Analytics } from '@vercel/analytics/react'

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <>
      {children}
      <Analytics />
    </>
  )
}
```

**Correct (loads after mount):**

```tsx
import { useEffect, useState } from 'react'

function AnalyticsLoader({ children }: { children: React.ReactNode }) {
  const [Analytics, setAnalytics] = useState<React.ComponentType | null>(null)

  useEffect(() => {
    import('@vercel/analytics/react').then(mod => setAnalytics(() => mod.Analytics))
  }, [])

  return (
    <>
      {children}
      {Analytics ? <Analytics /> : null}
    </>
  )
}
```

Alternatively, load on first interaction (e.g. first click or route change) with `import()` inside the handler so the analytics script never blocks the initial bundle.
