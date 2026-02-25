---
title: Entry Animations Without JavaScript Timing
impact: HIGH
impactDescription: eliminates requestAnimationFrame and setTimeout hacks for initial render animations
tags: animation, starting-style, entry, transition, rAF
browser: 85%
---

## Entry Animations Without JavaScript Timing

Animating an element's appearance when it first renders (e.g., fading in a card, sliding in a notification) traditionally required a two-step JavaScript hack: render the element in its "before" state, then use `requestAnimationFrame` or `setTimeout` to add a class that triggers the transition. This creates a flash of the initial state, is timing-dependent, and adds unnecessary JavaScript. The `@starting-style` at-rule defines the "before" state directly in CSS — the browser transitions from those values to the element's normal styles automatically on first render.

**Avoid (requestAnimationFrame class toggling):**

```js
// Render element in hidden state, then trigger transition after paint
const card = document.createElement('div');
card.className = 'card';
container.appendChild(card);

// Must wait for the browser to paint the initial state
requestAnimationFrame(() => {
  requestAnimationFrame(() => {
    card.classList.add('visible');
  });
});
// Double rAF is needed because single rAF isn't reliable across browsers
```

```css
.card {
  opacity: 0;
  transform: translateY(10px);
  transition:
    opacity 0.3s ease,
    transform 0.3s ease;
}

.card.visible {
  opacity: 1;
  transform: translateY(0);
}
```

Or the `setTimeout` variant:

```js
// Fragile — timing depends on browser, layout complexity, and device speed
el.classList.add('card');
setTimeout(() => el.classList.add('visible'), 50);
```

**Prefer (modern CSS — `@starting-style`):**

```css
.card {
  opacity: 1;
  transform: translateY(0);
  transition:
    opacity 0.3s ease,
    transform 0.3s ease;

  @starting-style {
    opacity: 0;
    transform: translateY(10px);
  }
}
/* No JavaScript, no rAF, no setTimeout — the browser handles the timing */
```

The element transitions from the `@starting-style` values to its normal computed values the moment it enters the DOM or becomes visible. No class toggling, no timing hacks.

### How `@starting-style` works

1. The browser reads the `@starting-style` block to determine the "from" values.
2. On the element's first style computation (insertion into the DOM, `display` changing from `none` to visible, etc.), the browser applies the starting values.
3. The transition then runs from those starting values to the element's normal computed styles.

### Nested syntax (recommended)

```css
.notification {
  opacity: 1;
  translate: 0;
  transition:
    opacity 0.3s,
    translate 0.3s;

  @starting-style {
    opacity: 0;
    translate: 0 -1rem;
  }
}
```

### Standalone syntax (alternative)

```css
.notification {
  opacity: 1;
  translate: 0;
  transition:
    opacity 0.3s,
    translate 0.3s;
}

@starting-style {
  .notification {
    opacity: 0;
    translate: 0 -1rem;
  }
}
```

Both forms are equivalent. The nested syntax is more readable and keeps the starting state co-located with the element's styles.

### Animating elements from `display: none`

`@starting-style` pairs with `transition-behavior: allow-discrete` (see `animation-display-transition`) to animate elements that toggle between `display: none` and visible states:

```css
.modal {
  opacity: 1;
  scale: 1;
  transition:
    opacity 0.3s,
    scale 0.3s,
    overlay 0.3s,
    display 0.3s;
  transition-behavior: allow-discrete;

  @starting-style {
    opacity: 0;
    scale: 0.95;
  }
}

.modal.hidden {
  opacity: 0;
  scale: 0.95;
  display: none;
}
```

This gives you both entry and exit animations for elements that use `display: none` — without JavaScript timing or visibility hacks.

### Popover entry animations

`@starting-style` is the correct way to animate popovers and dialogs on open:

```css
[popover] {
  opacity: 1;
  scale: 1;
  transition:
    opacity 0.2s,
    scale 0.2s,
    overlay 0.2s,
    display 0.2s;
  transition-behavior: allow-discrete;

  @starting-style {
    opacity: 0;
    scale: 0.95;
  }
}
```

### List item stagger

Combine with `nth-child` or `sibling-index()` for staggered entry animations:

```css
.list-item {
  opacity: 1;
  translate: 0;
  transition:
    opacity 0.3s ease,
    translate 0.3s ease;
  transition-delay: calc(var(--index, 0) * 0.05s);

  @starting-style {
    opacity: 0;
    translate: 0 0.5rem;
  }
}
```

### Common entry animation patterns

```css
/* Fade in */
.fade-in {
  opacity: 1;
  transition: opacity 0.3s ease;

  @starting-style {
    opacity: 0;
  }
}

/* Slide up and fade */
.slide-up {
  opacity: 1;
  translate: 0;
  transition:
    opacity 0.4s ease,
    translate 0.4s ease;

  @starting-style {
    opacity: 0;
    translate: 0 1rem;
  }
}

/* Scale in */
.scale-in {
  opacity: 1;
  scale: 1;
  transition:
    opacity 0.3s ease,
    scale 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);

  @starting-style {
    opacity: 0;
    scale: 0.9;
  }
}

/* Respect reduced motion */
@media (prefers-reduced-motion: reduce) {
  .fade-in,
  .slide-up,
  .scale-in {
    transition-duration: 0.01ms;
  }
}
```

🟡 Newly available (~85%). Supported in all modern browsers. Falls back gracefully — in unsupporting browsers, the element renders immediately in its final state (no animation, but no broken layout).

Reference: [modern-css.com](https://modern-css.com) · [MDN — @starting-style](https://developer.mozilla.org/en-US/docs/Web/CSS/@starting-style)
