---
title: Nesting Selectors Without Sass or Less
impact: HIGH
impactDescription: eliminates preprocessor dependency for selector nesting
tags: workflow, nesting, sass, less, build-step
browser: 91%
---

## Nesting Selectors Without Sass or Less

CSS nesting was the #1 reason teams adopted Sass or Less — writing nested selectors required a compiler, a build step, and a `node_modules` dependency. Native CSS nesting uses the same `&` syntax and works in plain `.css` files with zero tooling.

**Avoid (requires Sass compiler):**

```scss
// .scss file — requires sass/dart-sass build step
.nav {
  background: #fff;

  & a {
    color: #888;
    text-decoration: none;

    &:hover {
      color: #333;
    }
  }

  & .logo {
    font-weight: 700;
  }
}
// $ sass input.scss output.css
```

**Prefer (plain CSS — no build):**

```css
/* .css file — works natively in the browser */
.nav {
  background: #fff;

  & a {
    color: #888;
    text-decoration: none;

    &:hover {
      color: #333;
    }
  }

  & .logo {
    font-weight: 700;
  }
}
```

Same syntax, same output, no compiler, no build step, no dependency.

### Nesting rules

```css
/* Compound selectors — & is required when starting with a type selector */
.card {
  /* Class, attribute, pseudo-class — & is optional */
  .title {
    font-size: 1.25rem;
  }
  :hover {
    opacity: 0.9;
  }
  [aria-expanded] {
    border-color: blue;
  }

  /* Type selectors MUST use & */
  & h2 {
    margin: 0;
  }
  & p {
    color: #666;
  }
}
```

### Nesting media and container queries

```css
.hero {
  padding: 2rem;

  @media (width >= 768px) {
    padding: 4rem;
  }

  @container (width < 400px) {
    padding: 1rem;
  }
}
```

Media queries and container queries nest directly inside a rule block — no `&` needed. The browser scopes the query to the parent selector automatically.

### Nesting with combinators

```css
.card {
  /* Direct child */
  & > .header {
    border-bottom: 1px solid #eee;
  }

  /* Adjacent sibling */
  & + .card {
    margin-top: 1rem;
  }

  /* General sibling */
  & ~ .card {
    opacity: 0.8;
  }
}
```

### Deep nesting — keep it shallow

Native nesting supports arbitrary depth, but the same Sass best practice applies: **keep nesting to 2–3 levels max** to avoid specificity bloat and selector chains that are hard to override.

```css
/* ✅ Shallow — readable, low specificity */
.card {
  & .title {
    font-size: 1.25rem;
  }
  & .body {
    color: #444;
  }
}

/* ❌ Too deep — high specificity, hard to override */
.page {
  & .section {
    & .card {
      & .title {
        & span {
          color: red; /* specificity: 0,5,0 — hard to override without !important */
        }
      }
    }
  }
}
```

### Migrating from Sass

Most Sass nesting translates 1:1 to native CSS nesting. The key differences:

| Sass                         | Native CSS                        |
| ---------------------------- | --------------------------------- |
| `&-suffix` (BEM: `&__title`) | ❌ Not supported — use full class |
| Nesting `h2 { }` directly    | Must use `& h2 { }` for types     |
| `@extend`                    | ❌ Not available — use `@layer`   |
| `@mixin` / `@include`        | Use `@scope` or custom properties |

The `&-suffix` pattern (`&__title`, `&--active`) that BEM-style Sass relies on does **not** work in native CSS nesting. This is by design — `&` represents the full parent selector, not a string to concatenate. If your codebase relies heavily on this pattern, consider migrating to `@scope` (see `workflow-scope`) or flat class names.

✅ Widely available (~91%). Supported in all modern browsers. Safe to use in new projects without a preprocessor.

Reference: [modern-css.com](https://modern-css.com) · [MDN — CSS nesting](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_nesting)
