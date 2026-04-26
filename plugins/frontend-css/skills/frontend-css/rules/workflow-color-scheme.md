---
title: Dark Mode Defaults Without Extra CSS
impact: HIGH
impactDescription: automatic dark mode for native form controls, scrollbars, and system colors without manual overrides
tags: workflow, color-scheme, dark-mode, prefers-color-scheme, system-colors
browser: 93%
---

## Dark Mode Defaults Without Extra CSS

When implementing dark mode, developers often write dozens of `prefers-color-scheme: dark` overrides for every native form control, scrollbar, and system-chrome element — `<input>`, `<select>`, `<textarea>`, `<button>`, `<hr>`, scrollbar tracks, and more. The `color-scheme` property tells the browser to render all of these in the user's preferred color scheme automatically — no per-element overrides needed.

**Avoid (manual dark mode overrides for every control):**

```css
@media (prefers-color-scheme: dark) {
  input,
  select,
  textarea,
  button {
    background-color: #1e1e1e;
    color: #eee;
    border-color: #555;
  }

  hr {
    border-color: #444;
  }

  /* scrollbars, focus rings, selection colors, etc. — all need manual overrides */
}
```

This is tedious, incomplete (you'll miss controls), and fights the browser's default styles instead of embracing them.

**Prefer (modern CSS):**

```css
:root {
  color-scheme: light dark;
}
```

One line. The browser switches all native UI elements — form controls, scrollbars, `<hr>`, focus rings, system colors (`Canvas`, `CanvasText`, `LinkText`, etc.) — to match the user's `prefers-color-scheme` preference automatically.

### How it works

`color-scheme` declares which color schemes the page supports. The browser then:

1. Renders all native controls in the user's preferred scheme.
2. Adjusts system colors (`Canvas`, `CanvasText`, etc.) to match.
3. Applies the correct default background and text color to the page.

### Values

```css
/* Support both light and dark — browser follows OS preference */
:root {
  color-scheme: light dark;
}

/* Light only — native controls always render in light mode */
:root {
  color-scheme: light;
}

/* Dark only — native controls always render in dark mode */
:root {
  color-scheme: dark;
}

/* Per-element override — useful for always-dark headers or footers */
.dark-header {
  color-scheme: dark;
}
```

### Combining with custom styles

`color-scheme` handles native/system UI. Your custom-styled elements still need `prefers-color-scheme` or `light-dark()` for custom properties and colors:

```css
:root {
  color-scheme: light dark;

  /* Custom tokens — use light-dark() for values that change */
  --surface: light-dark(#fff, #1a1a1a);
  --text: light-dark(#111, #eee);
  --border: light-dark(#ddd, #333);
}

body {
  background: var(--surface);
  color: var(--text);
}
```

### Per-element scoping

Apply `color-scheme` to specific subtrees when parts of the page should always use a specific scheme:

```css
/* Page follows OS preference */
:root {
  color-scheme: light dark;
}

/* This section is always dark, regardless of OS preference */
.promo-banner {
  color-scheme: dark;
  background: #111;
  color: #eee;
}

/* This form is always light */
.print-form {
  color-scheme: light;
}
```

### HTML meta tag alternative

For the fastest possible render (before CSS loads), declare the color scheme in the HTML `<head>`:

```html
<meta name="color-scheme" content="light dark" />
```

This prevents a flash of the wrong color scheme during page load.

`color-scheme` is the foundation of dark mode support. Set it first, then layer custom color overrides on top with `light-dark()` (see `color-light-dark`) and custom properties. See also `workflow-registered-properties` for typed custom properties that can transition between themes.

✅ Widely available (~93%). Supported in all modern browsers. No fallback needed.

Reference: [modern-css.com](https://modern-css.com) · [MDN — color-scheme](https://developer.mozilla.org/en-US/docs/Web/CSS/color-scheme)
