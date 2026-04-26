---
title: Lazy Rendering Without IntersectionObserver
impact: HIGH
impactDescription: eliminates JavaScript observer setup for off-screen rendering deferral
tags: workflow, content-visibility, lazy-rendering, intersection-observer, performance
browser: 93%
---

## Lazy Rendering Without IntersectionObserver

Deferring rendering of off-screen content traditionally requires setting up an `IntersectionObserver` in JavaScript — creating the observer, defining thresholds, observing elements, swapping placeholders, and cleaning up. The `content-visibility: auto` property tells the browser to skip layout and paint for off-screen elements automatically, with zero JavaScript.

**Avoid (JavaScript IntersectionObserver):**

```js
const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        renderContent(entry.target);
        observer.unobserve(entry.target);
      }
    });
  },
  {rootMargin: '200px'},
);

document.querySelectorAll('.section').forEach((el) => observer.observe(el));
// + cleanup on unmount, placeholder sizing, loading states…
```

**Prefer (modern CSS):**

```css
.section {
  content-visibility: auto;
  contain-intrinsic-size: auto 500px;
}
```

The browser automatically skips layout, paint, and style computation for elements that are off-screen. When the user scrolls near them, the browser renders them just in time. No JavaScript, no observers, no cleanup.

### How `contain-intrinsic-size` works

Without `contain-intrinsic-size`, an element with `content-visibility: auto` would collapse to zero height when off-screen, causing the scrollbar to jump as elements enter and exit the viewport. The intrinsic size provides an estimated placeholder height:

```css
/* Fixed estimate */
.card {
  content-visibility: auto;
  contain-intrinsic-size: auto 300px;
}

/* The `auto` keyword remembers the last rendered size, so the estimate
   is only used on the first render — after that, the real size is cached */
```

### Common use cases

```css
/* Long article sections */
article > section {
  content-visibility: auto;
  contain-intrinsic-size: auto 600px;
}

/* List items in a long feed */
.feed-item {
  content-visibility: auto;
  contain-intrinsic-size: auto 120px;
}

/* Tab panels that are off-screen */
.tab-panel:not(.active) {
  content-visibility: hidden;
  /* Like display: none but preserves state (scroll position, form data) */
}
```

### `content-visibility` values

| Value     | Behavior                                                                  |
| --------- | ------------------------------------------------------------------------- |
| `visible` | Default — no containment, normal rendering                                |
| `auto`    | Off-screen elements skip rendering; on-screen elements render normally    |
| `hidden`  | Always skips rendering — like `display: none` but preserves element state |

### Performance impact

For pages with many off-screen elements (long feeds, dashboards, documentation), `content-visibility: auto` can reduce initial render time by 5–10×. The browser skips the most expensive parts of rendering (layout and paint) for content the user hasn't scrolled to yet.

### Caveats

- **Find-in-page**: Browsers still allow Ctrl+F to find text in `content-visibility: auto` elements — the browser renders them on demand when searched.
- **Anchor links**: Navigating to a `#hash` inside a hidden section triggers rendering automatically.
- **Accessibility**: Screen readers can still access the content — `content-visibility: auto` does not add `aria-hidden`.

✅ Widely available (~93%). Safe to use without fallback. Unsupporting browsers simply render everything as normal (no visual difference, just no performance optimization).

Reference: [modern-css.com](https://modern-css.com) · [web.dev — content-visibility](https://web.dev/articles/content-visibility) · [MDN — content-visibility](https://developer.mozilla.org/en-US/docs/Web/CSS/content-visibility)
