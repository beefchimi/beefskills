---
title: Customizable Selects Without a JavaScript Library
impact: HIGH
impactDescription: eliminates Select2 / Choices.js dependencies and DOM rebuilding for styleable dropdowns
tags: layout, select, base-select, appearance, form-controls, select2, choices
browser: 96%
---

## Customizable Selects Without a JavaScript Library

Native `<select>` elements have historically been impossible to style, forcing developers to use libraries like Select2, Choices.js, or Downshift that rebuild the entire control from scratch — adding bundle weight, breaking native keyboard behavior, hurting accessibility, and fighting with form semantics. The `appearance: base-select` value opens the native `<select>` to full CSS customization while preserving all built-in behaviors.

**Avoid (JavaScript library replacing the native select):**

```js
// Select2 — 30 KB+ gzipped, jQuery dependency
$('#my-select').select2({
  placeholder: 'Choose an option',
  allowClear: true,
});

// Choices.js — 20 KB+ gzipped
new Choices('#my-select', {
  searchEnabled: true,
  itemSelectText: '',
});
// Both rebuild the entire DOM, breaking native form submission,
// autofill, keyboard navigation, and mobile picker UX
```

**Prefer (native `<select>` with `base-select`):**

```css
select,
select::picker(select) {
  appearance: base-select;
}

/* Now you can fully style the select and its dropdown */
select {
  border: 1px solid #ccc;
  border-radius: 0.5rem;
  padding: 0.5rem 1rem;
  font-size: 1rem;
  background: white;
}

/* Style the dropdown picker */
select::picker(select) {
  border: 1px solid #ddd;
  border-radius: 0.5rem;
  box-shadow: 0 4px 16px rgb(0 0 0 / 0.1);
  padding: 0.25rem;
}

/* Style individual options */
option {
  padding: 0.5rem 0.75rem;
  border-radius: 0.25rem;
}

option:hover {
  background: oklch(0.95 0.02 250);
}

option:checked {
  background: oklch(0.55 0.2 250);
  color: white;
}
```

```html
<select>
  <option value="">Choose a framework</option>
  <option value="react">React</option>
  <option value="vue">Vue</option>
  <option value="svelte">Svelte</option>
</select>
```

### What you get for free

The native `<select>` with `base-select` preserves everything that JS libraries break:

- **Native form participation** — works with `<form>`, `FormData`, validation, and autofill.
- **Keyboard navigation** — arrow keys, type-ahead search, Enter to select, Escape to close.
- **Mobile optimization** — mobile browsers show the native bottom-sheet picker when appropriate.
- **Accessibility** — screen reader announcements, ARIA semantics, and focus management built in.
- **Top-layer rendering** — the picker renders above all other content (no z-index battles).

### Customizing the dropdown arrow

```css
/* Replace the default arrow indicator */
select::picker-icon {
  content: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>');
  block-size: 1em;
}
```

### Rich option content

With `base-select`, options can contain more than plain text:

```html
<select>
  <option value="us">
    <img src="flags/us.svg" alt="" width="20" />
    United States
  </option>
  <option value="gb">
    <img src="flags/gb.svg" alt="" width="20" />
    United Kingdom
  </option>
</select>
```

✅ Widely available (~96%). Supported in all modern browsers. This is the future of styleable form controls — remove your Select2 / Choices.js dependencies.

Reference: [modern-css.com](https://modern-css.com) · [Open UI — Customizable Select](https://open-ui.org/components/customizableselect/)
