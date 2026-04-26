---
title: Vivid Colors Beyond sRGB
impact: HIGH
impactDescription: unlocks 50% more color range for displays that support P3 and wider gamuts
tags: color, wide-gamut, oklch, display-p3, srgb, gamut
browser: 90%
---

## Vivid Colors Beyond sRGB

The `rgb()`, `hsl()`, and hex color notations are limited to the sRGB color space — a gamut defined in 1996 that covers only about 35% of visible colors. Modern displays (nearly all phones, tablets, and recent laptops) support the Display P3 gamut, which is ~50% larger than sRGB. Colors specified in sRGB look washed out compared to what the hardware can actually render. Using `oklch()` or `color(display-p3 …)` lets you access the full range of vivid, saturated colors your users' screens can display.

**Avoid (sRGB-only — washed out on modern displays):**

```css
.hero {
  color: rgb(200, 80, 50);
  background: #4f46e5;
}
/* sRGB gamut only — leaving 50%+ of display capability unused */
```

**Prefer (wide-gamut color):**

```css
.hero {
  color: oklch(0.65 0.25 30);
  background: oklch(0.5 0.25 265);
}

/* Or using the display-p3 color space explicitly */
.vivid-accent {
  color: color(display-p3 1 0.2 0.1);
}
```

### Why `oklch()` is the recommended default

`oklch()` is both wide-gamut and perceptually uniform — equal numeric changes in lightness, chroma, or hue produce equal perceived changes. This makes it ideal for building color scales, adjusting shades, and ensuring consistent contrast:

```css
:root {
  /* Same hue and chroma, only lightness changes — even perceived steps */
  --brand-100: oklch(0.95 0.05 264);
  --brand-200: oklch(0.85 0.1 264);
  --brand-300: oklch(0.75 0.15 264);
  --brand-400: oklch(0.65 0.2 264);
  --brand-500: oklch(0.55 0.25 264);
  --brand-600: oklch(0.45 0.22 264);
  --brand-700: oklch(0.35 0.18 264);
}
```

### `oklch()` vs. `color(display-p3 …)`

| Feature                    | `oklch()`                           | `color(display-p3 …)`        |
| -------------------------- | ----------------------------------- | ---------------------------- |
| Gamut                      | Unbounded (any visible color)       | P3 gamut only                |
| Perceptually uniform       | ✅ Yes                              | ❌ No                        |
| Intuitive to author        | ✅ Lightness, chroma, hue           | ❌ Red, green, blue channels |
| Building color scales      | ✅ Excellent                        | ❌ Same issues as `rgb()`    |
| Specifying exact P3 colors | Use `oklch()` and let browser clamp | ✅ Direct P3 channel control |

For most use cases, `oklch()` is the better choice. Use `color(display-p3 …)` when you need to specify an exact P3 color value from a design tool that exports in P3.

### Fallback for older browsers

Browsers that don't understand wide-gamut colors will ignore the declaration and use the previous one. Use the cascade for graceful degradation:

```css
.accent {
  /* sRGB fallback */
  background: #4f46e5;
  /* Wide-gamut override — ignored by browsers that don't support it */
  background: oklch(0.5 0.25 265);
}
```

Or use `@supports` for more complex fallback logic:

```css
.gradient {
  background: linear-gradient(135deg, #e040fb, #536dfe);
}

@supports (color: oklch(0 0 0)) {
  .gradient {
    background: linear-gradient(135deg, oklch(0.7 0.3 320), oklch(0.55 0.25 265));
  }
}
```

### Gamut mapping

When an `oklch()` color exceeds the display's gamut (e.g., specifying a P3 color on an sRGB-only monitor), the browser automatically clamps it to the closest in-gamut color. You don't need to manually provide sRGB alternatives for every color — the browser handles it.

### Common wide-gamut use cases

```css
/* Vivid brand accents that pop on P3 displays */
.cta {
  background: oklch(0.65 0.3 145); /* vibrant green — impossible in sRGB */
}

/* Saturated gradients */
.hero-bg {
  background: linear-gradient(
    135deg,
    oklch(0.6 0.3 330),
    /* hot pink */ oklch(0.5 0.28 265) /* electric blue */
  );
}

/* Rich photography overlays */
.overlay {
  background: oklch(0.2 0.05 250 / 0.8); /* deep blue-tinted overlay with alpha */
}
```

### Alpha channel syntax

Both `oklch()` and `color()` support the `/` alpha syntax:

```css
.glass {
  background: oklch(0.98 0.01 250 / 0.5);
  /* 50% transparent — no separate rgba() call needed */
}

.tinted {
  background: color(display-p3 0.2 0.1 0.4 / 0.75);
}
```

Use `oklch()` as your default color notation for all new CSS. It provides wide-gamut access, perceptual uniformity, and an intuitive authoring model. Reserve `rgb()` / hex for legacy codebases or when a design system explicitly requires sRGB values. See also `color-oklch` for more on building perceptually uniform palettes.

✅ Widely available (~90%). `oklch()` and `color(display-p3 …)` are supported in all modern browsers. Provide a hex or `rgb()` fallback line for the small number of older browsers if needed.

Reference: [modern-css.com](https://modern-css.com) · [MDN — oklch()](https://developer.mozilla.org/en-US/docs/Web/CSS/color_value/oklch) · [MDN — color()](https://developer.mozilla.org/en-US/docs/Web/CSS/color_value/color)
