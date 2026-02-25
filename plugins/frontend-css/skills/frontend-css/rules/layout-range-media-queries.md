---
title: Media Query Ranges Without min-width and max-width
impact: MEDIUM
impactDescription: cleaner, less error-prone responsive breakpoints
tags: layout, media-queries, range, responsive, breakpoints
browser: 94%
---

## Media Query Ranges Without min-width and max-width

The traditional `min-width` and `max-width` media query syntax is verbose, easy to get wrong at boundaries (the classic `max-width: 599px` vs `min-width: 600px` off-by-one), and unreadable when combined with `and`. The range syntax uses familiar comparison operators (`<`, `<=`, `>`, `>=`) and supports chained ranges in a single expression.

**Avoid (min/max with `and`):**

```css
/* Single bound */
@media (min-width: 600px) {
  .sidebar {
    display: block;
  }
}

/* Range — verbose, error-prone boundary */
@media (min-width: 600px) and (max-width: 1200px) {
  .container {
    max-width: 960px;
  }
}

/* Exclusive upper bound — off-by-one risk */
@media (max-width: 599px) {
  .nav {
    display: none;
  }
}
```

**Prefer (range syntax):**

```css
/* Single bound */
@media (width >= 600px) {
  .sidebar {
    display: block;
  }
}

/* Range — clear, chainable */
@media (600px <= width <= 1200px) {
  .container {
    max-width: 960px;
  }
}

/* Exclusive upper bound — no off-by-one */
@media (width < 600px) {
  .nav {
    display: none;
  }
}
```

**Works with other features too:**

```css
/* Height ranges */
@media (400px <= height <= 800px) {
  .hero {
    padding-block: 2rem;
  }
}

/* Resolution / pixel density */
@media (resolution >= 2dppx) {
  .logo {
    background-image: url('logo@2x.png');
  }
}

/* Aspect ratio */
@media (aspect-ratio > 16/9) {
  .cinematic {
    display: block;
  }
}
```

The range syntax eliminates the off-by-one trap entirely — `<` vs `<=` makes boundaries explicit. It also reads like a math expression, making complex queries self-documenting.

✅ Widely available (~94%). Supported in all modern browsers.

Reference: [modern-css.com](https://modern-css.com) · [MDN — Media query range syntax](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_media_queries/Using_media_queries#syntax_improvements_in_level_4)
