---
title: Exclusive Accordions Without JavaScript
impact: HIGH
impactDescription: eliminates JavaScript open/close toggle logic for accordion groups
tags: layout, details, accordion, exclusive, toggle
browser: 85%
---

## Exclusive Accordions Without JavaScript

Building an exclusive accordion (only one panel open at a time) traditionally requires JavaScript to listen for toggle events, loop through all panels, and close the others. The `name` attribute on `<details>` elements groups them — the browser automatically closes siblings when one opens, with zero JavaScript.

**Avoid (JavaScript toggle logic):**

```js
const allDetails = document.querySelectorAll('details');

allDetails.forEach((detail) => {
  detail.addEventListener('toggle', () => {
    if (detail.open) {
      allDetails.forEach((d) => {
        if (d !== detail) d.open = false;
      });
    }
  });
});
```

```html
<details>
  <summary>Section 1</summary>
  <p>Content 1</p>
</details>
<details>
  <summary>Section 2</summary>
  <p>Content 2</p>
</details>
<details>
  <summary>Section 3</summary>
  <p>Content 3</p>
</details>
```

**Prefer (shared `name` attribute):**

```html
<details name="faq">
  <summary>Section 1</summary>
  <p>Content 1</p>
</details>
<details name="faq">
  <summary>Section 2</summary>
  <p>Content 2</p>
</details>
<details name="faq">
  <summary>Section 3</summary>
  <p>Content 3</p>
</details>
<!-- Browser closes others automatically when one opens -->
```

No JavaScript, no event listeners, no loops. The `name` attribute creates the exclusive group — all `<details>` elements with the same `name` value form a group where only one can be open at a time.

### Styling the accordion

```css
details {
  border: 1px solid #ddd;
  border-radius: 0.5rem;
  padding: 0;
}

details + details {
  margin-top: -1px; /* collapse borders */
}

summary {
  padding: 1rem;
  cursor: pointer;
  font-weight: 600;
  list-style: none;
}

summary::marker {
  content: '';
}

summary::after {
  content: '+';
  float: inline-end;
  transition: rotate 200ms ease;
}

details[open] summary::after {
  rotate: 45deg;
}

details > :not(summary) {
  padding-inline: 1rem;
  padding-block-end: 1rem;
}
```

### Multiple independent groups on one page

Different `name` values create independent accordion groups:

```html
<!-- Group 1 -->
<details name="faq">…</details>
<details name="faq">…</details>

<!-- Group 2 — independent from group 1 -->
<details name="specs">…</details>
<details name="specs">…</details>
```

### Non-exclusive accordions

If you want multiple panels open simultaneously, simply omit the `name` attribute — `<details>` elements without a shared `name` operate independently by default.

🟡 Newly available (~85%). Supported in all modern browsers. Falls back gracefully — in older browsers, all panels can open simultaneously (non-exclusive behavior), which is still functional.

Reference: [modern-css.com](https://modern-css.com) · [MDN — details name attribute](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/details#name)
