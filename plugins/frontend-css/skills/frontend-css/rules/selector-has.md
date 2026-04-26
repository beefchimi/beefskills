---
title: Selecting Parent Elements Without JavaScript
impact: HIGH
impactDescription: eliminates JavaScript closest() and class toggling for parent-based styling
tags: selectors, has, parent-selector, relational, javascript
browser: 94%
---

## Selecting Parent Elements Without JavaScript

CSS has historically been unable to style a parent based on its children. The only way to apply styles to a `.card` that contains an `<img>` was JavaScript — querying elements, traversing the DOM with `closest()`, and toggling classes. The `:has()` relational pseudo-class finally gives CSS the ability to select elements based on their descendants, siblings, or subsequent content — no JavaScript, no class toggling, no DOM traversal.

**Avoid (JavaScript DOM traversal + class toggling):**

```js
// Style cards differently when they contain an image
document.querySelectorAll('.card').forEach((card) => {
  if (card.querySelector('img')) {
    card.classList.add('card--has-image');
  }
});

// Must re-run on every DOM change (dynamic content, SPA navigation)
const observer = new MutationObserver(() => {
  // re-check all cards…
});
```

```css
.card--has-image {
  grid-template-rows: auto 1fr;
}
```

**Prefer (modern CSS):**

```css
.card:has(img) {
  grid-template-rows: auto 1fr;
}
/* No JavaScript, no class toggling, no mutation observers */
```

The browser re-evaluates `:has()` automatically when the DOM changes — if an image is added or removed, the styles update instantly.

### Common patterns

**Parent styling based on child state:**

```css
/* Form group with an invalid input */
.form-group:has(:user-invalid) {
  border-color: red;
  background: oklch(0.97 0.02 25);
}

/* Form group with a focused input */
.form-group:has(:focus-visible) {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
}

/* Nav item with an active link */
.nav-item:has(a[aria-current='page']) {
  background: var(--nav-active-bg);
}
```

**Conditional layout based on content:**

```css
/* Card layout changes when an image is present */
.card:has(img) {
  display: grid;
  grid-template-columns: 200px 1fr;
}

.card:not(:has(img)) {
  display: flex;
  flex-direction: column;
}

/* Section with more than a certain number of items — combine with :nth-child */
.grid:has(> :nth-child(4)) {
  grid-template-columns: repeat(2, 1fr);
}

.grid:has(> :nth-child(7)) {
  grid-template-columns: repeat(3, 1fr);
}
```

**Sibling-aware styling:**

```css
/* Style a label when its adjacent input is focused */
label:has(+ input:focus-visible) {
  color: var(--accent);
  font-weight: 600;
}

/* Style a heading when followed by a subtitle */
h1:has(+ .subtitle) {
  margin-bottom: 0.25rem;
}
```

**Page-level conditional styling:**

```css
/* Apply styles to body based on the presence of a modal */
body:has(dialog[open]) {
  overflow: hidden;
}

/* Different page layout when sidebar is present */
body:has(.sidebar) {
  --content-max-width: 720px;
}

body:not(:has(.sidebar)) {
  --content-max-width: 960px;
}
```

**Empty state detection:**

```css
/* Show empty state message when list has no items */
.list:not(:has(li)) .empty-state {
  display: block;
}

.list:has(li) .empty-state {
  display: none;
}
```

### Combining with other modern selectors

`:has()` composes powerfully with `:is()`, `:where()`, and `:not()`:

```css
/* Card with any media element */
.card:has(:is(img, video, svg)) {
  grid-template-rows: auto 1fr;
}

/* Zero-specificity version for resets */
:where(.card):has(img) {
  overflow: hidden;
}

/* Cards WITHOUT images */
.card:not(:has(img)) {
  padding-top: 2rem;
}
```

### Performance considerations

`:has()` is evaluated by the browser's selector engine and is generally fast for common patterns. However, avoid deeply nested or overly broad `:has()` selectors that force the browser to scan large subtrees:

```css
/* ✅ Good — scoped, shallow */
.card:has(> img) {
}
.form-group:has(:focus) {
}

/* ⚠️ Potentially expensive — unbounded depth on a high-level element */
html:has(.some-deeply-nested-class) {
}
```

Use the direct child combinator (`>`) inside `:has()` when you only need to check immediate children, limiting the search scope.

### Specificity

`:has()` contributes the specificity of its most specific argument, just like `:is()`:

```css
/* Specificity of .card:has(img) is (0, 1, 1) — .card + img */
.card:has(img) {
}

/* Specificity of .card:has(.featured) is (0, 2, 0) — .card + .featured */
.card:has(.featured) {
}
```

✅ Widely available (~94%). Supported in all modern browsers. `:has()` is one of the most impactful CSS additions in years — it eliminates entire categories of JavaScript DOM manipulation.

Reference: [modern-css.com](https://modern-css.com) · [MDN — :has()](https://developer.mozilla.org/en-US/docs/Web/CSS/:has)
