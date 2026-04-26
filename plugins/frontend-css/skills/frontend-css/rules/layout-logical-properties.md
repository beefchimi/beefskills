---
title: Direction-Aware Layouts Without Left and Right
impact: HIGH
impactDescription: eliminates RTL overrides and simplifies internationalization
tags: layout, logical-properties, rtl, internationalization, margin, padding
browser: 96%
---

## Direction-Aware Layouts Without Left and Right

Physical properties like `margin-left` and `padding-right` assume a left-to-right writing direction. Supporting RTL languages requires duplicate overrides with `[dir="rtl"]` selectors. Logical properties adapt automatically to the document's writing mode and direction — one declaration works for every language.

**Avoid (physical properties with RTL overrides):**

```css
.sidebar {
  margin-left: 1rem;
  padding-right: 1rem;
  border-top: 1px solid #ddd;
}

[dir='rtl'] .sidebar {
  margin-left: 0;
  margin-right: 1rem;
  padding-right: 0;
  padding-left: 1rem;
}
```

**Prefer (logical properties):**

```css
.sidebar {
  margin-inline-start: 1rem;
  padding-inline-end: 1rem;
  border-block-start: 1px solid #ddd;
}
/* No RTL override needed — adapts automatically */
```

**Logical property mapping:**

| Physical           | Logical               |
| ------------------ | --------------------- |
| `margin-left`      | `margin-inline-start` |
| `margin-right`     | `margin-inline-end`   |
| `padding-top`      | `padding-block-start` |
| `padding-bottom`   | `padding-block-end`   |
| `border-left`      | `border-inline-start` |
| `border-right`     | `border-inline-end`   |
| `top`              | `inset-block-start`   |
| `left`             | `inset-inline-start`  |
| `width`            | `inline-size`         |
| `height`           | `block-size`          |
| `text-align: left` | `text-align: start`   |

Use logical properties by default in all new CSS. They cost nothing in browsers that only serve LTR content and make the codebase RTL-ready without any refactoring later.

✅ Widely available (~96%). Supported in all major browsers.

Reference: [modern-css.com](https://modern-css.com)
