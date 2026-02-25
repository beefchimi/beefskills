---
title: Aligning Nested Grids Without Duplicating Tracks
impact: HIGH
impactDescription: nested grids inherit parent track sizing for true alignment
tags: layout, grid, subgrid, nested-grid, alignment
browser: 88%
---

## Aligning Nested Grids Without Duplicating Tracks

When a child grid needs to align its content with the parent grid's columns or rows, the old approach was to duplicate the parent's `grid-template-columns` definition in the child. This creates a maintenance burden — every change to the parent tracks must be mirrored in every child. `subgrid` lets a nested grid inherit track sizing from its parent, keeping everything aligned with zero duplication.

**Avoid (duplicating parent tracks in child):**

```css
.parent-grid {
  display: grid;
  grid-template-columns: 200px 1fr 1fr;
  gap: 16px;
}

.child-grid {
  display: grid;
  grid-column: 1 / -1;
  /* Must manually duplicate parent tracks — breaks when parent changes */
  grid-template-columns: 200px 1fr 1fr;
  gap: 16px;
}
```

**Prefer (subgrid inherits parent tracks):**

```css
.parent-grid {
  display: grid;
  grid-template-columns: 200px 1fr 1fr;
  gap: 16px;
}

.child-grid {
  display: grid;
  grid-column: 1 / -1;
  grid-template-columns: subgrid;
  /* Inherits parent's column tracks — always in sync */
}
```

### Common use case: card grids with aligned content

Cards in a grid often have headers, bodies, and footers that should align across cards. Without subgrid, each card sizes its rows independently:

```css
.card-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

.card {
  display: grid;
  grid-row: span 3;
  grid-template-rows: subgrid;
  /* Header, body, and footer rows align across all cards */
}
```

`subgrid` works for both `grid-template-columns` and `grid-template-rows`, and the child still participates in the parent's gap. You can subgrid one axis while defining the other independently.

🟡 Newly available (~88%). Supported in all modern browsers since late 2023. For older browsers, duplicating tracks is a safe fallback.

Reference: [modern-css.com](https://modern-css.com) · [MDN — subgrid](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_grid_layout/Subgrid)
