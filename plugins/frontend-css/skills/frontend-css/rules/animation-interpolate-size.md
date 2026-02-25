---
title: Smooth Height Auto Animations Without JavaScript
impact: HIGH
impactDescription: eliminates JavaScript scrollHeight measurement and manual pixel-based height transitions
tags: animation, interpolate-size, height-auto, transition, accordion
browser: 69%
---

## Smooth Height Auto Animations Without JavaScript

Animating an element's height from `0` to `auto` is one of the most common UI patterns (accordions, collapsible panels, expandable sections) — and one of the hardest to do without JavaScript. The browser cannot transition to `height: auto` because `auto` is a keyword, not a numeric value. The traditional workaround measures `scrollHeight` in JavaScript, sets an explicit pixel height, waits for `transitionend`, then resets to `auto`. The `interpolate-size: allow-keywords` declaration tells the browser to interpolate between numeric values and sizing keywords like `auto`, enabling smooth CSS-only height transitions.

**Avoid (JavaScript scrollHeight measurement):**

```js
// Expand: measure, set explicit height, then snap to auto
function expand(el) {
  el.style.height = el.scrollHeight + 'px'; // force reflow to measure
  el.addEventListener(
    'transitionend',
    () => {
      el.style.height = 'auto'; // snap to auto after transition
    },
    {once: true},
  );
}

// Collapse: read current height, set explicit, then transition to 0
function collapse(el) {
  el.style.height = el.scrollHeight + 'px'; // set current height explicitly
  requestAnimationFrame(() => {
    el.style.height = '0'; // now the transition can run
  });
}
// Layout thrashing on every open/close, fragile timing, must handle interruption
```

```css
.panel {
  overflow: hidden;
  transition: height 0.3s ease;
}
```

Or the `max-height` hack:

```css
.panel {
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.3s ease;
}

.panel.open {
  max-height: 500px; /* magic number — too small clips content, too large delays close */
}
```

The `max-height` approach produces a mismatched easing curve (the animation covers the full range from 0 to 500px but the content only fills part of it) and a delayed collapse when the content is much shorter than the max.

**Prefer (modern CSS):**

```css
:root {
  interpolate-size: allow-keywords;
}

.accordion-content {
  height: 0;
  overflow: hidden;
  transition: height 0.3s ease;
}

.accordion-content.open {
  height: auto;
}
```

Zero JavaScript measurement. Zero magic numbers. The browser smoothly interpolates between `height: 0` and `height: auto` (the intrinsic content height) with proper easing — the animation matches the actual content size exactly.

### How it works

`interpolate-size: allow-keywords` opts the element (and its descendants, since it inherits) into keyword interpolation. Once enabled, the browser can transition or animate between:

- `height: 0` → `height: auto`
- `width: auto` → `width: 200px`
- `min-height: 0` → `min-height: max-content`
- Any numeric value → any sizing keyword (`auto`, `min-content`, `max-content`, `fit-content`)

### Setting it globally

Because `interpolate-size` inherits, setting it on `:root` enables keyword interpolation for the entire page:

```css
:root {
  interpolate-size: allow-keywords;
}
```

This is safe to apply globally — it only affects elements that actually have transitions or animations on sizing properties. Elements without transitions render identically.

### Accordion pattern — pure CSS

```html
<details name="faq">
  <summary>Question 1</summary>
  <div class="details-content">
    <p>Answer to question 1.</p>
  </div>
</details>
<details name="faq">
  <summary>Question 2</summary>
  <div class="details-content">
    <p>
      Answer to question 2, which is much longer and demonstrates that the animation adapts to the
      actual content height.
    </p>
  </div>
</details>
```

```css
:root {
  interpolate-size: allow-keywords;
}

details .details-content {
  height: 0;
  overflow: hidden;
  opacity: 0;
  transition:
    height 0.3s ease,
    opacity 0.3s ease;
}

details[open] .details-content {
  height: auto;
  opacity: 1;
}
```

### Width animations

The same pattern works for width transitions — collapsible sidebars, expanding search inputs, etc.:

```css
.sidebar {
  width: 0;
  overflow: hidden;
  transition: width 0.3s ease;
}

.sidebar.expanded {
  width: auto; /* or width: max-content */
}
```

### Combining with `@starting-style` for entry animations

```css
:root {
  interpolate-size: allow-keywords;
}

.panel {
  height: auto;
  transition: height 0.3s ease;

  @starting-style {
    height: 0;
  }
}
```

### Why not `calc-size()`?

The `calc-size()` function is a more targeted alternative that enables keyword interpolation on a per-property basis:

```css
.panel.open {
  height: calc-size(auto);
}
```

`interpolate-size: allow-keywords` is the simpler, global approach — set it once on `:root` and forget about it. Use `calc-size()` when you need to perform arithmetic on keyword sizes (e.g., `calc-size(auto, size + 2rem)` for auto height plus padding compensation).

🟡 Newly available (~69%). Supported in Chromium and Firefox. For broader support, use the JavaScript `scrollHeight` approach as a fallback:

```js
if (!CSS.supports('interpolate-size', 'allow-keywords')) {
  // Fall back to JS measurement approach
}
```

Reference: [modern-css.com](https://modern-css.com) · [MDN — interpolate-size](https://developer.mozilla.org/en-US/docs/Web/CSS/interpolate-size)
