---
title: Drop Caps Without Float Hacks
impact: MEDIUM
impactDescription: eliminates fragile float-based drop cap styling with a single declaration
tags: typography, initial-letter, drop-cap, float, first-letter
browser: 91%
---

## Drop Caps Without Float Hacks

Creating a drop cap (a large first letter that spans multiple lines) traditionally required floating the `::first-letter` pseudo-element, manually sizing it, and tweaking `line-height` to align with the surrounding text. The result is fragile — it breaks across fonts, font sizes, and line heights. The `initial-letter` property sizes and sinks the first letter automatically, adapting to the surrounding typography.

**Avoid (float hack for drop caps):**

```css
.article::first-letter {
  float: left;
  font-size: 3.5em;
  line-height: 0.8;
  margin-right: 0.1em;
  margin-top: 0.05em;
  /* Magic numbers — break when font or line-height changes */
}
```

The float approach requires manual tuning of `font-size`, `line-height`, `margin-top`, and `margin-right` to visually align the letter. Every change to the body font, size, or line-height requires re-tuning these values.

**Prefer (modern CSS):**

```css
.article::first-letter {
  initial-letter: 3;
}
```

One declaration. The number specifies how many lines the initial letter should span. The browser automatically sizes the letter and aligns its baseline with the Nth line of text.

### How the value works

```css
/* Span 3 lines — letter is sized to fill 3 lines of text */
.intro::first-letter {
  initial-letter: 3;
}

/* Span 2 lines — smaller drop cap */
.sidebar::first-letter {
  initial-letter: 2;
}

/* Span 4 lines — dramatic editorial style */
.feature::first-letter {
  initial-letter: 4;
}
```

### Raised caps (sink fewer lines than span)

The `initial-letter` property accepts two values: the size (how many lines tall) and the sink (how many lines the letter drops into):

```css
/* Raised cap — 3 lines tall but only sinks 1 line (raised above the text) */
.raised::first-letter {
  initial-letter: 3 1;
}

/* Sunken cap — 3 lines tall and sinks all 3 lines (fully inline with text) */
.sunken::first-letter {
  initial-letter: 3 3;
}

/* Default behavior: initial-letter: 3 is equivalent to initial-letter: 3 3 */
```

### Styling the drop cap

`initial-letter` controls sizing and alignment. You can combine it with other styles for visual flair:

```css
.article::first-letter {
  initial-letter: 3;
  color: oklch(0.55 0.2 250);
  font-family: 'Georgia', serif;
  font-weight: 700;
  margin-inline-end: 0.15em;
}
```

### Combining with custom fonts

Unlike the float hack, `initial-letter` adapts to any font's metrics automatically — no magic numbers to adjust per typeface:

```css
/* Works correctly regardless of which font loads */
.prose::first-letter {
  initial-letter: 3;
  font-family: var(--heading-font, serif);
}
```

### Prefixed version for broader support

```css
.article::first-letter {
  -webkit-initial-letter: 3;
  initial-letter: 3;
}
```

✅ Widely available (~91%). Supported in Chromium and Safari (with `-webkit-` prefix) and Firefox. The prefixed `-webkit-initial-letter` covers older Safari versions. Falls back gracefully — without support, the first letter renders at normal size.

Reference: [modern-css.com](https://modern-css.com) · [MDN — initial-letter](https://developer.mozilla.org/en-US/docs/Web/CSS/initial-letter)
