---
title: Responsive Components Without Media Queries
impact: HIGH
impactDescription: components respond to their own size, not the viewport
tags: layout, container-queries, responsive, components, media-queries
browser: 93%
---

## Responsive Components Without Media Queries

Viewport-based `@media` queries tie component layout to the window size, which breaks when the same component appears in different contexts (sidebar vs. main content vs. modal). `@container` queries let a component respond to the size of its own container, making it truly reusable regardless of where it's placed in the page.

**Avoid (viewport media queries on components):**

```css
.card {
  display: flex;
  flex-direction: row;
}

@media (max-width: 768px) {
  .card {
    flex-direction: column;
  }
}
/* Breaks when .card is in a narrow sidebar on a wide screen */
```

**Prefer (container queries):**

```css
.card-wrapper {
  container-type: inline-size;
}

.card {
  display: flex;
  flex-direction: row;
}

@container (width < 400px) {
  .card {
    flex-direction: column;
  }
}
/* Adapts to its container, not the viewport */
```

### Container query setup

Any element can become a containment context. Use `container-type` (or the shorthand `container`) on the parent:

```css
/* Size containment on inline axis (most common) */
.sidebar {
  container-type: inline-size;
}

/* Named container for targeted queries */
.sidebar {
  container: sidebar / inline-size;
}

@container sidebar (width < 300px) {
  .nav-link span {
    display: none; /* collapse labels, show icons only */
  }
}
```

### Range syntax

Container queries support the same range syntax as modern media queries:

```css
/* Old syntax */
@container (min-width: 400px) and (max-width: 800px) {
  .card {
    /* ... */
  }
}

/* Modern range syntax */
@container (400px <= width <= 800px) {
  .card {
    /* ... */
  }
}
```

### Common patterns

```css
/* Responsive grid item that stacks when its container is narrow */
.product-card-container {
  container-type: inline-size;
}

@container (width >= 500px) {
  .product-card {
    display: grid;
    grid-template-columns: 200px 1fr;
    gap: 1rem;
  }
}

@container (width < 500px) {
  .product-card {
    display: flex;
    flex-direction: column;
  }
}
```

Container queries are the correct tool for component-level responsiveness. Reserve `@media` queries for page-level layout shifts (e.g., switching from single-column to multi-column) and user preference queries (`prefers-color-scheme`, `prefers-reduced-motion`).

✅ Widely available (~93%). Safe to use without fallback.

Reference: [modern-css.com](https://modern-css.com) · [MDN — @container](https://developer.mozilla.org/en-US/docs/Web/CSS/@container)
