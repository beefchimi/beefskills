---
title: Multiple Font Weights Without Multiple Files
impact: HIGH
impactDescription: reduces font requests and file count while unlocking continuous weight/width ranges
tags: typography, variable-fonts, font-face, font-weight, performance
browser: 96%
---

## Multiple Font Weights Without Multiple Files

Loading separate font files for each weight (400, 500, 600, 700…) means multiple HTTP requests, more bytes to download, and a combinatorial explosion when you also need italic variants. Variable fonts pack an entire weight range (and often width, slant, and optical size axes) into a single file — fewer requests, smaller total size, and access to any weight value, not just the predefined ones.

**Avoid (separate file per weight):**

```css
@font-face {
  font-family: "MyFont";
  src: url("MyFont-Regular.woff2") format("woff2");
  font-weight: 400;
  font-style: normal;
}

@font-face {
  font-family: "MyFont";
  src: url("MyFont-Medium.woff2") format("woff2");
  font-weight: 500;
  font-style: normal;
}

@font-face {
  font-family: "MyFont";
  src: url("MyFont-SemiBold.woff2") format("woff2");
  font-weight: 600;
  font-style: normal;
}

@font-face {
  font-family: "MyFont";
  src: url("MyFont-Bold.woff2") format("woff2");
  font-weight: 700;
  font-style: normal;
}

/* 4 files, 4 HTTP requests, ~80–120 KB total
   Only these exact weights are available */
```

**Prefer (single variable font file):**

```css
@font-face {
  font-family: "MyFont";
  src: url("MyFont-Variable.woff2") format("woff2");
  font-weight: 100 900;
  font-display: swap;
}
```

One file, one request. The `font-weight: 100 900` range descriptor tells the browser this single file covers every weight from 100 to 900 — including intermediate values like 450 or 550 that static fonts cannot express.

### Using continuous weight values

```css
body {
  font-family: "MyFont", system-ui, sans-serif;
  font-weight: 400;
}

h1 {
  font-weight: 800;
}

h2 {
  font-weight: 650; /* not possible with static fonts */
}

.subtitle {
  font-weight: 350; /* fine-tuned lighter weight */
}

/* Responsive weight — heavier on larger screens for better readability */
h1 {
  font-weight: 700;
}

@media (width >= 1024px) {
  h1 {
    font-weight: 800;
  }
}
```

### Variable font axes

Beyond weight, variable fonts can expose additional axes:

```css
@font-face {
  font-family: "MyVar";
  src: url("MyVar.woff2") format("woff2");
  font-weight: 100 900;
  font-stretch: 75% 125%; /* width axis */
  font-style: oblique 0deg 12deg; /* slant axis */
}

.condensed-bold {
  font-weight: 700;
  font-stretch: 75%;
}

.wide-light {
  font-weight: 300;
  font-stretch: 125%;
}
```

### Custom axes with `font-variation-settings`

Some variable fonts expose custom axes (e.g., optical size, grade) via four-letter tags:

```css
/* Standard axes — prefer the high-level properties */
h1 {
  font-weight: 700; /* 'wght' axis */
  font-stretch: 110%; /* 'wdth' axis */
  font-style: oblique 6deg; /* 'slnt' axis */
  font-optical-sizing: auto; /* 'opsz' axis */
}

/* Custom axes — use font-variation-settings */
.display-text {
  font-variation-settings:
    "GRAD" 88,
    "CASL" 1;
}
```

Prefer the high-level CSS properties (`font-weight`, `font-stretch`, `font-style`) over `font-variation-settings` for standard axes — they compose with other CSS features like `font-weight: bolder` inheritance, while `font-variation-settings` replaces the entire setting map on each declaration.

### Animating font properties

Variable fonts unlock smooth CSS transitions and animations on typographic properties:

```css
.hover-weight {
  font-weight: 400;
  transition: font-weight 200ms ease;
}

.hover-weight:hover {
  font-weight: 700;
}
```

### Performance considerations

- A single variable font file is typically **smaller** than 3+ static weight files combined, but **larger** than any single static weight file.
- If you only use one weight (e.g., body text at 400), a static font file may be smaller.
- If you use 2+ weights, a variable font almost always wins on total transfer size and eliminates the extra HTTP requests.
- Use `unicode-range` subsetting for multilingual sites to load only the character sets needed.

```css
@font-face {
  font-family: "MyFont";
  src: url("MyFont-Latin.woff2") format("woff2");
  font-weight: 100 900;
  unicode-range: U+0000-00FF, U+0131, U+0152-0153; /* Latin subset */
  font-display: swap;
}
```

### Combining with `font-display`

Always pair variable fonts with `font-display: swap` (see `typo-font-display`) to prevent invisible text during loading:

```css
@font-face {
  font-family: "MyFont";
  src: url("MyFont-Variable.woff2") format("woff2");
  font-weight: 100 900;
  font-display: swap;
}
```

✅ Widely available (~96%). Variable fonts are supported in all modern browsers. Most popular font families (Inter, Roboto Flex, Source Sans 3, etc.) ship variable font versions. Use them by default whenever 2+ weights are needed.

Reference: [modern-css.com](https://modern-css.com) · [MDN — Variable fonts](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_fonts/Variable_fonts_guide) · [v-fonts.com](https://v-fonts.com)
