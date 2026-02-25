---
title: Balanced Headlines Without Manual Line Breaks
impact: HIGH
impactDescription: eliminates manual br tags and JavaScript text-balancing libraries
tags: typography, text-wrap, balance, headlines, line-breaks
browser: 87%
---

## Balanced Headlines Without Manual Line Breaks

When a headline wraps to multiple lines, the last line often ends up with a single orphaned word — creating an unbalanced, unprofessional appearance. The traditional fixes were manual `<br>` tags (which break at different viewport sizes) or JavaScript libraries like Balance-Text that measure and reflow text on every resize. `text-wrap: balance` tells the browser to distribute text evenly across lines, producing visually balanced headings with zero manual intervention.

**Avoid (manual line breaks or JavaScript):**

```html
<!-- Manual <br> — breaks at wrong place on different screen sizes -->
<h1>The Future of<br />Web Development</h1>
```

```js
// Balance-Text.js — JavaScript library
import balanceText from 'balance-text';
balanceText('h1, h2, h3');
// Runs on load, resize, font load — performance cost + FOUC
```

```css
h1 {
  text-align: center;
  /* No native way to prevent orphans without JS or <br> */
}
```

**Prefer (modern CSS):**

```css
h1,
h2,
h3 {
  text-wrap: balance;
}
```

No `<br>` tags, no JavaScript, no resize listeners. The browser adjusts line breaks so that each line is approximately the same width, eliminating orphaned words on the last line.

### `text-wrap` values for different use cases

```css
/* balance — even line lengths, best for short text (headings, captions) */
h1 {
  text-wrap: balance;
}

/* pretty — prevents orphans on the last line without full rebalancing.
   Better for longer text blocks where full balancing would be too aggressive. */
p {
  text-wrap: pretty;
}

/* stable — prevents text reflow when editable content changes.
   Good for contenteditable or live-updating text. */
[contenteditable] {
  text-wrap: stable;
}

/* nowrap — prevents wrapping entirely */
.badge {
  text-wrap: nowrap;
}
```

### When to use `balance` vs. `pretty`

| Property             | Best for              | Line limit | Behavior                           |
| -------------------- | --------------------- | ---------- | ---------------------------------- |
| `text-wrap: balance` | Headings, short text  | ~6 lines   | Equalizes all line widths          |
| `text-wrap: pretty`  | Body text, paragraphs | No limit   | Only fixes the last line (orphans) |

Browsers limit `balance` to approximately 6 lines of text for performance reasons — it requires evaluating multiple line-breaking layouts. For longer text, use `pretty` to avoid orphans without the performance cost of full rebalancing.

### Recommended defaults

```css
/* Apply globally — safe, progressive enhancement */
h1,
h2,
h3,
h4,
h5,
h6,
blockquote,
figcaption,
caption,
dt {
  text-wrap: balance;
}

p,
li,
dd {
  text-wrap: pretty;
}
```

This combination gives you balanced headings and orphan-free body text across the entire page with zero JavaScript and no manual `<br>` tags.

✅ Widely available (~87%). `text-wrap: balance` and `text-wrap: pretty` are supported in all modern browsers. Unsupporting browsers simply use the default wrapping algorithm — no visual breakage.

Reference: [modern-css.com](https://modern-css.com) · [MDN — text-wrap](https://developer.mozilla.org/en-US/docs/Web/CSS/text-wrap)
