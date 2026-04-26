---
title: Range Style Queries Without Multiple Blocks
impact: MEDIUM
impactDescription: eliminates duplicated @container style() blocks for each discrete value
tags: workflow, container-queries, style-queries, custom-properties, range
browser: 88%
---

## Range Style Queries Without Multiple Blocks

Container style queries let you apply styles based on the computed value of a custom property on an ancestor container. However, querying discrete values requires a separate `@container style()` block for each value — which quickly becomes unmanageable for numeric ranges (e.g., progress percentages). Range-based style queries accept comparison operators, collapsing dozens of blocks into a single rule.

**Avoid (per-value style query blocks):**

```css
/* One block per value — doesn't scale */
@container style(--progress: 0%) {
  .bar {
    width: 0%;
    background: red;
  }
}
@container style(--progress: 10%) {
  .bar {
    width: 10%;
    background: red;
  }
}
@container style(--progress: 20%) {
  .bar {
    width: 20%;
    background: red;
  }
}
/* …repeat for 30%, 40%, 50%, 60%, 70%, 80%, 90%, 100% */

@container style(--progress: 50%) {
  .bar {
    background: orange;
  }
}
@container style(--progress: 51%) {
  .bar {
    background: orange;
  }
}
/* Impossible to cover every possible value */
```

**Prefer (range-based style queries):**

```css
@container style(--progress <= 25%) {
  .bar {
    background: oklch(0.6 0.25 25); /* red */
  }
}

@container style(25% < --progress <= 50%) {
  .bar {
    background: oklch(0.7 0.2 60); /* orange */
  }
}

@container style(50% < --progress <= 75%) {
  .bar {
    background: oklch(0.75 0.18 95); /* yellow-green */
  }
}

@container style(--progress > 75%) {
  .bar {
    background: oklch(0.65 0.2 145); /* green */
  }
}
```

### Setting up the container

The container element holds the custom property that child elements query:

```html
<div class="progress-wrapper" style="--progress: 68%">
  <div class="bar"></div>
  <span class="label">68%</span>
</div>
```

```css
.progress-wrapper {
  container-type: normal; /* style queries don't need size containment */
}

.bar {
  height: 8px;
  width: var(--progress);
  border-radius: 4px;
  transition:
    width 0.3s,
    background 0.3s;
}
```

### Combining with size queries

Style queries and size queries can be composed in a single `@container` rule:

```css
@container (width >= 300px) and style(--progress > 50%) {
  .label {
    display: inline; /* show percentage label only when there's room and progress is meaningful */
  }
}
```

### Common patterns

```css
/* Theme variant switching */
@container style(--variant: danger) {
  .alert {
    border-color: red;
  }
}

@container style(--variant: success) {
  .alert {
    border-color: green;
  }
}

/* Numeric range — e.g., rating-based styling */
@container style(--rating >= 4) {
  .star-display {
    color: gold;
  }
}

@container style(--rating < 2) {
  .star-display {
    color: #ccc;
  }
}
```

### Registering the custom property for range queries

For numeric range comparisons to work correctly, the custom property should be registered with a type so the browser can compare values:

```css
@property --progress {
  syntax: '<percentage>';
  inherits: true;
  initial-value: 0%;
}
```

Without registration, the property is a string and range comparisons may not evaluate as expected. See `workflow-registered-properties` for details on `@property`.

🟡 Newly available (~88%). Discrete style queries (`style(--x: value)`) have broader support than range comparisons. Use `@property` registration for numeric ranges. Fallback: use discrete value matching or JavaScript class toggling.

Reference: [modern-css.com](https://modern-css.com) · [MDN — @container style queries](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_containment/Container_size_and_style_queries#container_style_queries)
