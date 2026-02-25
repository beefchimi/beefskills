---
title: Preventing Scroll Chaining Without JavaScript
impact: HIGH
impactDescription: eliminates JavaScript wheel/touch event interception for scroll containment
tags: layout, scroll, overscroll-behavior, modal, overflow
browser: 96%
---

## Preventing Scroll Chaining Without JavaScript

When a user scrolls to the end of a scrollable element (like a modal or sidebar), the browser "chains" the scroll to the parent — causing the page behind a modal to scroll. The old fix was intercepting `wheel` and `touchmove` events in JavaScript with `preventDefault()`, which blocks the main thread, fights passive listener defaults, and is fragile across input methods. `overscroll-behavior: contain` solves this declaratively with zero JavaScript.

**Avoid (JavaScript wheel/touch event prevention):**

```js
// Block page scroll when inside modal
modal.addEventListener(
  'wheel',
  (e) => {
    const atTop = modal.scrollTop === 0;
    const atBottom = modal.scrollTop + modal.clientHeight >= modal.scrollHeight;
    if ((e.deltaY < 0 && atTop) || (e.deltaY > 0 && atBottom)) {
      e.preventDefault();
    }
  },
  {passive: false}, // must opt out of passive to call preventDefault
);

// Also need touchmove handling for mobile
modal.addEventListener(
  'touchmove',
  (e) => {
    /* similar logic */
  },
  {passive: false},
);
```

**Prefer (modern CSS):**

```css
.modal-content {
  overflow-y: auto;
  overscroll-behavior: contain;
}
/* Page stays still when modal scroll reaches the boundary */
```

### Common use cases

```css
/* Modal / dialog — prevent background scroll chaining */
dialog {
  overscroll-behavior: contain;
}

/* Chat panel / sidebar — keep scroll isolated */
.chat-messages {
  overflow-y: auto;
  overscroll-behavior-y: contain;
}

/* Pull-to-refresh opt-out on a specific container */
.custom-scroll-area {
  overscroll-behavior-y: none;
}
```

### Values

| Value     | Behavior                                                            |
| --------- | ------------------------------------------------------------------- |
| `auto`    | Default — scroll chains to ancestor when boundary is reached        |
| `contain` | Scroll stops at the element boundary, no chaining                   |
| `none`    | Same as `contain`, and also prevents overscroll glow/bounce effects |

`overscroll-behavior` is a shorthand for `overscroll-behavior-x` and `overscroll-behavior-y`. Use the axis-specific property when you only need to contain one direction.

✅ Widely available (~96%). Supported in all major browsers. No fallback needed.

Reference: [modern-css.com](https://modern-css.com) · [MDN — overscroll-behavior](https://developer.mozilla.org/en-US/docs/Web/CSS/overscroll-behavior)
