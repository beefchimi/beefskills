---
title: Staggered Animations Without nth-child Hacks
impact: MEDIUM
impactDescription: eliminates per-item nth-child rules for staggered animation delays
tags: animation, sibling-index, stagger, nth-child, delay, transition
browser: 70%
---

## Staggered Animations Without nth-child Hacks

Creating staggered animations — where each item in a list animates with a progressively longer delay — traditionally requires either a custom `--i` variable on every `nth-child` selector or inline `style` attributes set from JavaScript. The `sibling-index()` function returns each element's position among its siblings as a number, letting you calculate staggered delays with a single rule instead of N rules.

**Avoid (nth-child per item — doesn't scale):**

```css
li:nth-child(1) {
  --i: 0;
}
li:nth-child(2) {
  --i: 1;
}
li:nth-child(3) {
  --i: 2;
}
li:nth-child(4) {
  --i: 3;
}
li:nth-child(5) {
  --i: 4;
}
li:nth-child(6) {
  --i: 5;
}
/* …repeat for every possible item count */

li {
  opacity: 0;
  animation: fade-in 0.3s ease forwards;
  animation-delay: calc(0.05s * var(--i));
}
```

Or the JavaScript workaround:

```js
document.querySelectorAll('li').forEach((el, i) => {
  el.style.setProperty('--i', i);
});
// Must re-run on every DOM change
```

Both approaches require knowing (or iterating) the number of items in advance. Adding or removing an item means updating the CSS or re-running the JavaScript.

**Prefer (modern CSS with `sibling-index()`):**

```css
li {
  opacity: 0;
  animation: fade-in 0.3s ease forwards;
  animation-delay: calc(0.05s * (sibling-index() - 1));
}

@keyframes fade-in {
  to {
    opacity: 1;
    translate: 0;
  }
}
```

One rule. Works for any number of items. No JavaScript, no per-item selectors, no inline styles. The browser computes `sibling-index()` automatically for each element based on its position among its siblings.

### How `sibling-index()` works

`sibling-index()` returns a 1-based integer representing the element's position among its parent's children (counting only elements, not text nodes):

```
<ul>
  <li>…</li>   <!-- sibling-index() = 1 -->
  <li>…</li>   <!-- sibling-index() = 2 -->
  <li>…</li>   <!-- sibling-index() = 3 -->
</ul>
```

It can be used anywhere a `<number>` or `<integer>` is expected in a CSS value — inside `calc()`, `clamp()`, `min()`, `max()`, and custom property assignments.

### Common stagger patterns

```css
/* Fade in from below with staggered delay */
.stagger-item {
  opacity: 0;
  translate: 0 10px;
  animation: reveal 0.4s ease forwards;
  animation-delay: calc(0.06s * (sibling-index() - 1));
}

@keyframes reveal {
  to {
    opacity: 1;
    translate: 0 0;
  }
}
```

```css
/* Staggered transition on hover of a parent */
.menu:hover .menu-item {
  opacity: 1;
  translate: 0;
  transition-delay: calc(0.04s * (sibling-index() - 1));
}

.menu-item {
  opacity: 0;
  translate: 0 -8px;
  transition:
    opacity 0.2s ease,
    translate 0.2s ease;
}
```

### Capping the maximum delay

For long lists, stagger delays can accumulate to feel sluggish. Cap the delay with `min()`:

```css
li {
  animation-delay: calc(min(0.05s * (sibling-index() - 1), 0.5s));
  /* Items beyond the 10th all animate at 0.5s — no infinite wait */
}
```

Or use a logarithmic curve for a natural easing of the stagger effect:

```css
li {
  /* Delay increases rapidly at first, then levels off */
  animation-delay: calc(0.15s * log(sibling-index()));
}
```

### Dynamic z-index stacking

`sibling-index()` is useful beyond animation — any value that depends on element order benefits:

```css
/* Stack cards with increasing z-index */
.card {
  position: relative;
  z-index: calc(sibling-index());
}

/* Reverse stack — first card on top */
.card-stack .card {
  z-index: calc(100 - sibling-index());
}
```

### Progressive scale or opacity

```css
/* Each item slightly more transparent than the previous */
.fade-trail > * {
  opacity: calc(1 - (sibling-index() - 1) * 0.1);
}

/* Each item progressively smaller */
.scale-trail > * {
  scale: calc(1 - (sibling-index() - 1) * 0.05);
}
```

### Combining with `sibling-count()`

The related `sibling-count()` function returns the total number of siblings, enabling proportional calculations:

```css
/* Distribute items evenly around a circle */
.radial > * {
  --angle: calc(360deg / sibling-count() * (sibling-index() - 1));
  rotate: var(--angle);
  translate: 0 -120px;
}
```

### Fallback for older browsers

```css
/* Static fallback — no stagger, but content still appears */
li {
  opacity: 1;
}

@supports (animation-delay: calc(0.05s * sibling-index())) {
  li {
    opacity: 0;
    animation: fade-in 0.3s ease forwards;
    animation-delay: calc(0.05s * (sibling-index() - 1));
  }
}
```

Or use the JavaScript `--i` variable approach as a fallback and disable it when `sibling-index()` is supported.

🟡 Newly available (~70%). Supported in Chromium and Firefox. For broader compatibility, use the JavaScript `--i` variable pattern as a fallback. The CSS version can coexist — the `sibling-index()` rule will override the JS-set `--i` in supporting browsers.

Reference: [modern-css.com](https://modern-css.com) · [CSS Values Level 5 — sibling-index()](https://drafts.csswg.org/css-values-5/#tree-counting)
