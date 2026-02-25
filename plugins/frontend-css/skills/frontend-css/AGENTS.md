# Modern CSS Best Practices

**Version 1.0.0**
Modern CSS

> **Note:**
> This document is for agents and LLMs when maintaining, generating, or refactoring
> CSS codebases. Every legacy hack has a clean, native CSS replacement — use it.
> Patterns sourced from and inspired by [modern-css.com](https://modern-css.com).

---

## Abstract

Modern CSS best-practices guide distilled from modern-css.com. 75 rules across
6 categories: layout, workflow, typography, color, selectors, and animation.
Each rule compares a legacy hack or JavaScript workaround with its clean, native
CSS replacement. Includes browser support tiers and progressive enhancement notes.

---

## Table of Contents

1. [Layout](#1-layout) — **CRITICAL**
   - 1.1 Tooltip Positioning Without JavaScript
   - 1.2 Aspect Ratios Without the Padding Hack
   - 1.3 Customizable Selects Without a JavaScript Library
   - 1.4 Modal Controls Without onclick Handlers
   - 1.5 Responsive Components Without Media Queries
   - 1.6 Corner Shapes Beyond Rounded Borders
   - 1.7 Dialog Light Dismiss Without Click-Outside Listeners
   - 1.8 Mobile Viewport Height Without the 100vh Hack
   - 1.9 Exclusive Accordions Without JavaScript
   - 1.10 Auto-Growing Textarea Without JavaScript
   - 1.11 Spacing Elements Without Margin Hacks
   - 1.12 Named Grid Areas Instead of Line Numbers or Floats
   - 1.13 Centering Elements Without the Transform Hack
   - 1.14 Positioning Shorthand Without Four Properties
   - 1.15 Direction-Aware Layouts Without Left and Right
   - 1.16 Modal Dialogs Without a JavaScript Library
   - 1.17 Responsive Images Without the Background-Image Hack
   - 1.18 Preventing Scroll Chaining Without JavaScript
   - 1.19 Dropdown Menus Without JavaScript Toggles
   - 1.20 Hover Tooltips Without JavaScript Events
   - 1.21 Media Query Ranges Without min-width and max-width
   - 1.22 Carousel Navigation Without a JavaScript Library
   - 1.23 Scroll Snapping Without a Carousel Library
   - 1.24 Preventing Layout Shift From Scrollbar Appearance
   - 1.25 Scrollbar Styling Without -webkit- Pseudo-Elements
   - 1.26 Path Shapes Without SVG Clip Paths
   - 1.27 Sticky Headers Without JavaScript Scroll Listeners
   - 1.28 Filling Available Space Without calc Workarounds
   - 1.29 Aligning Nested Grids Without Duplicating Tracks
   - 1.30 Scaling Elements Without Transform Hacks

2. [Workflow](#2-workflow) — **HIGH**
   - 2.1 Typed Attribute Values Without JavaScript
   - 2.2 Controlling Specificity Without !important
   - 2.3 Dark Mode Defaults Without Extra CSS
   - 2.4 Lazy Rendering Without IntersectionObserver
   - 2.5 Reusable CSS Logic Without Sass Mixins
   - 2.6 Theme Variables Without a Preprocessor
   - 2.7 Inline Conditional Styles Without JavaScript
   - 2.8 Nesting Selectors Without Sass or Less
   - 2.9 Typed Custom Properties Without JavaScript
   - 2.10 Scoped Styles Without BEM Naming
   - 2.11 Range Style Queries Without Multiple Blocks
   - 2.12 CSS Feature Detection Without JavaScript

3. [Typography](#3-typography) — **HIGH**
   - 3.1 Fluid Typography Without Media Queries
   - 3.2 Font Loading Without Invisible Text
   - 3.3 Drop Caps Without Float Hacks
   - 3.4 Multiline Text Truncation Without JavaScript
   - 3.5 Vertical Text Centering Without Padding Hacks
   - 3.6 Balanced Headlines Without Manual Line Breaks
   - 3.7 Multiple Font Weights Without Multiple Files

4. [Color](#4-color) — **MEDIUM-HIGH**
   - 4.1 Styling Form Controls Without Rebuilding Them
   - 4.2 Frosted Glass Effect Without Opacity Hacks
   - 4.3 Readable Text Without Manual Contrast Checks
   - 4.4 Dark Mode Colors Without Duplicating Values
   - 4.5 Mixing Colors Without a Preprocessor
   - 4.6 Perceptually Uniform Colors With oklch
   - 4.7 Color Variants Without Sass Functions
   - 4.8 Vivid Colors Beyond sRGB

5. [Selectors](#5-selectors) — **MEDIUM-HIGH**
   - 5.1 Focus Styles Without Annoying Mouse Users
   - 5.2 Selecting Parent Elements Without JavaScript
   - 5.3 Text Highlighting Without DOM Manipulation
   - 5.4 Grouping Selectors Without Repetition
   - 5.5 Scroll Spy Without IntersectionObserver
   - 5.6 Form Validation Styles Without JavaScript
   - 5.7 Low-Specificity Resets Without Complicated Selectors

6. [Animation](#6-animation) — **MEDIUM**
   - 6.1 Animating Display None Without Workarounds
   - 6.2 Independent Transforms Without the Shorthand
   - 6.3 Smooth Height Auto Animations Without JavaScript
   - 6.4 Custom Easing Curves Without cubic-bezier Guessing
   - 6.5 Reduced Motion Without JavaScript Detection
   - 6.6 Sticky & Snapped Element Styling Without JavaScript
   - 6.7 Scroll-Linked Animations Without a Library
   - 6.8 Responsive Clip Paths Without SVG
   - 6.9 Staggered Animations Without nth-child Hacks
   - 6.10 Entry Animations Without JavaScript Timing
   - 6.11 Page Transitions Without a Framework

---

## 1. Layout

### 1.1 Tooltip Positioning Without JavaScript

Libraries like Popper.js and Floating UI exist solely to position a floating element relative to a trigger — computing rects, flipping on overflow, updating on scroll and resize. CSS Anchor Positioning does all of this declaratively with zero JavaScript, zero dependencies, and compositor-level performance.

**Avoid (Popper.js / Floating UI):**

```js
// npm install @floating-ui/dom — 10 KB+ gzipped
import {computePosition, flip, shift, offset} from '@floating-ui/dom';

async function updateTooltip(trigger, tooltip) {
  const {x, y} = await computePosition(trigger, tooltip, {
    placement: 'bottom',
    middleware: [offset(8), flip(), shift({padding: 8})],
  });
  tooltip.style.left = `${x}px`;
  tooltip.style.top = `${y}px`;
}

// Must re-run on scroll, resize, layout changes…
window.addEventListener('scroll', () => updateTooltip(trigger, tooltip));
window.addEventListener('resize', () => updateTooltip(trigger, tooltip));
```

```css
.tooltip {
  position: fixed;
  z-index: 9999;
}
```

**Prefer (CSS Anchor Positioning):**

```css
.trigger {
  anchor-name: --tip;
}

.tooltip {
  position: fixed;
  position-anchor: --tip;

  /* Place below the trigger with 8px offset */
  inset-area: bottom;
  margin-top: 8px;

  /* Auto-flip if it would overflow the viewport */
  position-try-fallbacks: flip-block, flip-inline;

  /* Sizing constraints */
  max-inline-size: 300px;
}
```

```html
<button class="trigger">Hover me</button>
<div class="tooltip" popover>Tooltip content here</div>
```

**Multiple anchors and named fallbacks:**

```css
/* Position try fallbacks with custom positions */
@position-try --above {
  inset-area: top;
  margin-bottom: 8px;
}

@position-try --right {
  inset-area: right;
  margin-left: 8px;
}

.tooltip {
  position: fixed;
  position-anchor: --tip;
  inset-area: bottom;
  margin-top: 8px;
  position-try-fallbacks: --above, --right;
}
```

**Anchoring with `anchor()` functions for precise control:**

```css
.tooltip {
  position: fixed;
  position-anchor: --tip;

  /* Explicit anchor function placement */
  top: anchor(bottom);
  left: anchor(center);
  translate: -50% 0;
}
```

CSS Anchor Positioning handles scroll tracking, viewport flipping, and repositioning automatically — the browser re-evaluates on every frame without JavaScript. No event listeners, no `requestAnimationFrame`, no z-index wars.

🟡 Newly available (~77%). Supported in Chromium browsers and Firefox. Use behind `@supports (anchor-name: --x)` with a Floating UI fallback for Safari until support ships.

Reference: [modern-css.com](https://modern-css.com) · [MDN — CSS Anchor Positioning](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_anchor_positioning)

### 1.2 Aspect Ratios Without the Padding Hack

The old `padding-top` trick exploits the fact that vertical padding percentages are relative to the element's width. It works, but requires a wrapper element, absolute positioning on the child, and a magic number (`56.25%` = 9/16) that is unintuitive to read or maintain. The `aspect-ratio` property replaces all of this with a single, self-documenting declaration.

**Avoid (padding-top hack):**

```css
.video-wrapper {
  position: relative;
  padding-top: 56.25%; /* 16:9 magic number */
  height: 0;
}

.video-wrapper > * {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
}
```

**Prefer (modern CSS):**

```css
.video-wrapper {
  aspect-ratio: 16 / 9;
}
```

The element sizes itself — no wrapper, no absolute positioning, no magic percentages.

**Common aspect ratios:**

```css
.widescreen {
  aspect-ratio: 16 / 9;
}
.photo {
  aspect-ratio: 4 / 3;
}
.square {
  aspect-ratio: 1;
}
.portrait {
  aspect-ratio: 3 / 4;
}
.cinema {
  aspect-ratio: 2.35 / 1;
}
```

**Responsive image cards:**

```css
.card-image {
  aspect-ratio: 3 / 2;
  object-fit: cover;
  width: 100%;
}
```

`aspect-ratio` is respected by the intrinsic sizing algorithm, so it works with `min-height`, `max-height`, and flexbox/grid without conflict. If both `width` and `height` are explicitly set, `aspect-ratio` is overridden — it only fills in the missing dimension.

✅ Widely available (~93%). No fallback needed.

Reference: [modern-css.com](https://modern-css.com)

### 1.3 Customizable Selects Without a JavaScript Library

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

### 1.4 Modal Controls Without onclick Handlers

Opening a `<dialog>` or toggling a `[popover]` traditionally requires inline `onclick` handlers or `addEventListener` calls. The `commandfor` and `command` attributes let you declaratively wire a button to a target element's built-in actions — no JavaScript, no query selectors, no event delegation.

**Avoid (onclick with querySelector):**

```html
<button onclick="document.querySelector('#dlg').showModal()">Open</button>
<dialog id="dlg">
  <p>Dialog content</p>
  <button onclick="this.closest('dialog').close()">Close</button>
</dialog>
```

Or with event listeners:

```js
openBtn.addEventListener('click', () => dialog.showModal());
closeBtn.addEventListener('click', () => dialog.close());
```

**Prefer (declarative `commandfor` + `command`):**

```html
<button commandfor="dlg" command="show-modal">Open</button>

<dialog id="dlg">
  <p>Dialog content</p>
  <button commandfor="dlg" command="close">Close</button>
</dialog>
```

Zero JavaScript. The browser connects the button to the target element and invokes the specified command on click.

### Available commands

| Target element | Command          | Equivalent JS        |
| -------------- | ---------------- | -------------------- |
| `<dialog>`     | `show-modal`     | `dialog.showModal()` |
| `<dialog>`     | `close`          | `dialog.close()`     |
| `<dialog>`     | `show`           | `dialog.show()`      |
| `[popover]`    | `toggle-popover` | `el.togglePopover()` |
| `[popover]`    | `show-popover`   | `el.showPopover()`   |
| `[popover]`    | `hide-popover`   | `el.hidePopover()`   |

### Multiple triggers for the same target

```html
<button commandfor="settings" command="show-modal">⚙️ Settings</button>
<button commandfor="settings" command="show-modal">Open Settings</button>

<dialog id="settings">
  <h2>Settings</h2>
  <!-- content -->
  <button commandfor="settings" command="close">Done</button>
</dialog>
```

### Combined with popover

```html
<button commandfor="confirm" command="show-modal">Delete Account</button>

<dialog id="confirm">
  <p>Are you sure?</p>
  <button commandfor="confirm" command="close">Cancel</button>
  <button type="submit" form="delete-form">Confirm</button>
</dialog>
```

`commandfor` is the successor to `popovertarget` for dialogs, and generalizes the pattern of declaratively connecting a trigger button to a target element's action. The `command` event also fires on the target, allowing custom logic without replacing the declarative wiring:

```js
dialog.addEventListener('command', (e) => {
  if (e.command === 'close') {
    // run cleanup before the browser closes the dialog
  }
});
```

🟡 Newly available (~72%). Supported in Chromium and Firefox. Use `onclick` as a fallback for Safari until support lands.

Reference: [modern-css.com](https://modern-css.com) · [MDN — commandfor attribute](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/button#commandfor)

### 1.5 Responsive Components Without Media Queries

Viewport-based `@media` queries tie component layout to the window size, which breaks when the same component appears in different contexts (sidebar vs. main content vs. modal). `@container` queries let a component respond to the size of its own container, making it truly reusable regardless of where it's placed in the page.

**Avoid (viewport media queries on components):**

```css
.card {
  display: flex;
  flex-direction: row;
}

@media (max-width: 768px) {
  .card {
    flex-direction: column;
  }
}
/* Breaks when .card is in a narrow sidebar on a wide screen */
```

**Prefer (container queries):**

```css
.card-wrapper {
  container-type: inline-size;
}

.card {
  display: flex;
  flex-direction: row;
}

@container (width < 400px) {
  .card {
    flex-direction: column;
  }
}
/* Adapts to its container, not the viewport */
```

### Container query setup

Any element can become a containment context. Use `container-type` (or the shorthand `container`) on the parent:

```css
/* Size containment on inline axis (most common) */
.sidebar {
  container-type: inline-size;
}

/* Named container for targeted queries */
.sidebar {
  container: sidebar / inline-size;
}

@container sidebar (width < 300px) {
  .nav-link span {
    display: none; /* collapse labels, show icons only */
  }
}
```

### Range syntax

Container queries support the same range syntax as modern media queries:

```css
/* Old syntax */
@container (min-width: 400px) and (max-width: 800px) {
  .card {
    /* ... */
  }
}

/* Modern range syntax */
@container (400px <= width <= 800px) {
  .card {
    /* ... */
  }
}
```

### Common patterns

```css
/* Responsive grid item that stacks when its container is narrow */
.product-card-container {
  container-type: inline-size;
}

@container (width >= 500px) {
  .product-card {
    display: grid;
    grid-template-columns: 200px 1fr;
    gap: 1rem;
  }
}

@container (width < 500px) {
  .product-card {
    display: flex;
    flex-direction: column;
  }
}
```

Container queries are the correct tool for component-level responsiveness. Reserve `@media` queries for page-level layout shifts (e.g., switching from single-column to multi-column) and user preference queries (`prefers-color-scheme`, `prefers-reduced-motion`).

✅ Widely available (~93%). Safe to use without fallback.

Reference: [modern-css.com](https://modern-css.com) · [MDN — @container](https://developer.mozilla.org/en-US/docs/Web/CSS/@container)

### 1.6 Corner Shapes Beyond Rounded Borders

Creating smooth, continuous-curvature corners (squircles — the shape Apple uses on app icons) traditionally required a multi-point `clip-path: polygon()` with 20+ manually calculated coordinates, or an SVG mask. The `corner-shape` property paired with `border-radius` produces these shapes in a single declaration, and the browser handles the math.

**Avoid (complex clip-path polygon):**

```css
.card {
  clip-path: polygon(
    0% 8%,
    0.3% 5.6%,
    1.2% 3.5%,
    2.6% 1.8%,
    4.5% 0.7%,
    7% 0.1%,
    10% 0%,
    90% 0%,
    93% 0.1%,
    95.5% 0.7%,
    97.4% 1.8%,
    98.8% 3.5%,
    99.7% 5.6%,
    100% 8%,
    100% 92%,
    99.7% 94.4%,
    98.8% 96.5%,
    97.4% 98.2%,
    95.5% 99.3%,
    93% 99.9%,
    90% 100%,
    10% 100%,
    7% 99.9%,
    4.5% 99.3%,
    2.6% 98.2%,
    1.2% 96.5%,
    0.3% 94.4%,
    0% 92%
  );
  /* Fragile, not responsive, no box-shadow or border support */
}
```

Or an SVG mask approach:

```css
.card {
  mask-image: url('squircle.svg');
  mask-size: 100% 100%;
  /* Requires an external SVG asset, still no box-shadow */
}
```

**Prefer (modern CSS):**

```css
.card {
  border-radius: 2em;
  corner-shape: squircle;
}
```

The `corner-shape` property modifies how `border-radius` curves are drawn. Instead of a circular arc, `squircle` produces a superellipse — a smooth, continuous curve that avoids the abrupt transition between the flat edge and the rounded corner.

### Available corner shapes

```css
/* Standard circular arcs (default) */
.default {
  border-radius: 1rem;
  corner-shape: round;
}

/* Superellipse / continuous curvature (Apple-style) */
.smooth {
  border-radius: 2rem;
  corner-shape: squircle;
}

/* Angled notch */
.notch {
  border-radius: 1rem;
  corner-shape: notch;
}

/* Beveled / straight cut */
.bevel {
  border-radius: 1rem;
  corner-shape: bevel;
}

/* Scooped inward curve */
.scoop {
  border-radius: 1rem;
  corner-shape: scoop;
}
```

### Advantages over clip-path workarounds

- **Works with `box-shadow` and `border`** — `clip-path` clips both away.
- **Responsive** — scales with the element, no fixed pixel coordinates.
- **Composable** — each corner can have a different radius and they all use the same shape.
- **No external assets** — no SVG masks or image references.

### Progressive enhancement

```css
.card {
  border-radius: 2em; /* circular fallback in all browsers */
  corner-shape: squircle; /* upgraded in supporting browsers */
}
```

Since `corner-shape` degrades gracefully to standard `border-radius` rounding, there is no visual breakage in unsupporting browsers — just a slightly less refined curve.

🟡 Newly available (~67%). Progressive enhancement is safe — older browsers simply render standard rounded corners.

Reference: [modern-css.com](https://modern-css.com) · [CSS Round Display spec — corner-shape](https://drafts.csswg.org/css-borders-4/#corner-shape)

### 1.7 Dialog Light Dismiss Without Click-Outside Listeners

Allowing users to close a modal by clicking the backdrop (a.k.a. "light dismiss") traditionally requires JavaScript that listens for clicks on the `::backdrop` pseudo-element or checks whether the click target is outside the dialog bounds. The `closedby` attribute on `<dialog>` makes this behavior declarative — no event listeners, no coordinate math.

**Avoid (JavaScript click-outside detection):**

```js
// Listen for clicks on the dialog element itself (backdrop clicks hit the dialog)
dialog.addEventListener('click', (e) => {
  // Check if the click was on the backdrop (outside the dialog box)
  const rect = dialog.getBoundingClientRect();
  const clickedInDialog =
    e.clientX >= rect.left &&
    e.clientX <= rect.right &&
    e.clientY >= rect.top &&
    e.clientY <= rect.bottom;

  if (!clickedInDialog) {
    dialog.close();
  }
});
```

Or the common workaround using a wrapper `<div>`:

```html
<dialog id="dlg">
  <div class="dialog-inner" onclick="event.stopPropagation()">
    <!-- content -->
  </div>
</dialog>
```

```js
dlg.addEventListener('click', () => dlg.close());
// Inner div stops propagation to prevent closing when clicking content
```

**Prefer (modern HTML):**

```html
<dialog closedby="any">
  <h2>Confirm Action</h2>
  <p>Are you sure you want to proceed?</p>
  <button onclick="this.closest('dialog').close()">Cancel</button>
  <button onclick="this.closest('dialog').close('confirm')">Confirm</button>
</dialog>
```

No JavaScript listeners for light dismiss — the browser handles backdrop clicks and Escape key natively.

### `closedby` values

| Value          | Escape key | Backdrop click | Explicit `.close()` |
| -------------- | ---------- | -------------- | ------------------- |
| `any`          | ✅         | ✅             | ✅                  |
| `closerequest` | ✅         | ❌             | ✅                  |
| `none`         | ❌         | ❌             | ✅                  |

```html
<!-- Light dismiss — closes on backdrop click or Escape -->
<dialog closedby="any">…</dialog>

<!-- Close on Escape only, no backdrop click -->
<dialog closedby="closerequest">…</dialog>

<!-- Only closable programmatically — for critical confirmations -->
<dialog closedby="none">…</dialog>
```

### Combining with Popover API

The `closedby` attribute aligns with how the Popover API handles light dismiss (`popover="auto"`). For non-modal floating content (dropdowns, tooltips), prefer the Popover API. Reserve `<dialog closedby="any">` for modal dialogs that need backdrop + light dismiss.

### Styling

```css
dialog {
  border: none;
  border-radius: 0.75rem;
  padding: 1.5rem;
  max-width: min(90vw, 480px);
}

dialog::backdrop {
  background: rgb(0 0 0 / 0.4);
  backdrop-filter: blur(4px);
}
```

🟡 Newly available (~69%). Supported in Chromium and Firefox. For browsers without support, `closedby="any"` is ignored and the dialog falls back to default behavior (Escape to close, no backdrop click). Add a JavaScript fallback for broader support if light dismiss is critical to UX.

Reference: [modern-css.com](https://modern-css.com) · [MDN — dialog closedby](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/dialog#closedby)

### 1.8 Mobile Viewport Height Without the 100vh Hack

On mobile browsers, `100vh` includes the area behind the browser's address bar and toolbar, causing content to overflow the visible area. The dynamic viewport unit `dvh` adapts to the actual visible height as browser chrome appears and disappears.

**Avoid (100vh overflows on mobile):**

```css
.hero {
  height: 100vh;
}
/* Content extends behind the address bar on iOS Safari / Chrome Android */
```

**Prefer (dvh adapts to browser chrome):**

```css
.hero {
  height: 100dvh;
}
/* Shrinks/grows as the address bar shows/hides */
```

### Choosing the right unit

There are three viewport-relative height units for different use cases:

```css
/* Dynamic — updates as browser chrome shows/hides (most common) */
.hero {
  height: 100dvh;
}

/* Small — smallest possible viewport (chrome visible). Safe for
   "must always fit" elements like sticky footers. */
.sticky-footer {
  min-height: 100svh;
}

/* Large — largest possible viewport (chrome hidden). Use when you
   want maximum space and can tolerate temporary overflow. */
.splash {
  height: 100lvh;
}
```

### Width equivalents

The same logic applies to width (relevant on some mobile browsers and foldables):

```css
.sidebar {
  width: 100dvw; /* instead of 100vw */
}
```

### Fallback for older browsers

```css
.hero {
  height: 100vh; /* fallback */
  height: 100dvh; /* override in supporting browsers */
}
```

✅ Widely available (~93%). Safe to use with a `vh` fallback line for the small number of older browsers.

Reference: [modern-css.com](https://modern-css.com) · [MDN: Viewport units](https://developer.mozilla.org/en-US/docs/Web/CSS/length#viewport_units)

### 1.9 Exclusive Accordions Without JavaScript

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

### 1.10 Auto-Growing Textarea Without JavaScript

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

### 1.11 Spacing Elements Without Margin Hacks

The `gap` property on flex and grid containers replaces the classic pattern of applying margins to children and then removing them from the last (or first) child. It keeps spacing concerns on the parent, avoids negative-margin workarounds, and works with wrapping layouts without extra overrides.

**Avoid (margin hack with last-child override):**

```css
.grid > * {
  margin-right: 16px;
}
.grid > *:last-child {
  margin-right: 0;
}
```

Or the negative-margin wrapper hack:

```css
.grid-wrapper {
  margin-right: -16px;
}
.grid-wrapper > * {
  margin-right: 16px;
}
```

**Prefer (gap on the container):**

```css
.grid {
  display: flex;
  gap: 16px;
}
```

For different row and column spacing:

```css
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 24px 16px; /* row-gap column-gap */
}
```

`gap` works on both `display: flex` and `display: grid`. It respects wrapping in flex layouts without extra overrides, and it composes cleanly with `justify-content` and `align-items` — no margin collapse surprises.

✅ Widely available (~95%). Use freely.

Reference: [modern-css.com](https://modern-css.com)

### 1.12 Named Grid Areas Instead of Line Numbers or Floats

Grid line numbers (`grid-column: 1 / 3`) are hard to read and brittle when the layout changes. Float-based layouts require clearfixes and margin hacks. Named grid areas make the layout visually obvious in the CSS itself and trivial to rearrange.

**Avoid (floats or numeric grid lines):**

```css
/* Float-based — fragile, requires clearfix */
.header {
  float: left;
  width: 100%;
}
.sidebar {
  float: left;
  width: 25%;
}
.main {
  float: left;
  width: 75%;
}
.footer {
  clear: both;
}

/* Or numeric grid lines — hard to visualize */
.header {
  grid-column: 1 / 3;
  grid-row: 1;
}
.sidebar {
  grid-column: 1;
  grid-row: 2;
}
.main {
  grid-column: 2;
  grid-row: 2;
}
.footer {
  grid-column: 1 / 3;
  grid-row: 3;
}
```

**Prefer (named grid areas):**

```css
.layout {
  display: grid;
  grid-template-areas:
    'header  header'
    'sidebar main'
    'footer  footer';
  grid-template-columns: 250px 1fr;
  grid-template-rows: auto 1fr auto;
  min-height: 100dvh;
}

.header {
  grid-area: header;
}
.sidebar {
  grid-area: sidebar;
}
.main {
  grid-area: main;
}
.footer {
  grid-area: footer;
}

/* Rearranging is a one-line change */
@media (width < 768px) {
  .layout {
    grid-template-areas:
      'header'
      'main'
      'sidebar'
      'footer';
    grid-template-columns: 1fr;
  }
}
```

The `grid-template-areas` property acts as a visual ASCII map of your layout. Reordering content across breakpoints is a single property change — no line numbers to recalculate, no floats to clear.

✅ Widely available (~96%). No fallback needed.

Reference: [modern-css.com](https://modern-css.com)

### 1.13 Centering Elements Without the Transform Hack

The absolute-position + transform centering hack requires styling the child, knowing the parent's position context, and breaks easily when content size changes. `display: grid; place-items: center` on the parent centers any number of children with zero child styles.

**Avoid (absolute + transform):**

```css
.parent {
  position: relative;
}

.child {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}
```

**Prefer (grid centering):**

```css
.parent {
  display: grid;
  place-items: center;
}
/* child needs nothing */
```

This also works with `display: flex; align-items: center; justify-content: center;` but `place-items: center` on grid is the most concise single-property solution. The child requires no positioning, no transforms, and no knowledge of its own dimensions.

✅ Widely available (96%+) — safe to use without fallback.

Reference: [modern-css.com](https://modern-css.com)

### 1.14 Positioning Shorthand Without Four Properties

Writing `top: 0; right: 0; bottom: 0; left: 0;` to stretch an element to its container is verbose and error-prone. The `inset` shorthand replaces all four in a single declaration, following the same 1-to-4-value pattern as `margin` and `padding`.

**Avoid (four directional properties):**

```css
.overlay {
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
}

.inset-box {
  position: fixed;
  top: 16px;
  right: 24px;
  bottom: 16px;
  left: 24px;
}
```

**Prefer (inset shorthand):**

```css
.overlay {
  position: absolute;
  inset: 0;
}

/* top/bottom 16px, left/right 24px */
.inset-box {
  position: fixed;
  inset: 16px 24px;
}
```

`inset` accepts 1–4 values using the same shorthand logic as `margin`: `inset: top right bottom left`, `inset: block inline`, or `inset: all`. You can also use the logical equivalents `inset-block` and `inset-inline` for internationalization-ready positioning.

```css
/* Logical property equivalents */
.sidebar {
  position: absolute;
  inset-block: 0; /* top and bottom */
  inset-inline-start: 0; /* left in LTR, right in RTL */
  inline-size: 280px;
}
```

✅ Widely available — supported in all major browsers.

Reference: [MDN — inset](https://developer.mozilla.org/en-US/docs/Web/CSS/inset)

### 1.15 Direction-Aware Layouts Without Left and Right

Physical properties like `margin-left` and `padding-right` assume a left-to-right writing direction. Supporting RTL languages requires duplicate overrides with `[dir="rtl"]` selectors. Logical properties adapt automatically to the document's writing mode and direction — one declaration works for every language.

**Avoid (physical properties with RTL overrides):**

```css
.sidebar {
  margin-left: 1rem;
  padding-right: 1rem;
  border-top: 1px solid #ddd;
}

[dir='rtl'] .sidebar {
  margin-left: 0;
  margin-right: 1rem;
  padding-right: 0;
  padding-left: 1rem;
}
```

**Prefer (logical properties):**

```css
.sidebar {
  margin-inline-start: 1rem;
  padding-inline-end: 1rem;
  border-block-start: 1px solid #ddd;
}
/* No RTL override needed — adapts automatically */
```

**Logical property mapping:**

| Physical           | Logical               |
| ------------------ | --------------------- |
| `margin-left`      | `margin-inline-start` |
| `margin-right`     | `margin-inline-end`   |
| `padding-top`      | `padding-block-start` |
| `padding-bottom`   | `padding-block-end`   |
| `border-left`      | `border-inline-start` |
| `border-right`     | `border-inline-end`   |
| `top`              | `inset-block-start`   |
| `left`             | `inset-inline-start`  |
| `width`            | `inline-size`         |
| `height`           | `block-size`          |
| `text-align: left` | `text-align: start`   |

Use logical properties by default in all new CSS. They cost nothing in browsers that only serve LTR content and make the codebase RTL-ready without any refactoring later.

✅ Widely available (~96%). Supported in all major browsers.

Reference: [modern-css.com](https://modern-css.com)

### 1.16 Modal Dialogs Without a JavaScript Library

Custom modals built with `<div>` overlays require managing z-index stacking, scroll locking, focus trapping, ESC key handling, and backdrop click-to-close — often pulling in a library or 50+ lines of JavaScript. The native `<dialog>` element with `showModal()` handles all of this out of the box.

**Avoid (custom overlay + JavaScript):**

```css
.overlay {
  position: fixed;
  inset: 0;
  z-index: 999;
  background: rgb(0 0 0 / 0.5);
  display: none;
}
.overlay.open {
  display: flex;
  align-items: center;
  justify-content: center;
}
.modal {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  z-index: 1000;
}
```

```js
// JS: open/close, ESC key, focus trap, scroll lock, click-outside
overlay.addEventListener('click', (e) => {
  if (e.target === overlay) close();
});
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') close();
});
// + focus trap logic (first/last focusable element cycling)
// + document.body.style.overflow = 'hidden'
```

**Prefer (native `<dialog>`):**

```html
<dialog id="my-dialog">
  <h2>Dialog Title</h2>
  <p>Content goes here.</p>
  <button onclick="this.closest('dialog').close()">Close</button>
</dialog>

<button onclick="document.getElementById('my-dialog').showModal()">Open</button>
```

```css
dialog {
  padding: 1.5rem;
  border: none;
  border-radius: 8px;
  max-width: min(90vw, 500px);
}

dialog::backdrop {
  background: rgb(0 0 0 / 0.5);
}
```

The browser provides for free:

- **Focus trapping** — Tab cycles within the dialog while open.
- **ESC to close** — Built-in keyboard dismissal.
- **Backdrop** — The `::backdrop` pseudo-element renders above all other content.
- **Top layer** — `showModal()` places the dialog in the top layer, above all z-index stacking contexts.
- **Scroll lock** — The page behind the dialog does not scroll.
- **Inert background** — Content behind the dialog is non-interactive.
- **`aria-modal`** — Implicit accessibility semantics.

**Styling the backdrop animation:**

```css
dialog[open]::backdrop {
  background: rgb(0 0 0 / 0.5);
  animation: fade-in 200ms ease-out;
}

@keyframes fade-in {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}
```

**Non-modal dialogs** (no backdrop, no focus trap) use `.show()` instead of `.showModal()` — useful for tooltips or side panels that don't block interaction with the rest of the page.

✅ Widely available (~96%). Use freely — the native `<dialog>` element is supported in all major browsers.

Reference: [modern-css.com](https://modern-css.com) · [MDN — dialog element](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/dialog)

### 1.17 Responsive Images Without the Background-Image Hack

Using `background-image` with `background-size: cover` on empty `<div>` elements loses semantics, accessibility (`alt` text), native lazy loading, and `<picture>` / `srcset` support. The `object-fit` property gives `<img>` elements the same cropping and sizing behavior while keeping all the benefits of a real image element.

**Avoid (background-image hack):**

```css
.card-image {
  background-image: url('hero.jpg');
  background-size: cover;
  background-position: center;
  width: 100%;
  height: 200px;
}
```

```html
<div class="card-image"></div>
<!-- no alt text, no lazy loading, no srcset -->
```

**Prefer (object-fit on a real image):**

```css
.card-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
  object-position: center;
}
```

```html
<img class="card-image" src="hero.jpg" alt="Description of the image" loading="lazy" />
```

`object-fit` accepts the same keywords as `background-size` — `cover`, `contain`, `fill`, `none`, and `scale-down`. Pair it with `object-position` to control the focal point, just like `background-position`.

✅ Widely available (~96%). No fallback needed.

Reference: [modern-css.com](https://modern-css.com)

### 1.18 Preventing Scroll Chaining Without JavaScript

When a user scrolls to the end of a scrollable element (like a modal or sidebar), the browser "chains" the scroll to the parent — causing the page behind a modal to scroll. The old fix was intercepting `wheel` and `touchmove` events in JavaScript with `preventDefault()`, which blocks the main thread, fights passive listener defaults, and is fragile across input methods. `overscroll-behavior: contain` solves this declaratively with zero JavaScript.

**Avoid (JavaScript wheel/touch event prevention):**

```js
// Block page scroll when inside modal
modal.addEventListener(
  'wheel',
  (e) => {
    const atTop = modal.scrollTop === 0;
    const atBottom = modal.scrollTop + modal.clientHeight >= modal.scrollHeight;
    if ((e.deltaY < 0 && atTop) || (e.deltaY > 0 && atBottom)) {
      e.preventDefault();
    }
  },
  {passive: false}, // must opt out of passive to call preventDefault
);

// Also need touchmove handling for mobile
modal.addEventListener(
  'touchmove',
  (e) => {
    /* similar logic */
  },
  {passive: false},
);
```

**Prefer (modern CSS):**

```css
.modal-content {
  overflow-y: auto;
  overscroll-behavior: contain;
}
/* Page stays still when modal scroll reaches the boundary */
```

### Common use cases

```css
/* Modal / dialog — prevent background scroll chaining */
dialog {
  overscroll-behavior: contain;
}

/* Chat panel / sidebar — keep scroll isolated */
.chat-messages {
  overflow-y: auto;
  overscroll-behavior-y: contain;
}

/* Pull-to-refresh opt-out on a specific container */
.custom-scroll-area {
  overscroll-behavior-y: none;
}
```

### Values

| Value     | Behavior                                                            |
| --------- | ------------------------------------------------------------------- |
| `auto`    | Default — scroll chains to ancestor when boundary is reached        |
| `contain` | Scroll stops at the element boundary, no chaining                   |
| `none`    | Same as `contain`, and also prevents overscroll glow/bounce effects |

`overscroll-behavior` is a shorthand for `overscroll-behavior-x` and `overscroll-behavior-y`. Use the axis-specific property when you only need to contain one direction.

✅ Widely available (~96%). Supported in all major browsers. No fallback needed.

Reference: [modern-css.com](https://modern-css.com) · [MDN — overscroll-behavior](https://developer.mozilla.org/en-US/docs/Web/CSS/overscroll-behavior)

### 1.19 Dropdown Menus Without JavaScript Toggles

Building a dropdown menu traditionally requires JavaScript for toggling visibility, closing on outside click, closing on Escape, managing `aria-expanded`, and stacking context. The Popover API (`[popover]` + `[popovertarget]`) provides all of this behavior natively — light dismiss, top-layer stacking, focus management, and keyboard support — with zero JavaScript.

**Avoid (JavaScript toggle with manual event handling):**

```css
.menu {
  display: none;
}
.menu.open {
  display: block;
}
```

```js
// Open/close toggle
btn.addEventListener('click', () => {
  menu.classList.toggle('open');
});

// Close on outside click
document.addEventListener('click', (e) => {
  if (!menu.contains(e.target) && e.target !== btn) {
    menu.classList.remove('open');
  }
});

// Close on Escape
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') menu.classList.remove('open');
});

// Manually manage aria-expanded…
```

**Prefer (Popover API):**

```html
<button popovertarget="menu">Options ▾</button>

<div id="menu" popover>
  <ul role="menu">
    <li role="menuitem"><a href="/settings">Settings</a></li>
    <li role="menuitem"><a href="/profile">Profile</a></li>
    <li role="menuitem"><button>Sign out</button></li>
  </ul>
</div>
```

```css
#menu[popover] {
  /* Renders in the top layer — no z-index battles */
  margin: 0;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 0.5rem;
  box-shadow: 0 4px 12px rgb(0 0 0 / 0.1);

  /* Position relative to the trigger */
  position: absolute;
  inset: unset;
}
```

The browser automatically handles:

- **Toggle on click** — clicking the `[popovertarget]` button opens/closes the popover.
- **Light dismiss** — clicking outside or pressing Escape closes the popover.
- **Top layer rendering** — the popover sits above all other content (no `z-index` needed).
- **Accessibility** — proper focus management and screen reader announcements.

### Popover variants

```html
<!-- Auto (default) — light dismiss, only one open at a time -->
<div id="menu" popover>…</div>
<div id="menu" popover="auto">…</div>

<!-- Manual — must be explicitly closed, multiple can coexist -->
<div id="panel" popover="manual">…</div>
```

### Styling open/closed states

```css
[popover] {
  /* Closed state — the browser handles hiding */
  opacity: 0;
  transition:
    opacity 0.2s,
    overlay 0.2s,
    display 0.2s;
  transition-behavior: allow-discrete;
}

[popover]:popover-open {
  opacity: 1;
}

/* Entry animation */
[popover] {
  @starting-style {
    opacity: 0;
  }
}
```

### Styling the backdrop

```css
[popover]::backdrop {
  background: rgb(0 0 0 / 0.15);
  backdrop-filter: blur(2px);
}
```

✅ Widely available (~86%). The Popover API is supported in all modern browsers. No polyfill needed for new projects.

Reference: [modern-css.com](https://modern-css.com) · [MDN — Popover API](https://developer.mozilla.org/en-US/docs/Web/API/Popover_API)

### 1.20 Hover Tooltips Without JavaScript Events

Building hover tooltips traditionally requires JavaScript `mouseenter`, `mouseleave`, `focus`, `blur` listeners, positioning logic, and `aria-describedby` wiring. The `popover=hint` type combined with the `interesttarget` attribute provides native hover/focus tooltip behavior — including show delay, graceful dismissal, and accessibility — with zero JavaScript.

**Avoid (JavaScript event listeners):**

```js
const btn = document.querySelector('.trigger');
const tip = document.querySelector('.tooltip');
let timeout;

btn.addEventListener('mouseenter', () => {
  timeout = setTimeout(() => showTooltip(btn, tip), 200);
});
btn.addEventListener('mouseleave', () => {
  clearTimeout(timeout);
  tip.hidden = true;
});
btn.addEventListener('focus', () => showTooltip(btn, tip));
btn.addEventListener('blur', () => (tip.hidden = true));

function showTooltip(anchor, tooltip) {
  // + positioning logic (getBoundingClientRect, viewport checks)
  tooltip.hidden = false;
}
```

```css
.tooltip {
  position: fixed;
  z-index: 9999;
  background: #333;
  color: white;
  padding: 0.5rem 0.75rem;
  border-radius: 4px;
  font-size: 0.875rem;
}
```

**Prefer (popover hint with interesttarget):**

```html
<button interesttarget="tip">Hover me</button>

<div id="tip" popover="hint">Tooltip content goes here</div>
```

```css
[popover='hint'] {
  margin: 0;
  padding: 0.5rem 0.75rem;
  background: #333;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 0.875rem;
  max-inline-size: 250px;
}
```

The browser handles:

- **Show on hover/focus** — appears after a brief delay when hovering or focusing the trigger.
- **Hide on leave** — gracefully dismisses when the pointer moves away.
- **Light dismiss** — pressing Escape closes the tooltip.
- **Top layer** — renders above all other content, no `z-index` battles.
- **Accessibility** — proper association between trigger and tooltip for screen readers.

### Popover type comparison

| Type               | Trigger          | Light dismiss | Multiple open |
| ------------------ | ---------------- | ------------- | ------------- |
| `popover="auto"`   | Click            | Yes           | No            |
| `popover="hint"`   | Hover / focus    | Yes           | With auto     |
| `popover="manual"` | Explicit JS only | No            | Yes           |

### With anchor positioning for precise placement

```css
.trigger {
  anchor-name: --tip-anchor;
}

[popover='hint'] {
  position: fixed;
  position-anchor: --tip-anchor;
  inset-area: top;
  margin-bottom: 6px;
  position-try-fallbacks: flip-block;
}
```

### Styling the open state with animation

```css
[popover='hint'] {
  opacity: 0;
  transition:
    opacity 0.15s ease-out,
    overlay 0.15s,
    display 0.15s;
  transition-behavior: allow-discrete;
}

[popover='hint']:popover-open {
  opacity: 1;
}

[popover='hint'] {
  @starting-style {
    opacity: 0;
  }
}
```

`popover=hint` is specifically designed for non-interactive, informational content that appears on hover or focus — exactly the tooltip pattern. For interactive popup content (menus, pickers), use `popover="auto"` with a click trigger instead.

🟡 Newly available (~86%). The `interesttarget` attribute and `popover="hint"` are shipping across modern browsers. For older browsers, a simple CSS `:hover` + `:focus-visible` fallback provides a baseline tooltip experience.

Reference: [modern-css.com](https://modern-css.com) · [MDN — Popover API](https://developer.mozilla.org/en-US/docs/Web/API/Popover_API)

### 1.21 Media Query Ranges Without min-width and max-width

The traditional `min-width` and `max-width` media query syntax is verbose, easy to get wrong at boundaries (the classic `max-width: 599px` vs `min-width: 600px` off-by-one), and unreadable when combined with `and`. The range syntax uses familiar comparison operators (`<`, `<=`, `>`, `>=`) and supports chained ranges in a single expression.

**Avoid (min/max with `and`):**

```css
/* Single bound */
@media (min-width: 600px) {
  .sidebar {
    display: block;
  }
}

/* Range — verbose, error-prone boundary */
@media (min-width: 600px) and (max-width: 1200px) {
  .container {
    max-width: 960px;
  }
}

/* Exclusive upper bound — off-by-one risk */
@media (max-width: 599px) {
  .nav {
    display: none;
  }
}
```

**Prefer (range syntax):**

```css
/* Single bound */
@media (width >= 600px) {
  .sidebar {
    display: block;
  }
}

/* Range — clear, chainable */
@media (600px <= width <= 1200px) {
  .container {
    max-width: 960px;
  }
}

/* Exclusive upper bound — no off-by-one */
@media (width < 600px) {
  .nav {
    display: none;
  }
}
```

**Works with other features too:**

```css
/* Height ranges */
@media (400px <= height <= 800px) {
  .hero {
    padding-block: 2rem;
  }
}

/* Resolution / pixel density */
@media (resolution >= 2dppx) {
  .logo {
    background-image: url('logo@2x.png');
  }
}

/* Aspect ratio */
@media (aspect-ratio > 16/9) {
  .cinematic {
    display: block;
  }
}
```

The range syntax eliminates the off-by-one trap entirely — `<` vs `<=` makes boundaries explicit. It also reads like a math expression, making complex queries self-documenting.

✅ Widely available (~94%). Supported in all modern browsers.

Reference: [modern-css.com](https://modern-css.com) · [MDN — Media query range syntax](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_media_queries/Using_media_queries#syntax_improvements_in_level_4)

### 1.22 Carousel Navigation Without a JavaScript Library

JavaScript carousel libraries like Swiper and Slick provide prev/next buttons and pagination dots, but they rebuild the entire scroll experience from scratch — adding bundle weight, DOM manipulation, and touch event handlers. The `::scroll-button()` and `::scroll-marker` pseudo-elements add native navigation controls on top of CSS Scroll Snap with zero JavaScript.

**Avoid (JavaScript carousel library for navigation):**

```js
// Swiper.js or Slick carousel
import Swiper from 'swiper';

new Swiper('.carousel', {
  navigation: {
    nextEl: '.swiper-button-next',
    prevEl: '.swiper-button-prev',
  },
  pagination: {
    el: '.swiper-pagination',
    clickable: true,
  },
});
// + custom DOM elements for buttons and dots
// + resize observers, scroll handlers, active state management
```

**Prefer (CSS scroll markers and buttons):**

```css
.carousel {
  display: flex;
  overflow-x: auto;
  scroll-snap-type: x mandatory;
  gap: 1rem;
}

.carousel > * {
  scroll-snap-align: start;
  flex-shrink: 0;
}

/* Prev / Next buttons — browser-generated */
.carousel::scroll-button(left) {
  content: '←';
}

.carousel::scroll-button(right) {
  content: '→';
}

/* Pagination dots — one per snap child */
.carousel > li::scroll-marker {
  content: '';
  display: inline-block;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: #ccc;
}

/* Active dot styling */
.carousel > li::scroll-marker:target-current {
  background: var(--accent, #333);
}
```

### How it works

- `::scroll-button(left)` and `::scroll-button(right)` generate prev/next navigation buttons that scroll the container by one snap interval. The browser handles scroll animation and disabling at boundaries.
- `::scroll-marker` generates a pagination indicator for each child element. Clicking a marker scrolls to the associated item.
- `:target-current` on a `::scroll-marker` targets the currently snapped/visible item — no JavaScript active-state management needed.

### Styling the scroll marker group

```css
.carousel::scroll-marker-group {
  display: flex;
  gap: 0.5rem;
  justify-content: center;
  padding-block: 0.75rem;
}
```

### Combining with scroll snap

These pseudo-elements are designed to work on top of CSS Scroll Snap (`scroll-snap-type` + `scroll-snap-align`). They do not replace scroll snap — they enhance it with navigation UI. See `layout-scroll-snap` for the base scroll snap setup.

🟡 Newly available (~72%). Support is shipping progressively in Chromium browsers. Use as a progressive enhancement layer — the underlying scroll snap carousel works without these pseudo-elements, and JavaScript carousel controls can serve as a fallback.

Reference: [modern-css.com](https://modern-css.com) · [CSS Overflow Level 5 — Scroll Markers](https://drafts.csswg.org/css-overflow-5/#scroll-markers)

### 1.23 Scroll Snapping Without a Carousel Library

JavaScript carousel libraries like Slick, Swiper, and Flickity rebuild scroll behavior from scratch — adding bundle weight, touch event listeners, and DOM manipulation. CSS Scroll Snap provides native, GPU-accelerated snap points with momentum scrolling, accessibility, and touch support built in.

**Avoid (JavaScript carousel library):**

```js
// Slick, Swiper, or custom scroll/touch handlers
import Swiper from 'swiper';

new Swiper('.carousel', {
  slidesPerView: 'auto',
  spaceBetween: 16,
  navigation: {next: '.next', prev: '.prev'},
  pagination: {el: '.dots'},
});
// + touch handlers, resize observers, DOM cloning for "infinite" mode
```

**Prefer (CSS Scroll Snap):**

```css
.carousel {
  display: flex;
  gap: 16px;
  overflow-x: auto;
  scroll-snap-type: x mandatory;
  scroll-padding-inline: 16px; /* inset snap points for peek effect */
  -webkit-overflow-scrolling: touch;
}

.carousel > * {
  scroll-snap-align: start;
  flex-shrink: 0;
}
```

**Snap alignment options:**

```css
/* Snap to the start edge of each item */
.item {
  scroll-snap-align: start;
}

/* Snap to the center — good for "focus" carousels */
.item {
  scroll-snap-align: center;
}

/* Snap to the end edge */
.item {
  scroll-snap-align: end;
}
```

**Mandatory vs. proximity:**

```css
/* mandatory — always snaps to the nearest snap point after scroll */
.container {
  scroll-snap-type: x mandatory;
}

/* proximity — only snaps when near a snap point (more natural for long lists) */
.container {
  scroll-snap-type: x proximity;
}

/* Both axes */
.grid-container {
  scroll-snap-type: both mandatory;
}
```

**Vertical scroll snapping (full-page sections):**

```css
.page {
  height: 100dvh;
  overflow-y: auto;
  scroll-snap-type: y mandatory;
}

.page > section {
  height: 100dvh;
  scroll-snap-align: start;
}
```

**Preventing overscroll bounce at boundaries:**

```css
.carousel {
  scroll-snap-type: x mandatory;
  overscroll-behavior-x: contain; /* no page navigation on swipe past ends */
}
```

For navigation buttons and pagination dots on top of CSS Scroll Snap, see `layout-scroll-markers` (using `::scroll-button()` and `::scroll-marker` pseudo-elements).

✅ Widely available (~96%). Native momentum scrolling, keyboard-accessible, and works with assistive technology — no library needed.

Reference: [modern-css.com](https://modern-css.com) · [MDN: CSS Scroll Snap](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_scroll_snap)

### 1.24 Preventing Layout Shift From Scrollbar Appearance

When content grows long enough to trigger a scrollbar, the page content shifts left to make room for it. This causes a visible layout jump — especially noticeable on navigations between pages with and without scrollbars. The old workarounds either force a permanent scrollbar or hardcode a pixel offset.

**Avoid (always-visible scrollbar or hardcoded padding):**

```css
/* Forces scrollbar even on short pages — ugly */
body {
  overflow-y: scroll;
}

/* Or hardcode the scrollbar width — fragile, OS-dependent */
body {
  padding-right: 17px;
}
```

Both approaches are brittle. Classic scrollbar widths vary between operating systems (15–17px on Windows, overlay on macOS), and forcing a visible scrollbar on short content looks broken.

**Prefer (modern CSS):**

```css
body {
  scrollbar-gutter: stable;
}
```

The browser reserves space for the scrollbar track whether or not the content overflows. No layout shift, no hardcoded widths, and overlay scrollbars (macOS default) are unaffected — the gutter collapses to zero automatically.

**Both-edges variant** for symmetrical layouts:

```css
body {
  scrollbar-gutter: stable both-edges;
}
/* Reserves equal space on both sides — keeps content perfectly centered */
```

**Common use cases:**

```css
/* Page-level — prevent shift between route changes */
html {
  scrollbar-gutter: stable;
}

/* Modal or sidebar scroll containers */
.modal-body {
  overflow-y: auto;
  scrollbar-gutter: stable;
}
```

`scrollbar-gutter` only affects classic (non-overlay) scrollbars. On systems that use overlay scrollbars by default (e.g. macOS), it has no visible effect — which is the correct behavior since overlay scrollbars don't cause layout shift.

✅ Widely available (~90%). Safe to use without fallback.

Reference: [modern-css.com](https://modern-css.com) · [MDN — scrollbar-gutter](https://developer.mozilla.org/en-US/docs/Web/CSS/scrollbar-gutter)

### 1.25 Scrollbar Styling Without -webkit- Pseudo-Elements

The `::-webkit-scrollbar` family of pseudo-elements only works in Chromium and Safari, requires multiple selectors to style different parts, and produces inconsistent results across engines. The standard `scrollbar-width` and `scrollbar-color` properties provide cross-browser scrollbar customization in two lines.

**Avoid (webkit-only pseudo-elements):**

```css
/* Chromium and Safari only */
::-webkit-scrollbar {
  width: 8px;
}
::-webkit-scrollbar-track {
  background: transparent;
}
::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
  background: #555;
}
/* Firefox and other engines ignore all of this */
```

**Prefer (standard properties):**

```css
* {
  scrollbar-width: thin;
  scrollbar-color: #888 transparent;
  /* thumb-color  track-color */
}
```

### Values for `scrollbar-width`

| Value  | Description                                      |
| ------ | ------------------------------------------------ |
| `auto` | Default platform scrollbar width                 |
| `thin` | Narrower scrollbar (platform decides exact size) |
| `none` | Hides scrollbar but keeps content scrollable     |

### Scoped to specific containers

```css
.sidebar {
  overflow-y: auto;
  scrollbar-width: thin;
  scrollbar-color: oklch(0.6 0.02 250) transparent;
}
```

### Dark mode aware

```css
.scrollable {
  scrollbar-width: thin;
  scrollbar-color: light-dark(#aaa, #555) transparent;
}
```

The standard properties give you less granular control than the webkit pseudo-elements (no separate hover states, no border-radius on the thumb), but they work everywhere and cover the vast majority of scrollbar customization needs. If you need pixel-perfect scrollbar designs, consider a CSS-only approach with `scrollbar-color` as the baseline and `::-webkit-scrollbar` as a progressive enhancement for Chromium/Safari.

🟡 Newly available (~75%). Firefox has supported these since 2018; Chromium and Safari added support more recently. Use as a progressive enhancement — the default scrollbar is a fine fallback.

Reference: [modern-css.com](https://modern-css.com) · [MDN — scrollbar-color](https://developer.mozilla.org/en-US/docs/Web/CSS/scrollbar-color)

### 1.26 Path Shapes Without SVG Clip Paths

The `clip-path: path()` function only accepts pixel values, making shapes non-responsive — they break at different sizes and require manual recalculation for every breakpoint. The `shape()` function accepts percentage-based coordinates, making clip paths fluid and responsive by default.

**Avoid (pixel-based path — not responsive):**

```css
.hero {
  clip-path: path('M 0 0 L 800 0 L 800 400 Q 400 500 0 400 Z');
  /* Fixed pixel values — breaks on resize */
}
```

Or relying on an inline SVG `<clipPath>` element:

```html
<svg width="0" height="0">
  <defs>
    <clipPath id="wave" clipPathUnits="objectBoundingBox">
      <path d="M0,0 L1,0 L1,0.8 Q0.5,1.05 0,0.8 Z" />
    </clipPath>
  </defs>
</svg>
```

```css
.hero {
  clip-path: url(#wave);
  /* Requires hidden SVG in the DOM — extra markup, fragile references */
}
```

**Prefer (shape() with percentage-based coordinates):**

```css
.hero {
  clip-path: shape(from 0% 0%, line to 100% 0%, line to 100% 80%, curve to 0% 80% via 50% 105%);
  /* Fully responsive — scales with the element */
}
```

### Shape commands

The `shape()` function uses drawing commands similar to SVG path syntax but with CSS values:

```css
.badge {
  clip-path: shape(
    from 50% 0%,
    line to 100% 35%,
    line to 82% 100%,
    line to 18% 100%,
    line to 0% 35%,
    close
  );
}
```

| Command  | Description                                            |
| -------- | ------------------------------------------------------ |
| `from`   | Starting point of the shape                            |
| `line`   | Straight line to a point                               |
| `curve`  | Cubic or quadratic Bézier curve (`via` control points) |
| `smooth` | Smooth continuation of a previous curve                |
| `arc`    | Elliptical arc to a point                              |
| `close`  | Closes the path back to the starting point             |

### Mixing units

Because `shape()` accepts CSS values, you can mix units and use `calc()`:

```css
.notch {
  clip-path: shape(
    from 0% 0%,
    line to calc(50% - 40px) 0%,
    line to 50% 20px,
    line to calc(50% + 40px) 0%,
    line to 100% 0%,
    line to 100% 100%,
    line to 0% 100%,
    close
  );
}
```

The `shape()` function is the CSS-native answer to responsive clipping. Unlike `path()`, it uses the element's own coordinate system with percentage values, so shapes scale naturally without JavaScript or SVG dependencies.

🟡 Newly available (~85%). Supported in modern Chromium and Firefox. Use behind `@supports (clip-path: shape(from 0% 0%, line to 100% 100%))` with a `polygon()` or `path()` fallback if needed.

Reference: [modern-css.com](https://modern-css.com) · [MDN — shape()](https://developer.mozilla.org/en-US/docs/Web/CSS/basic-shape/shape)

### 1.27 Sticky Headers Without JavaScript Scroll Listeners

JavaScript scroll listeners that read `getBoundingClientRect()` and toggle a `.fixed` class force synchronous layout on every frame. `position: sticky` is declarative, GPU-composited, and requires zero JavaScript.

**Avoid (JavaScript scroll listener):**

```js
// JS: scroll listener + getBoundingClientRect
// then add/remove .fixed class
window.addEventListener('scroll', () => {
  const rect = header.getBoundingClientRect();
  header.classList.toggle('fixed', rect.top <= 0);
});
```

```css
.header.fixed {
  position: fixed;
  top: 0;
  width: 100%;
  z-index: 10;
}
```

**Prefer (modern CSS):**

```css
.header {
  position: sticky;
  top: 0;
  z-index: 10;
}
```

No JavaScript, no layout thrashing, no class toggling. The element sticks in its natural document flow and respects its containing block.

**Nested sticky elements** work too — each sticky element sticks within its own scroll container or containing block:

```css
.sidebar {
  position: sticky;
  top: 1rem;
  align-self: start; /* important inside grid/flex parents */
}
```

✅ Widely available (~96%). Use freely.

Reference: [modern-css.com](https://modern-css.com) · [MDN position: sticky](https://developer.mozilla.org/en-US/docs/Web/CSS/position#sticky)

### 1.28 Filling Available Space Without calc Workarounds

When an element needs to fill its container while respecting its own margins, the old approach was `width: calc(100% - …)` or `width: 100%` (which overflows with margins). The `stretch` keyword tells the browser to fill the available space automatically, accounting for margins, padding, and borders.

**Avoid (calc or overflow):**

```css
.full {
  width: calc(100% - 40px);
  /* fragile — must manually match the margin sum */
}

/* or worse: */
.full {
  width: 100%;
  /* overflows container when margins are present */
}
```

**Prefer (modern CSS):**

```css
.full {
  width: stretch;
  margin-inline: 20px;
  /* fills container minus margins — no math needed */
}
```

`stretch` works for `width`, `height`, `min-width`, `min-height`, `max-width`, and `max-height`. The browser handles the subtraction automatically, so layouts stay correct even when margins or padding change.

✅ Widely available (~90%). Previously required `-webkit-fill-available` / `-moz-available` prefixes — the unprefixed `stretch` keyword is now supported across modern browsers.

Reference: [modern-css.com](https://modern-css.com)

### 1.29 Aligning Nested Grids Without Duplicating Tracks

When a child grid needs to align its content with the parent grid's columns or rows, the old approach was to duplicate the parent's `grid-template-columns` definition in the child. This creates a maintenance burden — every change to the parent tracks must be mirrored in every child. `subgrid` lets a nested grid inherit track sizing from its parent, keeping everything aligned with zero duplication.

**Avoid (duplicating parent tracks in child):**

```css
.parent-grid {
  display: grid;
  grid-template-columns: 200px 1fr 1fr;
  gap: 16px;
}

.child-grid {
  display: grid;
  grid-column: 1 / -1;
  /* Must manually duplicate parent tracks — breaks when parent changes */
  grid-template-columns: 200px 1fr 1fr;
  gap: 16px;
}
```

**Prefer (subgrid inherits parent tracks):**

```css
.parent-grid {
  display: grid;
  grid-template-columns: 200px 1fr 1fr;
  gap: 16px;
}

.child-grid {
  display: grid;
  grid-column: 1 / -1;
  grid-template-columns: subgrid;
  /* Inherits parent's column tracks — always in sync */
}
```

### Common use case: card grids with aligned content

Cards in a grid often have headers, bodies, and footers that should align across cards. Without subgrid, each card sizes its rows independently:

```css
.card-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

.card {
  display: grid;
  grid-row: span 3;
  grid-template-rows: subgrid;
  /* Header, body, and footer rows align across all cards */
}
```

`subgrid` works for both `grid-template-columns` and `grid-template-rows`, and the child still participates in the parent's gap. You can subgrid one axis while defining the other independently.

🟡 Newly available (~88%). Supported in all modern browsers since late 2023. For older browsers, duplicating tracks is a safe fallback.

Reference: [modern-css.com](https://modern-css.com) · [MDN — subgrid](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_grid_layout/Subgrid)

### 1.30 Scaling Elements Without Transform Hacks

`transform: scale()` visually resizes an element but does not affect its layout box — the element still occupies its original space, forcing developers to add negative margins or other hacks to compensate. The `zoom` property scales the element _and_ its layout box together, so surrounding content reflows naturally without any compensation.

**Avoid (transform scale with margin hack):**

```css
.thumb {
  transform: scale(0.5);
  margin-bottom: -50%; /* hack to collapse the leftover space */
  transform-origin: top left;
}
```

The element visually shrinks but its original bounding box remains, leaving a gap that must be manually offset. The negative margin value depends on the scale factor and the element's dimensions — fragile and hard to maintain.

**Prefer (zoom):**

```css
.thumb {
  zoom: 0.5;
}
/* Layout box shrinks with the visual — no margin hack needed */
```

### Key differences from `transform: scale()`

| Behavior                  | `transform: scale()` | `zoom`                |
| ------------------------- | -------------------- | --------------------- |
| Affects layout box        | ❌ No                | ✅ Yes                |
| Triggers reflow           | ❌ No                | ✅ Yes                |
| Needs margin compensation | ✅ Yes               | ❌ No                 |
| Sub-pixel rendering       | Smooth               | Nearest-pixel         |
| Animatable on compositor  | ✅ Yes               | ❌ No (causes reflow) |

### When to use which

```css
/* Use zoom for static scaling — layout reflows correctly */
.preview-pane {
  zoom: 0.75;
}

/* Use transform: scale() for animations — GPU-composited, no reflow */
.card:hover {
  transform: scale(1.05);
  transition: transform 0.2s ease;
}
```

`zoom` is the right choice when you want an element to physically occupy less (or more) space in the layout. `transform: scale()` remains the right choice for hover effects and animations where you _want_ the layout box to stay stable while the visual scales.

### Zoom for responsive previews

```css
/* Scale down an entire component preview without layout disruption */
.component-preview {
  zoom: 0.6;
  border: 1px solid #ddd;
  border-radius: 8px;
  overflow: hidden;
}
```

✅ Widely available (~97%). The `zoom` property was a long-standing non-standard feature in Chromium and Safari that has now been standardized and is supported across all major browsers including Firefox.

Reference: [modern-css.com](https://modern-css.com) · [MDN — zoom](https://developer.mozilla.org/en-US/docs/Web/CSS/zoom)


## 2. Workflow

### 2.1 Typed Attribute Values Without JavaScript

Reading `data-*` attributes for styling has traditionally required JavaScript — fetching the value from `el.dataset`, then applying it as an inline style. The enhanced `attr()` function with type coercion lets CSS read and use attribute values directly, with proper typing, fallback values, and no JavaScript.

**Avoid (JavaScript reading dataset):**

```js
// Read data attribute and apply as inline style
const bar = document.querySelector('.bar');
bar.style.width = bar.dataset.pct + '%';

// Or for multiple elements
document.querySelectorAll('[data-pct]').forEach((el) => {
  el.style.width = el.dataset.pct + '%';
});
// Must re-run on every DOM change, breaks SSR, adds layout thrashing
```

```html
<div class="bar" data-pct="75"></div>
```

**Prefer (enhanced `attr()` with type coercion):**

```css
.bar {
  width: attr(data-pct type(<percentage>));
}
```

```html
<div class="bar" data-pct="75%"></div>
<!-- CSS reads the value directly — no JavaScript needed -->
```

### Type coercion options

The enhanced `attr()` function supports explicit type declarations so the browser interprets the attribute value correctly:

```css
/* Percentage values */
.progress {
  width: attr(data-value type(<percentage>), 0%);
}

/* Length values */
.spacer {
  height: attr(data-gap type(<length>), 1rem);
}

/* Number values */
.grid {
  grid-template-columns: repeat(attr(data-cols type(<number>), 3), 1fr);
}

/* Color values */
.badge {
  background: attr(data-color type(<color>), gray);
}

/* Custom ident for keywords */
.layout {
  display: attr(data-display type(<custom-ident>), block);
}
```

### Fallback values

The third argument provides a fallback when the attribute is missing or cannot be parsed:

```css
.bar {
  /* If data-pct is missing or not a valid percentage, use 0% */
  width: attr(data-pct type(<percentage>), 0%);
  background: attr(data-color type(<color>), oklch(0.6 0.2 250));
}
```

### Using with `calc()` and custom properties

```css
.meter {
  --pct: attr(data-value type(<number>), 0);
  width: calc(var(--pct) * 1%);
  background: oklch(calc(0.3 + var(--pct) * 0.005) 0.2 140);
}
```

### Common patterns

```css
/* Star rating from attribute */
.stars::before {
  content: '★★★★★';
  background: linear-gradient(90deg, gold attr(data-rating type(<percentage>), 0%), #ddd 0);
  background-clip: text;
  -webkit-background-clip: text;
  color: transparent;
}

/* Dynamic grid columns from markup */
.grid {
  display: grid;
  grid-template-columns: repeat(attr(data-cols type(<number>), 3), 1fr);
  gap: attr(data-gap type(<length>), 1rem);
}
```

The enhanced `attr()` function turns HTML attributes into typed CSS values without a JavaScript intermediary. This keeps styling concerns in CSS, works with SSR/static HTML, and requires no event listeners or DOM observers to stay in sync.

🟠 Limited support (~42%). Currently shipping in Chromium. Use behind `@supports (width: attr(x type(<length>)))` with a JavaScript fallback or CSS custom property alternative for broader support.

Reference: [modern-css.com](https://modern-css.com) · [MDN — attr()](https://developer.mozilla.org/en-US/docs/Web/CSS/attr)

### 2.2 Controlling Specificity Without !important

When component styles clash with utility classes or third-party CSS, the traditional fix is to pile on more specific selectors or reach for `!important` — which then requires `!important` on every override, creating an arms race that makes stylesheets unmaintainable. `@layer` lets you define explicit priority order between groups of styles, regardless of selector specificity or source order.

**Avoid (!important escalation):**

```css
/* Base */
.card .title {
  color: #333;
}

/* Override needs higher specificity */
.page .card .title {
  color: #111;
}

/* Utility needs !important to win */
.page .card .title.special {
  color: red !important;
}

/* Now EVERYTHING needs !important to override the utility */
.page .card .title.special.active {
  color: blue !important;
}
```

**Prefer (cascade layers):**

```css
@layer base, components, utilities;

@layer base {
  h1,
  h2,
  h3 {
    margin-block: 0;
    font-weight: 600;
  }

  a {
    color: oklch(0.55 0.2 250);
  }
}

@layer components {
  .card .title {
    color: #111;
  }

  .btn {
    padding: 0.5rem 1rem;
    border-radius: 0.5rem;
  }
}

@layer utilities {
  .text-red {
    color: red;
  }

  .mt-4 {
    margin-top: 1rem;
  }
}
```

Layers declared later in the `@layer` order list always win over earlier layers, **regardless of selector specificity**. A simple `.mt-4` in the `utilities` layer beats a `.page .card .title` in `components` — no `!important` needed.

### How layer priority works

```css
@layer base, components, utilities;
/*         ↑ lowest     ↑ highest priority */
```

- Styles in `utilities` override `components`, which override `base`.
- Within the same layer, normal specificity and source order rules still apply.
- **Unlayered styles** beat all layered styles — so existing CSS that you haven't moved into layers continues to work.

### Layer ordering strategies

```css
/* Explicit order declaration (recommended) */
@layer reset, base, components, utilities;

/* Third-party CSS in its own low-priority layer */
@layer vendor, base, components, utilities;

@import url('vendor-lib.css') layer(vendor);
```

### Importing external CSS into a layer

```css
/* Third-party styles cannot override your component layer */
@import url('normalize.css') layer(reset);
@import url('some-lib.css') layer(vendor);

@layer reset, vendor, base, components, utilities;
```

### Nested layers

```css
@layer components {
  @layer card {
    .card {
      border: 1px solid #ddd;
    }
  }

  @layer button {
    .btn {
      cursor: pointer;
    }
  }
}

/* Reference nested layers with dot notation */
@layer components.card {
  .card {
    border-radius: 0.5rem;
  }
}
```

### Anonymous layers for one-off resets

```css
/* Anonymous (unnamed) layers are always lower priority than named layers */
@layer {
  * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }
}
```

### Key rules to remember

| Scenario                     | Winner                                     |
| ---------------------------- | ------------------------------------------ |
| Layer A vs. Layer B          | Whichever is declared later in the order   |
| Layered vs. unlayered        | Unlayered styles always win                |
| `!important` in layers       | Priority **reverses** — earlier layer wins |
| Same layer, same specificity | Source order (last wins)                   |

The reversal of `!important` within layers is intentional — it lets reset/base layers protect critical styles with `!important` that component layers cannot accidentally override.

✅ Widely available (~95%). Supported in all major browsers. Safe to adopt now.

Reference: [modern-css.com](https://modern-css.com) · [MDN — @layer](https://developer.mozilla.org/en-US/docs/Web/CSS/@layer)

### 2.3 Dark Mode Defaults Without Extra CSS

When implementing dark mode, developers often write dozens of `prefers-color-scheme: dark` overrides for every native form control, scrollbar, and system-chrome element — `<input>`, `<select>`, `<textarea>`, `<button>`, `<hr>`, scrollbar tracks, and more. The `color-scheme` property tells the browser to render all of these in the user's preferred color scheme automatically — no per-element overrides needed.

**Avoid (manual dark mode overrides for every control):**

```css
@media (prefers-color-scheme: dark) {
  input,
  select,
  textarea,
  button {
    background-color: #1e1e1e;
    color: #eee;
    border-color: #555;
  }

  hr {
    border-color: #444;
  }

  /* scrollbars, focus rings, selection colors, etc. — all need manual overrides */
}
```

This is tedious, incomplete (you'll miss controls), and fights the browser's default styles instead of embracing them.

**Prefer (modern CSS):**

```css
:root {
  color-scheme: light dark;
}
```

One line. The browser switches all native UI elements — form controls, scrollbars, `<hr>`, focus rings, system colors (`Canvas`, `CanvasText`, `LinkText`, etc.) — to match the user's `prefers-color-scheme` preference automatically.

### How it works

`color-scheme` declares which color schemes the page supports. The browser then:

1. Renders all native controls in the user's preferred scheme.
2. Adjusts system colors (`Canvas`, `CanvasText`, etc.) to match.
3. Applies the correct default background and text color to the page.

### Values

```css
/* Support both light and dark — browser follows OS preference */
:root {
  color-scheme: light dark;
}

/* Light only — native controls always render in light mode */
:root {
  color-scheme: light;
}

/* Dark only — native controls always render in dark mode */
:root {
  color-scheme: dark;
}

/* Per-element override — useful for always-dark headers or footers */
.dark-header {
  color-scheme: dark;
}
```

### Combining with custom styles

`color-scheme` handles native/system UI. Your custom-styled elements still need `prefers-color-scheme` or `light-dark()` for custom properties and colors:

```css
:root {
  color-scheme: light dark;

  /* Custom tokens — use light-dark() for values that change */
  --surface: light-dark(#fff, #1a1a1a);
  --text: light-dark(#111, #eee);
  --border: light-dark(#ddd, #333);
}

body {
  background: var(--surface);
  color: var(--text);
}
```

### Per-element scoping

Apply `color-scheme` to specific subtrees when parts of the page should always use a specific scheme:

```css
/* Page follows OS preference */
:root {
  color-scheme: light dark;
}

/* This section is always dark, regardless of OS preference */
.promo-banner {
  color-scheme: dark;
  background: #111;
  color: #eee;
}

/* This form is always light */
.print-form {
  color-scheme: light;
}
```

### HTML meta tag alternative

For the fastest possible render (before CSS loads), declare the color scheme in the HTML `<head>`:

```html
<meta name="color-scheme" content="light dark" />
```

This prevents a flash of the wrong color scheme during page load.

`color-scheme` is the foundation of dark mode support. Set it first, then layer custom color overrides on top with `light-dark()` (see `color-light-dark`) and custom properties. See also `workflow-registered-properties` for typed custom properties that can transition between themes.

✅ Widely available (~93%). Supported in all modern browsers. No fallback needed.

Reference: [modern-css.com](https://modern-css.com) · [MDN — color-scheme](https://developer.mozilla.org/en-US/docs/Web/CSS/color-scheme)

### 2.4 Lazy Rendering Without IntersectionObserver

Deferring rendering of off-screen content traditionally requires setting up an `IntersectionObserver` in JavaScript — creating the observer, defining thresholds, observing elements, swapping placeholders, and cleaning up. The `content-visibility: auto` property tells the browser to skip layout and paint for off-screen elements automatically, with zero JavaScript.

**Avoid (JavaScript IntersectionObserver):**

```js
const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        renderContent(entry.target);
        observer.unobserve(entry.target);
      }
    });
  },
  {rootMargin: '200px'},
);

document.querySelectorAll('.section').forEach((el) => observer.observe(el));
// + cleanup on unmount, placeholder sizing, loading states…
```

**Prefer (modern CSS):**

```css
.section {
  content-visibility: auto;
  contain-intrinsic-size: auto 500px;
}
```

The browser automatically skips layout, paint, and style computation for elements that are off-screen. When the user scrolls near them, the browser renders them just in time. No JavaScript, no observers, no cleanup.

### How `contain-intrinsic-size` works

Without `contain-intrinsic-size`, an element with `content-visibility: auto` would collapse to zero height when off-screen, causing the scrollbar to jump as elements enter and exit the viewport. The intrinsic size provides an estimated placeholder height:

```css
/* Fixed estimate */
.card {
  content-visibility: auto;
  contain-intrinsic-size: auto 300px;
}

/* The `auto` keyword remembers the last rendered size, so the estimate
   is only used on the first render — after that, the real size is cached */
```

### Common use cases

```css
/* Long article sections */
article > section {
  content-visibility: auto;
  contain-intrinsic-size: auto 600px;
}

/* List items in a long feed */
.feed-item {
  content-visibility: auto;
  contain-intrinsic-size: auto 120px;
}

/* Tab panels that are off-screen */
.tab-panel:not(.active) {
  content-visibility: hidden;
  /* Like display: none but preserves state (scroll position, form data) */
}
```

### `content-visibility` values

| Value     | Behavior                                                                  |
| --------- | ------------------------------------------------------------------------- |
| `visible` | Default — no containment, normal rendering                                |
| `auto`    | Off-screen elements skip rendering; on-screen elements render normally    |
| `hidden`  | Always skips rendering — like `display: none` but preserves element state |

### Performance impact

For pages with many off-screen elements (long feeds, dashboards, documentation), `content-visibility: auto` can reduce initial render time by 5–10×. The browser skips the most expensive parts of rendering (layout and paint) for content the user hasn't scrolled to yet.

### Caveats

- **Find-in-page**: Browsers still allow Ctrl+F to find text in `content-visibility: auto` elements — the browser renders them on demand when searched.
- **Anchor links**: Navigating to a `#hash` inside a hidden section triggers rendering automatically.
- **Accessibility**: Screen readers can still access the content — `content-visibility: auto` does not add `aria-hidden`.

✅ Widely available (~93%). Safe to use without fallback. Unsupporting browsers simply render everything as normal (no visual difference, just no performance optimization).

Reference: [modern-css.com](https://modern-css.com) · [web.dev — content-visibility](https://web.dev/articles/content-visibility) · [MDN — content-visibility](https://developer.mozilla.org/en-US/docs/Web/CSS/content-visibility)

### 2.5 Reusable CSS Logic Without Sass Mixins

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

### 2.6 Theme Variables Without a Preprocessor

Sass and Less variables (`$primary`, `@primary`) compile to static values — they cannot change at runtime, cannot be scoped to a subtree, and require a build step. CSS custom properties (`--primary`) are live in the browser, cascade through the DOM, can be updated with JavaScript or media queries, and need no preprocessor.

**Avoid (Sass variables — static, build-time only):**

```scss
// Sass: requires a compiler, produces static output
$primary: #7c3aed;
$surface: #ffffff;
$text: #111111;

.btn {
  background: $primary; // compiles to background: #7c3aed — frozen
  color: $surface;
}

// Theming requires generating separate stylesheets or duplicating rules
```

**Prefer (CSS custom properties — live, cascading, runtime):**

```css
:root {
  --primary: #7c3aed;
  --surface: #ffffff;
  --text: #111111;
}

.btn {
  background: var(--primary);
  color: var(--surface);
}
```

### Runtime theming with no JavaScript

```css
/* Dark mode — override at the root */
@media (prefers-color-scheme: dark) {
  :root {
    --primary: #a78bfa;
    --surface: #1a1a2e;
    --text: #eeeeee;
  }
}

/* Scoped theme — override on a subtree */
.card.danger {
  --primary: #dc2626;
  --surface: #fef2f2;
}
/* All descendants using var(--primary) pick up the scoped value */
```

### Fallback values

```css
.box {
  /* Second argument is the fallback if --accent is not defined */
  color: var(--accent, #7c3aed);

  /* Nested fallbacks */
  background: var(--card-bg, var(--surface, white));
}
```

### Combining with calc for design tokens

```css
:root {
  --space-unit: 0.25rem;
  --space-1: calc(var(--space-unit) * 1); /* 0.25rem */
  --space-2: calc(var(--space-unit) * 2); /* 0.50rem */
  --space-4: calc(var(--space-unit) * 4); /* 1.00rem */
  --space-8: calc(var(--space-unit) * 8); /* 2.00rem */
}

.card {
  padding: var(--space-4);
  gap: var(--space-2);
}
```

### JavaScript interop

```js
// Read a custom property value
const primary = getComputedStyle(document.documentElement).getPropertyValue('--primary');

// Update a custom property at runtime
document.documentElement.style.setProperty('--primary', '#2563eb');

// Scope to a specific element
card.style.setProperty('--primary', '#dc2626');
```

### When Sass variables are still appropriate

Sass variables still have a role for **build-time constants** that should never change at runtime — breakpoint values used in `@media` rules, configuration flags, or values consumed only by Sass functions. But for anything that touches the rendered page — colors, spacing, typography, component theming — CSS custom properties are the modern default.

✅ Widely available (~96%). Supported in all major browsers. No fallback needed.

Reference: [modern-css.com](https://modern-css.com) · [MDN — Using CSS custom properties](https://developer.mozilla.org/en-US/docs/Web/CSS/Using_CSS_custom_properties)

### 2.7 Inline Conditional Styles Without JavaScript

Applying conditional styles today typically requires JavaScript to toggle classes or set inline styles based on state. The CSS `if()` function evaluates conditions inline — including style queries against custom properties — and resolves to one of two values, removing the need for JavaScript class toggling in many common scenarios.

**Avoid (JavaScript class toggling):**

```js
// Toggle class based on a variant property
el.classList.toggle('primary', isPrimary);
el.classList.toggle('secondary', !isPrimary);
```

```css
.btn {
  background: gray;
}
.btn.primary {
  background: blue;
}
.btn.secondary {
  background: gray;
}
```

Or with inline styles:

```js
el.style.background = isPrimary ? 'blue' : 'gray';
```

**Prefer (CSS `if()` with style queries):**

```css
.btn {
  --variant: secondary;
  background: if(style(--variant: primary): blue; else: gray);
  color: if(style(--variant: primary): white; else: #333);
}
```

```html
<!-- Set the variant via custom property -->
<button class="btn" style="--variant: primary">Save</button>
<button class="btn">Cancel</button>
```

No JavaScript needed — the custom property drives the conditional styling directly in CSS.

### Multiple conditions

```css
.badge {
  --status: info;

  background: if(
    style(--status: success): oklch(0.75 0.18 145) ; else if
      style(--status: warning): oklch(0.8 0.16 80) ; else if
      style(--status: error): oklch(0.65 0.22 25) ; else: oklch(0.9 0.02 250)
  );
}
```

### Combining with media and supports conditions

`if()` can also evaluate media and supports conditions inline, removing the need for separate `@media` or `@supports` blocks for single-property changes:

```css
.hero {
  padding: if(media(width >= 768px): 4rem; else: 1.5rem);
}

.layout {
  display: if(supports(display: grid): grid; else: flex);
}
```

### Boolean custom property pattern

For simple on/off toggles, a boolean-style custom property keeps things clean:

```css
.card {
  --featured: false;

  border: if(style(--featured: true): 2px solid var(--accent) ; else: 1px solid #ddd);
  box-shadow: if(style(--featured: true): 0 4px 16px rgb(0 0 0 / 0.1) ; else: none);
}
```

```html
<div class="card" style="--featured: true">Featured item</div>
<div class="card">Regular item</div>
```

### Comparison with existing patterns

| Pattern                      | Requires JS | Scales to N variants | Inline |
| ---------------------------- | ----------- | -------------------- | ------ |
| Class toggling               | ✅          | ❌ (class per state) | ❌     |
| Custom property + `if()`     | ❌          | ✅                   | ✅     |
| Style queries (`@container`) | ❌          | ✅                   | ❌     |

`if()` is best suited for simple, per-property conditional values. For larger conditional blocks affecting many properties, `@container style()` queries remain more ergonomic.

🟠 Limited (~35%). The CSS `if()` function is an emerging feature with partial browser support. Use as a progressive enhancement behind `@supports` or wait for broader adoption. The JavaScript class-toggling approach remains the safe fallback.

Reference: [modern-css.com](https://modern-css.com) · [CSS Values Level 5 — if()](https://drafts.csswg.org/css-values-5/#if-notation)

### 2.8 Nesting Selectors Without Sass or Less

CSS nesting was the #1 reason teams adopted Sass or Less — writing nested selectors required a compiler, a build step, and a `node_modules` dependency. Native CSS nesting uses the same `&` syntax and works in plain `.css` files with zero tooling.

**Avoid (requires Sass compiler):**

```scss
// .scss file — requires sass/dart-sass build step
.nav {
  background: #fff;

  & a {
    color: #888;
    text-decoration: none;

    &:hover {
      color: #333;
    }
  }

  & .logo {
    font-weight: 700;
  }
}
// $ sass input.scss output.css
```

**Prefer (plain CSS — no build):**

```css
/* .css file — works natively in the browser */
.nav {
  background: #fff;

  & a {
    color: #888;
    text-decoration: none;

    &:hover {
      color: #333;
    }
  }

  & .logo {
    font-weight: 700;
  }
}
```

Same syntax, same output, no compiler, no build step, no dependency.

### Nesting rules

```css
/* Compound selectors — & is required when starting with a type selector */
.card {
  /* Class, attribute, pseudo-class — & is optional */
  .title {
    font-size: 1.25rem;
  }
  :hover {
    opacity: 0.9;
  }
  [aria-expanded] {
    border-color: blue;
  }

  /* Type selectors MUST use & */
  & h2 {
    margin: 0;
  }
  & p {
    color: #666;
  }
}
```

### Nesting media and container queries

```css
.hero {
  padding: 2rem;

  @media (width >= 768px) {
    padding: 4rem;
  }

  @container (width < 400px) {
    padding: 1rem;
  }
}
```

Media queries and container queries nest directly inside a rule block — no `&` needed. The browser scopes the query to the parent selector automatically.

### Nesting with combinators

```css
.card {
  /* Direct child */
  & > .header {
    border-bottom: 1px solid #eee;
  }

  /* Adjacent sibling */
  & + .card {
    margin-top: 1rem;
  }

  /* General sibling */
  & ~ .card {
    opacity: 0.8;
  }
}
```

### Deep nesting — keep it shallow

Native nesting supports arbitrary depth, but the same Sass best practice applies: **keep nesting to 2–3 levels max** to avoid specificity bloat and selector chains that are hard to override.

```css
/* ✅ Shallow — readable, low specificity */
.card {
  & .title {
    font-size: 1.25rem;
  }
  & .body {
    color: #444;
  }
}

/* ❌ Too deep — high specificity, hard to override */
.page {
  & .section {
    & .card {
      & .title {
        & span {
          color: red; /* specificity: 0,5,0 — hard to override without !important */
        }
      }
    }
  }
}
```

### Migrating from Sass

Most Sass nesting translates 1:1 to native CSS nesting. The key differences:

| Sass                         | Native CSS                        |
| ---------------------------- | --------------------------------- |
| `&-suffix` (BEM: `&__title`) | ❌ Not supported — use full class |
| Nesting `h2 { }` directly    | Must use `& h2 { }` for types     |
| `@extend`                    | ❌ Not available — use `@layer`   |
| `@mixin` / `@include`        | Use `@scope` or custom properties |

The `&-suffix` pattern (`&__title`, `&--active`) that BEM-style Sass relies on does **not** work in native CSS nesting. This is by design — `&` represents the full parent selector, not a string to concatenate. If your codebase relies heavily on this pattern, consider migrating to `@scope` (see `workflow-scope`) or flat class names.

✅ Widely available (~91%). Supported in all modern browsers. Safe to use in new projects without a preprocessor.

Reference: [modern-css.com](https://modern-css.com) · [MDN — CSS nesting](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_nesting)

### 2.9 Typed Custom Properties Without JavaScript

Untyped custom properties (`--foo: 0`) are opaque strings to the browser — they can't be animated, aren't validated, and don't inherit predictably when unset. The `@property` at-rule registers a custom property with a syntax type, initial value, and inheritance flag, unlocking transitions, animations, and type checking with zero JavaScript.

**Avoid (untyped custom properties — no animation or validation):**

```css
:root {
  --hue: 0;
}

.gradient {
  background: hsl(var(--hue), 80%, 60%);
  transition: --hue 1s; /* Does nothing — browser sees a string, not a number */
}

.gradient:hover {
  --hue: 120; /* Snaps instantly, no interpolation */
}
```

Or the JavaScript equivalent for registering:

```js
CSS.registerProperty({
  name: '--hue',
  syntax: '<angle>',
  inherits: false,
  initialValue: '0deg',
});
```

**Prefer (CSS `@property` rule):**

```css
@property --hue {
  syntax: '<angle>';
  inherits: false;
  initial-value: 0deg;
}

.gradient {
  --hue: 0deg;
  background: hsl(var(--hue) 80% 60%);
  transition: --hue 1s ease;
}

.gradient:hover {
  --hue: 120deg; /* Smoothly animates through the hue spectrum */
}
```

No JavaScript, no `CSS.registerProperty()` call. The browser knows the property is an `<angle>`, so it can interpolate between values.

### Supported syntax types

| Syntax                | Example values                      | Use case                          |
| --------------------- | ----------------------------------- | --------------------------------- |
| `<number>`            | `0`, `1.5`, `-3`                    | Counters, multipliers             |
| `<integer>`           | `0`, `1`, `42`                      | Step-based values                 |
| `<length>`            | `0px`, `2rem`, `50vw`               | Spacing, sizing                   |
| `<percentage>`        | `0%`, `50%`, `100%`                 | Progress, ratios                  |
| `<angle>`             | `0deg`, `180deg`, `0.5turn`         | Rotation, hue                     |
| `<color>`             | `red`, `#fff`, `oklch(0.7 0.2 250)` | Color transitions                 |
| `<length-percentage>` | `10px`, `50%`                       | Flexible spacing                  |
| `<time>`              | `0s`, `200ms`                       | Duration control                  |
| `<custom-ident>`      | `ease`, `my-name`                   | Named tokens                      |
| `*`                   | Any value                           | Untyped (same as not registering) |

### Animating gradients

Gradients can't normally be animated because they're images, not interpolatable values. Registered properties solve this:

```css
@property --gradient-angle {
  syntax: '<angle>';
  inherits: false;
  initial-value: 0deg;
}

.conic {
  background: conic-gradient(from var(--gradient-angle), #f06, #9f6, #06f, #f06);
  animation: spin 3s linear infinite;
}

@keyframes spin {
  to {
    --gradient-angle: 360deg;
  }
}
```

### Animating color stops

```css
@property --stop-1 {
  syntax: '<color>';
  inherits: false;
  initial-value: oklch(0.7 0.25 330);
}

@property --stop-2 {
  syntax: '<color>';
  inherits: false;
  initial-value: oklch(0.6 0.2 250);
}

.hero {
  background: linear-gradient(135deg, var(--stop-1), var(--stop-2));
  transition:
    --stop-1 0.6s,
    --stop-2 0.6s;
}

.hero:hover {
  --stop-1: oklch(0.8 0.2 80);
  --stop-2: oklch(0.5 0.25 150);
}
```

### Type safety and fallback values

When a registered property receives an invalid value, it falls back to the `initial-value` rather than becoming `unset`. This prevents broken styles from propagating:

```css
@property --spacing {
  syntax: '<length>';
  inherits: true;
  initial-value: 1rem;
}

.card {
  --spacing: banana; /* Invalid — falls back to 1rem, not broken layout */
  padding: var(--spacing);
}
```

✅ Widely available (~92%). Supported in all major browsers. Use freely for any custom property that needs animation, interpolation, or type validation.

Reference: [modern-css.com](https://modern-css.com) · [MDN — @property](https://developer.mozilla.org/en-US/docs/Web/CSS/@property)

### 2.10 Scoped Styles Without BEM Naming

BEM (`.card__title`, `.card__body--active`) is a naming convention that simulates scoping by encoding the component hierarchy into class names. CSS Modules and styled-components solve the same problem with build tools or JavaScript. The `@scope` at-rule provides real, browser-native style scoping — selectors inside a `@scope` block only match elements within the specified subtree, with no naming conventions, no build step, and no runtime overhead.

**Avoid (BEM naming convention):**

```css
/* BEM — verbose, manual, no enforcement */
.card__title {
  font-size: 1.25rem;
  font-weight: 600;
}
.card__body {
  color: #444;
  line-height: 1.6;
}
.card__body--highlighted {
  background: #fef3c7;
}
/* Nothing prevents .card__title from leaking if used outside .card */
```

Or CSS Modules (requires a bundler):

```css
/* card.module.css — build tool hashes class names */
.title {
  font-size: 1.25rem;
}
.body {
  color: #444;
}
/* Requires Webpack/Vite CSS Modules plugin, framework integration,
   and import { styles } from './card.module.css' in JS */
```

**Prefer (@scope for native scoping):**

```css
@scope (.card) {
  .title {
    font-size: 1.25rem;
    font-weight: 600;
  }
  .body {
    color: #444;
    line-height: 1.6;
  }
  .body.highlighted {
    background: #fef3c7;
  }
}
/* .title only matches inside .card — enforced by the browser */
```

```html
<div class="card">
  <h2 class="title">Card Title</h2>
  <div class="body">Card content here.</div>
</div>

<!-- This .title is NOT affected by the scoped rules -->
<h2 class="title">Page Title</h2>
```

### Scoping with a lower boundary (donut scope)

`@scope` supports an optional `to` clause that defines where the scope ends — creating a "donut" scope that styles the outer component without leaking into nested components:

```css
@scope (.card) to (.card-slot) {
  p {
    color: #444;
  }
  /* Styles paragraphs inside .card but NOT inside .card-slot */
}
```

```html
<div class="card">
  <p>This paragraph is styled.</p>
  <div class="card-slot">
    <p>This paragraph is NOT styled — outside the scope.</p>
  </div>
</div>
```

This solves the classic component composition problem where a parent's styles bleed into slotted or nested child components.

### Inline scoping with `<style>`

`@scope` can be used without a selector when placed inside a `<style>` element — it scopes to the parent of the `<style>` tag:

```html
<div class="widget">
  <style>
    @scope {
      p {
        color: navy;
      }
      .label {
        font-weight: 600;
      }
    }
  </style>
  <p class="label">Only styled within this widget.</p>
</div>
```

### Specificity advantage

Selectors inside `@scope` have the same specificity as their unwrapped equivalents — `.title` inside `@scope (.card)` has (0,1,0) specificity, not (0,2,0). This avoids the specificity inflation that comes from manually nesting `.card .title` and makes scoped styles easier to override with utility classes.

### When to use what

| Approach          | Build step | Runtime cost | Scoping enforcement | Specificity impact |
| ----------------- | ---------- | ------------ | ------------------- | ------------------ |
| BEM naming        | None       | None         | Convention only     | Normal             |
| CSS Modules       | Required   | None         | Build-time hashing  | Normal             |
| styled-components | Required   | Runtime JS   | Runtime generation  | Normal             |
| `@scope`          | None       | None         | Browser-enforced    | No inflation       |

🟡 Newly available (~84%). Supported in Chromium and Firefox. For projects that must support older browsers, BEM or CSS Modules remain valid strategies — but prefer `@scope` for new code in modern browser targets.

Reference: [modern-css.com](https://modern-css.com) · [MDN — @scope](https://developer.mozilla.org/en-US/docs/Web/CSS/@scope)

### 2.11 Range Style Queries Without Multiple Blocks

Container style queries let you apply styles based on the computed value of a custom property on an ancestor container. However, querying discrete values requires a separate `@container style()` block for each value — which quickly becomes unmanageable for numeric ranges (e.g., progress percentages). Range-based style queries accept comparison operators, collapsing dozens of blocks into a single rule.

**Avoid (per-value style query blocks):**

```css
/* One block per value — doesn't scale */
@container style(--progress: 0%) {
  .bar {
    width: 0%;
    background: red;
  }
}
@container style(--progress: 10%) {
  .bar {
    width: 10%;
    background: red;
  }
}
@container style(--progress: 20%) {
  .bar {
    width: 20%;
    background: red;
  }
}
/* …repeat for 30%, 40%, 50%, 60%, 70%, 80%, 90%, 100% */

@container style(--progress: 50%) {
  .bar {
    background: orange;
  }
}
@container style(--progress: 51%) {
  .bar {
    background: orange;
  }
}
/* Impossible to cover every possible value */
```

**Prefer (range-based style queries):**

```css
@container style(--progress <= 25%) {
  .bar {
    background: oklch(0.6 0.25 25); /* red */
  }
}

@container style(25% < --progress <= 50%) {
  .bar {
    background: oklch(0.7 0.2 60); /* orange */
  }
}

@container style(50% < --progress <= 75%) {
  .bar {
    background: oklch(0.75 0.18 95); /* yellow-green */
  }
}

@container style(--progress > 75%) {
  .bar {
    background: oklch(0.65 0.2 145); /* green */
  }
}
```

### Setting up the container

The container element holds the custom property that child elements query:

```html
<div class="progress-wrapper" style="--progress: 68%">
  <div class="bar"></div>
  <span class="label">68%</span>
</div>
```

```css
.progress-wrapper {
  container-type: normal; /* style queries don't need size containment */
}

.bar {
  height: 8px;
  width: var(--progress);
  border-radius: 4px;
  transition:
    width 0.3s,
    background 0.3s;
}
```

### Combining with size queries

Style queries and size queries can be composed in a single `@container` rule:

```css
@container (width >= 300px) and style(--progress > 50%) {
  .label {
    display: inline; /* show percentage label only when there's room and progress is meaningful */
  }
}
```

### Common patterns

```css
/* Theme variant switching */
@container style(--variant: danger) {
  .alert {
    border-color: red;
  }
}

@container style(--variant: success) {
  .alert {
    border-color: green;
  }
}

/* Numeric range — e.g., rating-based styling */
@container style(--rating >= 4) {
  .star-display {
    color: gold;
  }
}

@container style(--rating < 2) {
  .star-display {
    color: #ccc;
  }
}
```

### Registering the custom property for range queries

For numeric range comparisons to work correctly, the custom property should be registered with a type so the browser can compare values:

```css
@property --progress {
  syntax: '<percentage>';
  inherits: true;
  initial-value: 0%;
}
```

Without registration, the property is a string and range comparisons may not evaluate as expected. See `workflow-registered-properties` for details on `@property`.

🟡 Newly available (~88%). Discrete style queries (`style(--x: value)`) have broader support than range comparisons. Use `@property` registration for numeric ranges. Fallback: use discrete value matching or JavaScript class toggling.

Reference: [modern-css.com](https://modern-css.com) · [MDN — @container style queries](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_containment/Container_size_and_style_queries#container_style_queries)

### 2.12 CSS Feature Detection Without JavaScript

Testing for CSS feature support traditionally required JavaScript — either the Modernizr library (which adds classes to `<html>`) or the `CSS.supports()` API with manual class toggling. The `@supports` at-rule performs feature detection entirely in CSS, with no JavaScript, no library, and no render-blocking script.

**Avoid (JavaScript feature detection):**

```js
// Modernizr — 10 KB+ library that runs on page load
// Adds classes like .flexbox, .no-flexbox to <html>

// Or manual CSS.supports() check
if (CSS.supports('display', 'grid')) {
  document.documentElement.classList.add('grid');
} else {
  document.documentElement.classList.add('no-grid');
}
```

```css
.grid .layout {
  display: grid;
}
.no-grid .layout {
  display: flex;
  flex-wrap: wrap;
}
```

**Prefer (`@supports` — pure CSS):**

```css
.layout {
  /* Fallback for all browsers */
  display: flex;
  flex-wrap: wrap;
}

@supports (display: grid) {
  .layout {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  }
}
/* No JavaScript, no render-blocking script, no class toggling */
```

### Logical operators

`@supports` accepts `and`, `or`, and `not` for compound feature checks:

```css
/* Multiple features required */
@supports (container-type: inline-size) and (display: grid) {
  .card-wrapper {
    container-type: inline-size;
  }
}

/* Negation — target browsers that lack a feature */
@supports not (backdrop-filter: blur(10px)) {
  .glass {
    background: rgb(255 255 255 / 0.85);
    /* opaque fallback when backdrop-filter is unavailable */
  }
}

/* Any of several features */
@supports (scroll-timeline-name: --tl) or (animation-timeline: view()) {
  .reveal {
    animation: fade-in linear both;
    animation-timeline: view();
  }
}
```

### Selector feature detection

`@supports` can also test for selector support using the `selector()` function:

```css
/* Only apply if :has() is supported */
@supports selector(:has(*)) {
  .card:has(img) {
    grid-template-rows: auto 1fr;
  }
}

/* Only apply if :focus-visible is supported */
@supports selector(:focus-visible) {
  :focus:not(:focus-visible) {
    outline: none;
  }
}
```

### Common progressive enhancement patterns

```css
/* Anchor positioning with Floating UI fallback */
@supports (anchor-name: --tip) {
  .tooltip {
    position: fixed;
    position-anchor: --tip;
    inset-area: top;
  }
}

/* Container queries with media query fallback */
.card {
  flex-direction: column;
}

@media (width >= 600px) {
  .card {
    flex-direction: row;
  }
}

@supports (container-type: inline-size) {
  .card-wrapper {
    container-type: inline-size;
  }

  @container (width >= 400px) {
    .card {
      flex-direction: row;
    }
  }
}
```

### When to use `@supports` vs. just writing the property

Modern CSS is designed to ignore properties it doesn't understand — an unknown declaration is silently skipped. In many cases, you don't need `@supports` at all; just write the modern property after the fallback:

```css
.hero {
  height: 100vh; /* fallback */
  height: 100dvh; /* override in supporting browsers */
}
```

Reserve `@supports` for cases where the fallback and the enhancement are **mutually exclusive** — i.e., you need to remove or change the fallback styles when the feature is present, not just add to them.

✅ Widely available (~96%). `@supports` itself is supported in all modern browsers. Use it freely for progressive enhancement of newer CSS features.

Reference: [modern-css.com](https://modern-css.com) · [MDN — @supports](https://developer.mozilla.org/en-US/docs/Web/CSS/@supports)


## 3. Typography

### 3.1 Fluid Typography Without Media Queries

Scaling typography across screen sizes traditionally requires multiple `@media` breakpoints, each with a hardcoded `font-size` override. The result is a staircase of jumps rather than a smooth scale, and every new element needs its own stack of breakpoints. The `clamp()` function produces fluid, continuously scaling typography in a single line — no media queries, no jumps.

**Avoid (breakpoint staircase):**

```css
h1 {
  font-size: 1.5rem;
}

@media (min-width: 600px) {
  h1 {
    font-size: 2rem;
  }
}

@media (min-width: 900px) {
  h1 {
    font-size: 2.5rem;
  }
}

@media (min-width: 1200px) {
  h1 {
    font-size: 3rem;
  }
}
/* 4 blocks for one element — multiply by every heading, body text, caption… */
```

**Prefer (fluid clamp):**

```css
h1 {
  font-size: clamp(1.5rem, 1rem + 2.5vw, 3rem);
}
/* Scales smoothly from 1.5rem → 3rem across all viewport widths */
```

One declaration replaces the entire breakpoint stack. The value transitions linearly between the minimum and maximum, with the middle expression controlling the rate of change.

### How `clamp()` works

```
clamp(MIN, PREFERRED, MAX)
```

- **MIN** — the smallest the value can be (floor).
- **PREFERRED** — the fluid expression, usually involving `vw` or `vi` units. This is the value used when it falls between MIN and MAX.
- **MAX** — the largest the value can be (ceiling).

The browser evaluates: `max(MIN, min(PREFERRED, MAX))`.

### Building the preferred value

The preferred expression typically combines a `rem` base with a `vw` scaler:

```css
/* Formula: rem-base + vw-scaler */
font-size: clamp(1rem, 0.5rem + 2vw, 2rem);
/*               ↑         ↑              ↑
              floor   scales with vw    ceiling */
```

The `rem` component ensures the text scales with the user's font-size preference (accessibility). The `vw` component adds viewport responsiveness. **Never use `vw` alone** — it ignores user font-size settings.

### Complete type scale with clamp

```css
:root {
  --text-xs: clamp(0.75rem, 0.7rem + 0.25vw, 0.875rem);
  --text-sm: clamp(0.875rem, 0.8rem + 0.35vw, 1rem);
  --text-base: clamp(1rem, 0.9rem + 0.5vw, 1.125rem);
  --text-lg: clamp(1.125rem, 0.95rem + 0.85vw, 1.5rem);
  --text-xl: clamp(1.25rem, 1rem + 1.25vw, 2rem);
  --text-2xl: clamp(1.5rem, 1rem + 2.5vw, 3rem);
  --text-3xl: clamp(2rem, 1.2rem + 4vw, 4rem);
}

h1 {
  font-size: var(--text-3xl);
}
h2 {
  font-size: var(--text-2xl);
}
h3 {
  font-size: var(--text-xl);
}
body {
  font-size: var(--text-base);
}
```

### Fluid spacing too

`clamp()` is not limited to font sizes — use it for spacing, padding, and gaps:

```css
:root {
  --space-sm: clamp(0.5rem, 0.3rem + 1vw, 1rem);
  --space-md: clamp(1rem, 0.5rem + 2.5vw, 2rem);
  --space-lg: clamp(1.5rem, 0.75rem + 3.75vw, 3rem);
}

section {
  padding-block: var(--space-lg);
  gap: var(--space-md);
}
```

### Accessibility note

Always include a `rem` component in the preferred expression. Using `clamp(16px, 4vw, 32px)` ignores the user's browser font-size preference. Using `clamp(1rem, 0.5rem + 2vw, 2rem)` respects it.

✅ Widely available (~95%). Supported in all major browsers. No fallback needed.

Reference: [modern-css.com](https://modern-css.com) · [MDN — clamp()](https://developer.mozilla.org/en-US/docs/Web/CSS/clamp)

### 3.2 Font Loading Without Invisible Text

By default, browsers hide text entirely while a custom web font is loading — a behavior known as Flash of Invisible Text (FOIT). On slow connections, users stare at a blank page for several seconds. The `font-display` descriptor in `@font-face` controls this behavior, letting you show a fallback font immediately and swap in the custom font when it's ready.

**Avoid (default behavior — invisible text):**

```css
@font-face {
  font-family: 'MyFont';
  src: url('myfont.woff2') format('woff2');
  /* No font-display — browser hides text for up to 3 seconds while loading */
}

body {
  font-family: 'MyFont', sans-serif;
}
/* Users on slow connections see nothing until the font downloads */
```

**Prefer (font-display: swap):**

```css
@font-face {
  font-family: 'MyFont';
  src: url('myfont.woff2') format('woff2');
  font-display: swap;
}

body {
  font-family: 'MyFont', sans-serif;
}
/* Text is immediately visible in the fallback font, then swaps when ready */
```

### font-display values

| Value      | Block period    | Swap period     | Best for                                                               |
| ---------- | --------------- | --------------- | ---------------------------------------------------------------------- |
| `auto`     | Browser decides | Browser decides | Default — usually same as `block`                                      |
| `block`    | ~3 seconds      | Infinite        | Icon fonts (blank squares are worse than waiting)                      |
| `swap`     | ~100ms          | Infinite        | Body and heading text (most common choice)                             |
| `fallback` | ~100ms          | ~3 seconds      | Text where layout shift matters — uses fallback if font takes too long |
| `optional` | ~100ms          | None            | Non-critical fonts — only uses custom font if already cached           |

### Recommended strategy by font role

```css
/* Body text — always show content immediately */
@font-face {
  font-family: 'BodyFont';
  src: url('body.woff2') format('woff2');
  font-display: swap;
}

/* Heading / display font — acceptable to swap later */
@font-face {
  font-family: 'DisplayFont';
  src: url('display.woff2') format('woff2');
  font-display: swap;
}

/* Icon font — blank squares are worse than waiting */
@font-face {
  font-family: 'Icons';
  src: url('icons.woff2') format('woff2');
  font-display: block;
}

/* Non-essential decorative font — skip if not cached */
@font-face {
  font-family: 'Decorative';
  src: url('decorative.woff2') format('woff2');
  font-display: optional;
}
```

### Reducing layout shift from font swapping

`font-display: swap` introduces Flash of Unstyled Text (FOUT) — the fallback font renders first, then the custom font replaces it, potentially causing a layout shift. Mitigate this with:

```css
/* 1. Use size-adjust to match fallback metrics to the custom font */
@font-face {
  font-family: 'MyFont Fallback';
  src: local('Arial');
  size-adjust: 105%;
  ascent-override: 95%;
  descent-override: 22%;
  line-gap-override: 0%;
}

body {
  font-family: 'MyFont', 'MyFont Fallback', sans-serif;
}

/* 2. Preload critical fonts to minimize the swap window */
```

```html
<!-- Preload the most important font file -->
<link rel="preload" href="body.woff2" as="font" type="font/woff2" crossorigin />
```

### Google Fonts

Google Fonts supports `font-display` via a URL parameter:

```html
<link
  href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap"
  rel="stylesheet"
/>
```

The `&display=swap` parameter adds `font-display: swap` to the generated `@font-face` rules.

Always set `font-display` on every `@font-face` declaration. There is no good reason to leave it at the default `auto` (which typically means `block` — invisible text). For body and heading text, `swap` is the right default.

✅ Widely available (~96%). Supported in all major browsers. No fallback needed.

Reference: [modern-css.com](https://modern-css.com) · [MDN — font-display](https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face/font-display) · [web.dev — Avoid invisible text during font loading](https://web.dev/articles/avoid-invisible-text)

### 3.3 Drop Caps Without Float Hacks

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

### 3.4 Multiline Text Truncation Without JavaScript

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

### 3.5 Vertical Text Centering Without Padding Hacks

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

### 3.6 Balanced Headlines Without Manual Line Breaks

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

### 3.7 Multiple Font Weights Without Multiple Files

Loading separate font files for each weight (400, 500, 600, 700…) means multiple HTTP requests, more bytes to download, and a combinatorial explosion when you also need italic variants. Variable fonts pack an entire weight range (and often width, slant, and optical size axes) into a single file — fewer requests, smaller total size, and access to any weight value, not just the predefined ones.

**Avoid (separate file per weight):**

```css
@font-face {
  font-family: 'MyFont';
  src: url('MyFont-Regular.woff2') format('woff2');
  font-weight: 400;
  font-style: normal;
}

@font-face {
  font-family: 'MyFont';
  src: url('MyFont-Medium.woff2') format('woff2');
  font-weight: 500;
  font-style: normal;
}

@font-face {
  font-family: 'MyFont';
  src: url('MyFont-SemiBold.woff2') format('woff2');
  font-weight: 600;
  font-style: normal;
}

@font-face {
  font-family: 'MyFont';
  src: url('MyFont-Bold.woff2') format('woff2');
  font-weight: 700;
  font-style: normal;
}

/* 4 files, 4 HTTP requests, ~80–120 KB total
   Only these exact weights are available */
```

**Prefer (single variable font file):**

```css
@font-face {
  font-family: 'MyFont';
  src: url('MyFont-Variable.woff2') format('woff2');
  font-weight: 100 900;
  font-display: swap;
}
```

One file, one request. The `font-weight: 100 900` range descriptor tells the browser this single file covers every weight from 100 to 900 — including intermediate values like 450 or 550 that static fonts cannot express.

### Using continuous weight values

```css
body {
  font-family: 'MyFont', system-ui, sans-serif;
  font-weight: 400;
}

h1 {
  font-weight: 800;
}

h2 {
  font-weight: 650; /* not possible with static fonts */
}

.subtitle {
  font-weight: 350; /* fine-tuned lighter weight */
}

/* Responsive weight — heavier on larger screens for better readability */
h1 {
  font-weight: 700;
}

@media (width >= 1024px) {
  h1 {
    font-weight: 800;
  }
}
```

### Variable font axes

Beyond weight, variable fonts can expose additional axes:

```css
@font-face {
  font-family: 'MyVar';
  src: url('MyVar.woff2') format('woff2');
  font-weight: 100 900;
  font-stretch: 75% 125%; /* width axis */
  font-style: oblique 0deg 12deg; /* slant axis */
}

.condensed-bold {
  font-weight: 700;
  font-stretch: 75%;
}

.wide-light {
  font-weight: 300;
  font-stretch: 125%;
}
```

### Custom axes with `font-variation-settings`

Some variable fonts expose custom axes (e.g., optical size, grade) via four-letter tags:

```css
/* Standard axes — prefer the high-level properties */
h1 {
  font-weight: 700; /* 'wght' axis */
  font-stretch: 110%; /* 'wdth' axis */
  font-style: oblique 6deg; /* 'slnt' axis */
  font-optical-sizing: auto; /* 'opsz' axis */
}

/* Custom axes — use font-variation-settings */
.display-text {
  font-variation-settings:
    'GRAD' 88,
    'CASL' 1;
}
```

Prefer the high-level CSS properties (`font-weight`, `font-stretch`, `font-style`) over `font-variation-settings` for standard axes — they compose with other CSS features like `font-weight: bolder` inheritance, while `font-variation-settings` replaces the entire setting map on each declaration.

### Animating font properties

Variable fonts unlock smooth CSS transitions and animations on typographic properties:

```css
.hover-weight {
  font-weight: 400;
  transition: font-weight 0.2s ease;
}

.hover-weight:hover {
  font-weight: 700;
}
```

### Performance considerations

- A single variable font file is typically **smaller** than 3+ static weight files combined, but **larger** than any single static weight file.
- If you only use one weight (e.g., body text at 400), a static font file may be smaller.
- If you use 2+ weights, a variable font almost always wins on total transfer size and eliminates the extra HTTP requests.
- Use `unicode-range` subsetting for multilingual sites to load only the character sets needed.

```css
@font-face {
  font-family: 'MyFont';
  src: url('MyFont-Latin.woff2') format('woff2');
  font-weight: 100 900;
  unicode-range: U+0000-00FF, U+0131, U+0152-0153; /* Latin subset */
  font-display: swap;
}
```

### Combining with `font-display`

Always pair variable fonts with `font-display: swap` (see `typo-font-display`) to prevent invisible text during loading:

```css
@font-face {
  font-family: 'MyFont';
  src: url('MyFont-Variable.woff2') format('woff2');
  font-weight: 100 900;
  font-display: swap;
}
```

✅ Widely available (~96%). Variable fonts are supported in all modern browsers. Most popular font families (Inter, Roboto Flex, Source Sans 3, etc.) ship variable font versions. Use them by default whenever 2+ weights are needed.

Reference: [modern-css.com](https://modern-css.com) · [MDN — Variable fonts](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_fonts/Variable_fonts_guide) · [v-fonts.com](https://v-fonts.com)


## 4. Color

### 4.1 Styling Form Controls Without Rebuilding Them

Theming checkboxes, radio buttons, range sliders, and progress bars traditionally required `appearance: none` followed by 20+ lines of custom box, border, background, and pseudo-element styling — effectively rebuilding the control from scratch. This breaks native behavior (focus rings, indeterminate states, disabled styling), hurts accessibility, and varies wildly across browsers. The `accent-color` property themes these controls in a single declaration while preserving all native behavior.

**Avoid (appearance: none + full rebuild):**

```css
/* Rebuild checkbox from scratch — fragile, incomplete */
input[type='checkbox'] {
  appearance: none;
  width: 18px;
  height: 18px;
  border: 2px solid #ccc;
  border-radius: 3px;
  position: relative;
}

input[type='checkbox']:checked {
  background: #7c3aed;
  border-color: #7c3aed;
}

input[type='checkbox']:checked::after {
  content: '✓';
  position: absolute;
  top: -1px;
  left: 3px;
  color: white;
  font-size: 14px;
}

/* Missing: focus ring, indeterminate state, disabled state,
   high contrast mode, forced-colors, RTL, print styles… */
```

Repeat for radio buttons, range sliders, and progress bars — each requires its own full rebuild with different pseudo-elements across browser engines.

**Prefer (modern CSS):**

```css
input[type='checkbox'],
input[type='radio'],
input[type='range'],
progress {
  accent-color: #7c3aed;
}
```

One line. The browser applies your brand color to the active/checked state while automatically handling focus rings, disabled opacity, indeterminate states, high contrast mode, and every other native behavior.

### Theming with custom properties

```css
:root {
  --accent: oklch(0.55 0.25 285);
}

input,
progress,
meter {
  accent-color: var(--accent);
}
```

### Dark mode aware

```css
:root {
  accent-color: light-dark(#7c3aed, #a78bfa);
}
/* Or rely on the browser — accent-color adapts contrast automatically
   when paired with color-scheme: light dark */
```

### Per-component theming

```css
/* Success / danger variants */
.form-group.success input {
  accent-color: oklch(0.65 0.2 145);
}

.form-group.danger input {
  accent-color: oklch(0.6 0.22 25);
}

/* Rating slider */
input[type='range'].rating {
  accent-color: gold;
}

/* Upload progress */
progress.upload {
  accent-color: oklch(0.6 0.2 250);
}
```

### Elements affected by `accent-color`

| Element / State                         | Themed part                      |
| --------------------------------------- | -------------------------------- |
| `<input type="checkbox">`               | Checked background and checkmark |
| `<input type="radio">`                  | Selected dot and ring            |
| `<input type="range">`                  | Filled track and thumb           |
| `<progress>`                            | Filled bar                       |
| `<input type="checkbox">` indeterminate | Dash indicator                   |

### Automatic contrast

The browser automatically picks a contrasting color for the checkmark, radio dot, and other foreground elements based on the `accent-color` you provide. If you set a dark accent color, the checkmark will be light (and vice versa) — no manual `color: white` needed.

### When `accent-color` is not enough

`accent-color` covers basic theming (brand color on active states). For fully custom form control designs (custom shapes, animations, multi-part sliders), you still need `appearance: none` rebuilds or the newer `appearance: base-select` (see `layout-base-select`). But for the common case of "match my brand color," `accent-color` is the right tool.

### Global accent color

```css
/* Set once at the root — all form controls inherit it */
:root {
  accent-color: var(--brand);
}
```

This is the simplest way to brand an entire application's form controls with zero per-element styling.

✅ Widely available (~93%). Supported in all major browsers. No fallback needed — in unsupporting browsers, controls render with the default browser theme color.

Reference: [modern-css.com](https://modern-css.com) · [MDN — accent-color](https://developer.mozilla.org/en-US/docs/Web/CSS/accent-color)

### 4.2 Frosted Glass Effect Without Opacity Hacks

Creating a frosted glass (glass morphism) effect traditionally required a `::before` pseudo-element that duplicated the background image, applied a `filter: blur()`, and was layered behind the content with `z-index: -1`. This approach is fragile — it requires knowing and duplicating the background, breaks when the background changes, and adds extra DOM layers. `backdrop-filter` applies filters directly to the content behind an element, producing a true frosted glass effect with a single property.

**Avoid (pseudo-element background duplication):**

```css
.card {
  position: relative;
  overflow: hidden;
}

.card::before {
  content: '';
  position: absolute;
  inset: 0;
  background-image: url('bg.jpg');
  background-size: cover;
  background-position: center;
  filter: blur(12px);
  z-index: -1;
  /* Must duplicate and position the same background —
     breaks when the parent background changes */
}
```

Or the opacity-based approach that washes out the entire element:

```css
.overlay {
  background: rgba(255, 255, 255, 0.7);
  /* No blur — just a semi-transparent wash. Not glass morphism. */
}
```

**Prefer (modern CSS):**

```css
.glass {
  backdrop-filter: blur(12px);
  background: rgb(255 255 255 / 0.1);
}
```

Two lines. The blur applies to whatever is behind the element — images, text, video, gradients — without needing to know or duplicate the background content. The semi-transparent background tints the blurred area.

### Common glass morphism patterns

```css
/* Light glass card */
.glass-card {
  backdrop-filter: blur(16px) saturate(1.2);
  background: rgb(255 255 255 / 0.15);
  border: 1px solid rgb(255 255 255 / 0.2);
  border-radius: 1rem;
  box-shadow: 0 4px 24px rgb(0 0 0 / 0.1);
}

/* Dark glass card */
.glass-card-dark {
  backdrop-filter: blur(16px) saturate(1.5);
  background: rgb(0 0 0 / 0.25);
  border: 1px solid rgb(255 255 255 / 0.08);
  border-radius: 1rem;
}

/* Frosted navigation bar */
.navbar {
  position: sticky;
  top: 0;
  z-index: 10;
  backdrop-filter: blur(12px);
  background: rgb(255 255 255 / 0.7);
  border-bottom: 1px solid rgb(0 0 0 / 0.05);
}
```

### Dark mode aware glass

```css
.glass {
  backdrop-filter: blur(16px) saturate(1.2);
  background: light-dark(rgb(255 255 255 / 0.2), rgb(0 0 0 / 0.3));
  border: 1px solid light-dark(rgb(255 255 255 / 0.3), rgb(255 255 255 / 0.08));
}
```

### Available filter functions

`backdrop-filter` accepts the same filter functions as `filter`:

| Function       | Example                              | Effect                 |
| -------------- | ------------------------------------ | ---------------------- |
| `blur()`       | `backdrop-filter: blur(10px)`        | Gaussian blur          |
| `brightness()` | `backdrop-filter: brightness(0.8)`   | Darken or lighten      |
| `saturate()`   | `backdrop-filter: saturate(1.5)`     | Boost color saturation |
| `contrast()`   | `backdrop-filter: contrast(0.9)`     | Adjust contrast        |
| `grayscale()`  | `backdrop-filter: grayscale(1)`      | Remove color           |
| `sepia()`      | `backdrop-filter: sepia(0.5)`        | Warm vintage tone      |
| `hue-rotate()` | `backdrop-filter: hue-rotate(90deg)` | Shift hue              |
| `invert()`     | `backdrop-filter: invert(1)`         | Invert colors          |

Multiple filters can be chained in a single declaration:

```css
.glass {
  backdrop-filter: blur(12px) saturate(1.4) brightness(1.1);
}
```

### Performance considerations

- `backdrop-filter` is GPU-composited — it's performant for static or slowly scrolling content.
- Avoid applying it to large numbers of overlapping elements — each layer requires a separate compositing pass.
- On lower-end devices, consider providing a solid fallback behind a `@supports` check:

```css
.glass {
  /* Fallback — opaque background */
  background: rgb(255 255 255 / 0.85);
}

@supports (backdrop-filter: blur(1px)) {
  .glass {
    backdrop-filter: blur(12px);
    background: rgb(255 255 255 / 0.15);
  }
}
```

### Combining with border effects

A subtle inner border enhances the glass edge:

```css
.glass {
  backdrop-filter: blur(16px);
  background: rgb(255 255 255 / 0.1);
  border: 1px solid rgb(255 255 255 / 0.2);
  box-shadow:
    inset 0 1px 0 rgb(255 255 255 / 0.15),
    0 4px 24px rgb(0 0 0 / 0.08);
}
```

✅ Widely available (~96%). Supported in all major browsers. The `-webkit-backdrop-filter` prefix is no longer needed in modern browsers but can be included for older Safari versions.

Reference: [modern-css.com](https://modern-css.com) · [MDN — backdrop-filter](https://developer.mozilla.org/en-US/docs/Web/CSS/backdrop-filter)

### 4.3 Readable Text Without Manual Contrast Checks

Choosing whether to use white or black text on a colored background requires either manual checking against WCAG contrast ratios or a JavaScript function that calculates relative luminance. When the background color changes (theming, dark mode, user customization), the text color decision must be recalculated. The `contrast-color()` function automatically selects the most readable text color for any given background — no manual picking, no JavaScript, no contrast ratio math.

**Avoid (hardcoded text color — breaks when background changes):**

```css
.badge {
  background: var(--badge-bg);
  color: white; /* hardcoded — unreadable on light backgrounds */
}

/* Or: manual per-variant overrides */
.badge--info {
  background: #dbeafe;
  color: #1e3a5f; /* manually chosen for this specific blue */
}
.badge--warning {
  background: #fef3c7;
  color: #78350f; /* manually chosen for this specific yellow */
}
.badge--danger {
  background: #dc2626;
  color: white; /* manually chosen for this specific red */
}
/* Every new color variant needs a manually picked text color */
```

Or with JavaScript:

```js
function getContrastColor(bgHex) {
  const r = parseInt(bgHex.slice(1, 3), 16);
  const g = parseInt(bgHex.slice(3, 5), 16);
  const b = parseInt(bgHex.slice(5, 7), 16);
  const luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255;
  return luminance > 0.5 ? '#000000' : '#ffffff';
}
// Must re-run on every background change, doesn't handle non-hex colors
```

**Prefer (modern CSS):**

```css
.badge {
  background: var(--badge-bg);
  color: contrast-color(var(--badge-bg));
}
/* Automatically picks the most readable text color — any background, any theme */
```

No manual color pairing, no JavaScript luminance calculations. The browser evaluates the background color and selects the text color that provides the best contrast.

### How it works

`contrast-color()` takes a base color and returns the color (from the available options) that provides the highest contrast ratio against it:

```css
.tag {
  background: var(--tag-color);
  color: contrast-color(var(--tag-color));
  /* Returns black or white — whichever has higher contrast */
}
```

### Dynamic theming

The real power shows in dynamic theming where background colors are set via custom properties, user input, or runtime calculations:

```css
:root {
  --brand: oklch(0.6 0.2 250);
}

.hero {
  background: var(--brand);
  color: contrast-color(var(--brand));
  /* Adapts automatically as --brand changes */
}

.hero a {
  color: contrast-color(var(--brand));
  text-decoration: underline;
}
```

### With oklch color scales

Particularly useful when generating color scales from a single hue — the text color flips from dark to light automatically at the right lightness threshold:

```css
.swatch-1 {
  background: oklch(0.95 0.05 250);
  color: contrast-color(oklch(0.95 0.05 250)); /* → dark text */
}
.swatch-5 {
  background: oklch(0.55 0.2 250);
  color: contrast-color(oklch(0.55 0.2 250)); /* → light text */
}
.swatch-9 {
  background: oklch(0.25 0.1 250);
  color: contrast-color(oklch(0.25 0.1 250)); /* → light text */
}
```

### User-customizable colors

```css
/* User picks any background color via a color input */
.card {
  background: var(--user-color);
  color: contrast-color(var(--user-color));
  /* Always readable, no matter what color the user picks */
}
```

### Common use cases

```css
/* Colored badges with automatic text contrast */
.badge {
  background: var(--badge-color);
  color: contrast-color(var(--badge-color));
  padding: 0.125rem 0.5rem;
  border-radius: 999px;
}

/* Tag clouds with varied backgrounds */
.tag {
  background: var(--tag-bg);
  color: contrast-color(var(--tag-bg));
}

/* Data visualization labels on colored segments */
.chart-label {
  color: contrast-color(var(--segment-color));
}
```

### Fallback strategy

Given the very limited browser support, pair `contrast-color()` with a manual fallback:

```css
.badge {
  background: var(--badge-bg);
  color: white; /* safe fallback for dark backgrounds */
  color: contrast-color(var(--badge-bg)); /* override in supporting browsers */
}

/* Or use @supports */
@supports (color: contrast-color(red)) {
  .badge {
    color: contrast-color(var(--badge-bg));
  }
}
```

For broader support today, use a JavaScript utility to set a `--text-color` custom property based on the background luminance. Replace it with `contrast-color()` once support is sufficient.

🟠 Limited (~6%). Very early in browser adoption. Use as a progressive enhancement behind `@supports` with a manual color fallback. This is a feature to watch — when widely available, it will eliminate an entire class of accessibility bugs related to insufficient text contrast.

Reference: [modern-css.com](https://modern-css.com) · [CSS Color Level 6 — contrast-color()](https://drafts.csswg.org/css-color-6/#contrast-color)

### 4.4 Dark Mode Colors Without Duplicating Values

Implementing dark mode with `prefers-color-scheme` media queries requires duplicating every color declaration — once in the default block and once inside the `@media` block. As the design system grows, these paired declarations drift out of sync, and every new color token means editing two places. The `light-dark()` function accepts both values inline, keeping the light and dark variants together in a single declaration.

**Avoid (duplicated values in media query):**

```css
:root {
  --text: #111;
  --surface: #fff;
  --border: #ddd;
  --muted: #666;
}

@media (prefers-color-scheme: dark) {
  :root {
    --text: #eee;
    --surface: #1a1a1a;
    --border: #333;
    --muted: #999;
  }
}
/* Every new token requires editing both blocks — easy to forget one */
```

For component-level colors, it gets worse:

```css
.card {
  background: #fff;
  color: #111;
  border: 1px solid #ddd;
}

@media (prefers-color-scheme: dark) {
  .card {
    background: #1e1e1e;
    color: #eee;
    border-color: #444;
  }
}
/* Multiply by every component — hundreds of duplicated lines */
```

**Prefer (`light-dark()` inline):**

```css
:root {
  color-scheme: light dark; /* Required — tells the browser both schemes are supported */

  --text: light-dark(#111, #eee);
  --surface: light-dark(#fff, #1a1a1a);
  --border: light-dark(#ddd, #333);
  --muted: light-dark(#666, #999);
}

.card {
  background: light-dark(#fff, #1e1e1e);
  color: light-dark(#111, #eee);
  border: 1px solid light-dark(#ddd, #444);
}
/* Light and dark values live side by side — impossible to forget one */
```

### How it works

```
light-dark(light-value, dark-value)
```

- The first argument is used when the computed `color-scheme` is `light`.
- The second argument is used when it is `dark`.
- The `color-scheme` property **must** be set on the element or an ancestor — without it, `light-dark()` always resolves to the light value.

### Prerequisite: `color-scheme`

`light-dark()` reads from the element's resolved `color-scheme`, not from `prefers-color-scheme` directly. You must declare `color-scheme` for it to respond to the user's OS preference:

```css
:root {
  color-scheme: light dark;
}
/* Now light-dark() switches based on OS preference */
```

See `workflow-color-scheme` for details on the `color-scheme` property.

### Per-element overrides

Because `light-dark()` follows `color-scheme`, you can force sections of the page to a specific scheme:

```css
:root {
  color-scheme: light dark;
}

/* This footer is always dark, regardless of OS preference */
.footer {
  color-scheme: dark;
  background: light-dark(#fff, #111); /* resolves to #111 */
  color: light-dark(#111, #eee); /* resolves to #eee */
}

/* This form is always light */
.print-form {
  color-scheme: light;
  background: light-dark(#fff, #111); /* resolves to #fff */
}
```

### Combining with oklch for perceptually uniform theming

```css
:root {
  color-scheme: light dark;

  --brand: light-dark(oklch(0.55 0.2 264), oklch(0.75 0.15 264));
  --surface: light-dark(oklch(0.99 0.005 264), oklch(0.15 0.01 264));
  --text: light-dark(oklch(0.2 0.02 264), oklch(0.9 0.02 264));
}
```

### Using with custom properties for a complete design token system

```css
:root {
  color-scheme: light dark;

  /* Semantic tokens */
  --color-text-primary: light-dark(#111, #eee);
  --color-text-secondary: light-dark(#555, #aaa);
  --color-text-muted: light-dark(#888, #777);

  --color-bg-page: light-dark(#fff, #0f0f0f);
  --color-bg-card: light-dark(#fff, #1a1a1a);
  --color-bg-elevated: light-dark(#f5f5f5, #252525);

  --color-border-default: light-dark(#ddd, #333);
  --color-border-strong: light-dark(#aaa, #555);

  --color-accent: light-dark(oklch(0.55 0.22 264), oklch(0.72 0.18 264));
}
```

### When to still use `@media (prefers-color-scheme)`

`light-dark()` works for color values. For non-color changes between themes (e.g., swapping an image `src`, changing `font-weight`, or adjusting `opacity`), you still need the media query:

```css
/* Non-color theme changes still need @media */
@media (prefers-color-scheme: dark) {
  .logo {
    filter: brightness(1.2);
  }
  .hero-image {
    content: url('hero-dark.webp');
  }
}
```

`light-dark()` is a color function — it only works where a `<color>` value is expected. For everything else, use `prefers-color-scheme` media queries or container style queries.

🟡 Newly available (~83%). Supported in all modern browsers. Falls back gracefully — wrap in `@supports (color: light-dark(#000, #fff))` if you need to provide a separate fallback path.

Reference: [modern-css.com](https://modern-css.com) · [MDN — light-dark()](https://developer.mozilla.org/en-US/docs/Web/CSS/color_value/light-dark)

### 4.5 Mixing Colors Without a Preprocessor

Blending two colors together — for hover states, tints, shades, or palette generation — has historically required Sass's `mix()` function or manual hex math. The result is a static value baked in at compile time that cannot respond to theming, dark mode, or runtime changes. The native `color-mix()` function blends colors directly in the browser, works with custom properties, and supports perceptually uniform color spaces like `oklch`.

**Avoid (Sass mix — build-time only):**

```scss
// Sass — requires a compiler
$blue: #3b82f6;
$pink: #ec4899;

.blend {
  background: mix($blue, $pink, 60%);
  // Compiles to a static hex value — frozen at build time
}

.tint {
  background: mix($blue, white, 80%);
  // Cannot change at runtime, ignores custom properties
}

.shade {
  background: mix($blue, black, 80%);
}
```

**Prefer (native `color-mix()`):**

```css
.blend {
  background: color-mix(in oklch, #3b82f6 60%, #ec4899);
}

.tint {
  background: color-mix(in oklch, var(--brand) 80%, white);
}

.shade {
  background: color-mix(in oklch, var(--brand) 80%, black);
}
```

No build step, works with custom properties, and responds to runtime theme changes.

### Why the color space matters

The `in <color-space>` parameter controls how colors are interpolated. Different spaces produce different visual results:

```css
/* oklch — perceptually uniform, best for most use cases */
background: color-mix(in oklch, blue, yellow);

/* srgb — legacy color mixing, can produce muddy midpoints */
background: color-mix(in srgb, blue, yellow);

/* oklab — perceptually uniform, Cartesian (no hue interpolation) */
background: color-mix(in oklab, blue, yellow);

/* hsl — hue-based mixing, can produce unexpected intermediate hues */
background: color-mix(in hsl, blue, yellow);
```

**Recommendation:** Use `in oklch` as the default. It produces the most visually pleasing intermediate colors because it accounts for human perception — equal numeric steps produce equal perceived differences.

### Percentage control

The percentage controls how much of each color is in the mix:

```css
/* 75% first color, 25% second */
color-mix(in oklch, #3b82f6 75%, #ec4899)

/* 50/50 — equal blend (default if no percentages given) */
color-mix(in oklch, #3b82f6, #ec4899)

/* 25% first, 75% second */
color-mix(in oklch, #3b82f6 25%, #ec4899)
```

If only one percentage is specified, the other is inferred as the remainder to 100%.

### Generating tints and shades with custom properties

```css
:root {
  --brand: oklch(0.55 0.2 264);
}

.btn {
  background: var(--brand);
}

.btn:hover {
  /* 15% white mixed in — lighter */
  background: color-mix(in oklch, var(--brand) 85%, white);
}

.btn:active {
  /* 20% black mixed in — darker */
  background: color-mix(in oklch, var(--brand) 80%, black);
}

.btn-ghost {
  /* 10% of the brand color — subtle tint */
  background: color-mix(in oklch, var(--brand) 10%, transparent);
  color: var(--brand);
}
```

### Building a full shade palette

```css
:root {
  --blue: oklch(0.55 0.2 264);

  --blue-50: color-mix(in oklch, var(--blue) 5%, white);
  --blue-100: color-mix(in oklch, var(--blue) 15%, white);
  --blue-200: color-mix(in oklch, var(--blue) 30%, white);
  --blue-300: color-mix(in oklch, var(--blue) 50%, white);
  --blue-400: color-mix(in oklch, var(--blue) 75%, white);
  --blue-500: var(--blue);
  --blue-600: color-mix(in oklch, var(--blue) 85%, black);
  --blue-700: color-mix(in oklch, var(--blue) 70%, black);
  --blue-800: color-mix(in oklch, var(--blue) 50%, black);
  --blue-900: color-mix(in oklch, var(--blue) 30%, black);
}
```

Change `--blue` once and the entire palette updates — at runtime, with no build step.

### Transparency mixing

```css
/* Mix with transparent for alpha effects */
.overlay {
  background: color-mix(in oklch, var(--brand) 40%, transparent);
}

/* Equivalent to opacity but composited differently —
   color-mix produces a single color value, not a layered opacity effect */
```

### Comparison with `oklch(from …)` relative color syntax

Both `color-mix()` and relative color syntax (see `color-relative-syntax`) can produce lighter/darker variants. The difference:

| Technique                        | Best for                        | Flexibility        |
| -------------------------------- | ------------------------------- | ------------------ |
| `color-mix(in oklch, color, …)`  | Blending two arbitrary colors   | Two-color mixing   |
| `oklch(from var(--x) calc(…) …)` | Adjusting a single color's axes | Fine-grained edits |

Use `color-mix()` when you're blending two colors or mixing with white/black/transparent. Use relative color syntax when you need precise control over individual color channels (e.g., shifting hue, adjusting chroma independently).

🟡 Newly available (~89%). Supported in all modern browsers. Safe to use in new projects.

Reference: [modern-css.com](https://modern-css.com) · [MDN — color-mix()](https://developer.mozilla.org/en-US/docs/Web/CSS/color_value/color-mix)

### 4.6 Perceptually Uniform Colors With oklch

Building a color palette in hex or HSL requires manually picking each shade because perceived lightness is inconsistent — `hsl(60, 100%, 50%)` (yellow) looks far brighter than `hsl(240, 100%, 50%)` (blue) despite the same `L` value. `oklch()` uses a perceptually uniform lightness channel, so changing only `L` produces shades that genuinely look evenly spaced. Building entire palettes becomes a formula instead of guesswork.

**Avoid (hand-picked hex/HSL shades):**

```css
:root {
  --brand-50: #eef2ff;
  --brand-100: #e0e7ff;
  --brand-200: #c7d2fe;
  --brand-300: #a5b4fc;
  --brand-400: #818cf8;
  --brand-500: #6366f1;
  --brand-600: #4f46e5;
  --brand-700: #4338ca;
  --brand-800: #3730a3;
  --brand-900: #312e81;
  /* Each value hand-picked or generated externally — no relationship between them */
}
```

Or HSL with inconsistent perceived lightness:

```css
:root {
  --brand: hsl(239, 84%, 67%);
  --brand-light: hsl(239, 84%, 80%);
  --brand-dark: hsl(239, 84%, 40%);
  /* Lightness steps look uneven — HSL lightness ≠ perceived lightness */
}
```

**Prefer (oklch — perceptually uniform):**

```css
:root {
  --brand: oklch(0.55 0.2 264);
  --brand-light: oklch(0.75 0.2 264);
  --brand-dark: oklch(0.35 0.2 264);
  /* Only L changes — hue and chroma stay constant.
     Each step looks evenly lighter/darker to the human eye. */
}
```

### How oklch channels work

```
oklch(L C H)
       │ │ │
       │ │ └─ Hue: 0–360 (color wheel angle, like HSL)
       │ └─── Chroma: 0–0.4 (color intensity / saturation)
       └───── Lightness: 0–1 (perceptually uniform — the key advantage)
```

- **L (Lightness)**: `0` = black, `1` = white. Unlike HSL, equal numeric steps produce equal perceived brightness steps.
- **C (Chroma)**: `0` = gray, higher = more vivid. Maximum varies by hue. Unlike HSL saturation, chroma is absolute — `0.2` looks equally vivid across all hues.
- **H (Hue)**: `0`–`360` degree angle on the color wheel.

### Building a full palette with a formula

Because lightness is perceptually uniform, you can generate an entire shade scale by stepping `L` in equal increments:

```css
:root {
  --hue: 264;
  --chroma: 0.18;

  --color-50: oklch(0.97 calc(var(--chroma) * 0.3) var(--hue));
  --color-100: oklch(0.93 calc(var(--chroma) * 0.5) var(--hue));
  --color-200: oklch(0.87 calc(var(--chroma) * 0.7) var(--hue));
  --color-300: oklch(0.78 calc(var(--chroma) * 0.85) var(--hue));
  --color-400: oklch(0.68 var(--chroma) var(--hue));
  --color-500: oklch(0.55 var(--chroma) var(--hue));
  --color-600: oklch(0.48 var(--chroma) var(--hue));
  --color-700: oklch(0.4 var(--chroma) var(--hue));
  --color-800: oklch(0.32 calc(var(--chroma) * 0.9) var(--hue));
  --color-900: oklch(0.25 calc(var(--chroma) * 0.8) var(--hue));
  --color-950: oklch(0.18 calc(var(--chroma) * 0.7) var(--hue));
}
```

To create a second color (e.g., a success green), change only `--hue` — the lightness scale works identically because oklch is perceptually uniform.

### oklch vs. HSL comparison

| Feature                  | HSL                    | oklch                    |
| ------------------------ | ---------------------- | ------------------------ |
| Perceptually uniform     | ❌ No                  | ✅ Yes                   |
| Equal L steps look even  | ❌ No                  | ✅ Yes                   |
| Chroma consistent by hue | ❌ No (S is relative)  | ✅ Yes (C is absolute)   |
| Wide-gamut support       | ❌ sRGB only           | ✅ Display P3 and beyond |
| Palette from a formula   | ❌ Needs manual tuning | ✅ Step L evenly         |

### Alpha transparency

```css
.overlay {
  background: oklch(0.2 0.05 250 / 0.8);
  /* 80% opacity — slash-separated alpha like other modern color functions */
}
```

### When to use oklch vs. other formats

- **oklch** — palette generation, design tokens, any context where you manipulate lightness, chroma, or hue independently. Default choice for new CSS.
- **hex / rgb** — legacy code, one-off colors that don't need manipulation, or when matching exact brand hex values from a design system.
- **hsl** — avoid for new code; oklch does everything HSL does but with perceptual uniformity.
- **color(display-p3 …)** — when you need explicit P3 gamut targeting (see `color-wide-gamut`). oklch naturally reaches into P3 when chroma is high enough.

### Accessibility pairing with oklch

Because lightness is perceptually accurate, you can reliably check contrast by comparing `L` values:

```css
/* L difference of ~0.4+ generally meets WCAG AA for normal text */
--bg: oklch(0.97 0.02 264); /* L = 0.97 */
--text: oklch(0.3 0.05 264); /* L = 0.30, difference ≈ 0.67 ✅ */
```

This is not a substitute for proper contrast ratio calculation, but it gives a reliable quick sanity check that HSL cannot provide.

✅ Widely available (~90%). Supported in all modern browsers. Use as the default color format for new CSS. Falls back gracefully — provide a hex/rgb fallback line if you must support very old browsers.

Reference: [modern-css.com](https://modern-css.com) · [oklch.com color picker](https://oklch.com) · [MDN — oklch()](https://developer.mozilla.org/en-US/docs/Web/CSS/color_value/oklch)

### 4.7 Color Variants Without Sass Functions

Generating lighter, darker, or hue-shifted variants of a color traditionally required Sass functions like `lighten()`, `darken()`, `adjust-hue()`, and `mix()`. These compile to static hex values — they cannot reference CSS custom properties, cannot respond to theming changes at runtime, and lock your codebase into a preprocessor. The relative color syntax lets you derive new colors from any base color directly in CSS, using `from` to decompose the origin color and `calc()` to adjust its components.

**Avoid (Sass color functions — static, build-time only):**

```scss
// Sass — requires a compiler, produces frozen hex values
$brand: #4f46e5;

.btn {
  background: $brand;
}
.btn:hover {
  background: lighten($brand, 15%); // compiles to #8b83f0 — frozen
}
.btn:active {
  background: darken($brand, 10%); // compiles to #3730a3 — frozen
}
.badge {
  background: adjust-hue($brand, 30deg); // compiles to #464fe5 — frozen
}

// Cannot reference CSS custom properties:
// lighten(var(--brand), 15%) — ERROR
```

**Prefer (relative color syntax — live, runtime, composable):**

```css
:root {
  --brand: oklch(0.55 0.2 264);
}

.btn {
  background: var(--brand);
}

.btn:hover {
  /* Lighten: increase L (lightness) */
  background: oklch(from var(--brand) calc(l + 0.15) c h);
}

.btn:active {
  /* Darken: decrease L */
  background: oklch(from var(--brand) calc(l - 0.1) c h);
}

.badge {
  /* Shift hue by 30 degrees */
  background: oklch(from var(--brand) l c calc(h + 30));
}
```

The `from` keyword decomposes the origin color into its components (`l`, `c`, `h` in oklch), which you can then adjust with `calc()`. Because it references `var(--brand)`, changing the custom property at runtime updates every derived color automatically.

### Syntax breakdown

```
oklch(from <origin> <L> <C> <H>)
```

- `from <origin>` — the base color to derive from (any valid color, including `var()`).
- `l`, `c`, `h` — channel keywords that resolve to the origin color's component values.
- Use `calc()` to modify any channel, or pass it through unchanged.

### Common transformations

```css
:root {
  --color: oklch(0.6 0.2 250);
}

/* Lighten */
.light {
  color: oklch(from var(--color) calc(l + 0.2) c h);
}

/* Darken */
.dark {
  color: oklch(from var(--color) calc(l - 0.2) c h);
}

/* Desaturate (reduce chroma) */
.muted {
  color: oklch(from var(--color) l calc(c - 0.1) h);
}

/* Saturate (increase chroma) */
.vivid {
  color: oklch(from var(--color) l calc(c + 0.1) h);
}

/* Complement (opposite hue) */
.complement {
  color: oklch(from var(--color) l c calc(h + 180));
}

/* Semi-transparent variant */
.ghost {
  color: oklch(from var(--color) l c h / 0.5);
}

/* Adjust multiple channels at once */
.soft {
  color: oklch(from var(--color) calc(l + 0.15) calc(c * 0.6) h);
}
```

### Building a full palette from one token

```css
:root {
  --brand: oklch(0.55 0.22 264);

  --brand-50: oklch(from var(--brand) 0.97 calc(c * 0.15) h);
  --brand-100: oklch(from var(--brand) 0.93 calc(c * 0.3) h);
  --brand-200: oklch(from var(--brand) 0.87 calc(c * 0.5) h);
  --brand-300: oklch(from var(--brand) 0.78 calc(c * 0.7) h);
  --brand-400: oklch(from var(--brand) 0.68 calc(c * 0.85) h);
  --brand-500: oklch(from var(--brand) l c h);
  --brand-600: oklch(from var(--brand) calc(l - 0.08) c h);
  --brand-700: oklch(from var(--brand) calc(l - 0.15) c h);
  --brand-800: oklch(from var(--brand) calc(l - 0.22) c h);
  --brand-900: oklch(from var(--brand) calc(l - 0.28) calc(c * 0.8) h);
}
```

Change `--brand` to any color, and the entire palette regenerates at runtime — ideal for user-configurable themes, white-label products, or dark mode transitions.

### Works with any color space

The relative color syntax is not limited to `oklch`. You can use it with `hsl`, `rgb`, `lab`, `lch`, or any other supported color function:

```css
/* HSL-based relative color */
.light {
  color: hsl(from var(--color) h s calc(l + 20%));
}

/* RGB-based — useful for alpha adjustments */
.overlay {
  background: rgb(from var(--color) r g b / 0.3);
}
```

However, `oklch` is strongly recommended for lightness and saturation adjustments because its perceptual uniformity ensures that `+0.1` lightness produces the same visual change regardless of the starting hue. HSL and RGB do not have this property — see `color-oklch` for details.

### Replacing common Sass patterns

| Sass function           | Relative color syntax equivalent                |
| ----------------------- | ----------------------------------------------- |
| `lighten($c, 20%)`      | `oklch(from $c calc(l + 0.2) c h)`              |
| `darken($c, 10%)`       | `oklch(from $c calc(l - 0.1) c h)`              |
| `saturate($c, 20%)`     | `oklch(from $c l calc(c + 0.05) h)`             |
| `desaturate($c, 20%)`   | `oklch(from $c l calc(c - 0.05) h)`             |
| `adjust-hue($c, 30deg)` | `oklch(from $c l c calc(h + 30))`               |
| `rgba($c, 0.5)`         | `oklch(from $c l c h / 0.5)`                    |
| `complement($c)`        | `oklch(from $c l c calc(h + 180))`              |
| `mix($a, $b, 50%)`      | `color-mix(in oklch, $a, $b)` (see `color-mix`) |

🟡 Newly available (~87%). Supported in all modern browsers. For older browser fallback, provide a static color value before the relative color declaration:

```css
.btn:hover {
  background: #7c6ef0; /* static fallback */
  background: oklch(from var(--brand) calc(l + 0.15) c h);
}
```

Reference: [modern-css.com](https://modern-css.com) · [MDN — Relative color syntax](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_colors/Relative_colors)

### 4.8 Vivid Colors Beyond sRGB

The `rgb()`, `hsl()`, and hex color notations are limited to the sRGB color space — a gamut defined in 1996 that covers only about 35% of visible colors. Modern displays (nearly all phones, tablets, and recent laptops) support the Display P3 gamut, which is ~50% larger than sRGB. Colors specified in sRGB look washed out compared to what the hardware can actually render. Using `oklch()` or `color(display-p3 …)` lets you access the full range of vivid, saturated colors your users' screens can display.

**Avoid (sRGB-only — washed out on modern displays):**

```css
.hero {
  color: rgb(200, 80, 50);
  background: #4f46e5;
}
/* sRGB gamut only — leaving 50%+ of display capability unused */
```

**Prefer (wide-gamut color):**

```css
.hero {
  color: oklch(0.65 0.25 30);
  background: oklch(0.5 0.25 265);
}

/* Or using the display-p3 color space explicitly */
.vivid-accent {
  color: color(display-p3 1 0.2 0.1);
}
```

### Why `oklch()` is the recommended default

`oklch()` is both wide-gamut and perceptually uniform — equal numeric changes in lightness, chroma, or hue produce equal perceived changes. This makes it ideal for building color scales, adjusting shades, and ensuring consistent contrast:

```css
:root {
  /* Same hue and chroma, only lightness changes — even perceived steps */
  --brand-100: oklch(0.95 0.05 264);
  --brand-200: oklch(0.85 0.1 264);
  --brand-300: oklch(0.75 0.15 264);
  --brand-400: oklch(0.65 0.2 264);
  --brand-500: oklch(0.55 0.25 264);
  --brand-600: oklch(0.45 0.22 264);
  --brand-700: oklch(0.35 0.18 264);
}
```

### `oklch()` vs. `color(display-p3 …)`

| Feature                    | `oklch()`                           | `color(display-p3 …)`        |
| -------------------------- | ----------------------------------- | ---------------------------- |
| Gamut                      | Unbounded (any visible color)       | P3 gamut only                |
| Perceptually uniform       | ✅ Yes                              | ❌ No                        |
| Intuitive to author        | ✅ Lightness, chroma, hue           | ❌ Red, green, blue channels |
| Building color scales      | ✅ Excellent                        | ❌ Same issues as `rgb()`    |
| Specifying exact P3 colors | Use `oklch()` and let browser clamp | ✅ Direct P3 channel control |

For most use cases, `oklch()` is the better choice. Use `color(display-p3 …)` when you need to specify an exact P3 color value from a design tool that exports in P3.

### Fallback for older browsers

Browsers that don't understand wide-gamut colors will ignore the declaration and use the previous one. Use the cascade for graceful degradation:

```css
.accent {
  /* sRGB fallback */
  background: #4f46e5;
  /* Wide-gamut override — ignored by browsers that don't support it */
  background: oklch(0.5 0.25 265);
}
```

Or use `@supports` for more complex fallback logic:

```css
.gradient {
  background: linear-gradient(135deg, #e040fb, #536dfe);
}

@supports (color: oklch(0 0 0)) {
  .gradient {
    background: linear-gradient(135deg, oklch(0.7 0.3 320), oklch(0.55 0.25 265));
  }
}
```

### Gamut mapping

When an `oklch()` color exceeds the display's gamut (e.g., specifying a P3 color on an sRGB-only monitor), the browser automatically clamps it to the closest in-gamut color. You don't need to manually provide sRGB alternatives for every color — the browser handles it.

### Common wide-gamut use cases

```css
/* Vivid brand accents that pop on P3 displays */
.cta {
  background: oklch(0.65 0.3 145); /* vibrant green — impossible in sRGB */
}

/* Saturated gradients */
.hero-bg {
  background: linear-gradient(
    135deg,
    oklch(0.6 0.3 330),
    /* hot pink */ oklch(0.5 0.28 265) /* electric blue */
  );
}

/* Rich photography overlays */
.overlay {
  background: oklch(0.2 0.05 250 / 0.8); /* deep blue-tinted overlay with alpha */
}
```

### Alpha channel syntax

Both `oklch()` and `color()` support the `/` alpha syntax:

```css
.glass {
  background: oklch(0.98 0.01 250 / 0.5);
  /* 50% transparent — no separate rgba() call needed */
}

.tinted {
  background: color(display-p3 0.2 0.1 0.4 / 0.75);
}
```

Use `oklch()` as your default color notation for all new CSS. It provides wide-gamut access, perceptual uniformity, and an intuitive authoring model. Reserve `rgb()` / hex for legacy codebases or when a design system explicitly requires sRGB values. See also `color-oklch` for more on building perceptually uniform palettes.

✅ Widely available (~90%). `oklch()` and `color(display-p3 …)` are supported in all modern browsers. Provide a hex or `rgb()` fallback line for the small number of older browsers if needed.

Reference: [modern-css.com](https://modern-css.com) · [MDN — oklch()](https://developer.mozilla.org/en-US/docs/Web/CSS/color_value/oklch) · [MDN — color()](https://developer.mozilla.org/en-US/docs/Web/CSS/color_value/color)


## 5. Selectors

### 5.1 Focus Styles Without Annoying Mouse Users

Styling `:focus` applies the focus indicator on every interaction — keyboard, mouse, touch, and programmatic focus. This leads to one of two bad outcomes: either developers remove the outline entirely (`outline: none` — an accessibility failure) or users see distracting focus rings on every button click. `:focus-visible` applies focus styles only when the browser determines the user is navigating with a keyboard, giving you accessible focus indicators without visual noise on mouse and touch interactions.

**Avoid (:focus on everything — or removing it entirely):**

```css
/* Shows focus ring on mouse click — annoying */
:focus {
  outline: 2px solid blue;
}

/* Or the common "fix" that breaks accessibility */
:focus {
  outline: none;
}
/* Keyboard users can no longer see where they are — WCAG 2.4.7 failure */
```

Or the JavaScript workaround:

```js
// Track input method to toggle a class
document.addEventListener('keydown', () => document.body.classList.add('keyboard-user'));
document.addEventListener('mousedown', () => document.body.classList.remove('keyboard-user'));
```

```css
.keyboard-user :focus {
  outline: 2px solid blue;
}
```

**Prefer (modern CSS):**

```css
:focus-visible {
  outline: 2px solid var(--focus-color, oklch(0.55 0.2 264));
  outline-offset: 2px;
}
```

No JavaScript, no class toggling, no input-method tracking. The browser applies the outline only when the user is keyboard-navigating (Tab, arrow keys, etc.) and hides it for mouse and touch interactions.

### When `:focus-visible` matches

| Interaction             | `:focus` | `:focus-visible`   |
| ----------------------- | -------- | ------------------ |
| Mouse click on a button | ✅       | ❌                 |
| Tab to a button         | ✅       | ✅                 |
| Tab to a text input     | ✅       | ✅                 |
| Click into a text input | ✅       | ✅ (always shows)  |
| Programmatic `.focus()` | ✅       | Depends on context |
| Touch tap on a button   | ✅       | ❌                 |

Text inputs (`<input>`, `<textarea>`, `<select>`) always match `:focus-visible` because the user always needs to see where they're typing. Interactive controls like buttons and links only match when keyboard navigation is detected.

### Recommended global focus styles

```css
/* Visible focus ring for keyboard users */
:focus-visible {
  outline: 2px solid var(--focus-color, oklch(0.55 0.2 264));
  outline-offset: 2px;
}

/* Remove the default focus ring for mouse/touch — :focus-visible handles it */
:focus:not(:focus-visible) {
  outline: none;
}
```

The `:focus:not(:focus-visible)` rule explicitly removes the outline for non-keyboard focus, ensuring clean mouse interactions while keeping full keyboard accessibility.

### Custom focus ring designs

```css
/* Rounded focus ring that follows border-radius */
:focus-visible {
  outline: 2px solid var(--focus-color);
  outline-offset: 2px;
  border-radius: inherit; /* outline follows the element's border-radius in modern browsers */
}

/* Box-shadow alternative for more control */
:focus-visible {
  outline: none;
  box-shadow: 0 0 0 3px var(--focus-color);
}

/* High contrast — double ring for visibility on any background */
:focus-visible {
  outline: 2px solid var(--focus-color);
  outline-offset: 2px;
  box-shadow: 0 0 0 4px var(--surface-bg, white);
}
```

### Dark mode aware focus

```css
:root {
  --focus-color: light-dark(oklch(0.55 0.22 264), oklch(0.75 0.18 264));
}

:focus-visible {
  outline: 2px solid var(--focus-color);
  outline-offset: 2px;
}
```

### Per-component focus customization

```css
/* Buttons — standard ring */
button:focus-visible {
  outline: 2px solid var(--focus-color);
  outline-offset: 2px;
}

/* Cards — larger offset for grouped content */
.card:focus-visible {
  outline: 2px solid var(--focus-color);
  outline-offset: 4px;
}

/* Inputs — inner ring effect */
input:focus-visible,
textarea:focus-visible {
  outline: none;
  border-color: var(--focus-color);
  box-shadow: 0 0 0 3px oklch(0.55 0.2 264 / 0.25);
}
```

### Accessibility requirements

WCAG 2.2 Success Criterion 2.4.7 (Focus Visible, Level AA) requires that keyboard focus indicators are visible. `:focus-visible` satisfies this requirement — it ensures focus indicators appear whenever they're needed (keyboard navigation) while removing them when they're not (mouse/touch). See the `frontend-a11y` skill for full WCAG compliance patterns.

**Never do this:**

```css
/* ❌ Removes ALL focus indicators — WCAG failure */
* {
  outline: none !important;
}

/* ❌ Only styling :focus-visible without a :focus fallback for very old browsers */
:focus-visible {
  outline: 2px solid blue;
}
/* In browsers without :focus-visible support (now negligible), no focus ring at all */
```

✅ Widely available (~95%). Supported in all modern browsers. Use as the primary mechanism for focus styling — it is the correct, accessible default.

Reference: [modern-css.com](https://modern-css.com) · [MDN — :focus-visible](https://developer.mozilla.org/en-US/docs/Web/CSS/:focus-visible)

### 5.2 Selecting Parent Elements Without JavaScript

CSS has historically been unable to style a parent based on its children. The only way to apply styles to a `.card` that contains an `<img>` was JavaScript — querying elements, traversing the DOM with `closest()`, and toggling classes. The `:has()` relational pseudo-class finally gives CSS the ability to select elements based on their descendants, siblings, or subsequent content — no JavaScript, no class toggling, no DOM traversal.

**Avoid (JavaScript DOM traversal + class toggling):**

```js
// Style cards differently when they contain an image
document.querySelectorAll('.card').forEach((card) => {
  if (card.querySelector('img')) {
    card.classList.add('card--has-image');
  }
});

// Must re-run on every DOM change (dynamic content, SPA navigation)
const observer = new MutationObserver(() => {
  // re-check all cards…
});
```

```css
.card--has-image {
  grid-template-rows: auto 1fr;
}
```

**Prefer (modern CSS):**

```css
.card:has(img) {
  grid-template-rows: auto 1fr;
}
/* No JavaScript, no class toggling, no mutation observers */
```

The browser re-evaluates `:has()` automatically when the DOM changes — if an image is added or removed, the styles update instantly.

### Common patterns

**Parent styling based on child state:**

```css
/* Form group with an invalid input */
.form-group:has(:user-invalid) {
  border-color: red;
  background: oklch(0.97 0.02 25);
}

/* Form group with a focused input */
.form-group:has(:focus-visible) {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
}

/* Nav item with an active link */
.nav-item:has(a[aria-current='page']) {
  background: var(--nav-active-bg);
}
```

**Conditional layout based on content:**

```css
/* Card layout changes when an image is present */
.card:has(img) {
  display: grid;
  grid-template-columns: 200px 1fr;
}

.card:not(:has(img)) {
  display: flex;
  flex-direction: column;
}

/* Section with more than a certain number of items — combine with :nth-child */
.grid:has(> :nth-child(4)) {
  grid-template-columns: repeat(2, 1fr);
}

.grid:has(> :nth-child(7)) {
  grid-template-columns: repeat(3, 1fr);
}
```

**Sibling-aware styling:**

```css
/* Style a label when its adjacent input is focused */
label:has(+ input:focus-visible) {
  color: var(--accent);
  font-weight: 600;
}

/* Style a heading when followed by a subtitle */
h1:has(+ .subtitle) {
  margin-bottom: 0.25rem;
}
```

**Page-level conditional styling:**

```css
/* Apply styles to body based on the presence of a modal */
body:has(dialog[open]) {
  overflow: hidden;
}

/* Different page layout when sidebar is present */
body:has(.sidebar) {
  --content-max-width: 720px;
}

body:not(:has(.sidebar)) {
  --content-max-width: 960px;
}
```

**Empty state detection:**

```css
/* Show empty state message when list has no items */
.list:not(:has(li)) .empty-state {
  display: block;
}

.list:has(li) .empty-state {
  display: none;
}
```

### Combining with other modern selectors

`:has()` composes powerfully with `:is()`, `:where()`, and `:not()`:

```css
/* Card with any media element */
.card:has(:is(img, video, svg)) {
  grid-template-rows: auto 1fr;
}

/* Zero-specificity version for resets */
:where(.card):has(img) {
  overflow: hidden;
}

/* Cards WITHOUT images */
.card:not(:has(img)) {
  padding-top: 2rem;
}
```

### Performance considerations

`:has()` is evaluated by the browser's selector engine and is generally fast for common patterns. However, avoid deeply nested or overly broad `:has()` selectors that force the browser to scan large subtrees:

```css
/* ✅ Good — scoped, shallow */
.card:has(> img) {
}
.form-group:has(:focus) {
}

/* ⚠️ Potentially expensive — unbounded depth on a high-level element */
html:has(.some-deeply-nested-class) {
}
```

Use the direct child combinator (`>`) inside `:has()` when you only need to check immediate children, limiting the search scope.

### Specificity

`:has()` contributes the specificity of its most specific argument, just like `:is()`:

```css
/* Specificity of .card:has(img) is (0, 1, 1) — .card + img */
.card:has(img) {
}

/* Specificity of .card:has(.featured) is (0, 2, 0) — .card + .featured */
.card:has(.featured) {
}
```

✅ Widely available (~94%). Supported in all modern browsers. `:has()` is one of the most impactful CSS additions in years — it eliminates entire categories of JavaScript DOM manipulation.

Reference: [modern-css.com](https://modern-css.com) · [MDN — :has()](https://developer.mozilla.org/en-US/docs/Web/CSS/:has)

### 5.3 Text Highlighting Without DOM Manipulation

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

### 5.4 Grouping Selectors Without Repetition

When applying the same styles to multiple compound selectors that share a common ancestor or suffix, the traditional approach repeats the full selector for each variant. The `:is()` pseudo-class accepts a selector list as its argument, letting you factor out the shared parts and list only the differences — dramatically reducing repetition and improving readability.

**Avoid (repeated compound selectors):**

```css
.card h1,
.card h2,
.card h3,
.card h4 {
  margin-bottom: 0.5em;
}

nav a:hover,
nav a:focus,
nav a:focus-visible {
  color: var(--accent);
}

.sidebar .widget h2,
.sidebar .widget h3,
.main .widget h2,
.main .widget h3 {
  font-size: 1rem;
}
```

Each selector must be written out in full — the comma-separated list grows combinatorially when multiple parts vary.

**Prefer (:is() grouping):**

```css
.card :is(h1, h2, h3, h4) {
  margin-bottom: 0.5em;
}

nav a:is(:hover, :focus, :focus-visible) {
  color: var(--accent);
}

:is(.sidebar, .main) .widget :is(h2, h3) {
  font-size: 1rem;
}
```

The last example replaces 4 selectors (2 containers × 2 headings) with a single line. As the number of variants grows, the savings multiply.

### Specificity behavior

`:is()` takes the specificity of its **most specific argument**. This is important to understand:

```css
/* Specificity: (0, 1, 0) — same as .card */
:is(.card, .panel) h2 {
  color: #111;
}

/* Specificity: (0, 1, 1) — .card h2 level, even though div is (0, 0, 1) */
:is(.card, div) h2 {
  color: #111;
}
/* .card raises the specificity for the entire :is() — including the div match */
```

If you need zero specificity instead (e.g., for resets), use `:where()` — see `selector-where`.

### Common patterns

```css
/* Group pseudo-classes */
button:is(:hover, :focus-visible) {
  outline: 2px solid var(--focus-color);
}

/* Group structural selectors */
:is(header, main, footer) > .container {
  max-width: 1200px;
  margin-inline: auto;
}

/* Group attribute selectors */
input:is([type='text'], [type='email'], [type='password'], [type='search']) {
  border: 1px solid var(--border);
  padding: 0.5rem;
}

/* Deeply nested grouping */
:is(article, section, aside) :is(h1, h2, h3) {
  line-height: 1.2;
}
```

### Forgiving selector list

`:is()` uses a **forgiving selector list** — if one selector in the list is invalid, the others still work. This is different from a regular comma-separated selector list, where one invalid selector invalidates the entire rule:

```css
/* Regular list — if :unknown is invalid, the ENTIRE rule is discarded */
.card:hover,
.card:unknown {
  color: red;
}
/* Nothing applies */

/* :is() — :unknown is ignored, :hover still works */
.card:is(:hover, :unknown) {
  color: red;
}
/* :hover still applies */
```

This makes `:is()` safer for progressive enhancement when mixing well-supported and newer selectors.

### :is() vs. :where() vs. :not()

| Pseudo-class | Specificity      | Selector list | Use case                                   |
| ------------ | ---------------- | ------------- | ------------------------------------------ |
| `:is()`      | Highest in list  | Forgiving     | Grouping with normal specificity           |
| `:where()`   | Always (0, 0, 0) | Forgiving     | Resets and defaults (see `selector-where`) |
| `:not()`     | Highest in list  | Forgiving     | Exclusion                                  |

### Nesting with :is()

In native CSS nesting, `:is()` can simplify deeply nested rules:

```css
.card {
  & :is(h2, h3) {
    font-weight: 600;
  }

  & :is(p, li) {
    line-height: 1.6;
  }
}
```

✅ Widely available (~96%). Supported in all major browsers. Use freely — no fallback needed.

Reference: [modern-css.com](https://modern-css.com) · [MDN — :is()](https://developer.mozilla.org/en-US/docs/Web/CSS/:is)

### 5.5 Scroll Spy Without IntersectionObserver

Highlighting the current section's link in a navigation bar ("scroll spy") traditionally requires setting up an `IntersectionObserver` in JavaScript — creating the observer, configuring thresholds, iterating entries, toggling `.active` classes, and cleaning up on unmount. The `:target-current` pseudo-class applies styles to the navigation link whose `href` matches the currently visible/scrolled-to section — no JavaScript, no observers, no class toggling.

**Avoid (JavaScript IntersectionObserver):**

```js
const sections = document.querySelectorAll('section[id]');
const navLinks = document.querySelectorAll('nav a');

const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        navLinks.forEach((link) => link.classList.remove('active'));
        const activeLink = document.querySelector(`nav a[href="#${entry.target.id}"]`);
        if (activeLink) activeLink.classList.add('active');
      }
    });
  },
  {rootMargin: '-50% 0px', threshold: 0},
);

sections.forEach((section) => observer.observe(section));
// + cleanup on unmount / page transitions
// + edge cases: multiple sections visible, scroll direction, resize…
```

```css
nav a {
  color: #666;
}
nav a.active {
  color: var(--accent);
  font-weight: 600;
}
```

**Prefer (modern CSS):**

```css
nav a {
  color: #666;
}

nav a:target-current {
  color: var(--accent);
  font-weight: 600;
}
```

```html
<nav>
  <a href="#intro">Introduction</a>
  <a href="#features">Features</a>
  <a href="#pricing">Pricing</a>
  <a href="#faq">FAQ</a>
</nav>

<section id="intro">…</section>
<section id="features">…</section>
<section id="pricing">…</section>
<section id="faq">…</section>
```

Zero JavaScript. The browser tracks which section is in view and applies the pseudo-class to the corresponding anchor link automatically.

### How `:target-current` works

The browser evaluates which fragment (`#id`) on the page is currently the "target" — either from the URL hash or from scroll position when using `scroll-snap` or native scroll tracking. The `:target-current` pseudo-class matches the `<a>` element whose `href` points to that fragment.

### Styling patterns

```css
/* Underline indicator */
nav a:target-current {
  text-decoration: underline;
  text-underline-offset: 4px;
  text-decoration-thickness: 2px;
  text-decoration-color: var(--accent);
}

/* Background highlight */
nav a:target-current {
  background: oklch(0.55 0.2 264 / 0.1);
  border-radius: 0.25rem;
}

/* Sidebar indicator bar */
.toc a:target-current {
  color: var(--accent);
  border-inline-start: 3px solid var(--accent);
  padding-inline-start: 0.75rem;
}
```

### Table of contents for long articles

```html
<aside class="toc">
  <nav aria-label="Table of contents">
    <a href="#abstract">Abstract</a>
    <a href="#methodology">Methodology</a>
    <a href="#results">Results</a>
    <a href="#discussion">Discussion</a>
    <a href="#conclusion">Conclusion</a>
  </nav>
</aside>
```

```css
.toc a {
  display: block;
  padding: 0.25rem 0.75rem;
  color: #666;
  text-decoration: none;
  border-inline-start: 2px solid transparent;
  transition:
    color 0.2s,
    border-color 0.2s;
}

.toc a:target-current {
  color: var(--accent);
  border-inline-start-color: var(--accent);
  font-weight: 600;
}
```

### Combining with scroll snap

`:target-current` works particularly well with scroll snap sections, where the browser has a clear notion of which section is "current":

```css
.page {
  scroll-snap-type: y mandatory;
  overflow-y: auto;
  height: 100dvh;
}

.page > section {
  scroll-snap-align: start;
  min-height: 100dvh;
}

nav a:target-current {
  color: var(--accent);
}
```

### Differences from `:target`

| Pseudo-class      | Matches                                      | Updates on scroll |
| ----------------- | -------------------------------------------- | ----------------- |
| `:target`         | The element whose `id` matches the URL `#`   | ❌ No             |
| `:target-current` | The `<a>` whose `href` is the current target | ✅ Yes            |

`:target` matches the destination element and only updates when the URL hash changes. `:target-current` matches the navigation link and updates as the user scrolls — making it the correct tool for scroll spy behavior.

🟠 Limited (~48%). Early browser support. Use as a progressive enhancement with an IntersectionObserver JavaScript fallback for broader compatibility. The CSS version can coexist with the JS version — apply a `.no-target-current` class via `@supports` to disable the JS behavior when the native pseudo-class is available:

```css
@supports selector(:target-current) {
  /* Native scroll spy — disable JS version */
  nav a.active {
    all: unset; /* JS-applied class has no effect */
  }

  nav a:target-current {
    color: var(--accent);
    font-weight: 600;
  }
}
```

Reference: [modern-css.com](https://modern-css.com) · [CSS Selectors Level 4 — :target-current](https://drafts.csswg.org/selectors-4/#the-target-current-pseudo)

### 5.6 Form Validation Styles Without JavaScript

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

### 5.7 Low-Specificity Resets Without Complicated Selectors

Reset and base stylesheets need to set sensible defaults without making them hard to override. Traditional resets use class selectors (`.reset ul`) or element selectors that still carry specificity — forcing component styles to match or exceed that specificity to win. The `:where()` pseudo-class wraps any selector and reduces its specificity contribution to **zero**, making resets trivially overridable by any subsequent rule.

**Avoid (resets with non-zero specificity):**

```css
/* Reset with class — specificity (0,1,1) */
.reset ul,
.reset ol {
  margin: 0;
  padding-left: 1.5rem;
  list-style: none;
}

/* Even bare element selectors carry (0,0,1) specificity */
ul,
ol {
  margin: 0;
  padding-left: 1.5rem;
}

/* Component now needs >= (0,0,1) to override, or worse: */
.nav ul {
  padding-left: 0; /* specificity arms race begins */
}
```

**Prefer (zero-specificity reset with `:where()`):**

```css
:where(ul, ol) {
  margin: 0;
  padding-inline-start: 1.5rem;
}

:where(h1, h2, h3, h4, h5, h6) {
  margin-block: 0;
  font-weight: 600;
}

:where(a) {
  color: inherit;
  text-decoration: none;
}

:where(img, picture, video, canvas, svg) {
  display: block;
  max-width: 100%;
}

:where(button, input, select, textarea) {
  font: inherit;
}
```

Every rule above has specificity **(0,0,0)**. Any class, ID, or even a bare element selector in your component styles will override them without a fight — no `!important`, no specificity escalation.

### How `:where()` specificity works

| Selector                    | Specificity |
| --------------------------- | ----------- |
| `ul`                        | (0,0,1)     |
| `.reset ul`                 | (0,1,1)     |
| `:is(ul, ol)`               | (0,0,1)     |
| `:where(ul, ol)`            | **(0,0,0)** |
| `:where(.card, #main, div)` | **(0,0,0)** |

`:where()` always contributes zero specificity, **regardless of what's inside it** — even if the arguments include IDs or classes, the specificity contribution is still zero.

### `:where()` vs. `:is()` — choosing the right one

Both `:where()` and `:is()` accept selector lists and match identically. The only difference is specificity:

```css
/* :is() — takes the specificity of its most specific argument */
:is(ul, ol) {
  margin: 0;
}
/* Specificity: (0,0,1) — same as the most specific argument (ul or ol) */

/* :where() — always zero specificity */
:where(ul, ol) {
  margin: 0;
}
/* Specificity: (0,0,0) — always */
```

| Use case                           | Choose     | Why                                               |
| ---------------------------------- | ---------- | ------------------------------------------------- |
| Resets, base styles, defaults      | `:where()` | Must be easy to override                          |
| Component selectors, utility rules | `:is()`    | Should carry normal specificity to apply properly |
| Third-party CSS you import         | `:where()` | Prevents specificity leaks into your styles       |

### Complete modern CSS reset using `:where()`

```css
/* Box sizing reset */
:where(*, *::before, *::after) {
  box-sizing: border-box;
}

/* Remove default margins */
:where(body, h1, h2, h3, h4, h5, h6, p, figure, blockquote, dl, dd) {
  margin: 0;
}

/* Typography resets */
:where(h1, h2, h3, h4, h5, h6) {
  font-size: inherit;
  font-weight: inherit;
}

/* List resets */
:where(ol, ul) {
  list-style: none;
  padding: 0;
}

/* Link resets */
:where(a) {
  color: inherit;
  text-decoration: inherit;
}

/* Media resets */
:where(img, picture, video, canvas, svg) {
  display: block;
  max-width: 100%;
  height: auto;
}

/* Form resets */
:where(button, input, select, textarea) {
  font: inherit;
  color: inherit;
}

/* Table resets */
:where(table) {
  border-collapse: collapse;
}
```

Every rule has zero specificity — your component styles always win, trivially.

### Wrapping third-party base styles

If you import a CSS library that sets aggressive defaults, wrap its selectors in `:where()` to prevent specificity leaks:

```css
/* Third-party resets made safe */
@layer vendor {
  :where(.prose h1) {
    font-size: 2rem;
  }
  :where(.prose p) {
    line-height: 1.75;
  }
}
```

Combining `:where()` with `@layer` (see `workflow-cascade-layers`) gives you maximum control over both specificity and cascade priority.

✅ Widely available (~96%). Supported in all major browsers. Use freely in resets, base styles, and anywhere you need effortlessly overridable defaults.

Reference: [modern-css.com](https://modern-css.com) · [MDN — :where()](https://developer.mozilla.org/en-US/docs/Web/CSS/:where)


## 6. Animation

### 6.1 Animating Display None Without Workarounds

Transitioning an element to and from `display: none` has been impossible in CSS — the browser removes the element from the layout immediately, skipping any transition. The traditional workaround chains `visibility`, `opacity`, and `pointer-events` together, then uses a JavaScript `transitionend` listener to set `display: none` after the fade completes. The `transition-behavior: allow-discrete` property tells the browser to transition discrete properties like `display`, eliminating the multi-property hack and the JavaScript listener entirely.

**Avoid (visibility + opacity + JS transitionend):**

```js
// Wait for opacity transition to finish, then set display: none
function hideElement(el) {
  el.style.opacity = '0';
  el.style.pointerEvents = 'none';

  el.addEventListener(
    'transitionend',
    () => {
      el.style.display = 'none';
    },
    {once: true},
  );
}

function showElement(el) {
  el.style.display = 'block';
  // Force reflow so the browser sees display change before opacity change
  el.offsetHeight;
  el.style.opacity = '1';
  el.style.pointerEvents = '';
}
```

```css
.panel {
  opacity: 1;
  visibility: visible;
  pointer-events: auto;
  transition:
    opacity 0.2s ease,
    visibility 0.2s ease;
}

.panel.hidden {
  opacity: 0;
  visibility: hidden;
  pointer-events: none;
  /* display: none would skip the transition entirely */
}
/* Element is still in the layout (takes up space) even when "hidden" */
```

The `visibility` + `opacity` approach has a critical flaw: the element remains in the document flow and occupies space. True `display: none` removal requires JavaScript timing.

**Prefer (modern CSS with `allow-discrete`):**

```css
.panel {
  opacity: 1;
  display: block;
  transition:
    opacity 0.2s ease,
    display 0.2s ease,
    overlay 0.2s ease;
  transition-behavior: allow-discrete;
}

.panel.hidden {
  opacity: 0;
  display: none;
}
```

No JavaScript, no `transitionend` listener, no forced reflow hack. The browser:

1. Keeps `display: block` during the exit transition so `opacity` can animate.
2. Switches to `display: none` only after the transition completes.
3. On entry (removing `.hidden`), immediately sets `display: block` and then animates `opacity`.

### The `overlay` property

When transitioning elements in the top layer (dialogs, popovers), include `overlay` in the transition list to keep the element in the top layer during the exit animation:

```css
dialog {
  opacity: 1;
  transition:
    opacity 0.3s ease,
    display 0.3s ease,
    overlay 0.3s ease;
  transition-behavior: allow-discrete;
}

dialog:not([open]) {
  opacity: 0;
  display: none;
}
```

Without `overlay`, a closing dialog would drop out of the top layer immediately, snapping behind other content before the opacity fade completes.

### Combining with `@starting-style` for entry animations

`allow-discrete` handles the exit transition (block → none), but the entry transition (none → block) also needs a starting state. Use `@starting-style` to define what the element looks like when it first appears:

```css
.panel {
  opacity: 1;
  transform: translateY(0);
  display: block;
  transition:
    opacity 0.3s ease,
    transform 0.3s ease,
    display 0.3s ease;
  transition-behavior: allow-discrete;

  @starting-style {
    opacity: 0;
    transform: translateY(10px);
  }
}

.panel.hidden {
  opacity: 0;
  transform: translateY(10px);
  display: none;
}
```

See `animation-starting-style` for more on entry animations.

### Applying to popover and dialog

```css
[popover] {
  opacity: 0;
  transform: scale(0.95);
  transition:
    opacity 0.2s ease,
    transform 0.2s ease,
    display 0.2s ease,
    overlay 0.2s ease;
  transition-behavior: allow-discrete;
}

[popover]:popover-open {
  opacity: 1;
  transform: scale(1);
}

[popover]:popover-open {
  @starting-style {
    opacity: 0;
    transform: scale(0.95);
  }
}
```

### Shorthand syntax

You can specify `allow-discrete` per-property in the `transition` shorthand:

```css
.panel {
  transition:
    opacity 0.2s ease,
    display 0.2s ease allow-discrete,
    overlay 0.2s ease allow-discrete;
}
/* Only display and overlay are discrete — opacity transitions normally */
```

Or apply `transition-behavior: allow-discrete` as a blanket rule — it has no effect on properties that already transition continuously (like `opacity`), so it's safe to set globally.

### What `allow-discrete` actually does

Discrete properties (like `display`, `content-visibility`) have no intermediate values — they can only snap between states. `allow-discrete` tells the browser to delay the snap to the end of the transition duration (for exit) or apply it at the start (for entry), giving continuous properties like `opacity` and `transform` time to animate.

| Transition direction | When `display` changes            |
| -------------------- | --------------------------------- |
| Entry (none → block) | Immediately at transition start   |
| Exit (block → none)  | At the end of transition duration |

🟡 Newly available (~85%). Supported in all modern browsers. Falls back gracefully — in unsupporting browsers, the element snaps to `display: none` without animation, which is functional if not smooth.

Reference: [modern-css.com](https://modern-css.com) · [MDN — transition-behavior](https://developer.mozilla.org/en-US/docs/Web/CSS/transition-behavior)

### 6.2 Independent Transforms Without the Shorthand

When multiple transforms are applied to an element via the `transform` shorthand, changing any single transform requires rewriting the entire value — including the parts that didn't change. This makes animations verbose, error-prone, and impossible to compose independently (e.g., animating rotation on hover while translate runs on a separate keyframe timeline). The individual `translate`, `rotate`, and `scale` properties each operate independently, so you can animate one without touching the others.

**Avoid (transform shorthand — change one, rewrite all):**

```css
.icon {
  transform: translateX(10px) rotate(45deg) scale(1.2);
}

/* Want to animate only the rotation? Must rewrite everything: */
.icon:hover {
  transform: translateX(10px) rotate(90deg) scale(1.2);
  transition: transform 0.3s ease;
  /* translateX and scale are repeated just to keep them from resetting */
}

/* Separate keyframe animations on different axes? Impossible —
   the last transform declaration wins, overwriting everything. */
```

**Prefer (individual transform properties):**

```css
.icon {
  translate: 10px 0;
  rotate: 45deg;
  scale: 1.2;
}

/* Animate only the rotation — others are untouched */
.icon:hover {
  rotate: 90deg;
  transition: rotate 0.3s ease;
}
```

Each property is independent — changing `rotate` does not affect `translate` or `scale`. No rewriting, no accidental resets.

### Composing independent animations

Individual transform properties unlock the ability to run separate animations on different axes simultaneously:

```css
.floating-icon {
  animation:
    bob 2s ease-in-out infinite alternate,
    spin 4s linear infinite;
}

@keyframes bob {
  from {
    translate: 0 0;
  }
  to {
    translate: 0 -10px;
  }
}

@keyframes spin {
  to {
    rotate: 360deg;
  }
}
/* Both animations compose — impossible with the transform shorthand */
```

With the `transform` shorthand, only one `@keyframes` can animate `transform` at a time — the second would overwrite the first.

### Property syntax

```css
/* translate — accepts 1–3 values (x, y, z) */
.moved {
  translate: 20px; /* translateX(20px) */
  translate: 20px 10px; /* translateX(20px) translateY(10px) */
  translate: 20px 10px 5px; /* + translateZ(5px) */
}

/* rotate — accepts an angle, optionally with an axis */
.turned {
  rotate: 45deg; /* rotateZ(45deg) */
  rotate: x 45deg; /* rotateX(45deg) */
  rotate: y 45deg; /* rotateY(45deg) */
  rotate: 1 1 0 45deg; /* rotate3d(1, 1, 0, 45deg) */
}

/* scale — accepts 1–3 values (x, y, z) */
.sized {
  scale: 1.2; /* uniform scale */
  scale: 1.2 0.8; /* scaleX(1.2) scaleY(0.8) */
  scale: 1.2 0.8 1; /* + scaleZ(1) */
}
```

### Application order

Individual transform properties are always applied in this fixed order, regardless of declaration order in CSS:

1. `translate`
2. `rotate`
3. `scale`

Then `transform` (if also present) is applied after all three.

```css
/* These produce the same result regardless of source order */
.a {
  translate: 10px;
  rotate: 45deg;
  scale: 1.5;
}

.b {
  scale: 1.5;
  translate: 10px;
  rotate: 45deg;
}
/* Both apply as: translate → rotate → scale */
```

This fixed order means you cannot replicate every `transform` shorthand combination — `transform: rotate(45deg) translateX(100px)` (rotate first, then translate along the rotated axis) produces a different result than `translate: 100px; rotate: 45deg` (translate first, then rotate). For those cases, continue using the `transform` shorthand.

### Combining with the `transform` shorthand

Individual properties and the `transform` shorthand coexist. Individual properties apply first (in their fixed order), then `transform` applies on top:

```css
.card {
  translate: 0 -10px;
  transform: perspective(800px) rotateY(5deg);
  /* translate applies, then perspective + rotateY */
}
```

### When to use which

| Scenario                                           | Use                   |
| -------------------------------------------------- | --------------------- |
| Animate one axis independently                     | Individual properties |
| Compose multiple animations on different axes      | Individual properties |
| Hover/focus effects that change a single transform | Individual properties |
| Complex transform chains where order matters       | `transform` shorthand |
| 3D transforms with `perspective()`                 | `transform` shorthand |

### Transition examples

```css
/* Button hover — only scale, without rewriting translate/rotate */
.btn {
  scale: 1;
  transition: scale 0.15s ease;
}
.btn:hover {
  scale: 1.05;
}
.btn:active {
  scale: 0.98;
}

/* Card tilt on hover — independent rotation transition */
.card {
  rotate: 0deg;
  transition: rotate 0.3s ease;
}
.card:hover {
  rotate: -2deg;
}
```

✅ Widely available (~92%). Supported in all major browsers. Prefer individual properties over the `transform` shorthand for any single-axis animation or when composing multiple independent animations.

Reference: [modern-css.com](https://modern-css.com) · [MDN — translate](https://developer.mozilla.org/en-US/docs/Web/CSS/translate) · [MDN — rotate](https://developer.mozilla.org/en-US/docs/Web/CSS/rotate) · [MDN — scale](https://developer.mozilla.org/en-US/docs/Web/CSS/scale)

### 6.3 Smooth Height Auto Animations Without JavaScript

Animating an element's height from `0` to `auto` is one of the most common UI patterns (accordions, collapsible panels, expandable sections) — and one of the hardest to do without JavaScript. The browser cannot transition to `height: auto` because `auto` is a keyword, not a numeric value. The traditional workaround measures `scrollHeight` in JavaScript, sets an explicit pixel height, waits for `transitionend`, then resets to `auto`. The `interpolate-size: allow-keywords` declaration tells the browser to interpolate between numeric values and sizing keywords like `auto`, enabling smooth CSS-only height transitions.

**Avoid (JavaScript scrollHeight measurement):**

```js
// Expand: measure, set explicit height, then snap to auto
function expand(el) {
  el.style.height = el.scrollHeight + 'px'; // force reflow to measure
  el.addEventListener(
    'transitionend',
    () => {
      el.style.height = 'auto'; // snap to auto after transition
    },
    {once: true},
  );
}

// Collapse: read current height, set explicit, then transition to 0
function collapse(el) {
  el.style.height = el.scrollHeight + 'px'; // set current height explicitly
  requestAnimationFrame(() => {
    el.style.height = '0'; // now the transition can run
  });
}
// Layout thrashing on every open/close, fragile timing, must handle interruption
```

```css
.panel {
  overflow: hidden;
  transition: height 0.3s ease;
}
```

Or the `max-height` hack:

```css
.panel {
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.3s ease;
}

.panel.open {
  max-height: 500px; /* magic number — too small clips content, too large delays close */
}
```

The `max-height` approach produces a mismatched easing curve (the animation covers the full range from 0 to 500px but the content only fills part of it) and a delayed collapse when the content is much shorter than the max.

**Prefer (modern CSS):**

```css
:root {
  interpolate-size: allow-keywords;
}

.accordion-content {
  height: 0;
  overflow: hidden;
  transition: height 0.3s ease;
}

.accordion-content.open {
  height: auto;
}
```

Zero JavaScript measurement. Zero magic numbers. The browser smoothly interpolates between `height: 0` and `height: auto` (the intrinsic content height) with proper easing — the animation matches the actual content size exactly.

### How it works

`interpolate-size: allow-keywords` opts the element (and its descendants, since it inherits) into keyword interpolation. Once enabled, the browser can transition or animate between:

- `height: 0` → `height: auto`
- `width: auto` → `width: 200px`
- `min-height: 0` → `min-height: max-content`
- Any numeric value → any sizing keyword (`auto`, `min-content`, `max-content`, `fit-content`)

### Setting it globally

Because `interpolate-size` inherits, setting it on `:root` enables keyword interpolation for the entire page:

```css
:root {
  interpolate-size: allow-keywords;
}
```

This is safe to apply globally — it only affects elements that actually have transitions or animations on sizing properties. Elements without transitions render identically.

### Accordion pattern — pure CSS

```html
<details name="faq">
  <summary>Question 1</summary>
  <div class="details-content">
    <p>Answer to question 1.</p>
  </div>
</details>
<details name="faq">
  <summary>Question 2</summary>
  <div class="details-content">
    <p>
      Answer to question 2, which is much longer and demonstrates that the animation adapts to the
      actual content height.
    </p>
  </div>
</details>
```

```css
:root {
  interpolate-size: allow-keywords;
}

details .details-content {
  height: 0;
  overflow: hidden;
  opacity: 0;
  transition:
    height 0.3s ease,
    opacity 0.3s ease;
}

details[open] .details-content {
  height: auto;
  opacity: 1;
}
```

### Width animations

The same pattern works for width transitions — collapsible sidebars, expanding search inputs, etc.:

```css
.sidebar {
  width: 0;
  overflow: hidden;
  transition: width 0.3s ease;
}

.sidebar.expanded {
  width: auto; /* or width: max-content */
}
```

### Combining with `@starting-style` for entry animations

```css
:root {
  interpolate-size: allow-keywords;
}

.panel {
  height: auto;
  transition: height 0.3s ease;

  @starting-style {
    height: 0;
  }
}
```

### Why not `calc-size()`?

The `calc-size()` function is a more targeted alternative that enables keyword interpolation on a per-property basis:

```css
.panel.open {
  height: calc-size(auto);
}
```

`interpolate-size: allow-keywords` is the simpler, global approach — set it once on `:root` and forget about it. Use `calc-size()` when you need to perform arithmetic on keyword sizes (e.g., `calc-size(auto, size + 2rem)` for auto height plus padding compensation).

🟡 Newly available (~69%). Supported in Chromium and Firefox. For broader support, use the JavaScript `scrollHeight` approach as a fallback:

```js
if (!CSS.supports('interpolate-size', 'allow-keywords')) {
  // Fall back to JS measurement approach
}
```

Reference: [modern-css.com](https://modern-css.com) · [MDN — interpolate-size](https://developer.mozilla.org/en-US/docs/Web/CSS/interpolate-size)

### 6.4 Custom Easing Curves Without cubic-bezier Guessing

Complex easing curves like bounce, elastic, and spring effects have traditionally required JavaScript animation libraries (GSAP, Anime.js, Framer Motion) because `cubic-bezier()` can only represent a limited subset of curves — it cannot overshoot multiple times, bounce, or create step-like patterns. The `linear()` easing function accepts an arbitrary number of control points, letting you define any easing curve imaginable in pure CSS.

**Avoid (JavaScript animation library for bounce/spring):**

```js
// Anime.js — 17 KB+ gzipped
import anime from 'animejs';

anime({
  targets: '.card',
  translateY: [50, 0],
  easing: 'easeOutBounce',
  duration: 1000,
});

// Or GSAP
gsap.to('.card', {
  y: 0,
  ease: 'bounce.out',
  duration: 1,
});
// + library dependency, JS execution cost, not compositor-accelerated
```

**Prefer (CSS `linear()` easing):**

```css
.card {
  transition: transform 1s
    linear(
      0,
      0.004,
      0.016,
      0.035,
      0.063,
      0.098,
      0.141,
      0.191,
      0.25,
      0.316,
      0.391,
      0.473,
      0.563,
      0.66,
      0.766,
      0.879,
      1,
      0.891,
      0.813,
      0.766,
      0.75,
      0.766,
      0.813,
      0.891,
      1,
      0.938,
      0.906,
      0.938,
      1
    );
}

.card:hover {
  transform: translateY(-10px);
}
/* GPU-composited bounce — no JS library, no main thread work */
```

### How `linear()` works

`linear()` defines an easing curve as a series of output values at evenly spaced intervals (or at explicit positions). The browser interpolates linearly between each pair of points, creating a piecewise-linear approximation of any curve:

```
linear(output1, output2, output3, …)
```

- Each value is a number where `0` = start and `1` = end.
- Values above `1` create overshoot; values below `0` create undershoot.
- Points are evenly distributed unless explicit stops are provided.

### Common easing curves

**Bounce out:**

```css
.bounce {
  animation-timing-function: linear(
    0,
    0.004,
    0.016,
    0.035,
    0.063,
    0.098,
    0.141,
    0.191,
    0.25,
    0.316,
    0.391,
    0.473,
    0.563,
    0.66,
    0.766,
    0.879,
    1,
    0.891,
    0.813,
    0.766,
    0.75,
    0.766,
    0.813,
    0.891,
    1,
    0.938,
    0.906,
    0.938,
    1
  );
}
```

**Elastic out:**

```css
.elastic {
  animation-timing-function: linear(
    0,
    0.218 2.1%,
    0.862 6.5%,
    1.114,
    1.296 10.7%,
    1.346,
    1.37 12.9%,
    1.373,
    1.364 14.5%,
    1.315 16.2%,
    1.032 21.8%,
    0.941 24%,
    0.891 25.9%,
    0.877,
    0.869 27.8%,
    0.877,
    0.895 30.4%,
    1.012 38.3%,
    1.029,
    1.032 42.7%,
    1.024 44.1%,
    0.99 53.3%,
    0.997 55.2%,
    1.003 59.2%,
    1
  );
}
```

**Spring (gentle overshoot):**

```css
.spring {
  animation-timing-function: linear(
    0,
    0.009,
    0.035,
    0.078,
    0.141,
    0.223,
    0.326,
    0.45,
    0.594,
    0.758,
    0.938,
    1.026,
    1.078,
    1.096,
    1.087,
    1.054,
    1.009,
    0.963,
    0.927,
    0.907,
    0.903,
    0.916,
    0.94,
    0.969,
    0.993,
    1.008,
    1.014,
    1.012,
    1.004,
    0.998,
    0.996,
    0.998,
    1
  );
}
```

### Explicit stop positions

You can specify where each point falls on the timeline using percentages:

```css
.custom {
  transition-timing-function: linear(0, 0.5 25%, 1 50%, 0.8 75%, 1);
  /* Quick rise to 0.5 at 25%, peak at 50%, dip to 0.8 at 75%, settle at 1 */
}
```

### Generating `linear()` curves

Rather than hand-writing control points, use these tools:

- **[linear-easing-generator.netlify.app](https://linear-easing-generator.netlify.app)** — paste a JavaScript easing function and get the CSS `linear()` output.
- **[cubic-bezier.com](https://cubic-bezier.com)** — for simple curves that `cubic-bezier()` can handle (no overshoot beyond one bounce).

### When to use `linear()` vs. `cubic-bezier()`

| Easing type        | `cubic-bezier()`      | `linear()`                  |
| ------------------ | --------------------- | --------------------------- |
| Simple ease-in/out | ✅ Simpler, smaller   | Works but unnecessary       |
| Single overshoot   | ✅ Can express this   | Works                       |
| Multi-bounce       | ❌ Cannot express     | ✅ The only CSS option      |
| Elastic / spring   | ❌ Cannot express     | ✅ The only CSS option      |
| Steps              | Use `steps()` instead | Can approximate             |
| Arbitrary curve    | ❌ Limited to cubic   | ✅ Piecewise-linear approx. |

Use `cubic-bezier()` (or the built-in keywords `ease`, `ease-in`, `ease-out`, `ease-in-out`) for simple curves. Reach for `linear()` when you need bounce, spring, elastic, or any multi-phase easing that `cubic-bezier()` cannot represent.

### Composing with individual transforms

Combine `linear()` with individual transform properties (see `animation-individual-transforms`) for complex, multi-axis animations:

```css
.card {
  translate: 0 50px;
  opacity: 0;
  transition:
    translate 0.8s
      linear(
        0,
        0.063,
        0.25,
        0.563,
        1,
        0.891,
        0.813,
        0.766,
        0.75,
        0.766,
        0.813,
        0.891,
        1,
        0.938,
        0.906,
        0.938,
        1
      ),
    opacity 0.4s ease;
}

.card.visible {
  translate: 0;
  opacity: 1;
}
/* Bounce on Y axis, simple fade on opacity — independent timings */
```

🟡 Newly available (~87%). Supported in all modern browsers. For older browsers, the transition falls back to the default `ease` timing — still functional, just without the custom curve. No polyfill needed.

Reference: [modern-css.com](https://modern-css.com) · [MDN — linear()](https://developer.mozilla.org/en-US/docs/Web/CSS/easing-function/linear) · [Linear easing generator](https://linear-easing-generator.netlify.app)

### 6.5 Reduced Motion Without JavaScript Detection

Respecting a user's reduced-motion preference traditionally required JavaScript — checking `window.matchMedia('(prefers-reduced-motion)')`, listening for changes, and conditionally disabling animations via class toggling or inline styles. The `prefers-reduced-motion` media query handles this entirely in CSS, declaratively and without any JavaScript.

**Avoid (JavaScript matchMedia detection):**

```js
const mq = window.matchMedia('(prefers-reduced-motion: reduce)');

function handleMotionPreference(e) {
  if (e.matches) {
    document.querySelectorAll('[data-animate]').forEach((el) => {
      el.style.animation = 'none';
      el.style.transition = 'none';
    });
  } else {
    // Re-enable animations — must track and restore original values
  }
}

mq.addEventListener('change', handleMotionPreference);
handleMotionPreference(mq);
// Must run on load, track DOM changes, clean up listeners…
```

**Prefer (modern CSS):**

```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

No JavaScript, no event listeners, no class toggling. The browser applies these overrides automatically when the user has enabled "Reduce motion" in their OS settings (macOS, iOS, Windows, Android all support this).

### Why `0.01ms` instead of `0s` or `none`

Setting `animation-duration: 0s` or `animation: none` can break JavaScript that depends on `animationend` or `transitionend` events firing. A near-zero duration (`0.01ms`) ensures the animation still technically runs and fires completion events, but is imperceptible to the user.

### Targeted approach (recommended for production)

The global `*` override is a safety net. For production code, prefer targeting animations explicitly for more control:

```css
.fade-in {
  animation: fade-in 0.5s ease-out;
}

.slide-up {
  animation: slide-up 0.4s ease-out;
}

@media (prefers-reduced-motion: reduce) {
  .fade-in {
    animation: none;
    opacity: 1; /* ensure the final state is visible */
  }

  .slide-up {
    animation: none;
    transform: none; /* ensure the final state is applied */
  }
}
```

### Motion-first vs. no-motion-first approach

**Motion-first** (add animations, remove them for reduced-motion — most common):

```css
.card {
  animation: slide-up 0.3s ease-out;
}

@media (prefers-reduced-motion: reduce) {
  .card {
    animation: none;
  }
}
```

**No-motion-first** (start without animations, add them for users who haven't opted out — more progressive):

```css
.card {
  /* No animation by default */
}

@media (prefers-reduced-motion: no-preference) {
  .card {
    animation: slide-up 0.3s ease-out;
  }
}
```

The no-motion-first approach is safer — users with reduced-motion preferences see no animation by default, and you only add animations for users who explicitly haven't opted out.

### What to reduce vs. remove

Not all motion needs to be removed. The goal is to eliminate vestibular-trigger animations (large movements, parallax, spinning) while preserving meaningful UI feedback:

```css
@media (prefers-reduced-motion: reduce) {
  /* Remove: large movements, parallax, auto-play */
  .parallax {
    transform: none;
  }
  .carousel {
    scroll-behavior: auto;
  }
  .spinner {
    animation: none;
  }

  /* Keep but reduce: small UI feedback */
  .btn {
    transition-duration: 0.1s; /* fast but still provides feedback */
  }

  /* Keep: opacity fades (generally safe) */
  .fade {
    transition: opacity 0.15s ease;
  }
}
```

### Combining with `update` media query

For devices with low refresh rates (e-ink displays), further reduce animations:

```css
@media (update: slow) {
  * {
    animation: none !important;
    transition: none !important;
  }
}
```

### Accessibility requirement

WCAG 2.1 Success Criterion 2.3.3 (Animation from Interactions, Level AAA) requires that motion animation triggered by interaction can be disabled. The `prefers-reduced-motion` media query is the standard mechanism to satisfy this criterion. See the `frontend-a11y` skill for full WCAG compliance patterns.

✅ Widely available (~96%). Supported in all major browsers. Every project with animations should include `prefers-reduced-motion` handling — it is an accessibility requirement, not an optional enhancement.

Reference: [modern-css.com](https://modern-css.com) · [MDN — prefers-reduced-motion](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion) · [web.dev — prefers-reduced-motion](https://web.dev/articles/prefers-reduced-motion)

### 6.6 Sticky & Snapped Element Styling Without JavaScript

Detecting when a sticky element is "stuck" or when a scroll-snap child is "snapped" traditionally requires JavaScript scroll event listeners that compare `getBoundingClientRect()` values on every frame — causing layout thrashing and main-thread work. The `@container scroll-state()` query lets you style elements based on their scroll-related state declaratively in CSS, with zero JavaScript.

**Avoid (JavaScript scroll position checks):**

```js
// Check if sticky header is stuck
const header = document.querySelector('.header');

window.addEventListener('scroll', () => {
  const rect = header.getBoundingClientRect();
  header.classList.toggle('stuck', rect.top <= 0);
});

// Check if a snap child is currently snapped
const items = document.querySelectorAll('.carousel > *');
const carousel = document.querySelector('.carousel');

carousel.addEventListener('scroll', () => {
  items.forEach((item) => {
    const rect = item.getBoundingClientRect();
    const containerRect = carousel.getBoundingClientRect();
    const isSnapped = Math.abs(rect.left - containerRect.left) < 2;
    item.classList.toggle('snapped', isSnapped);
  });
});
// Runs on every scroll frame — layout thrashing, main-thread blocking
```

```css
.header.stuck {
  box-shadow: 0 2px 8px rgb(0 0 0 / 0.1);
  backdrop-filter: blur(8px);
}

.carousel > *.snapped {
  opacity: 1;
  scale: 1;
}
```

**Prefer (CSS scroll-state container queries):**

```css
.header {
  position: sticky;
  top: 0;
  container-type: scroll-state;
}

@container scroll-state(stuck: top) {
  .header {
    box-shadow: 0 2px 8px rgb(0 0 0 / 0.1);
    backdrop-filter: blur(8px);
  }
}
```

No JavaScript, no scroll listeners, no `getBoundingClientRect()`, no class toggling. The browser evaluates the scroll state internally and applies styles when the condition is met.

### Stuck state queries

Detect when a `position: sticky` element is stuck to an edge of its scroll container:

```css
.sticky-nav {
  position: sticky;
  top: 0;
  container-type: scroll-state;
  transition: box-shadow 0.2s ease;
}

/* Stuck to the top edge */
@container scroll-state(stuck: top) {
  .sticky-nav {
    box-shadow: 0 2px 12px rgb(0 0 0 / 0.08);
    border-bottom: 1px solid oklch(0.9 0.01 250);
  }
}

/* Stuck to the bottom edge */
.sticky-footer {
  position: sticky;
  bottom: 0;
  container-type: scroll-state;
}

@container scroll-state(stuck: bottom) {
  .sticky-footer {
    box-shadow: 0 -2px 12px rgb(0 0 0 / 0.08);
  }
}
```

### Snapped state queries

Detect when a scroll-snap child is currently snapped into position:

```css
.carousel {
  scroll-snap-type: x mandatory;
  container-type: scroll-state;
}

.carousel > .slide {
  scroll-snap-align: center;
  opacity: 0.5;
  scale: 0.95;
  transition:
    opacity 0.3s,
    scale 0.3s;
}

@container scroll-state(snapped: x) {
  .slide {
    opacity: 1;
    scale: 1;
  }
}
```

### Scrollable state queries

Detect whether a container is scrollable in a given direction (useful for showing/hiding scroll indicators):

```css
.scrollable-area {
  overflow-y: auto;
  container-type: scroll-state;
}

/* Show a "scroll for more" indicator only when there's content to scroll to */
@container scroll-state(scrollable: top) {
  .scroll-indicator-top {
    display: block;
  }
}

@container scroll-state(scrollable: bottom) {
  .scroll-indicator-bottom {
    display: block;
  }
}
```

### Common patterns

```css
/* Sticky header with progressive shadow */
.page-header {
  position: sticky;
  top: 0;
  z-index: 10;
  container-type: scroll-state;
  background: var(--surface);
}

@container scroll-state(stuck: top) {
  .page-header {
    background: light-dark(rgb(255 255 255 / 0.9), rgb(15 15 15 / 0.9));
    backdrop-filter: blur(12px);
    box-shadow: 0 1px 0 oklch(0.5 0 0 / 0.1);
  }
}

/* Carousel with active slide indicator */
.carousel-wrapper {
  container-type: scroll-state;
}

@container scroll-state(snapped: x) {
  .slide {
    /* Snapped slide gets full prominence */
    filter: none;
  }
}

.slide {
  filter: grayscale(0.5) brightness(0.8);
  transition: filter 0.3s ease;
}
```

### Stuck values

| Value    | Matches when                          |
| -------- | ------------------------------------- |
| `top`    | Stuck to the top edge                 |
| `right`  | Stuck to the right / inline-end edge  |
| `bottom` | Stuck to the bottom edge              |
| `left`   | Stuck to the left / inline-start edge |
| `none`   | Not currently stuck                   |

### Snapped values

| Value  | Matches when                            |
| ------ | --------------------------------------- |
| `x`    | Snapped on the horizontal (inline) axis |
| `y`    | Snapped on the vertical (block) axis    |
| `none` | Not currently snapped                   |

### Why this is better than JavaScript

- **No layout thrashing** — the browser evaluates state internally without forcing layout recalculation.
- **Compositor-driven** — state changes are detected at the compositing level, not on the main thread.
- **Declarative** — styles are defined in CSS where they belong, not spread across JS event handlers.
- **Automatic cleanup** — no observers to disconnect, no listeners to remove.

🟠 Limited (~50%). Early browser support, shipping in Chromium. Use as a progressive enhancement — the element works without the scroll-state styles (just without the visual polish), and a JavaScript `scroll` listener can serve as a fallback for broader compatibility.

Reference: [modern-css.com](https://modern-css.com) · [CSS Conditional Rules — scroll-state()](https://drafts.csswg.org/css-conditional-5/#scroll-state-container-query)

### 6.7 Scroll-Linked Animations Without a Library

Scroll-linked animations — fade-ins on scroll, parallax effects, progress indicators — traditionally require JavaScript scroll event listeners or IntersectionObserver setups that read scroll position, calculate progress, and apply styles on every frame. This blocks the main thread and can't be composited by the GPU. The `animation-timeline` property with `scroll()` and `view()` functions creates scroll-driven animations entirely in CSS, running on the compositor thread at 60fps with zero JavaScript.

**Avoid (JavaScript scroll listeners):**

```js
// IntersectionObserver for reveal-on-scroll
const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.style.opacity = '1';
        entry.target.style.transform = 'translateY(0)';
        observer.unobserve(entry.target);
      }
    });
  },
  {threshold: 0.1},
);

document.querySelectorAll('.reveal').forEach((el) => observer.observe(el));

// Or scroll progress bar with scroll listener
window.addEventListener('scroll', () => {
  const scrollPct = window.scrollY / (document.body.scrollHeight - window.innerHeight);
  progressBar.style.width = `${scrollPct * 100}%`;
});
// Runs on main thread, can't be GPU-composited, causes jank
```

```css
.reveal {
  opacity: 0;
  transform: translateY(20px);
  transition:
    opacity 0.6s,
    transform 0.6s;
}
```

**Prefer (CSS scroll-driven animations):**

```css
/* Reveal on scroll into view */
.reveal {
  animation: fade-in linear both;
  animation-timeline: view();
  animation-range: entry 0% entry 100%;
}

@keyframes fade-in {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
```

Zero JavaScript, GPU-composited, runs off the main thread.

### Two types of scroll timelines

**`view()` — element visibility timeline:**

Progresses from 0% to 100% as an element enters and exits the viewport (or a scroll container). Perfect for reveal animations, parallax, and intersection-based effects.

```css
.card {
  animation: slide-up linear both;
  animation-timeline: view();
  animation-range: entry 0% cover 40%;
}

@keyframes slide-up {
  from {
    opacity: 0;
    transform: translateY(40px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
```

**`scroll()` — container scroll progress timeline:**

Progresses from 0% to 100% based on the scroll position of a container. Perfect for progress bars, parallax backgrounds, and scroll-position indicators.

```css
/* Reading progress bar */
.progress-bar {
  position: fixed;
  top: 0;
  left: 0;
  height: 3px;
  background: var(--accent);
  transform-origin: left;
  animation: grow-width linear both;
  animation-timeline: scroll();
}

@keyframes grow-width {
  from {
    transform: scaleX(0);
  }
  to {
    transform: scaleX(1);
  }
}
```

### Animation range control

The `animation-range` property controls which portion of the scroll timeline drives the animation:

```css
/* Start when element enters, finish when fully in view */
.reveal {
  animation-timeline: view();
  animation-range: entry 0% entry 100%;
}

/* Start when element covers 20% of viewport, end at 60% */
.parallax {
  animation-timeline: view();
  animation-range: cover 20% cover 60%;
}

/* Start at entry, end when element starts to exit */
.sticky-effect {
  animation-timeline: view();
  animation-range: entry 100% exit 0%;
}
```

### Range keywords

| Keyword   | 0%                      | 100%                     |
| --------- | ----------------------- | ------------------------ |
| `cover`   | Element starts entering | Element finishes leaving |
| `contain` | Element fully inside    | Element starts to leave  |
| `entry`   | Element starts entering | Element fully entered    |
| `exit`    | Element starts leaving  | Element fully left       |

### Named scroll timelines

For animations driven by a specific scroll container (not the nearest ancestor):

```css
.scroll-container {
  overflow-y: auto;
  scroll-timeline-name: --main-scroll;
  scroll-timeline-axis: y;
}

.progress {
  animation: progress linear both;
  animation-timeline: --main-scroll;
}

@keyframes progress {
  from {
    width: 0%;
  }
  to {
    width: 100%;
  }
}
```

### Parallax effect

```css
.hero-bg {
  animation: parallax linear both;
  animation-timeline: scroll();
}

@keyframes parallax {
  from {
    transform: translateY(0);
  }
  to {
    transform: translateY(-30%);
  }
}
```

### Multiple scroll-driven animations

```css
.section-heading {
  animation:
    fade-in linear both,
    slide-right linear both;
  animation-timeline: view(), view();
  animation-range:
    entry 0% entry 80%,
    entry 10% entry 90%;
}

@keyframes fade-in {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes slide-right {
  from {
    transform: translateX(-30px);
  }
  to {
    transform: translateX(0);
  }
}
```

### Respecting reduced motion

Always pair scroll-driven animations with a `prefers-reduced-motion` check (see `animation-prefers-reduced-motion`):

```css
.reveal {
  animation: fade-in linear both;
  animation-timeline: view();
  animation-range: entry 0% entry 100%;
}

@media (prefers-reduced-motion: reduce) {
  .reveal {
    animation: none;
    opacity: 1;
  }
}
```

### Performance advantage

Scroll-driven animations defined in CSS run on the compositor thread — they don't block the main thread, don't cause JavaScript garbage collection pauses, and don't fight with `requestAnimationFrame` scheduling. This is a fundamental performance improvement over any JavaScript scroll-animation library.

🟡 Newly available (~78%). Supported in Chromium and Firefox. For Safari and older browsers, use an IntersectionObserver JavaScript fallback behind a `@supports` check:

```css
@supports (animation-timeline: view()) {
  .reveal {
    animation: fade-in linear both;
    animation-timeline: view();
    animation-range: entry 0% entry 100%;
  }
}
```

Reference: [modern-css.com](https://modern-css.com) · [MDN — animation-timeline](https://developer.mozilla.org/en-US/docs/Web/CSS/animation-timeline) · [scroll-driven-animations.style](https://scroll-driven-animations.style)

### 6.8 Responsive Clip Paths Without SVG

The `clip-path: path()` function only accepts pixel-based SVG path data — coordinates are fixed, making shapes non-responsive. They break at different element sizes and require recalculation for every breakpoint. The `shape()` function uses CSS values including percentages, `calc()`, and viewport units, producing clip paths that scale fluidly with the element.

**Avoid (pixel-based path — not responsive):**

```css
.shape {
  clip-path: path('M0 200 L100 0 L200 200 Z');
  /* Fixed pixel values — breaks when element is resized */
}
```

Or relying on an SVG `<clipPath>` element in the DOM:

```html
<svg width="0" height="0">
  <defs>
    <clipPath id="triangle" clipPathUnits="objectBoundingBox">
      <path d="M0,1 L0.5,0 L1,1 Z" />
    </clipPath>
  </defs>
</svg>
```

```css
.shape {
  clip-path: url(#triangle);
  /* Requires hidden SVG in the markup — extra DOM nodes, fragile ID references */
}
```

**Prefer (shape() with percentage-based coordinates):**

```css
.shape {
  clip-path: shape(from 0% 100%, line to 50% 0%, line to 100% 100%, close);
  /* Fully responsive — scales with the element */
}
```

### Drawing commands

The `shape()` function uses drawing commands similar to SVG path syntax but with CSS values:

```css
.wave-bottom {
  clip-path: shape(
    from 0% 0%,
    line to 100% 0%,
    line to 100% 80%,
    curve to 0% 80% via 50% 105%,
    close
  );
}
```

| Command  | Description                                            |
| -------- | ------------------------------------------------------ |
| `from`   | Starting point of the shape                            |
| `line`   | Straight line to a point                               |
| `curve`  | Cubic or quadratic Bézier curve (`via` control points) |
| `smooth` | Smooth continuation of a previous curve                |
| `arc`    | Elliptical arc to a point                              |
| `close`  | Closes the path back to the starting point             |

### Mixing units with calc()

Because `shape()` accepts any CSS value, you can mix units and use `calc()` for precise hybrid layouts:

```css
.notch {
  clip-path: shape(
    from 0% 0%,
    line to calc(50% - 30px) 0%,
    line to 50% 20px,
    line to calc(50% + 30px) 0%,
    line to 100% 0%,
    line to 100% 100%,
    line to 0% 100%,
    close
  );
}
```

### Animating clip paths

`shape()` clip paths can be transitioned and animated when the number and type of commands match between keyframes:

```css
.morph {
  clip-path: shape(from 0% 0%, line to 100% 0%, line to 100% 100%, line to 0% 100%, close);
  transition: clip-path 0.4s ease;
}

.morph:hover {
  clip-path: shape(from 10% 0%, line to 90% 0%, line to 100% 100%, line to 0% 100%, close);
}
```

### Common shape patterns

```css
/* Diagonal section divider */
.diagonal {
  clip-path: shape(from 0% 0%, line to 100% 0%, line to 100% 85%, line to 0% 100%, close);
}

/* Curved bottom edge */
.curved {
  clip-path: shape(
    from 0% 0%,
    line to 100% 0%,
    line to 100% 85%,
    curve to 0% 85% via 50% 110%,
    close
  );
}

/* Arrow / chevron */
.arrow {
  clip-path: shape(
    from 0% 0%,
    line to 75% 0%,
    line to 100% 50%,
    line to 75% 100%,
    line to 0% 100%,
    line to 25% 50%,
    close
  );
}

/* Pentagon */
.pentagon {
  clip-path: shape(
    from 50% 0%,
    line to 100% 38%,
    line to 82% 100%,
    line to 18% 100%,
    line to 0% 38%,
    close
  );
}
```

### When to use `shape()` vs. `polygon()`

| Feature              | `polygon()`          | `shape()`              |
| -------------------- | -------------------- | ---------------------- |
| Straight lines       | ✅ Yes               | ✅ Yes                 |
| Curves (Bézier, arc) | ❌ No                | ✅ Yes                 |
| Mixed units / calc() | ✅ Yes               | ✅ Yes                 |
| Animatable           | ✅ (matching points) | ✅ (matching commands) |
| Browser support      | ✅ Widely available  | ✅ Widely available    |

Use `polygon()` for simple straight-edged shapes (triangles, hexagons, diagonal cuts). Use `shape()` when you need curves, arcs, or complex paths that would otherwise require SVG.

✅ Widely available (~96%). Supported in all modern browsers. `shape()` is the CSS-native answer to responsive clipping — it replaces both `path()` for complex shapes and SVG `<clipPath>` elements with a single, responsive, animatable CSS function.

Reference: [modern-css.com](https://modern-css.com) · [MDN — shape()](https://developer.mozilla.org/en-US/docs/Web/CSS/basic-shape/shape)

### 6.9 Staggered Animations Without nth-child Hacks

Creating staggered animations — where each item in a list animates with a progressively longer delay — traditionally requires either a custom `--i` variable on every `nth-child` selector or inline `style` attributes set from JavaScript. The `sibling-index()` function returns each element's position among its siblings as a number, letting you calculate staggered delays with a single rule instead of N rules.

**Avoid (nth-child per item — doesn't scale):**

```css
li:nth-child(1) {
  --i: 0;
}
li:nth-child(2) {
  --i: 1;
}
li:nth-child(3) {
  --i: 2;
}
li:nth-child(4) {
  --i: 3;
}
li:nth-child(5) {
  --i: 4;
}
li:nth-child(6) {
  --i: 5;
}
/* …repeat for every possible item count */

li {
  opacity: 0;
  animation: fade-in 0.3s ease forwards;
  animation-delay: calc(0.05s * var(--i));
}
```

Or the JavaScript workaround:

```js
document.querySelectorAll('li').forEach((el, i) => {
  el.style.setProperty('--i', i);
});
// Must re-run on every DOM change
```

Both approaches require knowing (or iterating) the number of items in advance. Adding or removing an item means updating the CSS or re-running the JavaScript.

**Prefer (modern CSS with `sibling-index()`):**

```css
li {
  opacity: 0;
  animation: fade-in 0.3s ease forwards;
  animation-delay: calc(0.05s * (sibling-index() - 1));
}

@keyframes fade-in {
  to {
    opacity: 1;
    translate: 0;
  }
}
```

One rule. Works for any number of items. No JavaScript, no per-item selectors, no inline styles. The browser computes `sibling-index()` automatically for each element based on its position among its siblings.

### How `sibling-index()` works

`sibling-index()` returns a 1-based integer representing the element's position among its parent's children (counting only elements, not text nodes):

```
<ul>
  <li>…</li>   <!-- sibling-index() = 1 -->
  <li>…</li>   <!-- sibling-index() = 2 -->
  <li>…</li>   <!-- sibling-index() = 3 -->
</ul>
```

It can be used anywhere a `<number>` or `<integer>` is expected in a CSS value — inside `calc()`, `clamp()`, `min()`, `max()`, and custom property assignments.

### Common stagger patterns

```css
/* Fade in from below with staggered delay */
.stagger-item {
  opacity: 0;
  translate: 0 10px;
  animation: reveal 0.4s ease forwards;
  animation-delay: calc(0.06s * (sibling-index() - 1));
}

@keyframes reveal {
  to {
    opacity: 1;
    translate: 0 0;
  }
}
```

```css
/* Staggered transition on hover of a parent */
.menu:hover .menu-item {
  opacity: 1;
  translate: 0;
  transition-delay: calc(0.04s * (sibling-index() - 1));
}

.menu-item {
  opacity: 0;
  translate: 0 -8px;
  transition:
    opacity 0.2s ease,
    translate 0.2s ease;
}
```

### Capping the maximum delay

For long lists, stagger delays can accumulate to feel sluggish. Cap the delay with `min()`:

```css
li {
  animation-delay: calc(min(0.05s * (sibling-index() - 1), 0.5s));
  /* Items beyond the 10th all animate at 0.5s — no infinite wait */
}
```

Or use a logarithmic curve for a natural easing of the stagger effect:

```css
li {
  /* Delay increases rapidly at first, then levels off */
  animation-delay: calc(0.15s * log(sibling-index()));
}
```

### Dynamic z-index stacking

`sibling-index()` is useful beyond animation — any value that depends on element order benefits:

```css
/* Stack cards with increasing z-index */
.card {
  position: relative;
  z-index: calc(sibling-index());
}

/* Reverse stack — first card on top */
.card-stack .card {
  z-index: calc(100 - sibling-index());
}
```

### Progressive scale or opacity

```css
/* Each item slightly more transparent than the previous */
.fade-trail > * {
  opacity: calc(1 - (sibling-index() - 1) * 0.1);
}

/* Each item progressively smaller */
.scale-trail > * {
  scale: calc(1 - (sibling-index() - 1) * 0.05);
}
```

### Combining with `sibling-count()`

The related `sibling-count()` function returns the total number of siblings, enabling proportional calculations:

```css
/* Distribute items evenly around a circle */
.radial > * {
  --angle: calc(360deg / sibling-count() * (sibling-index() - 1));
  rotate: var(--angle);
  translate: 0 -120px;
}
```

### Fallback for older browsers

```css
/* Static fallback — no stagger, but content still appears */
li {
  opacity: 1;
}

@supports (animation-delay: calc(0.05s * sibling-index())) {
  li {
    opacity: 0;
    animation: fade-in 0.3s ease forwards;
    animation-delay: calc(0.05s * (sibling-index() - 1));
  }
}
```

Or use the JavaScript `--i` variable approach as a fallback and disable it when `sibling-index()` is supported.

🟡 Newly available (~70%). Supported in Chromium and Firefox. For broader compatibility, use the JavaScript `--i` variable pattern as a fallback. The CSS version can coexist — the `sibling-index()` rule will override the JS-set `--i` in supporting browsers.

Reference: [modern-css.com](https://modern-css.com) · [CSS Values Level 5 — sibling-index()](https://drafts.csswg.org/css-values-5/#tree-counting)

### 6.10 Entry Animations Without JavaScript Timing

Animating an element's appearance when it first renders (e.g., fading in a card, sliding in a notification) traditionally required a two-step JavaScript hack: render the element in its "before" state, then use `requestAnimationFrame` or `setTimeout` to add a class that triggers the transition. This creates a flash of the initial state, is timing-dependent, and adds unnecessary JavaScript. The `@starting-style` at-rule defines the "before" state directly in CSS — the browser transitions from those values to the element's normal styles automatically on first render.

**Avoid (requestAnimationFrame class toggling):**

```js
// Render element in hidden state, then trigger transition after paint
const card = document.createElement('div');
card.className = 'card';
container.appendChild(card);

// Must wait for the browser to paint the initial state
requestAnimationFrame(() => {
  requestAnimationFrame(() => {
    card.classList.add('visible');
  });
});
// Double rAF is needed because single rAF isn't reliable across browsers
```

```css
.card {
  opacity: 0;
  transform: translateY(10px);
  transition:
    opacity 0.3s ease,
    transform 0.3s ease;
}

.card.visible {
  opacity: 1;
  transform: translateY(0);
}
```

Or the `setTimeout` variant:

```js
// Fragile — timing depends on browser, layout complexity, and device speed
el.classList.add('card');
setTimeout(() => el.classList.add('visible'), 50);
```

**Prefer (modern CSS — `@starting-style`):**

```css
.card {
  opacity: 1;
  transform: translateY(0);
  transition:
    opacity 0.3s ease,
    transform 0.3s ease;

  @starting-style {
    opacity: 0;
    transform: translateY(10px);
  }
}
/* No JavaScript, no rAF, no setTimeout — the browser handles the timing */
```

The element transitions from the `@starting-style` values to its normal computed values the moment it enters the DOM or becomes visible. No class toggling, no timing hacks.

### How `@starting-style` works

1. The browser reads the `@starting-style` block to determine the "from" values.
2. On the element's first style computation (insertion into the DOM, `display` changing from `none` to visible, etc.), the browser applies the starting values.
3. The transition then runs from those starting values to the element's normal computed styles.

### Nested syntax (recommended)

```css
.notification {
  opacity: 1;
  translate: 0;
  transition:
    opacity 0.3s,
    translate 0.3s;

  @starting-style {
    opacity: 0;
    translate: 0 -1rem;
  }
}
```

### Standalone syntax (alternative)

```css
.notification {
  opacity: 1;
  translate: 0;
  transition:
    opacity 0.3s,
    translate 0.3s;
}

@starting-style {
  .notification {
    opacity: 0;
    translate: 0 -1rem;
  }
}
```

Both forms are equivalent. The nested syntax is more readable and keeps the starting state co-located with the element's styles.

### Animating elements from `display: none`

`@starting-style` pairs with `transition-behavior: allow-discrete` (see `animation-display-transition`) to animate elements that toggle between `display: none` and visible states:

```css
.modal {
  opacity: 1;
  scale: 1;
  transition:
    opacity 0.3s,
    scale 0.3s,
    overlay 0.3s,
    display 0.3s;
  transition-behavior: allow-discrete;

  @starting-style {
    opacity: 0;
    scale: 0.95;
  }
}

.modal.hidden {
  opacity: 0;
  scale: 0.95;
  display: none;
}
```

This gives you both entry and exit animations for elements that use `display: none` — without JavaScript timing or visibility hacks.

### Popover entry animations

`@starting-style` is the correct way to animate popovers and dialogs on open:

```css
[popover] {
  opacity: 1;
  scale: 1;
  transition:
    opacity 0.2s,
    scale 0.2s,
    overlay 0.2s,
    display 0.2s;
  transition-behavior: allow-discrete;

  @starting-style {
    opacity: 0;
    scale: 0.95;
  }
}
```

### List item stagger

Combine with `nth-child` or `sibling-index()` for staggered entry animations:

```css
.list-item {
  opacity: 1;
  translate: 0;
  transition:
    opacity 0.3s ease,
    translate 0.3s ease;
  transition-delay: calc(var(--index, 0) * 0.05s);

  @starting-style {
    opacity: 0;
    translate: 0 0.5rem;
  }
}
```

### Common entry animation patterns

```css
/* Fade in */
.fade-in {
  opacity: 1;
  transition: opacity 0.3s ease;

  @starting-style {
    opacity: 0;
  }
}

/* Slide up and fade */
.slide-up {
  opacity: 1;
  translate: 0;
  transition:
    opacity 0.4s ease,
    translate 0.4s ease;

  @starting-style {
    opacity: 0;
    translate: 0 1rem;
  }
}

/* Scale in */
.scale-in {
  opacity: 1;
  scale: 1;
  transition:
    opacity 0.3s ease,
    scale 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);

  @starting-style {
    opacity: 0;
    scale: 0.9;
  }
}

/* Respect reduced motion */
@media (prefers-reduced-motion: reduce) {
  .fade-in,
  .slide-up,
  .scale-in {
    transition-duration: 0.01ms;
  }
}
```

🟡 Newly available (~85%). Supported in all modern browsers. Falls back gracefully — in unsupporting browsers, the element renders immediately in its final state (no animation, but no broken layout).

Reference: [modern-css.com](https://modern-css.com) · [MDN — @starting-style](https://developer.mozilla.org/en-US/docs/Web/CSS/@starting-style)

### 6.11 Page Transitions Without a Framework

Animating between page navigations or DOM state changes traditionally required heavy libraries — Barba.js for multi-page transitions, React Transition Group or Framer Motion for SPA state transitions — each adding bundle weight, lifecycle complexity, and framework coupling. The View Transitions API provides native, GPU-accelerated transitions between DOM states with a single function call and pure CSS animation control.

**Avoid (Barba.js or React Transition Group):**

```js
// Barba.js — 10 KB+ gzipped, complex lifecycle hooks
import barba from '@barba/core';

barba.init({
  transitions: [
    {
      leave(data) {
        return gsap.to(data.current.container, {opacity: 0, duration: 0.3});
      },
      enter(data) {
        return gsap.from(data.next.container, {opacity: 0, duration: 0.3});
      },
    },
  ],
});
// + GSAP dependency, route management, cleanup, accessibility concerns
```

```jsx
// React Transition Group — manual className orchestration
<CSSTransition in={show} timeout={300} classNames="fade" unmountOnExit>
  <div className="page">{content}</div>
</CSSTransition>
```

**Prefer (View Transitions API):**

```js
document.startViewTransition(() => {
  // Update the DOM — any synchronous or async changes
  updateDOM();
});
```

```css
/* Default crossfade — works with zero CSS customization */
::view-transition-old(root) {
  animation: fade-out 0.25s ease-out;
}

::view-transition-new(root) {
  animation: fade-in 0.25s ease-in;
}
```

One function call, two CSS rules. The browser snapshots the old state, applies the DOM changes, snapshots the new state, and crossfades between them — all GPU-composited.

### How it works

1. **Snapshot** — The browser captures a screenshot of the current state.
2. **DOM update** — Your callback runs and modifies the DOM.
3. **Snapshot** — The browser captures a screenshot of the new state.
4. **Animate** — Old and new snapshots are crossfaded (or custom-animated) as CSS pseudo-elements.

The entire process happens on the compositor thread — no layout thrashing, no JavaScript animation loops.

### Named view transitions (morph effects)

Assign `view-transition-name` to elements that should animate independently (not just crossfade with the page):

```css
.hero-image {
  view-transition-name: hero;
}

.card-title {
  view-transition-name: title;
}
```

```css
/* The hero image morphs (position + size) between pages */
::view-transition-old(hero) {
  animation: none; /* disable default crossfade */
}

::view-transition-new(hero) {
  animation: none;
}

/* The browser auto-interpolates position, size, and transform */
::view-transition-group(hero) {
  animation-duration: 0.4s;
  animation-timing-function: ease-in-out;
}
```

Named elements get their own transition group — the browser morphs them from old position/size to new position/size, producing a smooth "shared element" transition like iOS and Android native apps.

### SPA state transitions

View transitions aren't limited to page navigation — use them for any DOM state change:

```js
// Tab switching
function switchTab(tabId) {
  document.startViewTransition(() => {
    document.querySelectorAll('.tab-panel').forEach((p) => (p.hidden = true));
    document.getElementById(tabId).hidden = false;
  });
}

// List item removal
function removeItem(id) {
  document.startViewTransition(() => {
    document.getElementById(id).remove();
  });
}

// Sorting / reordering
function sortList(compareFn) {
  document.startViewTransition(() => {
    const list = document.querySelector('.list');
    const items = [...list.children].sort(compareFn);
    list.replaceChildren(...items);
  });
}
```

### Multi-page (MPA) view transitions

For traditional multi-page apps (no SPA routing), opt in with CSS:

```css
@view-transition {
  navigation: auto;
}
```

The browser automatically applies view transitions when navigating between pages on the same origin — no JavaScript needed. Pair with `view-transition-name` on shared elements for morph effects across page loads.

### Custom animation examples

```css
/* Slide in from the right */
::view-transition-new(root) {
  animation: slide-in 0.3s ease-out;
}

::view-transition-old(root) {
  animation: slide-out 0.3s ease-in;
}

@keyframes slide-in {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
}

@keyframes slide-out {
  to {
    transform: translateX(-30%);
    opacity: 0;
  }
}

/* Scale-up entrance for modals */
::view-transition-new(modal) {
  animation: scale-up 0.25s ease-out;
}

@keyframes scale-up {
  from {
    transform: scale(0.9);
    opacity: 0;
  }
}
```

### Direction-aware transitions

Use `view-transition-type` to vary animations based on navigation direction:

```js
const transition = document.startViewTransition({
  update: () => updateDOM(),
  types: ['slide-forward'],
});
```

```css
::view-transition-old(root):active-view-transition-type(slide-forward) {
  animation: slide-out-left 0.3s ease;
}

::view-transition-new(root):active-view-transition-type(slide-forward) {
  animation: slide-in-right 0.3s ease;
}
```

### Respecting reduced motion

```css
@media (prefers-reduced-motion: reduce) {
  ::view-transition-group(*),
  ::view-transition-old(*),
  ::view-transition-new(*) {
    animation-duration: 0.01ms !important;
  }
}
```

### Framework integration

```jsx
// React — wrap state updates in startViewTransition
function handleNavigation(path) {
  document.startViewTransition(() => {
    flushSync(() => {
      navigate(path);
    });
  });
}
```

The `flushSync` call ensures React commits the DOM update synchronously inside the view transition callback, so the browser can capture before/after snapshots correctly.

### Async transitions

`startViewTransition` returns a `ViewTransition` object with promises for lifecycle tracking:

```js
const transition = document.startViewTransition(async () => {
  const data = await fetchNewContent();
  updateDOM(data);
});

// Wait for the transition to complete
await transition.finished;
console.log('Transition complete');

// Or handle the ready state (snapshots captured, animation about to start)
await transition.ready;
```

### Unique `view-transition-name` requirement

Each `view-transition-name` must be unique on the page at any given time. If two elements share the same name, the transition will fail. Use dynamic names for list items:

```css
.card {
  view-transition-name: var(--card-name);
}
```

```html
<div class="card" style="--card-name: card-1">…</div>
<div class="card" style="--card-name: card-2">…</div>
```

🟡 Newly available (~89%). Supported in Chromium and Firefox, with Safari support shipping. For broader compatibility, feature-detect before use:

```js
if (document.startViewTransition) {
  document.startViewTransition(() => updateDOM());
} else {
  updateDOM(); // Instant update — no animation, no breakage
}
```

The API is designed for graceful degradation — without support, the DOM update happens instantly with no visual transition, which is always a valid fallback.

Reference: [modern-css.com](https://modern-css.com) · [MDN — View Transitions API](https://developer.mozilla.org/en-US/docs/Web/API/View_Transitions_API)

