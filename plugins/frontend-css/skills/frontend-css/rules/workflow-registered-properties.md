---
title: Typed Custom Properties Without JavaScript
impact: HIGH
impactDescription: enables animation, validation, and initial values for custom properties without JS
tags: workflow, custom-properties, @property, animation, typed
browser: 92%
---

## Typed Custom Properties Without JavaScript

Untyped custom properties (`--foo: 0`) are opaque strings to the browser — they can't be animated, aren't validated, and don't inherit predictably when unset. The `@property` at-rule registers a custom property with a syntax type, initial value, and inheritance flag, unlocking transitions, animations, and type checking with zero JavaScript.

**Avoid (untyped custom properties — no animation or validation):**

```css
:root {
  --hue: 0;
}

.gradient {
  background: hsl(var(--hue), 80%, 60%);
  transition: --hue 1s; /* Does nothing — browser sees a string, not a number */
}

.gradient:hover {
  --hue: 120; /* Snaps instantly, no interpolation */
}
```

Or the JavaScript equivalent for registering:

```js
CSS.registerProperty({
  name: '--hue',
  syntax: '<angle>',
  inherits: false,
  initialValue: '0deg',
});
```

**Prefer (CSS `@property` rule):**

```css
@property --hue {
  syntax: '<angle>';
  inherits: false;
  initial-value: 0deg;
}

.gradient {
  --hue: 0deg;
  background: hsl(var(--hue) 80% 60%);
  transition: --hue 1s ease;
}

.gradient:hover {
  --hue: 120deg; /* Smoothly animates through the hue spectrum */
}
```

No JavaScript, no `CSS.registerProperty()` call. The browser knows the property is an `<angle>`, so it can interpolate between values.

### Supported syntax types

| Syntax                | Example values                      | Use case                          |
| --------------------- | ----------------------------------- | --------------------------------- |
| `<number>`            | `0`, `1.5`, `-3`                    | Counters, multipliers             |
| `<integer>`           | `0`, `1`, `42`                      | Step-based values                 |
| `<length>`            | `0px`, `2rem`, `50vw`               | Spacing, sizing                   |
| `<percentage>`        | `0%`, `50%`, `100%`                 | Progress, ratios                  |
| `<angle>`             | `0deg`, `180deg`, `0.5turn`         | Rotation, hue                     |
| `<color>`             | `red`, `#fff`, `oklch(0.7 0.2 250)` | Color transitions                 |
| `<length-percentage>` | `10px`, `50%`                       | Flexible spacing                  |
| `<time>`              | `0s`, `200ms`                       | Duration control                  |
| `<custom-ident>`      | `ease`, `my-name`                   | Named tokens                      |
| `*`                   | Any value                           | Untyped (same as not registering) |

### Animating gradients

Gradients can't normally be animated because they're images, not interpolatable values. Registered properties solve this:

```css
@property --gradient-angle {
  syntax: '<angle>';
  inherits: false;
  initial-value: 0deg;
}

.conic {
  background: conic-gradient(from var(--gradient-angle), #f06, #9f6, #06f, #f06);
  animation: spin 3s linear infinite;
}

@keyframes spin {
  to {
    --gradient-angle: 360deg;
  }
}
```

### Animating color stops

```css
@property --stop-1 {
  syntax: '<color>';
  inherits: false;
  initial-value: oklch(0.7 0.25 330);
}

@property --stop-2 {
  syntax: '<color>';
  inherits: false;
  initial-value: oklch(0.6 0.2 250);
}

.hero {
  background: linear-gradient(135deg, var(--stop-1), var(--stop-2));
  transition:
    --stop-1 0.6s,
    --stop-2 0.6s;
}

.hero:hover {
  --stop-1: oklch(0.8 0.2 80);
  --stop-2: oklch(0.5 0.25 150);
}
```

### Type safety and fallback values

When a registered property receives an invalid value, it falls back to the `initial-value` rather than becoming `unset`. This prevents broken styles from propagating:

```css
@property --spacing {
  syntax: '<length>';
  inherits: true;
  initial-value: 1rem;
}

.card {
  --spacing: banana; /* Invalid — falls back to 1rem, not broken layout */
  padding: var(--spacing);
}
```

✅ Widely available (~92%). Supported in all major browsers. Use freely for any custom property that needs animation, interpolation, or type validation.

Reference: [modern-css.com](https://modern-css.com) · [MDN — @property](https://developer.mozilla.org/en-US/docs/Web/CSS/@property)
