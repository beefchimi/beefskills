---
title: Centering Elements Without the Transform Hack
impact: HIGH
impactDescription: simplifies centering to a single parent declaration
tags: layout, grid, centering, place-items
browser: 96%
---

## Centering Elements Without the Transform Hack

The absolute-position + transform centering hack requires styling the child, knowing the parent's position context, and breaks easily when content size changes. `display: grid; place-items: center` on the parent centers any number of children with zero child styles.

**Avoid (absolute + transform):**

```css
.parent {
  position: relative;
}

.child {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}
```

**Prefer (grid centering):**

```css
.parent {
  display: grid;
  place-items: center;
}
/* child needs nothing */
```

This also works with `display: flex; align-items: center; justify-content: center;` but `place-items: center` on grid is the most concise single-property solution. The child requires no positioning, no transforms, and no knowledge of its own dimensions.

✅ Widely available (96%+) — safe to use without fallback.

Reference: [modern-css.com](https://modern-css.com)
