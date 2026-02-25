---
title: Animating Display None Without Workarounds
impact: HIGH
impactDescription: eliminates JavaScript transitionend listeners and visibility/opacity/pointer-events hacks
tags: animation, display, transition, allow-discrete, opacity, visibility
browser: 85%
---

## Animating Display None Without Workarounds

Transitioning an element to and from `display: none` has been impossible in CSS — the browser removes the element from the layout immediately, skipping any transition. The traditional workaround chains `visibility`, `opacity`, and `pointer-events` together, then uses a JavaScript `transitionend` listener to set `display: none` after the fade completes. The `transition-behavior: allow-discrete` property tells the browser to transition discrete properties like `display`, eliminating the multi-property hack and the JavaScript listener entirely.

**Avoid (visibility + opacity + JS transitionend):**

```js
// Wait for opacity transition to finish, then set display: none
function hideElement(el) {
  el.style.opacity = '0';
  el.style.pointerEvents = 'none';

  el.addEventListener(
    'transitionend',
    () => {
      el.style.display = 'none';
    },
    {once: true},
  );
}

function showElement(el) {
  el.style.display = 'block';
  // Force reflow so the browser sees display change before opacity change
  el.offsetHeight;
  el.style.opacity = '1';
  el.style.pointerEvents = '';
}
```

```css
.panel {
  opacity: 1;
  visibility: visible;
  pointer-events: auto;
  transition:
    opacity 0.2s ease,
    visibility 0.2s ease;
}

.panel.hidden {
  opacity: 0;
  visibility: hidden;
  pointer-events: none;
  /* display: none would skip the transition entirely */
}
/* Element is still in the layout (takes up space) even when "hidden" */
```

The `visibility` + `opacity` approach has a critical flaw: the element remains in the document flow and occupies space. True `display: none` removal requires JavaScript timing.

**Prefer (modern CSS with `allow-discrete`):**

```css
.panel {
  opacity: 1;
  display: block;
  transition:
    opacity 0.2s ease,
    display 0.2s ease,
    overlay 0.2s ease;
  transition-behavior: allow-discrete;
}

.panel.hidden {
  opacity: 0;
  display: none;
}
```

No JavaScript, no `transitionend` listener, no forced reflow hack. The browser:

1. Keeps `display: block` during the exit transition so `opacity` can animate.
2. Switches to `display: none` only after the transition completes.
3. On entry (removing `.hidden`), immediately sets `display: block` and then animates `opacity`.

### The `overlay` property

When transitioning elements in the top layer (dialogs, popovers), include `overlay` in the transition list to keep the element in the top layer during the exit animation:

```css
dialog {
  opacity: 1;
  transition:
    opacity 0.3s ease,
    display 0.3s ease,
    overlay 0.3s ease;
  transition-behavior: allow-discrete;
}

dialog:not([open]) {
  opacity: 0;
  display: none;
}
```

Without `overlay`, a closing dialog would drop out of the top layer immediately, snapping behind other content before the opacity fade completes.

### Combining with `@starting-style` for entry animations

`allow-discrete` handles the exit transition (block → none), but the entry transition (none → block) also needs a starting state. Use `@starting-style` to define what the element looks like when it first appears:

```css
.panel {
  opacity: 1;
  transform: translateY(0);
  display: block;
  transition:
    opacity 0.3s ease,
    transform 0.3s ease,
    display 0.3s ease;
  transition-behavior: allow-discrete;

  @starting-style {
    opacity: 0;
    transform: translateY(10px);
  }
}

.panel.hidden {
  opacity: 0;
  transform: translateY(10px);
  display: none;
}
```

See `animation-starting-style` for more on entry animations.

### Applying to popover and dialog

```css
[popover] {
  opacity: 0;
  transform: scale(0.95);
  transition:
    opacity 0.2s ease,
    transform 0.2s ease,
    display 0.2s ease,
    overlay 0.2s ease;
  transition-behavior: allow-discrete;
}

[popover]:popover-open {
  opacity: 1;
  transform: scale(1);
}

[popover]:popover-open {
  @starting-style {
    opacity: 0;
    transform: scale(0.95);
  }
}
```

### Shorthand syntax

You can specify `allow-discrete` per-property in the `transition` shorthand:

```css
.panel {
  transition:
    opacity 0.2s ease,
    display 0.2s ease allow-discrete,
    overlay 0.2s ease allow-discrete;
}
/* Only display and overlay are discrete — opacity transitions normally */
```

Or apply `transition-behavior: allow-discrete` as a blanket rule — it has no effect on properties that already transition continuously (like `opacity`), so it's safe to set globally.

### What `allow-discrete` actually does

Discrete properties (like `display`, `content-visibility`) have no intermediate values — they can only snap between states. `allow-discrete` tells the browser to delay the snap to the end of the transition duration (for exit) or apply it at the start (for entry), giving continuous properties like `opacity` and `transform` time to animate.

| Transition direction | When `display` changes            |
| -------------------- | --------------------------------- |
| Entry (none → block) | Immediately at transition start   |
| Exit (block → none)  | At the end of transition duration |

🟡 Newly available (~85%). Supported in all modern browsers. Falls back gracefully — in unsupporting browsers, the element snaps to `display: none` without animation, which is functional if not smooth.

## React

When building React UI, this modern CSS technique is generally discouraged. Instead, we prefer to unmount components that are not visually rendered on the screen. Therefor, transitioning discrete properties like `display` are not necessary.

Reference: [modern-css.com](https://modern-css.com) · [MDN — transition-behavior](https://developer.mozilla.org/en-US/docs/Web/CSS/transition-behavior)
