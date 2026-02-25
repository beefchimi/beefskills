---
title: Responsive Clip Paths Without SVG
impact: MEDIUM
impactDescription: percentage-based clip paths that scale with the element instead of fixed pixel values
tags: animation, clip-path, shape, path, responsive, svg
browser: 96%
---

## Responsive Clip Paths Without SVG

The `clip-path: path()` function only accepts pixel-based SVG path data — coordinates are fixed, making shapes non-responsive. They break at different element sizes and require recalculation for every breakpoint. The `shape()` function uses CSS values including percentages, `calc()`, and viewport units, producing clip paths that scale fluidly with the element.

**Avoid (pixel-based path — not responsive):**

```css
.shape {
  clip-path: path('M0 200 L100 0 L200 200 Z');
  /* Fixed pixel values — breaks when element is resized */
}
```

Or relying on an SVG `<clipPath>` element in the DOM:

```html
<svg width="0" height="0">
  <defs>
    <clipPath id="triangle" clipPathUnits="objectBoundingBox">
      <path d="M0,1 L0.5,0 L1,1 Z" />
    </clipPath>
  </defs>
</svg>
```

```css
.shape {
  clip-path: url(#triangle);
  /* Requires hidden SVG in the markup — extra DOM nodes, fragile ID references */
}
```

**Prefer (shape() with percentage-based coordinates):**

```css
.shape {
  clip-path: shape(from 0% 100%, line to 50% 0%, line to 100% 100%, close);
  /* Fully responsive — scales with the element */
}
```

### Drawing commands

The `shape()` function uses drawing commands similar to SVG path syntax but with CSS values:

```css
.wave-bottom {
  clip-path: shape(
    from 0% 0%,
    line to 100% 0%,
    line to 100% 80%,
    curve to 0% 80% via 50% 105%,
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

### Mixing units with calc()

Because `shape()` accepts any CSS value, you can mix units and use `calc()` for precise hybrid layouts:

```css
.notch {
  clip-path: shape(
    from 0% 0%,
    line to calc(50% - 30px) 0%,
    line to 50% 20px,
    line to calc(50% + 30px) 0%,
    line to 100% 0%,
    line to 100% 100%,
    line to 0% 100%,
    close
  );
}
```

### Animating clip paths

`shape()` clip paths can be transitioned and animated when the number and type of commands match between keyframes:

```css
.morph {
  clip-path: shape(from 0% 0%, line to 100% 0%, line to 100% 100%, line to 0% 100%, close);
  transition: clip-path 0.4s ease;
}

.morph:hover {
  clip-path: shape(from 10% 0%, line to 90% 0%, line to 100% 100%, line to 0% 100%, close);
}
```

### Common shape patterns

```css
/* Diagonal section divider */
.diagonal {
  clip-path: shape(from 0% 0%, line to 100% 0%, line to 100% 85%, line to 0% 100%, close);
}

/* Curved bottom edge */
.curved {
  clip-path: shape(
    from 0% 0%,
    line to 100% 0%,
    line to 100% 85%,
    curve to 0% 85% via 50% 110%,
    close
  );
}

/* Arrow / chevron */
.arrow {
  clip-path: shape(
    from 0% 0%,
    line to 75% 0%,
    line to 100% 50%,
    line to 75% 100%,
    line to 0% 100%,
    line to 25% 50%,
    close
  );
}

/* Pentagon */
.pentagon {
  clip-path: shape(
    from 50% 0%,
    line to 100% 38%,
    line to 82% 100%,
    line to 18% 100%,
    line to 0% 38%,
    close
  );
}
```

### When to use `shape()` vs. `polygon()`

| Feature              | `polygon()`          | `shape()`              |
| -------------------- | -------------------- | ---------------------- |
| Straight lines       | ✅ Yes               | ✅ Yes                 |
| Curves (Bézier, arc) | ❌ No                | ✅ Yes                 |
| Mixed units / calc() | ✅ Yes               | ✅ Yes                 |
| Animatable           | ✅ (matching points) | ✅ (matching commands) |
| Browser support      | ✅ Widely available  | ✅ Widely available    |

Use `polygon()` for simple straight-edged shapes (triangles, hexagons, diagonal cuts). Use `shape()` when you need curves, arcs, or complex paths that would otherwise require SVG.

✅ Widely available (~96%). Supported in all modern browsers. `shape()` is the CSS-native answer to responsive clipping — it replaces both `path()` for complex shapes and SVG `<clipPath>` elements with a single, responsive, animatable CSS function.

Reference: [modern-css.com](https://modern-css.com) · [MDN — shape()](https://developer.mozilla.org/en-US/docs/Web/CSS/basic-shape/shape)
