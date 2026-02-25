---
title: Carousel Navigation Without a JavaScript Library
impact: MEDIUM
impactDescription: native scroll navigation buttons and pagination dots without JS carousel dependencies
tags: layout, scroll-marker, scroll-button, carousel, pagination, navigation
browser: 72%
---

## Carousel Navigation Without a JavaScript Library

JavaScript carousel libraries like Swiper and Slick provide prev/next buttons and pagination dots, but they rebuild the entire scroll experience from scratch — adding bundle weight, DOM manipulation, and touch event handlers. The `::scroll-button()` and `::scroll-marker` pseudo-elements add native navigation controls on top of CSS Scroll Snap with zero JavaScript.

**Avoid (JavaScript carousel library for navigation):**

```js
// Swiper.js or Slick carousel
import Swiper from 'swiper';

new Swiper('.carousel', {
  navigation: {
    nextEl: '.swiper-button-next',
    prevEl: '.swiper-button-prev',
  },
  pagination: {
    el: '.swiper-pagination',
    clickable: true,
  },
});
// + custom DOM elements for buttons and dots
// + resize observers, scroll handlers, active state management
```

**Prefer (CSS scroll markers and buttons):**

```css
.carousel {
  display: flex;
  overflow-x: auto;
  scroll-snap-type: x mandatory;
  gap: 1rem;
}

.carousel > * {
  scroll-snap-align: start;
  flex-shrink: 0;
}

/* Prev / Next buttons — browser-generated */
.carousel::scroll-button(left) {
  content: '←';
}

.carousel::scroll-button(right) {
  content: '→';
}

/* Pagination dots — one per snap child */
.carousel > li::scroll-marker {
  content: '';
  display: inline-block;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: #ccc;
}

/* Active dot styling */
.carousel > li::scroll-marker:target-current {
  background: var(--accent, #333);
}
```

### How it works

- `::scroll-button(left)` and `::scroll-button(right)` generate prev/next navigation buttons that scroll the container by one snap interval. The browser handles scroll animation and disabling at boundaries.
- `::scroll-marker` generates a pagination indicator for each child element. Clicking a marker scrolls to the associated item.
- `:target-current` on a `::scroll-marker` targets the currently snapped/visible item — no JavaScript active-state management needed.

### Styling the scroll marker group

```css
.carousel::scroll-marker-group {
  display: flex;
  gap: 0.5rem;
  justify-content: center;
  padding-block: 0.75rem;
}
```

### Combining with scroll snap

These pseudo-elements are designed to work on top of CSS Scroll Snap (`scroll-snap-type` + `scroll-snap-align`). They do not replace scroll snap — they enhance it with navigation UI. See `layout-scroll-snap` for the base scroll snap setup.

🟡 Newly available (~72%). Support is shipping progressively in Chromium browsers. Use as a progressive enhancement layer — the underlying scroll snap carousel works without these pseudo-elements, and JavaScript carousel controls can serve as a fallback.

Reference: [modern-css.com](https://modern-css.com) · [CSS Overflow Level 5 — Scroll Markers](https://drafts.csswg.org/css-overflow-5/#scroll-markers)
