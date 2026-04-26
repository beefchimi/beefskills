---
title: Mobile Viewport Height Without the 100vh Hack
impact: HIGH
impactDescription: fixes mobile overflow caused by browser chrome
tags: layout, viewport, dvh, mobile, responsive
browser: 93%
---

## Mobile Viewport Height Without the 100vh Hack

On mobile browsers, `100vh` includes the area behind the browser's address bar and toolbar, causing content to overflow the visible area. The dynamic viewport unit `dvh` adapts to the actual visible height as browser chrome appears and disappears.

**Avoid (100vh overflows on mobile):**

```css
.hero {
  height: 100vh;
}
/* Content extends behind the address bar on iOS Safari / Chrome Android */
```

**Prefer (dvh adapts to browser chrome):**

```css
.hero {
  height: 100dvh;
}
/* Shrinks/grows as the address bar shows/hides */
```

### Choosing the right unit

There are three viewport-relative height units for different use cases:

```css
/* Dynamic — updates as browser chrome shows/hides (most common) */
.hero {
  height: 100dvh;
}

/* Small — smallest possible viewport (chrome visible). Safe for
   "must always fit" elements like sticky footers. */
.sticky-footer {
  min-height: 100svh;
}

/* Large — largest possible viewport (chrome hidden). Use when you
   want maximum space and can tolerate temporary overflow. */
.splash {
  height: 100lvh;
}
```

### Width equivalents

The same logic applies to width (relevant on some mobile browsers and foldables):

```css
.sidebar {
  width: 100dvw; /* instead of 100vw */
}
```

### Fallback for older browsers

```css
.hero {
  height: 100vh; /* fallback */
  height: 100dvh; /* override in supporting browsers */
}
```

✅ Widely available (~93%). Safe to use with a `vh` fallback line for the small number of older browsers.

Reference: [modern-css.com](https://modern-css.com) · [MDN: Viewport units](https://developer.mozilla.org/en-US/docs/Web/CSS/length#viewport_units)
