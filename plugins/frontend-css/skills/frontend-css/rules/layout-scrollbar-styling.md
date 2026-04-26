---
title: Scrollbar Styling Without -webkit- Pseudo-Elements
impact: MEDIUM
impactDescription: cross-browser scrollbar customization without vendor prefixes
tags: layout, scrollbar, scrollbar-width, scrollbar-color, webkit
browser: 75%
---

## Scrollbar Styling Without -webkit- Pseudo-Elements

The `::-webkit-scrollbar` family of pseudo-elements only works in Chromium and Safari, requires multiple selectors to style different parts, and produces inconsistent results across engines. The standard `scrollbar-width` and `scrollbar-color` properties provide cross-browser scrollbar customization in two lines.

**Avoid (webkit-only pseudo-elements):**

```css
/* Chromium and Safari only */
::-webkit-scrollbar {
  width: 8px;
}
::-webkit-scrollbar-track {
  background: transparent;
}
::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
  background: #555;
}
/* Firefox and other engines ignore all of this */
```

**Prefer (standard properties):**

```css
* {
  scrollbar-width: thin;
  scrollbar-color: #888 transparent;
  /* thumb-color  track-color */
}
```

### Values for `scrollbar-width`

| Value  | Description                                      |
| ------ | ------------------------------------------------ |
| `auto` | Default platform scrollbar width                 |
| `thin` | Narrower scrollbar (platform decides exact size) |
| `none` | Hides scrollbar but keeps content scrollable     |

### Scoped to specific containers

```css
.sidebar {
  overflow-y: auto;
  scrollbar-width: thin;
  scrollbar-color: oklch(0.6 0.02 250) transparent;
}
```

### Dark mode aware

```css
.scrollable {
  scrollbar-width: thin;
  scrollbar-color: light-dark(#aaa, #555) transparent;
}
```

The standard properties give you less granular control than the webkit pseudo-elements (no separate hover states, no border-radius on the thumb), but they work everywhere and cover the vast majority of scrollbar customization needs. If you need pixel-perfect scrollbar designs, consider a CSS-only approach with `scrollbar-color` as the baseline and `::-webkit-scrollbar` as a progressive enhancement for Chromium/Safari.

🟡 Newly available (~75%). Firefox has supported these since 2018; Chromium and Safari added support more recently. Use as a progressive enhancement — the default scrollbar is a fine fallback.

Reference: [modern-css.com](https://modern-css.com) · [MDN — scrollbar-color](https://developer.mozilla.org/en-US/docs/Web/CSS/scrollbar-color)
