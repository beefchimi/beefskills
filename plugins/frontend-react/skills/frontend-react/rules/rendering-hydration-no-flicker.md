---
title: Prevent Hydration Mismatch Without Flickering
impact: MEDIUM
impactDescription: avoids visual flicker and hydration errors
tags: rendering, ssr, hydration, localStorage, flicker
---

## Prevent Hydration Mismatch Without Flickering

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
