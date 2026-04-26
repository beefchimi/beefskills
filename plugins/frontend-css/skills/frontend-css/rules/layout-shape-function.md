---
title: Path Shapes Without SVG Clip Paths
impact: MEDIUM
impactDescription: responsive clip paths with percentage values instead of fixed pixels
tags: layout, clip-path, shape, path, responsive, svg
browser: 85%
---

## Path Shapes Without SVG Clip Paths

The `clip-path: path()` function only accepts pixel values, making shapes non-responsive — they break at different sizes and require manual recalculation for every breakpoint. The `shape()` function accepts percentage-based coordinates, making clip paths fluid and responsive by default.

**Avoid (pixel-based path — not responsive):**

```css
.hero {
  clip-path: path('M 0 0 L 800 0 L 800 400 Q 400 500 0 400 Z');
  /* Fixed pixel values — breaks on resize */
}
```

Or relying on an inline SVG `<clipPath>` element:

```html
<svg width="0" height="0">
  <defs>
    <clipPath id="wave" clipPathUnits="objectBoundingBox">
      <path d="M0,0 L1,0 L1,0.8 Q0.5,1.05 0,0.8 Z" />
    </clipPath>
  </defs>
</svg>
```

```css
.hero {
  clip-path: url(#wave);
  /* Requires hidden SVG in the DOM — extra markup, fragile references */
}
```

**Prefer (shape() with percentage-based coordinates):**

```css
.hero {
  clip-path: shape(from 0% 0%, line to 100% 0%, line to 100% 80%, curve to 0% 80% via 50% 105%);
  /* Fully responsive — scales with the element */
}
```

### Shape commands

The `shape()` function uses drawing commands similar to SVG path syntax but with CSS values:

```css
.badge {
  clip-path: shape(
    from 50% 0%,
    line to 100% 35%,
    line to 82% 100%,
    line to 18% 100%,
    line to 0% 35%,
    close
  );
}
```

| Command  | Description                                            |
| -------- | ------------------------------------------------------ |
| `from`   | Starting point of the shape                            |
| `line`   | Straight line to a point                               |
| `curve`  | Cubic or quadratic Bézier curve (`via` control points) |
| `smooth` | Smooth continuation of a previous curve                |
| `arc`    | Elliptical arc to a point                              |
| `close`  | Closes the path back to the starting point             |

### Mixing units

Because `shape()` accepts CSS values, you can mix units and use `calc()`:

```css
.notch {
  clip-path: shape(
    from 0% 0%,
    line to calc(50% - 40px) 0%,
    line to 50% 20px,
    line to calc(50% + 40px) 0%,
    line to 100% 0%,
    line to 100% 100%,
    line to 0% 100%,
    close
  );
}
```

The `shape()` function is the CSS-native answer to responsive clipping. Unlike `path()`, it uses the element's own coordinate system with percentage values, so shapes scale naturally without JavaScript or SVG dependencies.

🟡 Newly available (~85%). Supported in modern Chromium and Firefox. Use behind `@supports (clip-path: shape(from 0% 0%, line to 100% 100%))` with a `polygon()` or `path()` fallback if needed.

Reference: [modern-css.com](https://modern-css.com) · [MDN — shape()](https://developer.mozilla.org/en-US/docs/Web/CSS/basic-shape/shape)
