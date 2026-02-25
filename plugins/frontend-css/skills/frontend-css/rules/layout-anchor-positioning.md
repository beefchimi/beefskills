---
title: Tooltip Positioning Without JavaScript
impact: HIGH
impactDescription: eliminates Popper.js / Floating UI dependency and JavaScript positioning logic
tags: layout, anchor-positioning, tooltip, popover, floating-ui, popper
browser: 77%
---

## Tooltip Positioning Without JavaScript

Libraries like Popper.js and Floating UI exist solely to position a floating element relative to a trigger — computing rects, flipping on overflow, updating on scroll and resize. CSS Anchor Positioning does all of this declaratively with zero JavaScript, zero dependencies, and compositor-level performance.

**Avoid (Popper.js / Floating UI):**

```js
// npm install @floating-ui/dom — 10 KB+ gzipped
import {computePosition, flip, shift, offset} from '@floating-ui/dom';

async function updateTooltip(trigger, tooltip) {
  const {x, y} = await computePosition(trigger, tooltip, {
    placement: 'bottom',
    middleware: [offset(8), flip(), shift({padding: 8})],
  });
  tooltip.style.left = `${x}px`;
  tooltip.style.top = `${y}px`;
}

// Must re-run on scroll, resize, layout changes…
window.addEventListener('scroll', () => updateTooltip(trigger, tooltip));
window.addEventListener('resize', () => updateTooltip(trigger, tooltip));
```

```css
.tooltip {
  position: fixed;
  z-index: 9999;
}
```

**Prefer (CSS Anchor Positioning):**

```css
.trigger {
  anchor-name: --tip;
}

.tooltip {
  position: fixed;
  position-anchor: --tip;

  /* Place below the trigger with 8px offset */
  inset-area: bottom;
  margin-top: 8px;

  /* Auto-flip if it would overflow the viewport */
  position-try-fallbacks: flip-block, flip-inline;

  /* Sizing constraints */
  max-inline-size: 300px;
}
```

```html
<button class="trigger">Hover me</button>
<div class="tooltip" popover>Tooltip content here</div>
```

**Multiple anchors and named fallbacks:**

```css
/* Position try fallbacks with custom positions */
@position-try --above {
  inset-area: top;
  margin-bottom: 8px;
}

@position-try --right {
  inset-area: right;
  margin-left: 8px;
}

.tooltip {
  position: fixed;
  position-anchor: --tip;
  inset-area: bottom;
  margin-top: 8px;
  position-try-fallbacks: --above, --right;
}
```

**Anchoring with `anchor()` functions for precise control:**

```css
.tooltip {
  position: fixed;
  position-anchor: --tip;

  /* Explicit anchor function placement */
  top: anchor(bottom);
  left: anchor(center);
  translate: -50% 0;
}
```

CSS Anchor Positioning handles scroll tracking, viewport flipping, and repositioning automatically — the browser re-evaluates on every frame without JavaScript. No event listeners, no `requestAnimationFrame`, no z-index wars.

🟡 Newly available (~77%). Supported in Chromium browsers and Firefox. Use behind `@supports (anchor-name: --x)` with a Floating UI fallback for Safari until support ships.

Reference: [modern-css.com](https://modern-css.com) · [MDN — CSS Anchor Positioning](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_anchor_positioning)
