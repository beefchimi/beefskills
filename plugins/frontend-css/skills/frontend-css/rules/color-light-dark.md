---
title: Dark Mode Colors Without Duplicating Values
impact: HIGH
impactDescription: eliminates duplicated color declarations across prefers-color-scheme media queries
tags: color, light-dark, dark-mode, prefers-color-scheme, theming
browser: 83%
---

## Dark Mode Colors Without Duplicating Values

Implementing dark mode with `prefers-color-scheme` media queries requires duplicating every color declaration — once in the default block and once inside the `@media` block. As the design system grows, these paired declarations drift out of sync, and every new color token means editing two places. The `light-dark()` function accepts both values inline, keeping the light and dark variants together in a single declaration.

**Avoid (duplicated values in media query):**

```css
:root {
  --text: #111;
  --surface: #fff;
  --border: #ddd;
  --muted: #666;
}

@media (prefers-color-scheme: dark) {
  :root {
    --text: #eee;
    --surface: #1a1a1a;
    --border: #333;
    --muted: #999;
  }
}
/* Every new token requires editing both blocks — easy to forget one */
```

For component-level colors, it gets worse:

```css
.card {
  background: #fff;
  color: #111;
  border: 1px solid #ddd;
}

@media (prefers-color-scheme: dark) {
  .card {
    background: #1e1e1e;
    color: #eee;
    border-color: #444;
  }
}
/* Multiply by every component — hundreds of duplicated lines */
```

**Prefer (`light-dark()` inline):**

```css
:root {
  color-scheme: light dark; /* Required — tells the browser both schemes are supported */

  --text: light-dark(#111, #eee);
  --surface: light-dark(#fff, #1a1a1a);
  --border: light-dark(#ddd, #333);
  --muted: light-dark(#666, #999);
}

.card {
  background: light-dark(#fff, #1e1e1e);
  color: light-dark(#111, #eee);
  border: 1px solid light-dark(#ddd, #444);
}
/* Light and dark values live side by side — impossible to forget one */
```

### How it works

```
light-dark(light-value, dark-value)
```

- The first argument is used when the computed `color-scheme` is `light`.
- The second argument is used when it is `dark`.
- The `color-scheme` property **must** be set on the element or an ancestor — without it, `light-dark()` always resolves to the light value.

### Prerequisite: `color-scheme`

`light-dark()` reads from the element's resolved `color-scheme`, not from `prefers-color-scheme` directly. You must declare `color-scheme` for it to respond to the user's OS preference:

```css
:root {
  color-scheme: light dark;
}
/* Now light-dark() switches based on OS preference */
```

See `workflow-color-scheme` for details on the `color-scheme` property.

### Per-element overrides

Because `light-dark()` follows `color-scheme`, you can force sections of the page to a specific scheme:

```css
:root {
  color-scheme: light dark;
}

/* This footer is always dark, regardless of OS preference */
.footer {
  color-scheme: dark;
  background: light-dark(#fff, #111); /* resolves to #111 */
  color: light-dark(#111, #eee); /* resolves to #eee */
}

/* This form is always light */
.print-form {
  color-scheme: light;
  background: light-dark(#fff, #111); /* resolves to #fff */
}
```

### Combining with oklch for perceptually uniform theming

```css
:root {
  color-scheme: light dark;

  --brand: light-dark(oklch(0.55 0.2 264), oklch(0.75 0.15 264));
  --surface: light-dark(oklch(0.99 0.005 264), oklch(0.15 0.01 264));
  --text: light-dark(oklch(0.2 0.02 264), oklch(0.9 0.02 264));
}
```

### Using with custom properties for a complete design token system

```css
:root {
  color-scheme: light dark;

  /* Semantic tokens */
  --color-text-primary: light-dark(#111, #eee);
  --color-text-secondary: light-dark(#555, #aaa);
  --color-text-muted: light-dark(#888, #777);

  --color-bg-page: light-dark(#fff, #0f0f0f);
  --color-bg-card: light-dark(#fff, #1a1a1a);
  --color-bg-elevated: light-dark(#f5f5f5, #252525);

  --color-border-default: light-dark(#ddd, #333);
  --color-border-strong: light-dark(#aaa, #555);

  --color-accent: light-dark(oklch(0.55 0.22 264), oklch(0.72 0.18 264));
}
```

### When to still use `@media (prefers-color-scheme)`

`light-dark()` works for color values. For non-color changes between themes (e.g., swapping an image `src`, changing `font-weight`, or adjusting `opacity`), you still need the media query:

```css
/* Non-color theme changes still need @media */
@media (prefers-color-scheme: dark) {
  .logo {
    filter: brightness(1.2);
  }
  .hero-image {
    content: url('hero-dark.webp');
  }
}
```

`light-dark()` is a color function — it only works where a `<color>` value is expected. For everything else, use `prefers-color-scheme` media queries or container style queries.

🟡 Newly available (~83%). Supported in all modern browsers. Falls back gracefully — wrap in `@supports (color: light-dark(#000, #fff))` if you need to provide a separate fallback path.

Reference: [modern-css.com](https://modern-css.com) · [MDN — light-dark()](https://developer.mozilla.org/en-US/docs/Web/CSS/color_value/light-dark)
