---
title: Custom Easing Curves Without cubic-bezier Guessing
impact: MEDIUM
impactDescription: eliminates JavaScript animation library dependency for custom easing curves like bounce and elastic
tags: animation, linear, easing, cubic-bezier, bounce, spring
browser: 87%
---

## Custom Easing Curves Without cubic-bezier Guessing

Complex easing curves like bounce, elastic, and spring effects have traditionally required JavaScript animation libraries (GSAP, Anime.js, Framer Motion) because `cubic-bezier()` can only represent a limited subset of curves — it cannot overshoot multiple times, bounce, or create step-like patterns. The `linear()` easing function accepts an arbitrary number of control points, letting you define any easing curve imaginable in pure CSS.

**Avoid (JavaScript animation library for bounce/spring):**

```js
// Anime.js — 17 KB+ gzipped
import anime from 'animejs';

anime({
  targets: '.card',
  translateY: [50, 0],
  easing: 'easeOutBounce',
  duration: 1000,
});

// Or GSAP
gsap.to('.card', {
  y: 0,
  ease: 'bounce.out',
  duration: 1,
});
// + library dependency, JS execution cost, not compositor-accelerated
```

**Prefer (CSS `linear()` easing):**

```css
.card {
  transition: transform 1s
    linear(
      0,
      0.004,
      0.016,
      0.035,
      0.063,
      0.098,
      0.141,
      0.191,
      0.25,
      0.316,
      0.391,
      0.473,
      0.563,
      0.66,
      0.766,
      0.879,
      1,
      0.891,
      0.813,
      0.766,
      0.75,
      0.766,
      0.813,
      0.891,
      1,
      0.938,
      0.906,
      0.938,
      1
    );
}

.card:hover {
  transform: translateY(-10px);
}
/* GPU-composited bounce — no JS library, no main thread work */
```

### How `linear()` works

`linear()` defines an easing curve as a series of output values at evenly spaced intervals (or at explicit positions). The browser interpolates linearly between each pair of points, creating a piecewise-linear approximation of any curve:

```
linear(output1, output2, output3, …)
```

- Each value is a number where `0` = start and `1` = end.
- Values above `1` create overshoot; values below `0` create undershoot.
- Points are evenly distributed unless explicit stops are provided.

### Common easing curves

**Bounce out:**

```css
.bounce {
  animation-timing-function: linear(
    0,
    0.004,
    0.016,
    0.035,
    0.063,
    0.098,
    0.141,
    0.191,
    0.25,
    0.316,
    0.391,
    0.473,
    0.563,
    0.66,
    0.766,
    0.879,
    1,
    0.891,
    0.813,
    0.766,
    0.75,
    0.766,
    0.813,
    0.891,
    1,
    0.938,
    0.906,
    0.938,
    1
  );
}
```

**Elastic out:**

```css
.elastic {
  animation-timing-function: linear(
    0,
    0.218 2.1%,
    0.862 6.5%,
    1.114,
    1.296 10.7%,
    1.346,
    1.37 12.9%,
    1.373,
    1.364 14.5%,
    1.315 16.2%,
    1.032 21.8%,
    0.941 24%,
    0.891 25.9%,
    0.877,
    0.869 27.8%,
    0.877,
    0.895 30.4%,
    1.012 38.3%,
    1.029,
    1.032 42.7%,
    1.024 44.1%,
    0.99 53.3%,
    0.997 55.2%,
    1.003 59.2%,
    1
  );
}
```

**Spring (gentle overshoot):**

```css
.spring {
  animation-timing-function: linear(
    0,
    0.009,
    0.035,
    0.078,
    0.141,
    0.223,
    0.326,
    0.45,
    0.594,
    0.758,
    0.938,
    1.026,
    1.078,
    1.096,
    1.087,
    1.054,
    1.009,
    0.963,
    0.927,
    0.907,
    0.903,
    0.916,
    0.94,
    0.969,
    0.993,
    1.008,
    1.014,
    1.012,
    1.004,
    0.998,
    0.996,
    0.998,
    1
  );
}
```

### Explicit stop positions

You can specify where each point falls on the timeline using percentages:

```css
.custom {
  transition-timing-function: linear(0, 0.5 25%, 1 50%, 0.8 75%, 1);
  /* Quick rise to 0.5 at 25%, peak at 50%, dip to 0.8 at 75%, settle at 1 */
}
```

### Generating `linear()` curves

Rather than hand-writing control points, use these tools:

- **[linear-easing-generator.netlify.app](https://linear-easing-generator.netlify.app)** — paste a JavaScript easing function and get the CSS `linear()` output.
- **[cubic-bezier.com](https://cubic-bezier.com)** — for simple curves that `cubic-bezier()` can handle (no overshoot beyond one bounce).

### When to use `linear()` vs. `cubic-bezier()`

| Easing type        | `cubic-bezier()`      | `linear()`                  |
| ------------------ | --------------------- | --------------------------- |
| Simple ease-in/out | ✅ Simpler, smaller   | Works but unnecessary       |
| Single overshoot   | ✅ Can express this   | Works                       |
| Multi-bounce       | ❌ Cannot express     | ✅ The only CSS option      |
| Elastic / spring   | ❌ Cannot express     | ✅ The only CSS option      |
| Steps              | Use `steps()` instead | Can approximate             |
| Arbitrary curve    | ❌ Limited to cubic   | ✅ Piecewise-linear approx. |

Use `cubic-bezier()` (or the built-in keywords `ease`, `ease-in`, `ease-out`, `ease-in-out`) for simple curves. Reach for `linear()` when you need bounce, spring, elastic, or any multi-phase easing that `cubic-bezier()` cannot represent.

### Composing with individual transforms

Combine `linear()` with individual transform properties (see `animation-individual-transforms`) for complex, multi-axis animations:

```css
.card {
  translate: 0 50px;
  opacity: 0;
  transition:
    translate 0.8s
      linear(
        0,
        0.063,
        0.25,
        0.563,
        1,
        0.891,
        0.813,
        0.766,
        0.75,
        0.766,
        0.813,
        0.891,
        1,
        0.938,
        0.906,
        0.938,
        1
      ),
    opacity 0.4s ease;
}

.card.visible {
  translate: 0;
  opacity: 1;
}
/* Bounce on Y axis, simple fade on opacity — independent timings */
```

🟡 Newly available (~87%). Supported in all modern browsers. For older browsers, the transition falls back to the default `ease` timing — still functional, just without the custom curve. No polyfill needed.

Reference: [modern-css.com](https://modern-css.com) · [MDN — linear()](https://developer.mozilla.org/en-US/docs/Web/CSS/easing-function/linear) · [Linear easing generator](https://linear-easing-generator.netlify.app)
