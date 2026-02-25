---
title: Corner Shapes Beyond Rounded Borders
impact: MEDIUM
impactDescription: native squircle and other corner shapes without complex clip paths
tags: layout, corner-shape, squircle, border-radius, clip-path
browser: 67%
---

## Corner Shapes Beyond Rounded Borders

Creating smooth, continuous-curvature corners (squircles — the shape Apple uses on app icons) traditionally required a multi-point `clip-path: polygon()` with 20+ manually calculated coordinates, or an SVG mask. The `corner-shape` property paired with `border-radius` produces these shapes in a single declaration, and the browser handles the math.

**Avoid (complex clip-path polygon):**

```css
.card {
  clip-path: polygon(
    0% 8%,
    0.3% 5.6%,
    1.2% 3.5%,
    2.6% 1.8%,
    4.5% 0.7%,
    7% 0.1%,
    10% 0%,
    90% 0%,
    93% 0.1%,
    95.5% 0.7%,
    97.4% 1.8%,
    98.8% 3.5%,
    99.7% 5.6%,
    100% 8%,
    100% 92%,
    99.7% 94.4%,
    98.8% 96.5%,
    97.4% 98.2%,
    95.5% 99.3%,
    93% 99.9%,
    90% 100%,
    10% 100%,
    7% 99.9%,
    4.5% 99.3%,
    2.6% 98.2%,
    1.2% 96.5%,
    0.3% 94.4%,
    0% 92%
  );
  /* Fragile, not responsive, no box-shadow or border support */
}
```

Or an SVG mask approach:

```css
.card {
  mask-image: url('squircle.svg');
  mask-size: 100% 100%;
  /* Requires an external SVG asset, still no box-shadow */
}
```

**Prefer (modern CSS):**

```css
.card {
  border-radius: 2em;
  corner-shape: squircle;
}
```

The `corner-shape` property modifies how `border-radius` curves are drawn. Instead of a circular arc, `squircle` produces a superellipse — a smooth, continuous curve that avoids the abrupt transition between the flat edge and the rounded corner.

### Available corner shapes

```css
/* Standard circular arcs (default) */
.default {
  border-radius: 1rem;
  corner-shape: round;
}

/* Superellipse / continuous curvature (Apple-style) */
.smooth {
  border-radius: 2rem;
  corner-shape: squircle;
}

/* Angled notch */
.notch {
  border-radius: 1rem;
  corner-shape: notch;
}

/* Beveled / straight cut */
.bevel {
  border-radius: 1rem;
  corner-shape: bevel;
}

/* Scooped inward curve */
.scoop {
  border-radius: 1rem;
  corner-shape: scoop;
}
```

### Advantages over clip-path workarounds

- **Works with `box-shadow` and `border`** — `clip-path` clips both away.
- **Responsive** — scales with the element, no fixed pixel coordinates.
- **Composable** — each corner can have a different radius and they all use the same shape.
- **No external assets** — no SVG masks or image references.

### Progressive enhancement

```css
.card {
  border-radius: 2em; /* circular fallback in all browsers */
  corner-shape: squircle; /* upgraded in supporting browsers */
}
```

Since `corner-shape` degrades gracefully to standard `border-radius` rounding, there is no visual breakage in unsupporting browsers — just a slightly less refined curve.

🟡 Newly available (~67%). Progressive enhancement is safe — older browsers simply render standard rounded corners.

Reference: [modern-css.com](https://modern-css.com) · [CSS Round Display spec — corner-shape](https://drafts.csswg.org/css-borders-4/#corner-shape)
