---
title: Sticky & Snapped Element Styling Without JavaScript
impact: MEDIUM
impactDescription: eliminates JavaScript scroll position checks for styling stuck and snapped elements
tags: animation, scroll-state, sticky, snapped, container-query, scroll
browser: 50%
---

## Sticky & Snapped Element Styling Without JavaScript

Detecting when a sticky element is “stuck” or when a scroll-snap child is “snapped” traditionally requires JavaScript scroll event listeners that compare `getBoundingClientRect()` values on every frame — causing layout thrashing and main-thread work. The `@container scroll-state()` query lets you style elements based on their scroll-related state declaratively in CSS, with zero JavaScript.

**Avoid (JavaScript scroll position checks):**

```js
// Check if sticky header is stuck
const header = document.querySelector(".header");

window.addEventListener("scroll", () => {
  const rect = header.getBoundingClientRect();
  header.classList.toggle("stuck", rect.top <= 0);
});

// Check if a snap child is currently snapped
const items = document.querySelectorAll(".carousel > *");
const carousel = document.querySelector(".carousel");

carousel.addEventListener("scroll", () => {
  items.forEach((item) => {
    const rect = item.getBoundingClientRect();
    const containerRect = carousel.getBoundingClientRect();
    const isSnapped = Math.abs(rect.left - containerRect.left) < 2;
    item.classList.toggle("snapped", isSnapped);
  });
});
// Runs on every scroll frame — layout thrashing, main-thread blocking
```

```css
.header.stuck {
  box-shadow: 0 2px 8px rgb(0 0 0 / 0.1);
  backdrop-filter: blur(8px);
}

.carousel > *.snapped {
  opacity: 1;
  scale: 1;
}
```

**Prefer (CSS scroll-state container queries):**

```css
.header {
  position: sticky;
  top: 0;
  container-type: scroll-state;
}

@container scroll-state(stuck: top) {
  .header {
    box-shadow: 0 2px 8px rgb(0 0 0 / 0.1);
    backdrop-filter: blur(8px);
  }
}
```

No JavaScript, no scroll listeners, no `getBoundingClientRect()`, no class toggling. The browser evaluates the scroll state internally and applies styles when the condition is met.

### Stuck state queries

Detect when a `position: sticky` element is stuck to an edge of its scroll container:

```css
.sticky-nav {
  position: sticky;
  top: 0;
  container-type: scroll-state;
  transition: box-shadow 200ms ease;
}

/* Stuck to the top edge */
@container scroll-state(stuck: top) {
  .sticky-nav {
    box-shadow: 0 2px 12px rgb(0 0 0 / 0.08);
    border-bottom: 1px solid oklch(0.9 0.01 250);
  }
}

/* Stuck to the bottom edge */
.sticky-footer {
  position: sticky;
  bottom: 0;
  container-type: scroll-state;
}

@container scroll-state(stuck: bottom) {
  .sticky-footer {
    box-shadow: 0 -2px 12px rgb(0 0 0 / 0.08);
  }
}
```

### Snapped state queries

Detect when a scroll-snap child is currently snapped into position:

```css
.carousel {
  scroll-snap-type: x mandatory;
  container-type: scroll-state;
}

.carousel > .slide {
  scroll-snap-align: center;
  opacity: 0.5;
  scale: 0.95;
  transition:
    opacity 0.3s,
    scale 0.3s;
}

@container scroll-state(snapped: x) {
  .slide {
    opacity: 1;
    scale: 1;
  }
}
```

### Scrollable state queries

Detect whether a container is scrollable in a given direction (useful for showing/hiding scroll indicators):

```css
.scrollable-area {
  overflow-y: auto;
  container-type: scroll-state;
}

/* Show a "scroll for more" indicator only when there's content to scroll to */
@container scroll-state(scrollable: top) {
  .scroll-indicator-top {
    display: block;
  }
}

@container scroll-state(scrollable: bottom) {
  .scroll-indicator-bottom {
    display: block;
  }
}
```

### Common patterns

```css
/* Sticky header with progressive shadow */
.page-header {
  position: sticky;
  top: 0;
  z-index: 10;
  container-type: scroll-state;
  background: var(--surface);
}

@container scroll-state(stuck: top) {
  .page-header {
    background: light-dark(rgb(255 255 255 / 0.9), rgb(15 15 15 / 0.9));
    backdrop-filter: blur(12px);
    box-shadow: 0 1px 0 oklch(0.5 0 0 / 0.1);
  }
}

/* Carousel with active slide indicator */
.carousel-wrapper {
  container-type: scroll-state;
}

@container scroll-state(snapped: x) {
  .slide {
    /* Snapped slide gets full prominence */
    filter: none;
  }
}

.slide {
  filter: grayscale(0.5) brightness(0.8);
  transition: filter 0.3s ease;
}
```

### Stuck values

| Value    | Matches when                          |
| -------- | ------------------------------------- |
| `top`    | Stuck to the top edge                 |
| `right`  | Stuck to the right / inline-end edge  |
| `bottom` | Stuck to the bottom edge              |
| `left`   | Stuck to the left / inline-start edge |
| `none`   | Not currently stuck                   |

### Snapped values

| Value  | Matches when                            |
| ------ | --------------------------------------- |
| `x`    | Snapped on the horizontal (inline) axis |
| `y`    | Snapped on the vertical (block) axis    |
| `none` | Not currently snapped                   |

### Why this is better than JavaScript

- **No layout thrashing** — the browser evaluates state internally without forcing layout recalculation.
- **Compositor-driven** — state changes are detected at the compositing level, not on the main thread.
- **Declarative** — styles are defined in CSS where they belong, not spread across JS event handlers.
- **Automatic cleanup** — no observers to disconnect, no listeners to remove.

🟠 Limited (~50%). Early browser support, shipping in Chromium. Use as a progressive enhancement — the element works without the scroll-state styles (just without the visual polish), and a JavaScript `scroll` listener can serve as a fallback for broader compatibility.

Reference: [modern-css.com](https://modern-css.com) · [CSS Conditional Rules — scroll-state()](https://drafts.csswg.org/css-conditional-5/#scroll-state-container-query)
