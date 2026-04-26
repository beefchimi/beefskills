---
title: Hover Tooltips Without JavaScript Events
impact: MEDIUM
impactDescription: eliminates mouseenter/mouseleave/focus/blur JS listeners for tooltip behavior
tags: layout, popover, hint, tooltip, hover, interestfor
browser: 86%
---

## Hover Tooltips Without JavaScript Events

Building hover tooltips traditionally requires JavaScript `mouseenter`, `mouseleave`, `focus`, `blur` listeners, positioning logic, and `aria-describedby` wiring. The `popover=hint` type combined with the `interesttarget` attribute provides native hover/focus tooltip behavior — including show delay, graceful dismissal, and accessibility — with zero JavaScript.

**Avoid (JavaScript event listeners):**

```js
const btn = document.querySelector('.trigger');
const tip = document.querySelector('.tooltip');
let timeout;

btn.addEventListener('mouseenter', () => {
  timeout = setTimeout(() => showTooltip(btn, tip), 200);
});
btn.addEventListener('mouseleave', () => {
  clearTimeout(timeout);
  tip.hidden = true;
});
btn.addEventListener('focus', () => showTooltip(btn, tip));
btn.addEventListener('blur', () => (tip.hidden = true));

function showTooltip(anchor, tooltip) {
  // + positioning logic (getBoundingClientRect, viewport checks)
  tooltip.hidden = false;
}
```

```css
.tooltip {
  position: fixed;
  z-index: 9999;
  background: #333;
  color: white;
  padding: 0.5rem 0.75rem;
  border-radius: 4px;
  font-size: 0.875rem;
}
```

**Prefer (popover hint with interesttarget):**

```html
<button interesttarget="tip">Hover me</button>

<div id="tip" popover="hint">Tooltip content goes here</div>
```

```css
[popover='hint'] {
  margin: 0;
  padding: 0.5rem 0.75rem;
  background: #333;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 0.875rem;
  max-inline-size: 250px;
}
```

The browser handles:

- **Show on hover/focus** — appears after a brief delay when hovering or focusing the trigger.
- **Hide on leave** — gracefully dismisses when the pointer moves away.
- **Light dismiss** — pressing Escape closes the tooltip.
- **Top layer** — renders above all other content, no `z-index` battles.
- **Accessibility** — proper association between trigger and tooltip for screen readers.

### Popover type comparison

| Type               | Trigger          | Light dismiss | Multiple open |
| ------------------ | ---------------- | ------------- | ------------- |
| `popover="auto"`   | Click            | Yes           | No            |
| `popover="hint"`   | Hover / focus    | Yes           | With auto     |
| `popover="manual"` | Explicit JS only | No            | Yes           |

### With anchor positioning for precise placement

```css
.trigger {
  anchor-name: --tip-anchor;
}

[popover='hint'] {
  position: fixed;
  position-anchor: --tip-anchor;
  inset-area: top;
  margin-bottom: 6px;
  position-try-fallbacks: flip-block;
}
```

### Styling the open state with animation

```css
[popover='hint'] {
  opacity: 0;
  transition:
    opacity 0.15s ease-out,
    overlay 0.15s,
    display 0.15s;
  transition-behavior: allow-discrete;
}

[popover='hint']:popover-open {
  opacity: 1;
}

[popover='hint'] {
  @starting-style {
    opacity: 0;
  }
}
```

`popover=hint` is specifically designed for non-interactive, informational content that appears on hover or focus — exactly the tooltip pattern. For interactive popup content (menus, pickers), use `popover="auto"` with a click trigger instead.

🟡 Newly available (~86%). The `interesttarget` attribute and `popover="hint"` are shipping across modern browsers. For older browsers, a simple CSS `:hover` + `:focus-visible` fallback provides a baseline tooltip experience.

Reference: [modern-css.com](https://modern-css.com) · [MDN — Popover API](https://developer.mozilla.org/en-US/docs/Web/API/Popover_API)
