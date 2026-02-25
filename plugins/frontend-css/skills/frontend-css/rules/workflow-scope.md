---
title: Scoped Styles Without BEM Naming
impact: HIGH
impactDescription: native style scoping without naming conventions, build tools, or JavaScript
tags: workflow, scope, bem, css-modules, scoping, encapsulation
browser: 84%
---

## Scoped Styles Without BEM Naming

BEM (`.card__title`, `.card__body--active`) is a naming convention that simulates scoping by encoding the component hierarchy into class names. CSS Modules and styled-components solve the same problem with build tools or JavaScript. The `@scope` at-rule provides real, browser-native style scoping — selectors inside a `@scope` block only match elements within the specified subtree, with no naming conventions, no build step, and no runtime overhead.

**Avoid (BEM naming convention):**

```css
/* BEM — verbose, manual, no enforcement */
.card__title {
  font-size: 1.25rem;
  font-weight: 600;
}
.card__body {
  color: #444;
  line-height: 1.6;
}
.card__body--highlighted {
  background: #fef3c7;
}
/* Nothing prevents .card__title from leaking if used outside .card */
```

Or CSS Modules (requires a bundler):

```css
/* card.module.css — build tool hashes class names */
.title {
  font-size: 1.25rem;
}
.body {
  color: #444;
}
/* Requires Webpack/Vite CSS Modules plugin, framework integration,
   and import { styles } from './card.module.css' in JS */
```

**Prefer (@scope for native scoping):**

```css
@scope (.card) {
  .title {
    font-size: 1.25rem;
    font-weight: 600;
  }
  .body {
    color: #444;
    line-height: 1.6;
  }
  .body.highlighted {
    background: #fef3c7;
  }
}
/* .title only matches inside .card — enforced by the browser */
```

```html
<div class="card">
  <h2 class="title">Card Title</h2>
  <div class="body">Card content here.</div>
</div>

<!-- This .title is NOT affected by the scoped rules -->
<h2 class="title">Page Title</h2>
```

### Scoping with a lower boundary (donut scope)

`@scope` supports an optional `to` clause that defines where the scope ends — creating a "donut" scope that styles the outer component without leaking into nested components:

```css
@scope (.card) to (.card-slot) {
  p {
    color: #444;
  }
  /* Styles paragraphs inside .card but NOT inside .card-slot */
}
```

```html
<div class="card">
  <p>This paragraph is styled.</p>
  <div class="card-slot">
    <p>This paragraph is NOT styled — outside the scope.</p>
  </div>
</div>
```

This solves the classic component composition problem where a parent's styles bleed into slotted or nested child components.

### Inline scoping with `<style>`

`@scope` can be used without a selector when placed inside a `<style>` element — it scopes to the parent of the `<style>` tag:

```html
<div class="widget">
  <style>
    @scope {
      p {
        color: navy;
      }
      .label {
        font-weight: 600;
      }
    }
  </style>
  <p class="label">Only styled within this widget.</p>
</div>
```

### Specificity advantage

Selectors inside `@scope` have the same specificity as their unwrapped equivalents — `.title` inside `@scope (.card)` has (0,1,0) specificity, not (0,2,0). This avoids the specificity inflation that comes from manually nesting `.card .title` and makes scoped styles easier to override with utility classes.

### When to use what

| Approach          | Build step | Runtime cost | Scoping enforcement | Specificity impact |
| ----------------- | ---------- | ------------ | ------------------- | ------------------ |
| BEM naming        | None       | None         | Convention only     | Normal             |
| CSS Modules       | Required   | None         | Build-time hashing  | Normal             |
| styled-components | Required   | Runtime JS   | Runtime generation  | Normal             |
| `@scope`          | None       | None         | Browser-enforced    | No inflation       |

🟡 Newly available (~84%). Supported in Chromium and Firefox. For projects that must support older browsers, BEM or CSS Modules remain valid strategies — but prefer `@scope` for new code in modern browser targets.

Reference: [modern-css.com](https://modern-css.com) · [MDN — @scope](https://developer.mozilla.org/en-US/docs/Web/CSS/@scope)
