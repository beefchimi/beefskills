---
title: Readable Text Without Manual Contrast Checks
impact: MEDIUM
impactDescription: eliminates hardcoded white/black text color decisions and manual WCAG contrast checking
tags: color, contrast-color, accessibility, wcag, readable, text
browser: 6%
---

## Readable Text Without Manual Contrast Checks

Choosing whether to use white or black text on a colored background requires either manual checking against WCAG contrast ratios or a JavaScript function that calculates relative luminance. When the background color changes (theming, dark mode, user customization), the text color decision must be recalculated. The `contrast-color()` function automatically selects the most readable text color for any given background — no manual picking, no JavaScript, no contrast ratio math.

**Avoid (hardcoded text color — breaks when background changes):**

```css
.badge {
  background: var(--badge-bg);
  color: white; /* hardcoded — unreadable on light backgrounds */
}

/* Or: manual per-variant overrides */
.badge--info {
  background: #dbeafe;
  color: #1e3a5f; /* manually chosen for this specific blue */
}
.badge--warning {
  background: #fef3c7;
  color: #78350f; /* manually chosen for this specific yellow */
}
.badge--danger {
  background: #dc2626;
  color: white; /* manually chosen for this specific red */
}
/* Every new color variant needs a manually picked text color */
```

Or with JavaScript:

```js
function getContrastColor(bgHex) {
  const r = parseInt(bgHex.slice(1, 3), 16);
  const g = parseInt(bgHex.slice(3, 5), 16);
  const b = parseInt(bgHex.slice(5, 7), 16);
  const luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255;
  return luminance > 0.5 ? '#000000' : '#ffffff';
}
// Must re-run on every background change, doesn't handle non-hex colors
```

**Prefer (modern CSS):**

```css
.badge {
  background: var(--badge-bg);
  color: contrast-color(var(--badge-bg));
}
/* Automatically picks the most readable text color — any background, any theme */
```

No manual color pairing, no JavaScript luminance calculations. The browser evaluates the background color and selects the text color that provides the best contrast.

### How it works

`contrast-color()` takes a base color and returns the color (from the available options) that provides the highest contrast ratio against it:

```css
.tag {
  background: var(--tag-color);
  color: contrast-color(var(--tag-color));
  /* Returns black or white — whichever has higher contrast */
}
```

### Dynamic theming

The real power shows in dynamic theming where background colors are set via custom properties, user input, or runtime calculations:

```css
:root {
  --brand: oklch(0.6 0.2 250);
}

.hero {
  background: var(--brand);
  color: contrast-color(var(--brand));
  /* Adapts automatically as --brand changes */
}

.hero a {
  color: contrast-color(var(--brand));
  text-decoration: underline;
}
```

### With oklch color scales

Particularly useful when generating color scales from a single hue — the text color flips from dark to light automatically at the right lightness threshold:

```css
.swatch-1 {
  background: oklch(0.95 0.05 250);
  color: contrast-color(oklch(0.95 0.05 250)); /* → dark text */
}
.swatch-5 {
  background: oklch(0.55 0.2 250);
  color: contrast-color(oklch(0.55 0.2 250)); /* → light text */
}
.swatch-9 {
  background: oklch(0.25 0.1 250);
  color: contrast-color(oklch(0.25 0.1 250)); /* → light text */
}
```

### User-customizable colors

```css
/* User picks any background color via a color input */
.card {
  background: var(--user-color);
  color: contrast-color(var(--user-color));
  /* Always readable, no matter what color the user picks */
}
```

### Common use cases

```css
/* Colored badges with automatic text contrast */
.badge {
  background: var(--badge-color);
  color: contrast-color(var(--badge-color));
  padding: 0.125rem 0.5rem;
  border-radius: 999px;
}

/* Tag clouds with varied backgrounds */
.tag {
  background: var(--tag-bg);
  color: contrast-color(var(--tag-bg));
}

/* Data visualization labels on colored segments */
.chart-label {
  color: contrast-color(var(--segment-color));
}
```

### Fallback strategy

Given the very limited browser support, pair `contrast-color()` with a manual fallback:

```css
.badge {
  background: var(--badge-bg);
  color: white; /* safe fallback for dark backgrounds */
  color: contrast-color(var(--badge-bg)); /* override in supporting browsers */
}

/* Or use @supports */
@supports (color: contrast-color(red)) {
  .badge {
    color: contrast-color(var(--badge-bg));
  }
}
```

For broader support today, use a JavaScript utility to set a `--text-color` custom property based on the background luminance. Replace it with `contrast-color()` once support is sufficient.

🟠 Limited (~6%). Very early in browser adoption. Use as a progressive enhancement behind `@supports` with a manual color fallback. This is a feature to watch — when widely available, it will eliminate an entire class of accessibility bugs related to insufficient text contrast.

Reference: [modern-css.com](https://modern-css.com) · [CSS Color Level 6 — contrast-color()](https://drafts.csswg.org/css-color-6/#contrast-color)
