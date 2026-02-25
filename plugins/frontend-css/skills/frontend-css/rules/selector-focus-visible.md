---
title: Focus Styles Without Annoying Mouse Users
impact: HIGH
impactDescription: eliminates the tradeoff between accessible focus rings and clean mouse UX
tags: selectors, focus-visible, focus, accessibility, keyboard, outline
browser: 95%
---

## Focus Styles Without Annoying Mouse Users

Styling `:focus` applies the focus indicator on every interaction — keyboard, mouse, touch, and programmatic focus. This leads to one of two bad outcomes: either developers remove the outline entirely (`outline: none` — an accessibility failure) or users see distracting focus rings on every button click. `:focus-visible` applies focus styles only when the browser determines the user is navigating with a keyboard, giving you accessible focus indicators without visual noise on mouse and touch interactions.

**Avoid (:focus on everything — or removing it entirely):**

```css
/* Shows focus ring on mouse click — annoying */
:focus {
  outline: 2px solid blue;
}

/* Or the common "fix" that breaks accessibility */
:focus {
  outline: none;
}
/* Keyboard users can no longer see where they are — WCAG 2.4.7 failure */
```

Or the JavaScript workaround:

```js
// Track input method to toggle a class
document.addEventListener('keydown', () => document.body.classList.add('keyboard-user'));
document.addEventListener('mousedown', () => document.body.classList.remove('keyboard-user'));
```

```css
.keyboard-user :focus {
  outline: 2px solid blue;
}
```

**Prefer (modern CSS):**

```css
:focus-visible {
  outline: 2px solid var(--focus-color, oklch(0.55 0.2 264));
  outline-offset: 2px;
}
```

No JavaScript, no class toggling, no input-method tracking. The browser applies the outline only when the user is keyboard-navigating (Tab, arrow keys, etc.) and hides it for mouse and touch interactions.

### When `:focus-visible` matches

| Interaction             | `:focus` | `:focus-visible`   |
| ----------------------- | -------- | ------------------ |
| Mouse click on a button | ✅       | ❌                 |
| Tab to a button         | ✅       | ✅                 |
| Tab to a text input     | ✅       | ✅                 |
| Click into a text input | ✅       | ✅ (always shows)  |
| Programmatic `.focus()` | ✅       | Depends on context |
| Touch tap on a button   | ✅       | ❌                 |

Text inputs (`<input>`, `<textarea>`, `<select>`) always match `:focus-visible` because the user always needs to see where they're typing. Interactive controls like buttons and links only match when keyboard navigation is detected.

### Recommended global focus styles

```css
/* Visible focus ring for keyboard users */
:focus-visible {
  outline: 2px solid var(--focus-color, oklch(0.55 0.2 264));
  outline-offset: 2px;
}

/* Remove the default focus ring for mouse/touch — :focus-visible handles it */
:focus:not(:focus-visible) {
  outline: none;
}
```

The `:focus:not(:focus-visible)` rule explicitly removes the outline for non-keyboard focus, ensuring clean mouse interactions while keeping full keyboard accessibility.

### Custom focus ring designs

```css
/* Rounded focus ring that follows border-radius */
:focus-visible {
  outline: 2px solid var(--focus-color);
  outline-offset: 2px;
  border-radius: inherit; /* outline follows the element's border-radius in modern browsers */
}

/* Box-shadow alternative for more control */
:focus-visible {
  outline: none;
  box-shadow: 0 0 0 3px var(--focus-color);
}

/* High contrast — double ring for visibility on any background */
:focus-visible {
  outline: 2px solid var(--focus-color);
  outline-offset: 2px;
  box-shadow: 0 0 0 4px var(--surface-bg, white);
}
```

### Dark mode aware focus

```css
:root {
  --focus-color: light-dark(oklch(0.55 0.22 264), oklch(0.75 0.18 264));
}

:focus-visible {
  outline: 2px solid var(--focus-color);
  outline-offset: 2px;
}
```

### Per-component focus customization

```css
/* Buttons — standard ring */
button:focus-visible {
  outline: 2px solid var(--focus-color);
  outline-offset: 2px;
}

/* Cards — larger offset for grouped content */
.card:focus-visible {
  outline: 2px solid var(--focus-color);
  outline-offset: 4px;
}

/* Inputs — inner ring effect */
input:focus-visible,
textarea:focus-visible {
  outline: none;
  border-color: var(--focus-color);
  box-shadow: 0 0 0 3px oklch(0.55 0.2 264 / 0.25);
}
```

### Accessibility requirements

WCAG 2.2 Success Criterion 2.4.7 (Focus Visible, Level AA) requires that keyboard focus indicators are visible. `:focus-visible` satisfies this requirement — it ensures focus indicators appear whenever they're needed (keyboard navigation) while removing them when they're not (mouse/touch). See the `frontend-a11y` skill for full WCAG compliance patterns.

**Never do this:**

```css
/* ❌ Removes ALL focus indicators — WCAG failure */
* {
  outline: none !important;
}

/* ❌ Only styling :focus-visible without a :focus fallback for very old browsers */
:focus-visible {
  outline: 2px solid blue;
}
/* In browsers without :focus-visible support (now negligible), no focus ring at all */
```

✅ Widely available (~95%). Supported in all modern browsers. Use as the primary mechanism for focus styling — it is the correct, accessible default.

Reference: [modern-css.com](https://modern-css.com) · [MDN — :focus-visible](https://developer.mozilla.org/en-US/docs/Web/CSS/:focus-visible)
