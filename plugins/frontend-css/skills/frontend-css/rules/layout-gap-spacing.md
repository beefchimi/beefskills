---
title: Spacing Elements Without Margin Hacks
impact: HIGH
impactDescription: eliminates margin override patterns and simplifies spacing logic
tags: layout, flexbox, grid, gap, spacing, margins
browser: 95%
---

## Spacing Elements Without Margin Hacks

The `gap` property on flex and grid containers replaces the classic pattern of applying margins to children and then removing them from the last (or first) child. It keeps spacing concerns on the parent, avoids negative-margin workarounds, and works with wrapping layouts without extra overrides.

**Avoid (margin hack with last-child override):**

```css
.grid > * {
  margin-right: 16px;
}
.grid > *:last-child {
  margin-right: 0;
}
```

Or the negative-margin wrapper hack:

```css
.grid-wrapper {
  margin-right: -16px;
}
.grid-wrapper > * {
  margin-right: 16px;
}
```

**Prefer (gap on the container):**

```css
.grid {
  display: flex;
  gap: 16px;
}
```

For different row and column spacing:

```css
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 24px 16px; /* row-gap column-gap */
}
```

`gap` works on both `display: flex` and `display: grid`. It respects wrapping in flex layouts without extra overrides, and it composes cleanly with `justify-content` and `align-items` — no margin collapse surprises.

✅ Widely available (~95%). Use freely.

Reference: [modern-css.com](https://modern-css.com)
