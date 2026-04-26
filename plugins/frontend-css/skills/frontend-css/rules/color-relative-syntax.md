---
title: Color Variants Without Sass Functions
impact: HIGH
impactDescription: eliminates Sass lighten/darken/adjust-hue dependencies with native runtime color manipulation
tags: color, relative-color-syntax, oklch, lighten, darken, sass
browser: 87%
---

## Color Variants Without Sass Functions

Generating lighter, darker, or hue-shifted variants of a color traditionally required Sass functions like `lighten()`, `darken()`, `adjust-hue()`, and `mix()`. These compile to static hex values — they cannot reference CSS custom properties, cannot respond to theming changes at runtime, and lock your codebase into a preprocessor. The relative color syntax lets you derive new colors from any base color directly in CSS, using `from` to decompose the origin color and `calc()` to adjust its components.

**Avoid (Sass color functions — static, build-time only):**

```scss
// Sass — requires a compiler, produces frozen hex values
$brand: #4f46e5;

.btn {
  background: $brand;
}
.btn:hover {
  background: lighten($brand, 15%); // compiles to #8b83f0 — frozen
}
.btn:active {
  background: darken($brand, 10%); // compiles to #3730a3 — frozen
}
.badge {
  background: adjust-hue($brand, 30deg); // compiles to #464fe5 — frozen
}

// Cannot reference CSS custom properties:
// lighten(var(--brand), 15%) — ERROR
```

**Prefer (relative color syntax — live, runtime, composable):**

```css
:root {
  --brand: oklch(0.55 0.2 264);
}

.btn {
  background: var(--brand);
}

.btn:hover {
  /* Lighten: increase L (lightness) */
  background: oklch(from var(--brand) calc(l + 0.15) c h);
}

.btn:active {
  /* Darken: decrease L */
  background: oklch(from var(--brand) calc(l - 0.1) c h);
}

.badge {
  /* Shift hue by 30 degrees */
  background: oklch(from var(--brand) l c calc(h + 30));
}
```

The `from` keyword decomposes the origin color into its components (`l`, `c`, `h` in oklch), which you can then adjust with `calc()`. Because it references `var(--brand)`, changing the custom property at runtime updates every derived color automatically.

### Syntax breakdown

```
oklch(from <origin> <L> <C> <H>)
```

- `from <origin>` — the base color to derive from (any valid color, including `var()`).
- `l`, `c`, `h` — channel keywords that resolve to the origin color's component values.
- Use `calc()` to modify any channel, or pass it through unchanged.

### Common transformations

```css
:root {
  --color: oklch(0.6 0.2 250);
}

/* Lighten */
.light {
  color: oklch(from var(--color) calc(l + 0.2) c h);
}

/* Darken */
.dark {
  color: oklch(from var(--color) calc(l - 0.2) c h);
}

/* Desaturate (reduce chroma) */
.muted {
  color: oklch(from var(--color) l calc(c - 0.1) h);
}

/* Saturate (increase chroma) */
.vivid {
  color: oklch(from var(--color) l calc(c + 0.1) h);
}

/* Complement (opposite hue) */
.complement {
  color: oklch(from var(--color) l c calc(h + 180));
}

/* Semi-transparent variant */
.ghost {
  color: oklch(from var(--color) l c h / 0.5);
}

/* Adjust multiple channels at once */
.soft {
  color: oklch(from var(--color) calc(l + 0.15) calc(c * 0.6) h);
}
```

### Building a full palette from one token

```css
:root {
  --brand: oklch(0.55 0.22 264);

  --brand-50: oklch(from var(--brand) 0.97 calc(c * 0.15) h);
  --brand-100: oklch(from var(--brand) 0.93 calc(c * 0.3) h);
  --brand-200: oklch(from var(--brand) 0.87 calc(c * 0.5) h);
  --brand-300: oklch(from var(--brand) 0.78 calc(c * 0.7) h);
  --brand-400: oklch(from var(--brand) 0.68 calc(c * 0.85) h);
  --brand-500: oklch(from var(--brand) l c h);
  --brand-600: oklch(from var(--brand) calc(l - 0.08) c h);
  --brand-700: oklch(from var(--brand) calc(l - 0.15) c h);
  --brand-800: oklch(from var(--brand) calc(l - 0.22) c h);
  --brand-900: oklch(from var(--brand) calc(l - 0.28) calc(c * 0.8) h);
}
```

Change `--brand` to any color, and the entire palette regenerates at runtime — ideal for user-configurable themes, white-label products, or dark mode transitions.

### Works with any color space

The relative color syntax is not limited to `oklch`. You can use it with `hsl`, `rgb`, `lab`, `lch`, or any other supported color function:

```css
/* HSL-based relative color */
.light {
  color: hsl(from var(--color) h s calc(l + 20%));
}

/* RGB-based — useful for alpha adjustments */
.overlay {
  background: rgb(from var(--color) r g b / 0.3);
}
```

However, `oklch` is strongly recommended for lightness and saturation adjustments because its perceptual uniformity ensures that `+0.1` lightness produces the same visual change regardless of the starting hue. HSL and RGB do not have this property — see `color-oklch` for details.

### Replacing common Sass patterns

| Sass function           | Relative color syntax equivalent                |
| ----------------------- | ----------------------------------------------- |
| `lighten($c, 20%)`      | `oklch(from $c calc(l + 0.2) c h)`              |
| `darken($c, 10%)`       | `oklch(from $c calc(l - 0.1) c h)`              |
| `saturate($c, 20%)`     | `oklch(from $c l calc(c + 0.05) h)`             |
| `desaturate($c, 20%)`   | `oklch(from $c l calc(c - 0.05) h)`             |
| `adjust-hue($c, 30deg)` | `oklch(from $c l c calc(h + 30))`               |
| `rgba($c, 0.5)`         | `oklch(from $c l c h / 0.5)`                    |
| `complement($c)`        | `oklch(from $c l c calc(h + 180))`              |
| `mix($a, $b, 50%)`      | `color-mix(in oklch, $a, $b)` (see `color-mix`) |

🟡 Newly available (~87%). Supported in all modern browsers. For older browser fallback, provide a static color value before the relative color declaration:

```css
.btn:hover {
  background: #7c6ef0; /* static fallback */
  background: oklch(from var(--brand) calc(l + 0.15) c h);
}
```

Reference: [modern-css.com](https://modern-css.com) · [MDN — Relative color syntax](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_colors/Relative_colors)
