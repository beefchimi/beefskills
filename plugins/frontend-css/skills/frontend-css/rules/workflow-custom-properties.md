---
title: Theme Variables Without a Preprocessor
impact: HIGH
impactDescription: eliminates Sass/Less build dependency for theming and runtime variable updates
tags: workflow, custom-properties, variables, sass, less, theming
browser: 96%
---

## Theme Variables Without a Preprocessor

Sass and Less variables (`$primary`, `@primary`) compile to static values — they cannot change at runtime, cannot be scoped to a subtree, and require a build step. CSS custom properties (`--primary`) are live in the browser, cascade through the DOM, can be updated with JavaScript or media queries, and need no preprocessor.

**Avoid (Sass variables — static, build-time only):**

```scss
// Sass: requires a compiler, produces static output
$primary: #7c3aed;
$surface: #ffffff;
$text: #111111;

.btn {
  background: $primary; // compiles to background: #7c3aed — frozen
  color: $surface;
}

// Theming requires generating separate stylesheets or duplicating rules
```

**Prefer (CSS custom properties — live, cascading, runtime):**

```css
:root {
  --primary: #7c3aed;
  --surface: #ffffff;
  --text: #111111;
}

.btn {
  background: var(--primary);
  color: var(--surface);
}
```

### Runtime theming with no JavaScript

```css
/* Dark mode — override at the root */
@media (prefers-color-scheme: dark) {
  :root {
    --primary: #a78bfa;
    --surface: #1a1a2e;
    --text: #eeeeee;
  }
}

/* Scoped theme — override on a subtree */
.card.danger {
  --primary: #dc2626;
  --surface: #fef2f2;
}
/* All descendants using var(--primary) pick up the scoped value */
```

### Fallback values

```css
.box {
  /* Second argument is the fallback if --accent is not defined */
  color: var(--accent, #7c3aed);

  /* Nested fallbacks */
  background: var(--card-bg, var(--surface, white));
}
```

### Combining with calc for design tokens

```css
:root {
  --space-unit: 0.25rem;
  --space-1: calc(var(--space-unit) * 1); /* 0.25rem */
  --space-2: calc(var(--space-unit) * 2); /* 0.50rem */
  --space-4: calc(var(--space-unit) * 4); /* 1.00rem */
  --space-8: calc(var(--space-unit) * 8); /* 2.00rem */
}

.card {
  padding: var(--space-4);
  gap: var(--space-2);
}
```

### JavaScript interop

```js
// Read a custom property value
const primary = getComputedStyle(document.documentElement).getPropertyValue('--primary');

// Update a custom property at runtime
document.documentElement.style.setProperty('--primary', '#2563eb');

// Scope to a specific element
card.style.setProperty('--primary', '#dc2626');
```

### When Sass variables are still appropriate

Sass variables still have a role for **build-time constants** that should never change at runtime — breakpoint values used in `@media` rules, configuration flags, or values consumed only by Sass functions. But for anything that touches the rendered page — colors, spacing, typography, component theming — CSS custom properties are the modern default.

✅ Widely available (~96%). Supported in all major browsers. No fallback needed.

Reference: [modern-css.com](https://modern-css.com) · [MDN — Using CSS custom properties](https://developer.mozilla.org/en-US/docs/Web/CSS/Using_CSS_custom_properties)
