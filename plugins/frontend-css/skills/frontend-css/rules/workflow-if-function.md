---
title: Inline Conditional Styles Without JavaScript
impact: MEDIUM
impactDescription: eliminates JavaScript class toggling for simple conditional values
tags: workflow, if, conditional, custom-properties, toggle
browser: 35%
---

## Inline Conditional Styles Without JavaScript

Applying conditional styles today typically requires JavaScript to toggle classes or set inline styles based on state. The CSS `if()` function evaluates conditions inline — including style queries against custom properties — and resolves to one of two values, removing the need for JavaScript class toggling in many common scenarios.

**Avoid (JavaScript class toggling):**

```js
// Toggle class based on a variant property
el.classList.toggle('primary', isPrimary);
el.classList.toggle('secondary', !isPrimary);
```

```css
.btn {
  background: gray;
}
.btn.primary {
  background: blue;
}
.btn.secondary {
  background: gray;
}
```

Or with inline styles:

```js
el.style.background = isPrimary ? 'blue' : 'gray';
```

**Prefer (CSS `if()` with style queries):**

```css
.btn {
  --variant: secondary;
  background: if(style(--variant: primary): blue; else: gray);
  color: if(style(--variant: primary): white; else: #333);
}
```

```html
<!-- Set the variant via custom property -->
<button class="btn" style="--variant: primary">Save</button>
<button class="btn">Cancel</button>
```

No JavaScript needed — the custom property drives the conditional styling directly in CSS.

### Multiple conditions

```css
.badge {
  --status: info;

  background: if(
    style(--status: success): oklch(0.75 0.18 145) ; else if
      style(--status: warning): oklch(0.8 0.16 80) ; else if
      style(--status: error): oklch(0.65 0.22 25) ; else: oklch(0.9 0.02 250)
  );
}
```

### Combining with media and supports conditions

`if()` can also evaluate media and supports conditions inline, removing the need for separate `@media` or `@supports` blocks for single-property changes:

```css
.hero {
  padding: if(media(width >= 768px): 4rem; else: 1.5rem);
}

.layout {
  display: if(supports(display: grid): grid; else: flex);
}
```

### Boolean custom property pattern

For simple on/off toggles, a boolean-style custom property keeps things clean:

```css
.card {
  --featured: false;

  border: if(style(--featured: true): 2px solid var(--accent) ; else: 1px solid #ddd);
  box-shadow: if(style(--featured: true): 0 4px 16px rgb(0 0 0 / 0.1) ; else: none);
}
```

```html
<div class="card" style="--featured: true">Featured item</div>
<div class="card">Regular item</div>
```

### Comparison with existing patterns

| Pattern                      | Requires JS | Scales to N variants | Inline |
| ---------------------------- | ----------- | -------------------- | ------ |
| Class toggling               | ✅          | ❌ (class per state) | ❌     |
| Custom property + `if()`     | ❌          | ✅                   | ✅     |
| Style queries (`@container`) | ❌          | ✅                   | ❌     |

`if()` is best suited for simple, per-property conditional values. For larger conditional blocks affecting many properties, `@container style()` queries remain more ergonomic.

🟠 Limited (~35%). The CSS `if()` function is an emerging feature with partial browser support. Use as a progressive enhancement behind `@supports` or wait for broader adoption. The JavaScript class-toggling approach remains the safe fallback.

Reference: [modern-css.com](https://modern-css.com) · [CSS Values Level 5 — if()](https://drafts.csswg.org/css-values-5/#if-notation)
