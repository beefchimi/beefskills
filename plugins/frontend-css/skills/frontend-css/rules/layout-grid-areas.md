---
title: Named Grid Areas Instead of Line Numbers or Floats
impact: HIGH
impactDescription: readable, maintainable grid layouts
tags: layout, grid, grid-template-areas, float
browser: 96%
---

## Named Grid Areas Instead of Line Numbers or Floats

Grid line numbers (`grid-column: 1 / 3`) are hard to read and brittle when the layout changes. Float-based layouts require clearfixes and margin hacks. Named grid areas make the layout visually obvious in the CSS itself and trivial to rearrange.

**Avoid (floats or numeric grid lines):**

```css
/* Float-based — fragile, requires clearfix */
.header {
  float: left;
  width: 100%;
}
.sidebar {
  float: left;
  width: 25%;
}
.main {
  float: left;
  width: 75%;
}
.footer {
  clear: both;
}

/* Or numeric grid lines — hard to visualize */
.header {
  grid-column: 1 / 3;
  grid-row: 1;
}
.sidebar {
  grid-column: 1;
  grid-row: 2;
}
.main {
  grid-column: 2;
  grid-row: 2;
}
.footer {
  grid-column: 1 / 3;
  grid-row: 3;
}
```

**Prefer (named grid areas):**

```css
.layout {
  display: grid;
  grid-template-areas:
    'header  header'
    'sidebar main'
    'footer  footer';
  grid-template-columns: 250px 1fr;
  grid-template-rows: auto 1fr auto;
  min-height: 100dvh;
}

.header {
  grid-area: header;
}
.sidebar {
  grid-area: sidebar;
}
.main {
  grid-area: main;
}
.footer {
  grid-area: footer;
}

/* Rearranging is a one-line change */
@media (width < 768px) {
  .layout {
    grid-template-areas:
      'header'
      'main'
      'sidebar'
      'footer';
    grid-template-columns: 1fr;
  }
}
```

The `grid-template-areas` property acts as a visual ASCII map of your layout. Reordering content across breakpoints is a single property change — no line numbers to recalculate, no floats to clear.

✅ Widely available (~96%). No fallback needed.

Reference: [modern-css.com](https://modern-css.com)
