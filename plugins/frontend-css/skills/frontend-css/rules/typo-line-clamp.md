---
title: Multiline Text Truncation Without JavaScript
impact: HIGH
impactDescription: eliminates JavaScript character slicing and DOM measurement for text truncation
tags: typography, line-clamp, truncation, overflow, text
browser: 96%
---

## Multiline Text Truncation Without JavaScript

Truncating text to a specific number of lines traditionally required JavaScript that measures rendered height, slices text by character or word count, and appends an ellipsis — breaking on resize, font changes, and dynamic content. The `line-clamp` property (and its widely supported `-webkit-line-clamp` predecessor) handles this entirely in CSS with automatic ellipsis and responsive reflow.

**Avoid (JavaScript text truncation):**

```js
// Measure and truncate by character count — fragile
function truncate(el, maxLines) {
  const lineHeight = parseFloat(getComputedStyle(el).lineHeight);
  const maxHeight = lineHeight * maxLines;

  while (el.scrollHeight > maxHeight && el.textContent.length > 0) {
    el.textContent = el.textContent.slice(0, -1);
  }
  el.textContent = el.textContent.trim() + '…';
}

// Must re-run on resize, font load, and content changes
window.addEventListener('resize', () => truncate(el, 3));
```

Or server-side truncation by character count:

```js
// Cuts mid-word, doesn't account for font metrics or container width
const preview = text.slice(0, 120) + '…';
```

**Prefer (CSS line clamping):**

```css
.card-title {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
```

The browser handles ellipsis placement, reflows on resize, and works with any font, language, or container width — no JavaScript, no character counting, no resize observers.

### Why both `-webkit-` and unprefixed

The `-webkit-line-clamp` property has been supported across all browsers for years (including Firefox) via compatibility aliasing. The unprefixed `line-clamp` is the standardized version. Include both for maximum compatibility:

```css
.excerpt {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
```

### Common patterns

```css
/* Card description — 3 lines */
.card-description {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Single-line truncation — simpler, no line-clamp needed */
.card-title {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* Responsive line count with container queries */
.card-wrapper {
  container-type: inline-size;
}

.card-description {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

@container (width >= 400px) {
  .card-description {
    -webkit-line-clamp: 4;
    line-clamp: 4;
  }
}
```

### Expand/collapse pattern

```css
.expandable {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.expandable.expanded {
  -webkit-line-clamp: unset;
  line-clamp: unset;
}
```

```js
// Minimal JS — just toggle a class, no text manipulation
btn.addEventListener('click', () => el.classList.toggle('expanded'));
```

### Single-line vs. multiline truncation

| Lines | Technique                                                        |
| ----- | ---------------------------------------------------------------- |
| 1     | `white-space: nowrap; overflow: hidden; text-overflow: ellipsis` |
| 2+    | `line-clamp` with `-webkit-box` display                          |

For single-line truncation, `text-overflow: ellipsis` remains the simplest approach. `line-clamp` is specifically for multiline truncation where you need to limit visible lines while preserving word wrapping.

✅ Widely available (~96%). `-webkit-line-clamp` is supported in all major browsers. The unprefixed `line-clamp` is also broadly supported. Safe to use without fallback.

Reference: [modern-css.com](https://modern-css.com) · [MDN — line-clamp](https://developer.mozilla.org/en-US/docs/Web/CSS/line-clamp)
