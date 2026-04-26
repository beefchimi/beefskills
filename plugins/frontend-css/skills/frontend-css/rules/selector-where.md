---
title: Low-Specificity Resets Without Complicated Selectors
impact: HIGH
impactDescription: eliminates specificity conflicts in reset and base stylesheets
tags: selectors, where, specificity, reset, override
browser: 96%
---

## Low-Specificity Resets Without Complicated Selectors

Reset and base stylesheets need to set sensible defaults without making them hard to override. Traditional resets use class selectors (`.reset ul`) or element selectors that still carry specificity — forcing component styles to match or exceed that specificity to win. The `:where()` pseudo-class wraps any selector and reduces its specificity contribution to **zero**, making resets trivially overridable by any subsequent rule.

**Avoid (resets with non-zero specificity):**

```css
/* Reset with class — specificity (0,1,1) */
.reset ul,
.reset ol {
  margin: 0;
  padding-left: 1.5rem;
  list-style: none;
}

/* Even bare element selectors carry (0,0,1) specificity */
ul,
ol {
  margin: 0;
  padding-left: 1.5rem;
}

/* Component now needs >= (0,0,1) to override, or worse: */
.nav ul {
  padding-left: 0; /* specificity arms race begins */
}
```

**Prefer (zero-specificity reset with `:where()`):**

```css
:where(ul, ol) {
  margin: 0;
  padding-inline-start: 1.5rem;
}

:where(h1, h2, h3, h4, h5, h6) {
  margin-block: 0;
  font-weight: 600;
}

:where(a) {
  color: inherit;
  text-decoration: none;
}

:where(img, picture, video, canvas, svg) {
  display: block;
  max-width: 100%;
}

:where(button, input, select, textarea) {
  font: inherit;
}
```

Every rule above has specificity **(0,0,0)**. Any class, ID, or even a bare element selector in your component styles will override them without a fight — no `!important`, no specificity escalation.

### How `:where()` specificity works

| Selector                    | Specificity |
| --------------------------- | ----------- |
| `ul`                        | (0,0,1)     |
| `.reset ul`                 | (0,1,1)     |
| `:is(ul, ol)`               | (0,0,1)     |
| `:where(ul, ol)`            | **(0,0,0)** |
| `:where(.card, #main, div)` | **(0,0,0)** |

`:where()` always contributes zero specificity, **regardless of what's inside it** — even if the arguments include IDs or classes, the specificity contribution is still zero.

### `:where()` vs. `:is()` — choosing the right one

Both `:where()` and `:is()` accept selector lists and match identically. The only difference is specificity:

```css
/* :is() — takes the specificity of its most specific argument */
:is(ul, ol) {
  margin: 0;
}
/* Specificity: (0,0,1) — same as the most specific argument (ul or ol) */

/* :where() — always zero specificity */
:where(ul, ol) {
  margin: 0;
}
/* Specificity: (0,0,0) — always */
```

| Use case                           | Choose     | Why                                               |
| ---------------------------------- | ---------- | ------------------------------------------------- |
| Resets, base styles, defaults      | `:where()` | Must be easy to override                          |
| Component selectors, utility rules | `:is()`    | Should carry normal specificity to apply properly |
| Third-party CSS you import         | `:where()` | Prevents specificity leaks into your styles       |

### Complete modern CSS reset using `:where()`

```css
/* Box sizing reset */
:where(*, *::before, *::after) {
  box-sizing: border-box;
}

/* Remove default margins */
:where(body, h1, h2, h3, h4, h5, h6, p, figure, blockquote, dl, dd) {
  margin: 0;
}

/* Typography resets */
:where(h1, h2, h3, h4, h5, h6) {
  font-size: inherit;
  font-weight: inherit;
}

/* List resets */
:where(ol, ul) {
  list-style: none;
  padding: 0;
}

/* Link resets */
:where(a) {
  color: inherit;
  text-decoration: inherit;
}

/* Media resets */
:where(img, picture, video, canvas, svg) {
  display: block;
  max-width: 100%;
  height: auto;
}

/* Form resets */
:where(button, input, select, textarea) {
  font: inherit;
  color: inherit;
}

/* Table resets */
:where(table) {
  border-collapse: collapse;
}
```

Every rule has zero specificity — your component styles always win, trivially.

### Wrapping third-party base styles

If you import a CSS library that sets aggressive defaults, wrap its selectors in `:where()` to prevent specificity leaks:

```css
/* Third-party resets made safe */
@layer vendor {
  :where(.prose h1) {
    font-size: 2rem;
  }
  :where(.prose p) {
    line-height: 1.75;
  }
}
```

Combining `:where()` with `@layer` (see `workflow-cascade-layers`) gives you maximum control over both specificity and cascade priority.

✅ Widely available (~96%). Supported in all major browsers. Use freely in resets, base styles, and anywhere you need effortlessly overridable defaults.

Reference: [modern-css.com](https://modern-css.com) · [MDN — :where()](https://developer.mozilla.org/en-US/docs/Web/CSS/:where)
