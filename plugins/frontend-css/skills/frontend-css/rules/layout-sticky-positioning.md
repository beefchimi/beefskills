---
title: Sticky Headers Without JavaScript Scroll Listeners
impact: HIGH
impactDescription: eliminates scroll event JS and forced layouts
tags: layout, sticky, scroll, position, header
browser: 96%
---

## Sticky Headers Without JavaScript Scroll Listeners

JavaScript scroll listeners that read `getBoundingClientRect()` and toggle a `.fixed` class force synchronous layout on every frame. `position: sticky` is declarative, GPU-composited, and requires zero JavaScript.

**Avoid (JavaScript scroll listener):**

```js
// JS: scroll listener + getBoundingClientRect
// then add/remove .fixed class
window.addEventListener('scroll', () => {
  const rect = header.getBoundingClientRect();
  header.classList.toggle('fixed', rect.top <= 0);
});
```

```css
.header.fixed {
  position: fixed;
  top: 0;
  width: 100%;
  z-index: 10;
}
```

**Prefer (modern CSS):**

```css
.header {
  position: sticky;
  top: 0;
  z-index: 10;
}
```

No JavaScript, no layout thrashing, no class toggling. The element sticks in its natural document flow and respects its containing block.

**Nested sticky elements** work too — each sticky element sticks within its own scroll container or containing block:

```css
.sidebar {
  position: sticky;
  top: 1rem;
  align-self: start; /* important inside grid/flex parents */
}
```

✅ Widely available (~96%). Use freely.

Reference: [modern-css.com](https://modern-css.com) · [MDN position: sticky](https://developer.mozilla.org/en-US/docs/Web/CSS/position#sticky)
