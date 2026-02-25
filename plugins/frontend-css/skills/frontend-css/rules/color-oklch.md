---
title: Perceptually Uniform Colors With oklch
impact: HIGH
impactDescription: eliminates hand-picked hex shades with a predictable, perceptually uniform color model
tags: color, oklch, perceptual, color-space, palette, hsl
browser: 90%
---

## Perceptually Uniform Colors With oklch

Building a color palette in hex or HSL requires manually picking each shade because perceived lightness is inconsistent — `hsl(60, 100%, 50%)` (yellow) looks far brighter than `hsl(240, 100%, 50%)` (blue) despite the same `L` value. `oklch()` uses a perceptually uniform lightness channel, so changing only `L` produces shades that genuinely look evenly spaced. Building entire palettes becomes a formula instead of guesswork.

**Avoid (hand-picked hex/HSL shades):**

```css
:root {
  --brand-50: #eef2ff;
  --brand-100: #e0e7ff;
  --brand-200: #c7d2fe;
  --brand-300: #a5b4fc;
  --brand-400: #818cf8;
  --brand-500: #6366f1;
  --brand-600: #4f46e5;
  --brand-700: #4338ca;
  --brand-800: #3730a3;
  --brand-900: #312e81;
  /* Each value hand-picked or generated externally — no relationship between them */
}
```

Or HSL with inconsistent perceived lightness:

```css
:root {
  --brand: hsl(239, 84%, 67%);
  --brand-light: hsl(239, 84%, 80%);
  --brand-dark: hsl(239, 84%, 40%);
  /* Lightness steps look uneven — HSL lightness ≠ perceived lightness */
}
```

**Prefer (oklch — perceptually uniform):**

```css
:root {
  --brand: oklch(0.55 0.2 264);
  --brand-light: oklch(0.75 0.2 264);
  --brand-dark: oklch(0.35 0.2 264);
  /* Only L changes — hue and chroma stay constant.
     Each step looks evenly lighter/darker to the human eye. */
}
```

### How oklch channels work

```
oklch(L C H)
       │ │ │
       │ │ └─ Hue: 0–360 (color wheel angle, like HSL)
       │ └─── Chroma: 0–0.4 (color intensity / saturation)
       └───── Lightness: 0–1 (perceptually uniform — the key advantage)
```

- **L (Lightness)**: `0` = black, `1` = white. Unlike HSL, equal numeric steps produce equal perceived brightness steps.
- **C (Chroma)**: `0` = gray, higher = more vivid. Maximum varies by hue. Unlike HSL saturation, chroma is absolute — `0.2` looks equally vivid across all hues.
- **H (Hue)**: `0`–`360` degree angle on the color wheel.

### Building a full palette with a formula

Because lightness is perceptually uniform, you can generate an entire shade scale by stepping `L` in equal increments:

```css
:root {
  --hue: 264;
  --chroma: 0.18;

  --color-50: oklch(0.97 calc(var(--chroma) * 0.3) var(--hue));
  --color-100: oklch(0.93 calc(var(--chroma) * 0.5) var(--hue));
  --color-200: oklch(0.87 calc(var(--chroma) * 0.7) var(--hue));
  --color-300: oklch(0.78 calc(var(--chroma) * 0.85) var(--hue));
  --color-400: oklch(0.68 var(--chroma) var(--hue));
  --color-500: oklch(0.55 var(--chroma) var(--hue));
  --color-600: oklch(0.48 var(--chroma) var(--hue));
  --color-700: oklch(0.4 var(--chroma) var(--hue));
  --color-800: oklch(0.32 calc(var(--chroma) * 0.9) var(--hue));
  --color-900: oklch(0.25 calc(var(--chroma) * 0.8) var(--hue));
  --color-950: oklch(0.18 calc(var(--chroma) * 0.7) var(--hue));
}
```

To create a second color (e.g., a success green), change only `--hue` — the lightness scale works identically because oklch is perceptually uniform.

### oklch vs. HSL comparison

| Feature                  | HSL                    | oklch                    |
| ------------------------ | ---------------------- | ------------------------ |
| Perceptually uniform     | ❌ No                  | ✅ Yes                   |
| Equal L steps look even  | ❌ No                  | ✅ Yes                   |
| Chroma consistent by hue | ❌ No (S is relative)  | ✅ Yes (C is absolute)   |
| Wide-gamut support       | ❌ sRGB only           | ✅ Display P3 and beyond |
| Palette from a formula   | ❌ Needs manual tuning | ✅ Step L evenly         |

### Alpha transparency

```css
.overlay {
  background: oklch(0.2 0.05 250 / 0.8);
  /* 80% opacity — slash-separated alpha like other modern color functions */
}
```

### When to use oklch vs. other formats

- **oklch** — palette generation, design tokens, any context where you manipulate lightness, chroma, or hue independently. Default choice for new CSS.
- **hex / rgb** — legacy code, one-off colors that don't need manipulation, or when matching exact brand hex values from a design system.
- **hsl** — avoid for new code; oklch does everything HSL does but with perceptual uniformity.
- **color(display-p3 …)** — when you need explicit P3 gamut targeting (see `color-wide-gamut`). oklch naturally reaches into P3 when chroma is high enough.

### Accessibility pairing with oklch

Because lightness is perceptually accurate, you can reliably check contrast by comparing `L` values:

```css
/* L difference of ~0.4+ generally meets WCAG AA for normal text */
--bg: oklch(0.97 0.02 264); /* L = 0.97 */
--text: oklch(0.3 0.05 264); /* L = 0.30, difference ≈ 0.67 ✅ */
```

This is not a substitute for proper contrast ratio calculation, but it gives a reliable quick sanity check that HSL cannot provide.

✅ Widely available (~90%). Supported in all modern browsers. Use as the default color format for new CSS. Falls back gracefully — provide a hex/rgb fallback line if you must support very old browsers.

Reference: [modern-css.com](https://modern-css.com) · [oklch.com color picker](https://oklch.com) · [MDN — oklch()](https://developer.mozilla.org/en-US/docs/Web/CSS/color_value/oklch)
