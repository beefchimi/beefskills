---
title: Text Highlighting Without DOM Manipulation
impact: MEDIUM
impactDescription: eliminates innerHTML replacement and DOM mutation for search result highlighting
tags: selectors, highlight, search, custom-highlight, dom-manipulation
browser: 93%
---

## Text Highlighting Without DOM Manipulation

Highlighting search terms in a page traditionally requires replacing `innerHTML` with `<mark>` wrapper elements — a destructive operation that breaks event listeners, destroys component state, causes layout reflow, and opens XSS vectors if the search term isn't sanitized. The CSS Custom Highlight API with the `::highlight()` pseudo-element applies visual highlights to arbitrary text ranges without modifying the DOM at all.

**Avoid (innerHTML replacement — destructive):**

```js
// Destroys event listeners, breaks component state, XSS risk
function highlightMatches(el, term) {
  const regex = new RegExp(`(${term})`, 'gi');
  el.innerHTML = el.innerHTML.replace(regex, '<mark>$1</mark>');
  // Every call re-parses the entire subtree
  // Must "un-highlight" by restoring original HTML
}

// Or with jQuery:
// $(el).html($(el).html().replace(/term/g, '<mark>$&</mark>'));
```

Problems:

- **Destroys event listeners** — any `addEventListener` calls on child elements are lost.
- **Breaks framework state** — React, Vue, Svelte component trees are corrupted.
- **XSS vulnerability** — if `term` contains HTML, it's injected directly.
- **Layout thrashing** — full DOM teardown and rebuild triggers reflow.
- **Undo is complex** — must store and restore the original HTML.

**Prefer (CSS Custom Highlight API):**

```js
// Create a highlight range without touching the DOM
function highlightMatches(root, term) {
  // Clear previous highlights
  CSS.highlights.delete('search');

  if (!term) return;

  const treeWalker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
  const ranges = [];

  while (treeWalker.nextNode()) {
    const node = treeWalker.currentNode;
    const text = node.textContent;
    let match;
    const regex = new RegExp(term, 'gi');

    while ((match = regex.exec(text)) !== null) {
      const range = new Range();
      range.setStart(node, match.index);
      range.setEnd(node, match.index + match[0].length);
      ranges.push(range);
    }
  }

  if (ranges.length > 0) {
    const highlight = new Highlight(...ranges);
    CSS.highlights.set('search', highlight);
  }
}
```

```css
::highlight(search) {
  background: oklch(0.92 0.15 90); /* soft yellow */
  color: oklch(0.2 0.02 90);
}
```

Zero DOM mutation. Event listeners are preserved, framework state is untouched, and clearing the highlight is a single `CSS.highlights.delete('search')` call.

### How the Custom Highlight API works

1. **Find text ranges** — Use `Range` objects to mark start/end positions in text nodes.
2. **Create a `Highlight`** — Group ranges into a named `Highlight` object.
3. **Register it** — Add to `CSS.highlights` with a name (e.g., `'search'`).
4. **Style it** — Use `::highlight(name)` in CSS to apply visual styles.

### Multiple named highlights

You can register multiple independent highlight groups with different styles:

```js
CSS.highlights.set('search', new Highlight(...searchRanges));
CSS.highlights.set('spelling', new Highlight(...spellingRanges));
CSS.highlights.set('selection', new Highlight(...selectionRanges));
```

```css
::highlight(search) {
  background: oklch(0.92 0.15 90);
  color: oklch(0.2 0.02 90);
}

::highlight(spelling) {
  text-decoration: wavy underline red;
}

::highlight(selection) {
  background: oklch(0.85 0.12 264);
  color: white;
}
```

### Available properties in `::highlight()`

The `::highlight()` pseudo-element supports a limited set of properties focused on text appearance:

| Property                    | Supported |
| --------------------------- | --------- |
| `background-color`          | ✅        |
| `color`                     | ✅        |
| `text-decoration`           | ✅        |
| `text-shadow`               | ✅        |
| `-webkit-text-fill-color`   | ✅        |
| `-webkit-text-stroke-color` | ✅        |

It does **not** support `padding`, `margin`, `border`, `font-size`, or layout properties — it's purely a paint-level overlay on existing text.

### Clearing highlights

```js
// Remove a specific highlight
CSS.highlights.delete('search');

// Remove all highlights
CSS.highlights.clear();
```

### Practical search input integration

```js
const searchInput = document.querySelector('#search');
const content = document.querySelector('#content');

searchInput.addEventListener('input', (e) => {
  highlightMatches(content, e.target.value.trim());
});
```

```css
::highlight(search) {
  background: oklch(0.92 0.15 90);
  color: oklch(0.2 0.02 90);
  text-decoration: underline 2px oklch(0.7 0.15 90);
}

/* Respect reduced motion — skip animated highlight effects */
@media (prefers-reduced-motion: reduce) {
  ::highlight(search) {
    text-decoration: none;
  }
}
```

The Custom Highlight API is the correct tool for any use case where you need to visually mark text ranges — search results, code syntax highlighting, collaborative editing cursors, spelling/grammar indicators — without altering the DOM structure.

✅ Widely available (~93%). Supported in all modern browsers. Safe to use in production. For the small number of older browsers, fall back to `<mark>` element injection only when the Custom Highlight API is unavailable:

```js
if ('highlights' in CSS) {
  // Use Custom Highlight API
} else {
  // Fallback to innerHTML replacement
}
```

Reference: [modern-css.com](https://modern-css.com) · [MDN — CSS Custom Highlight API](https://developer.mozilla.org/en-US/docs/Web/API/CSS_Custom_Highlight_API)
