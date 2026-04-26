---
title: Vertical Text Centering Without Padding Hacks
impact: HIGH
impactDescription: eliminates manual padding tweaks for optically centered text in buttons and badges
tags: typography, text-box, trim, leading, optical-centering, buttons
browser: 79%
---

## Vertical Text Centering Without Padding Hacks

Text inside buttons, badges, and pills often looks vertically off-center even with equal `padding-top` and `padding-bottom`. This is because fonts include built-in leading (extra space above ascenders and below descenders) that shifts the visual center. The traditional fix is manually tweaking `padding-top` to be 1–2px less than `padding-bottom` — a fragile hack that breaks when the font, font-size, or line-height changes. The `text-box` property trims this intrinsic leading, producing true optical centering with symmetric padding.

**Avoid (manual padding tweaks):**

```css
.btn {
  padding: 10px 20px;
  /* Looks off-center — text sits slightly low */
  padding-top: 8px; /* hack: trim top to "look" centered */
  /* Breaks when font-family or font-size changes */
}

.badge {
  padding: 2px 8px;
  padding-top: 1px; /* another font-specific tweak */
}
```

Every font has different metrics, so these magic-number adjustments must be re-tuned for each typeface, weight, and size combination.

**Prefer (modern CSS):**

```css
h1,
button,
.badge,
.pill {
  text-box: trim-both cap alphabetic;
}
```

The browser trims the extra leading above the cap height and below the alphabetic baseline, leaving only the visible ink bounds. Symmetric `padding` now produces truly centered text — no manual tweaks, no font-specific hacks.

### How `text-box` works

`text-box` is a shorthand for `text-box-trim` and `text-box-edge`:

```css
/* Shorthand */
.btn {
  text-box: trim-both cap alphabetic;
}

/* Longhand equivalent */
.btn {
  text-box-trim: trim-both;
  text-box-edge: cap alphabetic;
}
```

### `text-box-trim` values

| Value        | Trims                    |
| ------------ | ------------------------ |
| `none`       | No trimming (default)    |
| `trim-start` | Trims leading above text |
| `trim-end`   | Trims leading below text |
| `trim-both`  | Trims above and below    |

### `text-box-edge` values

The edge values define the reference lines for trimming:

| Over edge | Under edge   | Description                                    |
| --------- | ------------ | ---------------------------------------------- |
| `cap`     | `alphabetic` | Most common — cap height to baseline           |
| `ex`      | `alphabetic` | x-height to baseline (for lowercase-only text) |
| `text`    | `text`       | Ascender to descender (preserves g/y/p tails)  |
| `auto`    | `auto`       | Browser chooses based on the dominant script   |

### Common patterns

```css
/* Buttons — optically centered text */
button {
  text-box: trim-both cap alphabetic;
  padding: 0.75rem 1.5rem;
  /* padding is now truly symmetric visually */
}

/* Badges and pills */
.badge {
  text-box: trim-both cap alphabetic;
  padding: 0.125rem 0.5rem;
  border-radius: 999px;
  font-size: 0.75rem;
}

/* Headlines flush against adjacent content */
h1 {
  text-box: trim-both cap alphabetic;
  /* No extra whitespace above the headline */
}

/* First and last elements in a card */
.card > :first-child {
  text-box: trim-start cap alphabetic;
}
.card > :last-child {
  text-box: trim-end cap alphabetic;
}
```

### Multi-line text

For multi-line text blocks, `trim-both` only trims the first line's top and the last line's bottom — intermediate lines retain their normal line-height spacing:

```css
.article-lead {
  text-box: trim-both cap alphabetic;
  line-height: 1.6;
  /* Line-height between lines is preserved; only the outer leading is trimmed */
}
```

### Why `cap alphabetic` is the most common choice

- `cap` trims to the capital letter height — aligns with the tops of H, T, B, etc.
- `alphabetic` trims to the baseline — aligns with the bottoms of a, e, o, etc. (descenders like g, y, p extend below).

This combination produces the tightest optical centering for UI elements like buttons and badges where the text is typically uppercase or single-line.

🟡 Newly available (~79%). Supported in Chromium and Safari. Falls back gracefully — in unsupporting browsers, text renders with its default leading, and the padding tweak is unnecessary if you accept slight visual asymmetry.

Reference: [modern-css.com](https://modern-css.com) · [MDN — text-box](https://developer.mozilla.org/en-US/docs/Web/CSS/text-box)
