---
title: Form Validation Styles Without JavaScript
impact: HIGH
impactDescription: eliminates JavaScript blur event listeners and manual class toggling for form validation feedback
tags: selectors, user-invalid, user-valid, form, validation, pseudo-class
browser: 85%
---

## Form Validation Styles Without JavaScript

Showing validation feedback (red borders on invalid fields, green on valid) traditionally required JavaScript that listens for `blur` events, checks validity, and adds a `.touched` or `.invalid` class — because the built-in `:invalid` pseudo-class fires immediately on page load before the user has interacted with the field. The `:user-invalid` and `:user-valid` pseudo-classes only activate after the user has actually interacted with the control, providing the correct timing with zero JavaScript.

**Avoid (JavaScript blur-based validation classes):**

```js
// Add .touched class on blur so :invalid only shows after interaction
document.querySelectorAll('input, select, textarea').forEach((el) => {
  el.addEventListener('blur', () => {
    el.classList.add('touched');
  });
});
```

```css
/* Only show validation styles after JS adds .touched */
input.touched:invalid {
  border-color: red;
  outline-color: red;
}

input.touched:valid {
  border-color: green;
}

/* Without .touched, :invalid fires on page load — terrible UX */
input:invalid {
  border-color: red; /* Shows red before user types anything */
}
```

**Prefer (modern CSS — no JavaScript):**

```css
input:user-invalid {
  border-color: oklch(0.6 0.22 25);
  outline-color: oklch(0.6 0.22 25);
}

input:user-valid {
  border-color: oklch(0.65 0.2 145);
}
```

No JavaScript, no event listeners, no class toggling. The browser tracks interaction state internally — `:user-invalid` only matches after the user has modified or blurred the field, and `:user-valid` only matches after successful interaction.

### When does `:user-invalid` activate?

The pseudo-class becomes active after the user has:

1. **Modified the value** — typed into a text input, selected an option, etc.
2. **Attempted to submit** the form (even if submission was blocked by validation).
3. **Blurred the field** after interacting with it.

It does **not** activate on page load, even if the field is initially invalid (e.g., an empty required field). This is the key difference from `:invalid`.

### Comparison with `:invalid`

| Pseudo-class    | Fires on page load | Fires before interaction | Fires after interaction |
| --------------- | ------------------ | ------------------------ | ----------------------- |
| `:invalid`      | ✅ Yes             | ✅ Yes                   | ✅ Yes                  |
| `:user-invalid` | ❌ No              | ❌ No                    | ✅ Yes                  |
| `:valid`        | ✅ Yes             | ✅ Yes                   | ✅ Yes                  |
| `:user-valid`   | ❌ No              | ❌ No                    | ✅ Yes                  |

### Complete form validation pattern

```css
/* Default state — neutral borders */
input,
select,
textarea {
  border: 1px solid oklch(0.8 0.01 250);
  border-radius: 0.375rem;
  padding: 0.5rem 0.75rem;
  transition: border-color 0.15s ease;
}

/* Valid after interaction — subtle success indicator */
:is(input, select, textarea):user-valid {
  border-color: oklch(0.65 0.2 145);
}

/* Invalid after interaction — clear error indicator */
:is(input, select, textarea):user-invalid {
  border-color: oklch(0.6 0.22 25);
  outline-color: oklch(0.6 0.22 25);
}

/* Error message visibility — hidden until user-invalid */
.field-error {
  display: none;
  color: oklch(0.55 0.22 25);
  font-size: 0.875rem;
  margin-top: 0.25rem;
}

/* Show error message when sibling input is user-invalid */
:is(input, select, textarea):user-invalid + .field-error {
  display: block;
}
```

```html
<div class="field">
  <label for="email">Email address</label>
  <input id="email" type="email" required />
  <p class="field-error">Please enter a valid email address.</p>
</div>
```

### With icons or indicators

```css
.input-wrapper {
  position: relative;
}

.input-wrapper input:user-valid ~ .icon-valid {
  display: block;
}

.input-wrapper input:user-invalid ~ .icon-invalid {
  display: block;
}

.icon-valid,
.icon-invalid {
  display: none;
  position: absolute;
  inset-inline-end: 0.75rem;
  inset-block-start: 50%;
  translate: 0 -50%;
}
```

### Pattern validation

`:user-invalid` works with all HTML validation attributes — `required`, `type`, `pattern`, `min`, `max`, `minlength`, `maxlength`, and `step`:

```css
/* Works with pattern attribute */
input[pattern]:user-invalid {
  border-color: oklch(0.6 0.22 25);
}

/* Works with min/max on number inputs */
input[type='number']:user-invalid {
  border-color: oklch(0.6 0.22 25);
}
```

```html
<input type="text" pattern="[A-Za-z]{3,}" title="At least 3 letters" required />
<input type="number" min="1" max="100" required />
```

### Combining with `:focus` for real-time feedback

```css
/* Show neutral focus ring while actively typing */
input:focus {
  outline: 2px solid oklch(0.6 0.15 250);
  outline-offset: 2px;
}

/* Override with validation color after interaction + re-focus */
input:focus:user-invalid {
  outline-color: oklch(0.6 0.22 25);
}

input:focus:user-valid {
  outline-color: oklch(0.65 0.2 145);
}
```

### Why not just use `:invalid` with `:not(:placeholder-shown)`?

A common workaround before `:user-invalid` was:

```css
/* Hack — requires a placeholder attribute on every input */
input:not(:placeholder-shown):invalid {
  border-color: red;
}
```

This only works on inputs with a `placeholder` attribute, doesn't work on `<select>` or `<textarea>` without placeholders, and doesn't handle the "submitted but not yet interacted" case. `:user-invalid` handles all these cases natively and correctly.

🟡 Newly available (~85%). Supported in all modern browsers. Falls back gracefully — in unsupporting browsers, the validation styles simply don't appear (neutral borders), which is better than showing errors on page load.

Reference: [modern-css.com](https://modern-css.com) · [MDN — :user-invalid](https://developer.mozilla.org/en-US/docs/Web/CSS/:user-invalid)
