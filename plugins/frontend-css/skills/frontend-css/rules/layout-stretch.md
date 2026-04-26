---
title: Filling Available Space Without calc Workarounds
impact: HIGH
impactDescription: eliminates fragile calc expressions and overflow bugs
tags: layout, width, stretch, fill-available
browser: 90%
---

## Filling Available Space Without calc Workarounds

When an element needs to fill its container while respecting its own margins, the old approach was `width: calc(100% - …)` or `width: 100%` (which overflows with margins). The `stretch` keyword tells the browser to fill the available space automatically, accounting for margins, padding, and borders.

**Avoid (calc or overflow):**

```css
.full {
  width: calc(100% - 40px);
  /* fragile — must manually match the margin sum */
}

/* or worse: */
.full {
  width: 100%;
  /* overflows container when margins are present */
}
```

**Prefer (modern CSS):**

```css
.full {
  width: stretch;
  margin-inline: 20px;
  /* fills container minus margins — no math needed */
}
```

`stretch` works for `width`, `height`, `min-width`, `min-height`, `max-width`, and `max-height`. The browser handles the subtraction automatically, so layouts stay correct even when margins or padding change.

✅ Widely available (~90%). Previously required `-webkit-fill-available` / `-moz-available` prefixes — the unprefixed `stretch` keyword is now supported across modern browsers.

Reference: [modern-css.com](https://modern-css.com)
