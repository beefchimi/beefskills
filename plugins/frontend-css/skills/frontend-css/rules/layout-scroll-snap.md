---
title: Scroll Snapping Without a Carousel Library
impact: HIGH
impactDescription: eliminates JavaScript carousel dependencies and touch handlers
tags: layout, scroll-snap, carousel, scroll, touch
browser: 96%
---

## Scroll Snapping Without a Carousel Library

JavaScript carousel libraries like Slick, Swiper, and Flickity rebuild scroll behavior from scratch — adding bundle weight, touch event listeners, and DOM manipulation. CSS Scroll Snap provides native, GPU-accelerated snap points with momentum scrolling, accessibility, and touch support built in.

**Avoid (JavaScript carousel library):**

```js
// Slick, Swiper, or custom scroll/touch handlers
import Swiper from 'swiper';

new Swiper('.carousel', {
  slidesPerView: 'auto',
  spaceBetween: 16,
  navigation: {next: '.next', prev: '.prev'},
  pagination: {el: '.dots'},
});
// + touch handlers, resize observers, DOM cloning for "infinite" mode
```

**Prefer (CSS Scroll Snap):**

```css
.carousel {
  display: flex;
  gap: 16px;
  overflow-x: auto;
  scroll-snap-type: x mandatory;
  scroll-padding-inline: 16px; /* inset snap points for peek effect */
  -webkit-overflow-scrolling: touch;
}

.carousel > * {
  scroll-snap-align: start;
  flex-shrink: 0;
}
```

**Snap alignment options:**

```css
/* Snap to the start edge of each item */
.item {
  scroll-snap-align: start;
}

/* Snap to the center — good for "focus" carousels */
.item {
  scroll-snap-align: center;
}

/* Snap to the end edge */
.item {
  scroll-snap-align: end;
}
```

**Mandatory vs. proximity:**

```css
/* mandatory — always snaps to the nearest snap point after scroll */
.container {
  scroll-snap-type: x mandatory;
}

/* proximity — only snaps when near a snap point (more natural for long lists) */
.container {
  scroll-snap-type: x proximity;
}

/* Both axes */
.grid-container {
  scroll-snap-type: both mandatory;
}
```

**Vertical scroll snapping (full-page sections):**

```css
.page {
  height: 100dvh;
  overflow-y: auto;
  scroll-snap-type: y mandatory;
}

.page > section {
  height: 100dvh;
  scroll-snap-align: start;
}
```

**Preventing overscroll bounce at boundaries:**

```css
.carousel {
  scroll-snap-type: x mandatory;
  overscroll-behavior-x: contain; /* no page navigation on swipe past ends */
}
```

For navigation buttons and pagination dots on top of CSS Scroll Snap, see `layout-scroll-markers` (using `::scroll-button()` and `::scroll-marker` pseudo-elements).

✅ Widely available (~96%). Native momentum scrolling, keyboard-accessible, and works with assistive technology — no library needed.

Reference: [modern-css.com](https://modern-css.com) · [MDN: CSS Scroll Snap](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_scroll_snap)
