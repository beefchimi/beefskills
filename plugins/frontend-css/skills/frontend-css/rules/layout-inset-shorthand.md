---
title: Positioning Shorthand Without Four Properties
impact: HIGH
impactDescription: cleaner overlays and absolute positioning
tags: layout, inset, positioning, shorthand
browser: 93%
---

## Positioning Shorthand Without Four Properties

Writing `top: 0; right: 0; bottom: 0; left: 0;` to stretch an element to its container is verbose and error-prone. The `inset` shorthand replaces all four in a single declaration, following the same 1-to-4-value pattern as `margin` and `padding`.

**Avoid (four directional properties):**

```css
.overlay {
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
}

.inset-box {
  position: fixed;
  top: 16px;
  right: 24px;
  bottom: 16px;
  left: 24px;
}
```

**Prefer (inset shorthand):**

```css
.overlay {
  position: absolute;
  inset: 0;
}

/* top/bottom 16px, left/right 24px */
.inset-box {
  position: fixed;
  inset: 16px 24px;
}
```

`inset` accepts 1–4 values using the same shorthand logic as `margin`: `inset: top right bottom left`, `inset: block inline`, or `inset: all`. You can also use the logical equivalents `inset-block` and `inset-inline` for internationalization-ready positioning.

```css
/* Logical property equivalents */
.sidebar {
  position: absolute;
  inset-block: 0; /* top and bottom */
  inset-inline-start: 0; /* left in LTR, right in RTL */
  inline-size: 280px;
}
```

✅ Widely available — supported in all major browsers.

Reference: [MDN — inset](https://developer.mozilla.org/en-US/docs/Web/CSS/inset)
