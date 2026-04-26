---
title: CSS Feature Detection Without JavaScript
impact: HIGH
impactDescription: eliminates Modernizr and CSS.supports() JavaScript for progressive enhancement
tags: workflow, supports, feature-detection, progressive-enhancement, modernizr
browser: 96%
---

## CSS Feature Detection Without JavaScript

Testing for CSS feature support traditionally required JavaScript — either the Modernizr library (which adds classes to `<html>`) or the `CSS.supports()` API with manual class toggling. The `@supports` at-rule performs feature detection entirely in CSS, with no JavaScript, no library, and no render-blocking script.

**Avoid (JavaScript feature detection):**

```js
// Modernizr — 10 KB+ library that runs on page load
// Adds classes like .flexbox, .no-flexbox to <html>

// Or manual CSS.supports() check
if (CSS.supports('display', 'grid')) {
  document.documentElement.classList.add('grid');
} else {
  document.documentElement.classList.add('no-grid');
}
```

```css
.grid .layout {
  display: grid;
}
.no-grid .layout {
  display: flex;
  flex-wrap: wrap;
}
```

**Prefer (`@supports` — pure CSS):**

```css
.layout {
  /* Fallback for all browsers */
  display: flex;
  flex-wrap: wrap;
}

@supports (display: grid) {
  .layout {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  }
}
/* No JavaScript, no render-blocking script, no class toggling */
```

### Logical operators

`@supports` accepts `and`, `or`, and `not` for compound feature checks:

```css
/* Multiple features required */
@supports (container-type: inline-size) and (display: grid) {
  .card-wrapper {
    container-type: inline-size;
  }
}

/* Negation — target browsers that lack a feature */
@supports not (backdrop-filter: blur(10px)) {
  .glass {
    background: rgb(255 255 255 / 0.85);
    /* opaque fallback when backdrop-filter is unavailable */
  }
}

/* Any of several features */
@supports (scroll-timeline-name: --tl) or (animation-timeline: view()) {
  .reveal {
    animation: fade-in linear both;
    animation-timeline: view();
  }
}
```

### Selector feature detection

`@supports` can also test for selector support using the `selector()` function:

```css
/* Only apply if :has() is supported */
@supports selector(:has(*)) {
  .card:has(img) {
    grid-template-rows: auto 1fr;
  }
}

/* Only apply if :focus-visible is supported */
@supports selector(:focus-visible) {
  :focus:not(:focus-visible) {
    outline: none;
  }
}
```

### Common progressive enhancement patterns

```css
/* Anchor positioning with Floating UI fallback */
@supports (anchor-name: --tip) {
  .tooltip {
    position: fixed;
    position-anchor: --tip;
    inset-area: top;
  }
}

/* Container queries with media query fallback */
.card {
  flex-direction: column;
}

@media (width >= 600px) {
  .card {
    flex-direction: row;
  }
}

@supports (container-type: inline-size) {
  .card-wrapper {
    container-type: inline-size;
  }

  @container (width >= 400px) {
    .card {
      flex-direction: row;
    }
  }
}
```

### When to use `@supports` vs. just writing the property

Modern CSS is designed to ignore properties it doesn't understand — an unknown declaration is silently skipped. In many cases, you don't need `@supports` at all; just write the modern property after the fallback:

```css
.hero {
  height: 100vh; /* fallback */
  height: 100dvh; /* override in supporting browsers */
}
```

Reserve `@supports` for cases where the fallback and the enhancement are **mutually exclusive** — i.e., you need to remove or change the fallback styles when the feature is present, not just add to them.

✅ Widely available (~96%). `@supports` itself is supported in all modern browsers. Use it freely for progressive enhancement of newer CSS features.

Reference: [modern-css.com](https://modern-css.com) · [MDN — @supports](https://developer.mozilla.org/en-US/docs/Web/CSS/@supports)
