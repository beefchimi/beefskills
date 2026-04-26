---
title: Mixing Colors Without a Preprocessor
impact: HIGH
impactDescription: eliminates Sass/Less dependency for color blending and palette generation
tags: color, color-mix, sass, mix, blending, palette
browser: 89%
---

## Mixing Colors Without a Preprocessor

Blending two colors together — for hover states, tints, shades, or palette generation — has historically required Sass's `mix()` function or manual hex math. The result is a static value baked in at compile time that cannot respond to theming, dark mode, or runtime changes. The native `color-mix()` function blends colors directly in the browser, works with custom properties, and supports perceptually uniform color spaces like `oklch`.

**Avoid (Sass mix — build-time only):**

```scss
// Sass — requires a compiler
$blue: #3b82f6;
$pink: #ec4899;

.blend {
  background: mix($blue, $pink, 60%);
  // Compiles to a static hex value — frozen at build time
}

.tint {
  background: mix($blue, white, 80%);
  // Cannot change at runtime, ignores custom properties
}

.shade {
  background: mix($blue, black, 80%);
}
```

**Prefer (native `color-mix()`):**

```css
.blend {
  background: color-mix(in oklch, #3b82f6 60%, #ec4899);
}

.tint {
  background: color-mix(in oklch, var(--brand) 80%, white);
}

.shade {
  background: color-mix(in oklch, var(--brand) 80%, black);
}
```

No build step, works with custom properties, and responds to runtime theme changes.

### Why the color space matters

The `in <color-space>` parameter controls how colors are interpolated. Different spaces produce different visual results:

```css
/* oklch — perceptually uniform, best for most use cases */
background: color-mix(in oklch, blue, yellow);

/* srgb — legacy color mixing, can produce muddy midpoints */
background: color-mix(in srgb, blue, yellow);

/* oklab — perceptually uniform, Cartesian (no hue interpolation) */
background: color-mix(in oklab, blue, yellow);

/* hsl — hue-based mixing, can produce unexpected intermediate hues */
background: color-mix(in hsl, blue, yellow);
```

**Recommendation:** Use `in oklch` as the default. It produces the most visually pleasing intermediate colors because it accounts for human perception — equal numeric steps produce equal perceived differences.

### Percentage control

The percentage controls how much of each color is in the mix:

```css
/* 75% first color, 25% second */
color-mix(in oklch, #3b82f6 75%, #ec4899)

/* 50/50 — equal blend (default if no percentages given) */
color-mix(in oklch, #3b82f6, #ec4899)

/* 25% first, 75% second */
color-mix(in oklch, #3b82f6 25%, #ec4899)
```

If only one percentage is specified, the other is inferred as the remainder to 100%.

### Generating tints and shades with custom properties

```css
:root {
  --brand: oklch(0.55 0.2 264);
}

.btn {
  background: var(--brand);
}

.btn:hover {
  /* 15% white mixed in — lighter */
  background: color-mix(in oklch, var(--brand) 85%, white);
}

.btn:active {
  /* 20% black mixed in — darker */
  background: color-mix(in oklch, var(--brand) 80%, black);
}

.btn-ghost {
  /* 10% of the brand color — subtle tint */
  background: color-mix(in oklch, var(--brand) 10%, transparent);
  color: var(--brand);
}
```

### Building a full shade palette

```css
:root {
  --blue: oklch(0.55 0.2 264);

  --blue-50: color-mix(in oklch, var(--blue) 5%, white);
  --blue-100: color-mix(in oklch, var(--blue) 15%, white);
  --blue-200: color-mix(in oklch, var(--blue) 30%, white);
  --blue-300: color-mix(in oklch, var(--blue) 50%, white);
  --blue-400: color-mix(in oklch, var(--blue) 75%, white);
  --blue-500: var(--blue);
  --blue-600: color-mix(in oklch, var(--blue) 85%, black);
  --blue-700: color-mix(in oklch, var(--blue) 70%, black);
  --blue-800: color-mix(in oklch, var(--blue) 50%, black);
  --blue-900: color-mix(in oklch, var(--blue) 30%, black);
}
```

Change `--blue` once and the entire palette updates — at runtime, with no build step.

### Transparency mixing

```css
/* Mix with transparent for alpha effects */
.overlay {
  background: color-mix(in oklch, var(--brand) 40%, transparent);
}

/* Equivalent to opacity but composited differently —
   color-mix produces a single color value, not a layered opacity effect */
```

### Comparison with `oklch(from …)` relative color syntax

Both `color-mix()` and relative color syntax (see `color-relative-syntax`) can produce lighter/darker variants. The difference:

| Technique                        | Best for                        | Flexibility        |
| -------------------------------- | ------------------------------- | ------------------ |
| `color-mix(in oklch, color, …)`  | Blending two arbitrary colors   | Two-color mixing   |
| `oklch(from var(--x) calc(…) …)` | Adjusting a single color's axes | Fine-grained edits |

Use `color-mix()` when you're blending two colors or mixing with white/black/transparent. Use relative color syntax when you need precise control over individual color channels (e.g., shifting hue, adjusting chroma independently).

🟡 Newly available (~89%). Supported in all modern browsers. Safe to use in new projects.

Reference: [modern-css.com](https://modern-css.com) · [MDN — color-mix()](https://developer.mozilla.org/en-US/docs/Web/CSS/color_value/color-mix)
