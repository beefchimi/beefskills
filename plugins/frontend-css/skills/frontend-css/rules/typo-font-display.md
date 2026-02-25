---
title: Font Loading Without Invisible Text
impact: HIGH
impactDescription: eliminates flash of invisible text (FOIT) during web font loading
tags: typography, font-display, font-loading, foit, fout, performance
browser: 96%
---

## Font Loading Without Invisible Text

By default, browsers hide text entirely while a custom web font is loading — a behavior known as Flash of Invisible Text (FOIT). On slow connections, users stare at a blank page for several seconds. The `font-display` descriptor in `@font-face` controls this behavior, letting you show a fallback font immediately and swap in the custom font when it's ready.

**Avoid (default behavior — invisible text):**

```css
@font-face {
  font-family: 'MyFont';
  src: url('myfont.woff2') format('woff2');
  /* No font-display — browser hides text for up to 3 seconds while loading */
}

body {
  font-family: 'MyFont', sans-serif;
}
/* Users on slow connections see nothing until the font downloads */
```

**Prefer (font-display: swap):**

```css
@font-face {
  font-family: 'MyFont';
  src: url('myfont.woff2') format('woff2');
  font-display: swap;
}

body {
  font-family: 'MyFont', sans-serif;
}
/* Text is immediately visible in the fallback font, then swaps when ready */
```

### font-display values

| Value      | Block period    | Swap period     | Best for                                                               |
| ---------- | --------------- | --------------- | ---------------------------------------------------------------------- |
| `auto`     | Browser decides | Browser decides | Default — usually same as `block`                                      |
| `block`    | ~3 seconds      | Infinite        | Icon fonts (blank squares are worse than waiting)                      |
| `swap`     | ~100ms          | Infinite        | Body and heading text (most common choice)                             |
| `fallback` | ~100ms          | ~3 seconds      | Text where layout shift matters — uses fallback if font takes too long |
| `optional` | ~100ms          | None            | Non-critical fonts — only uses custom font if already cached           |

### Recommended strategy by font role

```css
/* Body text — always show content immediately */
@font-face {
  font-family: 'BodyFont';
  src: url('body.woff2') format('woff2');
  font-display: swap;
}

/* Heading / display font — acceptable to swap later */
@font-face {
  font-family: 'DisplayFont';
  src: url('display.woff2') format('woff2');
  font-display: swap;
}

/* Icon font — blank squares are worse than waiting */
@font-face {
  font-family: 'Icons';
  src: url('icons.woff2') format('woff2');
  font-display: block;
}

/* Non-essential decorative font — skip if not cached */
@font-face {
  font-family: 'Decorative';
  src: url('decorative.woff2') format('woff2');
  font-display: optional;
}
```

### Reducing layout shift from font swapping

`font-display: swap` introduces Flash of Unstyled Text (FOUT) — the fallback font renders first, then the custom font replaces it, potentially causing a layout shift. Mitigate this with:

```css
/* 1. Use size-adjust to match fallback metrics to the custom font */
@font-face {
  font-family: 'MyFont Fallback';
  src: local('Arial');
  size-adjust: 105%;
  ascent-override: 95%;
  descent-override: 22%;
  line-gap-override: 0%;
}

body {
  font-family: 'MyFont', 'MyFont Fallback', sans-serif;
}

/* 2. Preload critical fonts to minimize the swap window */
```

```html
<!-- Preload the most important font file -->
<link rel="preload" href="body.woff2" as="font" type="font/woff2" crossorigin />
```

### Google Fonts

Google Fonts supports `font-display` via a URL parameter:

```html
<link
  href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap"
  rel="stylesheet"
/>
```

The `&display=swap` parameter adds `font-display: swap` to the generated `@font-face` rules.

Always set `font-display` on every `@font-face` declaration. There is no good reason to leave it at the default `auto` (which typically means `block` — invisible text). For body and heading text, `swap` is the right default.

✅ Widely available (~96%). Supported in all major browsers. No fallback needed.

Reference: [modern-css.com](https://modern-css.com) · [MDN — font-display](https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face/font-display) · [web.dev — Avoid invisible text during font loading](https://web.dev/articles/avoid-invisible-text)
