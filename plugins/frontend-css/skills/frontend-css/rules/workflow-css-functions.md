---
title: Reusable CSS Logic Without Sass Mixins
impact: MEDIUM
impactDescription: native CSS functions eliminate Sass/Less build dependency for reusable logic
tags: workflow, function, sass, mixin, preprocessor, native
browser: 67%
---

## Reusable CSS Logic Without Sass Mixins

Sass `@function` and `@mixin` directives require a build step, cannot access runtime values (like custom properties), and lock your codebase into a preprocessor toolchain. Native CSS `@function` lets you define reusable computation directly in plain `.css` files — no compiler, no build step, and full access to `var()`, `env()`, and other runtime values.

**Avoid (Sass function — requires build step):**

```scss
// Sass — must compile before the browser sees it
@function fluid($min, $max, $min-vw: 320px, $max-vw: 1200px) {
  $slope: ($max - $min) / ($max-vw - $min-vw);
  $intercept: $min - $slope * $min-vw;
  @return clamp(#{$min}, #{$intercept} + #{$slope * 100}vw, #{$max});
}

h1 {
  font-size: fluid(1rem, 2.5rem);
}
```

```scss
// Sass mixin — also build-time only
@mixin truncate($lines: 1) {
  display: -webkit-box;
  -webkit-line-clamp: $lines;
  line-clamp: $lines;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-title {
  @include truncate(3);
}
```

**Prefer (native CSS `@function`):**

```css
@function --fluid(--min, --max) {
  --slope: (var(--max) - var(--min)) / (1200 - 320);
  --intercept: var(--min) - var(--slope) * 320;
  @return clamp(var(--min), calc(var(--intercept) * 1px + var(--slope) * 100vw), var(--max));
}

h1 {
  font-size: --fluid(1rem, 2.5rem);
}
```

### Key differences from Sass functions

| Feature                      | Sass `@function`     | CSS `@function`             |
| ---------------------------- | -------------------- | --------------------------- |
| Build step required          | ✅ Yes               | ❌ No                       |
| Access to custom properties  | ❌ No (compile-time) | ✅ Yes (runtime)            |
| Access to viewport/env units | ❌ No                | ✅ Yes                      |
| Dynamic at runtime           | ❌ Static output     | ✅ Responds to state change |
| Works in plain `.css`        | ❌ Requires `.scss`  | ✅ Yes                      |

### Naming convention

Native CSS functions must start with a double dash (`--`) to avoid conflicts with current and future built-in CSS functions:

```css
@function --spacing(--multiplier) {
  @return calc(var(--space-unit, 0.25rem) * var(--multiplier));
}

.card {
  padding: --spacing(4);
  gap: --spacing(2);
}
```

### Using with custom properties for theming

Because native CSS functions run at computed-value time, they can reference custom properties that change dynamically (e.g., via class toggling or media queries):

```css
@function --surface(--lightness) {
  @return oklch(var(--lightness) 0.02 var(--surface-hue, 250));
}

:root {
  --surface-hue: 250;
}

.card {
  background: --surface(0.97);
  border-color: --surface(0.85);
}

.dark .card {
  /* Changing --surface-hue automatically updates all --surface() calls */
  --surface-hue: 260;
}
```

### Replacing Sass mixins with functions + custom properties

For patterns that Sass mixins handle (outputting multiple declarations), combine CSS functions with custom properties or use `@apply` proposals. For simple value computations, `@function` is a direct replacement:

```css
/* Fluid type scale */
@function --step(--n) {
  @return clamp(
    calc(1rem * pow(1.2, var(--n))),
    calc(1rem * pow(1.2, var(--n)) + 0.5vw),
    calc(1rem * pow(1.33, var(--n)))
  );
}

h1 {
  font-size: --step(4);
}
h2 {
  font-size: --step(3);
}
h3 {
  font-size: --step(2);
}
h4 {
  font-size: --step(1);
}
```

Native CSS functions are a fundamental step toward eliminating preprocessor dependencies. They enable the same DRY patterns that made Sass popular, but with the added power of runtime evaluation and zero build overhead.

🟡 Newly available (~67%). Supported in Chromium and Safari. Use behind `@supports` with a Sass-compiled fallback or static `clamp()`/`calc()` values for broader compatibility.

Reference: [modern-css.com](https://modern-css.com) · [CSS Functions and Mixins spec](https://drafts.csswg.org/css-mixins/)
