---
title: Typed Attribute Values Without JavaScript
impact: MEDIUM
impactDescription: eliminates JavaScript dataset reads for styling based on HTML attributes
tags: workflow, attr, data-attributes, dataset, typed
browser: 42%
---

## Typed Attribute Values Without JavaScript

Reading `data-*` attributes for styling has traditionally required JavaScript — fetching the value from `el.dataset`, then applying it as an inline style. The enhanced `attr()` function with type coercion lets CSS read and use attribute values directly, with proper typing, fallback values, and no JavaScript.

**Avoid (JavaScript reading dataset):**

```js
// Read data attribute and apply as inline style
const bar = document.querySelector('.bar');
bar.style.width = bar.dataset.pct + '%';

// Or for multiple elements
document.querySelectorAll('[data-pct]').forEach((el) => {
  el.style.width = el.dataset.pct + '%';
});
// Must re-run on every DOM change, breaks SSR, adds layout thrashing
```

```html
<div class="bar" data-pct="75"></div>
```

**Prefer (enhanced `attr()` with type coercion):**

```css
.bar {
  width: attr(data-pct type(<percentage>));
}
```

```html
<div class="bar" data-pct="75%"></div>
<!-- CSS reads the value directly — no JavaScript needed -->
```

### Type coercion options

The enhanced `attr()` function supports explicit type declarations so the browser interprets the attribute value correctly:

```css
/* Percentage values */
.progress {
  width: attr(data-value type(<percentage>), 0%);
}

/* Length values */
.spacer {
  height: attr(data-gap type(<length>), 1rem);
}

/* Number values */
.grid {
  grid-template-columns: repeat(attr(data-cols type(<number>), 3), 1fr);
}

/* Color values */
.badge {
  background: attr(data-color type(<color>), gray);
}

/* Custom ident for keywords */
.layout {
  display: attr(data-display type(<custom-ident>), block);
}
```

### Fallback values

The third argument provides a fallback when the attribute is missing or cannot be parsed:

```css
.bar {
  /* If data-pct is missing or not a valid percentage, use 0% */
  width: attr(data-pct type(<percentage>), 0%);
  background: attr(data-color type(<color>), oklch(0.6 0.2 250));
}
```

### Using with `calc()` and custom properties

```css
.meter {
  --pct: attr(data-value type(<number>), 0);
  width: calc(var(--pct) * 1%);
  background: oklch(calc(0.3 + var(--pct) * 0.005) 0.2 140);
}
```

### Common patterns

```css
/* Star rating from attribute */
.stars::before {
  content: '★★★★★';
  background: linear-gradient(90deg, gold attr(data-rating type(<percentage>), 0%), #ddd 0);
  background-clip: text;
  -webkit-background-clip: text;
  color: transparent;
}

/* Dynamic grid columns from markup */
.grid {
  display: grid;
  grid-template-columns: repeat(attr(data-cols type(<number>), 3), 1fr);
  gap: attr(data-gap type(<length>), 1rem);
}
```

The enhanced `attr()` function turns HTML attributes into typed CSS values without a JavaScript intermediary. This keeps styling concerns in CSS, works with SSR/static HTML, and requires no event listeners or DOM observers to stay in sync.

🟠 Limited support (~42%). Currently shipping in Chromium. Use behind `@supports (width: attr(x type(<length>)))` with a JavaScript fallback or CSS custom property alternative for broader support.

Reference: [modern-css.com](https://modern-css.com) · [MDN — attr()](https://developer.mozilla.org/en-US/docs/Web/CSS/attr)
