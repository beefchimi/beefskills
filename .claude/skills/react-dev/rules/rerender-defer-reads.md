---
title: Defer State Reads to Usage Point
impact: MEDIUM
impactDescription: avoids unnecessary subscriptions
tags: rerender, state, callbacks, optimization
---

## Defer State Reads to Usage Point

Don't subscribe to dynamic state (e.g. URL params, localStorage) if you only read it inside callbacks. Subscribing causes re-renders whenever that state changes even though you don't render from it.

**Incorrect (subscribes to URL changes for use only in callback):**

```tsx
function ShareButton({ chatId }: { chatId: string }) {
  const [params, setParams] = useState(() => new URLSearchParams(window.location.search))

  useEffect(() => {
    const onPopState = () => setParams(new URLSearchParams(window.location.search))
    window.addEventListener('popstate', onPopState)
    return () => window.removeEventListener('popstate', onPopState)
  }, [])

  const handleShare = () => {
    const ref = params.get('ref')
    shareChat(chatId, { ref })
  }

  return <button onClick={handleShare}>Share</button>
}
```

**Correct (reads on demand in callback, no subscription):**

```tsx
function ShareButton({ chatId }: { chatId: string }) {
  const handleShare = () => {
    const params = new URLSearchParams(window.location.search)
    const ref = params.get('ref')
    shareChat(chatId, { ref })
  }

  return <button onClick={handleShare}>Share</button>
}
```

Same idea applies to any reactive value you only use inside event handlers or effects: read it at the point of use instead of subscribing.
