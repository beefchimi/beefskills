---
title: Independent Transforms Without the Shorthand
impact: HIGH
impactDescription: eliminates rewriting the full transform shorthand when animating a single axis
tags: animation, transforms, translate, rotate, scale, individual
browser: 92%
---

## Independent Transforms Without the Shorthand

When multiple transforms are applied to an element via the `transform` shorthand, changing any single transform requires rewriting the entire value — including the parts that didn't change. This makes animations verbose, error-prone, and impossible to compose independently (e.g., animating rotation on hover while translate runs on a separate keyframe timeline). The individual `translate`, `rotate`, and `scale` properties each operate independently, so you can animate one without touching the others.

**Avoid (transform shorthand — change one, rewrite all):**

```css
.icon {
  transform: translateX(10px) rotate(45deg) scale(1.2);
}

/* Want to animate only the rotation? Must rewrite everything: */
.icon:hover {
  transform: translateX(10px) rotate(90deg) scale(1.2);
  transition: transform 0.3s ease;
  /* translateX and scale are repeated just to keep them from resetting */
}

/* Separate keyframe animations on different axes? Impossible —
   the last transform declaration wins, overwriting everything. */
```

**Prefer (individual transform properties):**

```css
.icon {
  translate: 10px 0;
  rotate: 45deg;
  scale: 1.2;
}

/* Animate only the rotation — others are untouched */
.icon:hover {
  rotate: 90deg;
  transition: rotate 0.3s ease;
}
```

Each property is independent — changing `rotate` does not affect `translate` or `scale`. No rewriting, no accidental resets.

### Composing independent animations

Individual transform properties unlock the ability to run separate animations on different axes simultaneously:

```css
.floating-icon {
  animation:
    bob 2s ease-in-out infinite alternate,
    spin 4s linear infinite;
}

@keyframes bob {
  from {
    translate: 0 0;
  }
  to {
    translate: 0 -10px;
  }
}

@keyframes spin {
  to {
    rotate: 360deg;
  }
}
/* Both animations compose — impossible with the transform shorthand */
```

With the `transform` shorthand, only one `@keyframes` can animate `transform` at a time — the second would overwrite the first.

### Property syntax

```css
/* translate — accepts 1–3 values (x, y, z) */
.moved {
  translate: 20px; /* translateX(20px) */
  translate: 20px 10px; /* translateX(20px) translateY(10px) */
  translate: 20px 10px 5px; /* + translateZ(5px) */
}

/* rotate — accepts an angle, optionally with an axis */
.turned {
  rotate: 45deg; /* rotateZ(45deg) */
  rotate: x 45deg; /* rotateX(45deg) */
  rotate: y 45deg; /* rotateY(45deg) */
  rotate: 1 1 0 45deg; /* rotate3d(1, 1, 0, 45deg) */
}

/* scale — accepts 1–3 values (x, y, z) */
.sized {
  scale: 1.2; /* uniform scale */
  scale: 1.2 0.8; /* scaleX(1.2) scaleY(0.8) */
  scale: 1.2 0.8 1; /* + scaleZ(1) */
}
```

### Application order

Individual transform properties are always applied in this fixed order, regardless of declaration order in CSS:

1. `translate`
2. `rotate`
3. `scale`

Then `transform` (if also present) is applied after all three.

```css
/* These produce the same result regardless of source order */
.a {
  translate: 10px;
  rotate: 45deg;
  scale: 1.5;
}

.b {
  scale: 1.5;
  translate: 10px;
  rotate: 45deg;
}
/* Both apply as: translate → rotate → scale */
```

This fixed order means you cannot replicate every `transform` shorthand combination — `transform: rotate(45deg) translateX(100px)` (rotate first, then translate along the rotated axis) produces a different result than `translate: 100px; rotate: 45deg` (translate first, then rotate). For those cases, continue using the `transform` shorthand.

### Combining with the `transform` shorthand

Individual properties and the `transform` shorthand coexist. Individual properties apply first (in their fixed order), then `transform` applies on top:

```css
.card {
  translate: 0 -10px;
  transform: perspective(800px) rotateY(5deg);
  /* translate applies, then perspective + rotateY */
}
```

### When to use which

| Scenario                                           | Use                   |
| -------------------------------------------------- | --------------------- |
| Animate one axis independently                     | Individual properties |
| Compose multiple animations on different axes      | Individual properties |
| Hover/focus effects that change a single transform | Individual properties |
| Complex transform chains where order matters       | `transform` shorthand |
| 3D transforms with `perspective()`                 | `transform` shorthand |

### Transition examples

```css
/* Button hover — only scale, without rewriting translate/rotate */
.btn {
  scale: 1;
  transition: scale 0.15s ease;
}
.btn:hover {
  scale: 1.05;
}
.btn:active {
  scale: 0.98;
}

/* Card tilt on hover — independent rotation transition */
.card {
  rotate: 0deg;
  transition: rotate 0.3s ease;
}
.card:hover {
  rotate: -2deg;
}
```

✅ Widely available (~92%). Supported in all major browsers. Prefer individual properties over the `transform` shorthand for any single-axis animation or when composing multiple independent animations.

Reference: [modern-css.com](https://modern-css.com) · [MDN — translate](https://developer.mozilla.org/en-US/docs/Web/CSS/translate) · [MDN — rotate](https://developer.mozilla.org/en-US/docs/Web/CSS/rotate) · [MDN — scale](https://developer.mozilla.org/en-US/docs/Web/CSS/scale)
