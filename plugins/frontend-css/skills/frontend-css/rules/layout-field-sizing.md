---
title: Auto-Growing Textarea Without JavaScript
impact: HIGH
impactDescription: eliminates JavaScript input event listeners and manual height calculation
tags: layout, field-sizing, textarea, auto-resize, form
browser: 73%
---

## Auto-Growing Textarea Without JavaScript

Auto-growing textareas have traditionally required JavaScript that listens to every `input` event, resets the element's height to `auto`, measures `scrollHeight`, and then sets an explicit pixel height. This causes layout thrashing on every keystroke. The `field-sizing: content` property makes form elements size themselves to their content automatically — no JavaScript, no forced reflows.

**Avoid (JavaScript auto-resize):**

```js
// Runs on every keystroke — causes layout thrashing
textarea.addEventListener('input', () => {
  textarea.style.height = 'auto'; // reset to measure
  textarea.style.height = textarea.scrollHeight + 'px'; // force reflow
});
```

```css
.textarea {
  resize: none;
  overflow: hidden;
}
```

**Prefer (modern CSS):**

```css
textarea {
  field-sizing: content;
  min-height: 3lh; /* minimum 3 lines — lh = line-height unit */
  max-height: 20lh; /* cap growth, then scroll */
}
```

Zero JavaScript, zero layout thrashing. The textarea grows and shrinks with its content automatically.

### The `lh` unit

The `lh` unit equals the element's computed `line-height`, making it perfect for sizing text containers by line count:

```css
textarea {
  field-sizing: content;
  min-height: 3lh; /* at least 3 lines visible */
  max-height: 50dvh; /* never taller than half the viewport */
  overflow-y: auto; /* scroll when max-height is reached */
}
```

### Works on other form elements too

`field-sizing: content` isn't limited to textareas — it works on `<input>` and `<select>` elements as well:

```css
/* Input that shrinks/grows with its value */
input[type='text'] {
  field-sizing: content;
  min-width: 5ch; /* minimum width of ~5 characters */
}

/* Select that fits its longest option */
select {
  field-sizing: content;
}
```

### Combining with container queries

```css
.comment-form-wrapper {
  container-type: inline-size;
}

textarea {
  field-sizing: content;
  min-height: 3lh;
}

@container (width < 400px) {
  textarea {
    min-height: 2lh;
  }
}
```

🟡 Newly available (~73%). Supported in Chromium and Firefox. For Safari fallback, use the JavaScript `input` event approach behind a `@supports` check or feature detection.

Reference: [modern-css.com](https://modern-css.com) · [MDN — field-sizing](https://developer.mozilla.org/en-US/docs/Web/CSS/field-sizing)
