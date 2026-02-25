---
name: frontend-css
description: Modern CSS patterns and native replacements for legacy hacks, JavaScript workarounds, and preprocessor dependencies. Use when writing, reviewing, or refactoring CSS — covers layout, animation, color, typography, selectors, and workflow modernization. Based on modern-css.com.
license: MIT
metadata:
  version: '1.0.0'
---

# Modern CSS Best Practices

Stop writing CSS like it's 2015. Every hack you still reach for — transform centering, padding aspect-ratios, JavaScript scroll listeners, Sass color functions — has a clean, native CSS replacement now.

This skill distills 75 modern CSS patterns across 6 categories, each comparing a legacy approach with its modern replacement. For general frontend/TypeScript performance patterns, see the `frontend-general` skill. For React-specific patterns, see the `frontend-react` skill. For accessibility, see the `frontend-a11y` skill.

## When to Apply

Reference these guidelines when:

- Writing new CSS or refactoring existing stylesheets.
- Replacing JavaScript-driven layout, animation, or interaction patterns with CSS-native alternatives.
- Removing preprocessor (Sass/Less) dependencies in favor of native CSS features.
- Reviewing CSS for outdated hacks or unnecessary complexity.
- Optimizing rendering performance with modern CSS capabilities.
- Building responsive layouts, dark mode, or theming systems.

## Browser Support Tiers

Each rule notes its approximate browser support. Use this to decide when a feature is safe to ship:

| Tier                        | Description                                  | Guidance                                      |
| --------------------------- | -------------------------------------------- | --------------------------------------------- |
| ✅ Widely available (90%+)  | Supported in all major browsers for 2+ years | Use freely, no fallback needed                |
| 🟡 Newly available (70–89%) | Recently shipped in major browsers           | Use with progressive enhancement              |
| 🟠 Limited (< 70%)          | Partial or single-engine support             | Use behind `@supports` or as enhancement only |

## Rule Categories by Priority

| Priority | Category   | Impact      | Prefix       |
| -------- | ---------- | ----------- | ------------ |
| 1        | Layout     | CRITICAL    | `layout-`    |
| 2        | Workflow   | HIGH        | `workflow-`  |
| 3        | Typography | HIGH        | `typo-`      |
| 4        | Color      | MEDIUM-HIGH | `color-`     |
| 5        | Selectors  | MEDIUM-HIGH | `selector-`  |
| 6        | Animation  | MEDIUM      | `animation-` |

## Quick Reference

### 1. Layout (CRITICAL) — 30 rules

Native CSS layout primitives that eliminate JavaScript libraries, position hacks, and complex workarounds.

- `layout-grid-centering`: Use `display: grid; place-items: center` instead of absolute + transform centering.
- `layout-gap-spacing`: Use `gap` instead of margin hacks with `:last-child` overrides.
- `layout-aspect-ratio`: Use `aspect-ratio` instead of the `padding-top` percentage hack.
- `layout-sticky-positioning`: Use `position: sticky` instead of JavaScript scroll listeners.
- `layout-object-fit`: Use `object-fit: cover` instead of `background-image` + `background-size`.
- `layout-dynamic-viewport`: Use `dvh` units instead of `100vh` that overflows on mobile.
- `layout-stretch`: Use `width: stretch` instead of `calc(100% - …)` workarounds.
- `layout-inset-shorthand`: Use `inset: 0` instead of `top: 0; right: 0; bottom: 0; left: 0`.
- `layout-logical-properties`: Use `margin-inline-start` / `padding-block-end` instead of directional properties with RTL overrides.
- `layout-grid-areas`: Use `grid-template-areas` instead of line numbers or float layouts.
- `layout-subgrid`: Use `grid-template-columns: subgrid` instead of duplicating parent tracks.
- `layout-scrollbar-gutter`: Use `scrollbar-gutter: stable` instead of `overflow-y: scroll` or hardcoded padding.
- `layout-scroll-snap`: Use `scroll-snap-type` + `scroll-snap-align` instead of carousel JS libraries.
- `layout-overscroll-behavior`: Use `overscroll-behavior: contain` instead of JavaScript wheel event prevention.
- `layout-scrollbar-styling`: Use `scrollbar-width` + `scrollbar-color` instead of `::-webkit-scrollbar` pseudo-elements.
- `layout-range-media-queries`: Use `(600px <= width <= 1200px)` instead of `(min-width) and (max-width)`.
- `layout-container-queries`: Use `@container` queries instead of viewport-based `@media` queries for component-level responsiveness.
- `layout-native-dialog`: Use the native `<dialog>` element instead of custom modal overlays with z-index and focus-trap JS.
- `layout-popover-api`: Use the Popover API (`[popover]` + `[popovertarget]`) instead of JS toggle menus.
- `layout-anchor-positioning`: Use CSS Anchor Positioning (`anchor-name` + `position-anchor`) instead of Popper.js / Floating UI.
- `layout-exclusive-accordions`: Use `<details name="…">` for exclusive accordions instead of JavaScript toggle logic.
- `layout-field-sizing`: Use `field-sizing: content` instead of JavaScript auto-resize on textarea.
- `layout-zoom`: Use `zoom` instead of `transform: scale()` with negative margin hacks.
- `layout-popover-hint`: Use `popover=hint` with `interestfor` instead of JavaScript mouseenter/mouseleave tooltips.
- `layout-commandfor`: Use `commandfor` + `command` attributes instead of `onclick` handlers for dialog/popover control.
- `layout-dialog-closedby`: Use `closedby="any"` on `<dialog>` instead of JavaScript click-outside listeners.
- `layout-base-select`: Use `appearance: base-select` instead of Select2 / Choices.js for styleable selects.
- `layout-shape-function`: Use `clip-path: shape()` with percentage-based values instead of pixel-based `path()`.
- `layout-corner-shape`: Use `corner-shape: squircle` instead of complex `clip-path: polygon()` workarounds.
- `layout-scroll-markers`: Use `::scroll-button()` and `::scroll-marker` pseudo-elements instead of carousel JS libraries.

### 2. Workflow (HIGH) — 12 rules

Modern CSS architecture features that replace preprocessors, JavaScript feature detection, and naming conventions.

- `workflow-custom-properties`: Use CSS custom properties (`var(--…)`) instead of Sass/Less variables.
- `workflow-native-nesting`: Use native CSS nesting (`& a { }`) instead of Sass/Less nesting.
- `workflow-cascade-layers`: Use `@layer` to control specificity instead of `!important` escalation.
- `workflow-supports`: Use `@supports` for feature detection instead of Modernizr or `CSS.supports()` in JS.
- `workflow-scope`: Use `@scope` for component-scoped styles instead of BEM naming or CSS Modules.
- `workflow-registered-properties`: Use `@property` to type and animate custom properties instead of untyped string tokens.
- `workflow-color-scheme`: Use `color-scheme: light dark` for automatic dark mode form controls instead of manual overrides.
- `workflow-content-visibility`: Use `content-visibility: auto` for lazy rendering instead of IntersectionObserver JS.
- `workflow-style-queries`: Use `@container style(--prop > value)` range queries instead of per-value style blocks.
- `workflow-attr-function`: Use enhanced `attr()` with type coercion instead of JavaScript `dataset` reads.
- `workflow-if-function`: Use `if()` for inline conditional values instead of JavaScript class toggling.
- `workflow-css-functions`: Use native `@function` instead of Sass `@function` / `@mixin`.

### 3. Typography (HIGH) — 7 rules

Modern typographic controls that eliminate media query stacks, JavaScript text manipulation, and float hacks.

- `typo-fluid-clamp`: Use `clamp()` for fluid sizing instead of breakpoint-based `font-size` overrides.
- `typo-text-wrap-balance`: Use `text-wrap: balance` instead of manual `<br>` or Balance-Text.js.
- `typo-font-display`: Use `font-display: swap` instead of invisible text during font loading.
- `typo-variable-fonts`: Use variable fonts with `font-weight: 100 900` instead of multiple `@font-face` blocks.
- `typo-line-clamp`: Use `line-clamp` (and `-webkit-line-clamp`) instead of JavaScript text truncation.
- `typo-initial-letter`: Use `initial-letter` instead of `float: left` hacks for drop caps.
- `typo-text-box-trim`: Use `text-box: trim-both cap alphabetic` for optical vertical centering instead of padding tweaks.

### 4. Color (MEDIUM-HIGH) — 8 rules

Modern color spaces, mixing, and theming that replace preprocessor functions, manual contrast checks, and pseudo-element hacks.

- `color-oklch`: Use `oklch()` for perceptually uniform color scales instead of hand-picked hex shades.
- `color-wide-gamut`: Use `oklch()` or `color(display-p3 …)` for vivid wide-gamut colors instead of sRGB-only `rgb()`.
- `color-relative-syntax`: Use relative color syntax (`oklch(from var(--brand) …)`) instead of Sass `lighten()` / `darken()`.
- `color-mix`: Use `color-mix(in oklch, …)` instead of Sass `mix()`.
- `color-light-dark`: Use `light-dark()` instead of duplicating values in `prefers-color-scheme` media queries.
- `color-backdrop-filter`: Use `backdrop-filter: blur()` for frosted glass instead of pseudo-element + filter hacks.
- `color-accent-color`: Use `accent-color` to style form controls instead of `appearance: none` rebuilds.
- `color-contrast-color`: Use `contrast-color()` for automatic readable text instead of hardcoded white/black.

### 5. Selectors (MEDIUM-HIGH) — 7 rules

Modern pseudo-classes and pseudo-elements that replace JavaScript DOM queries, specificity battles, and manual state management.

- `selector-is`: Use `:is()` to group selectors instead of repeating compound selectors.
- `selector-where`: Use `:where()` for zero-specificity resets instead of complex override chains.
- `selector-has`: Use `:has()` for parent selection instead of JavaScript `closest()` + class toggling.
- `selector-focus-visible`: Use `:focus-visible` instead of `:focus` to avoid showing outlines on mouse clicks.
- `selector-user-valid`: Use `:user-invalid` / `:user-valid` instead of JavaScript blur-based validation classes.
- `selector-highlight`: Use `::highlight()` and the CSS Custom Highlight API instead of DOM `innerHTML` replacement for search highlighting.
- `selector-target-current`: Use `:target-current` instead of IntersectionObserver-based scroll spy.

### 6. Animation (MEDIUM) — 11 rules

Modern animation and transition features that replace JavaScript animation libraries, timing hacks, and class toggling.

- `animation-prefers-reduced-motion`: Use `@media (prefers-reduced-motion)` instead of JavaScript `matchMedia` checks.
- `animation-individual-transforms`: Use `translate`, `rotate`, `scale` as individual properties instead of rewriting the full `transform` shorthand.
- `animation-display-transition`: Use `transition-behavior: allow-discrete` to animate `display: none` instead of visibility + opacity + JS listener hacks.
- `animation-starting-style`: Use `@starting-style` for entry animations instead of `requestAnimationFrame` class toggling.
- `animation-view-transitions`: Use the View Transitions API instead of Barba.js or React Transition Group.
- `animation-scroll-timeline`: Use `animation-timeline: view()` for scroll-linked animations instead of JS scroll listeners.
- `animation-interpolate-size`: Use `interpolate-size: allow-keywords` to animate `height: auto` instead of JS `scrollHeight` measurement.
- `animation-linear-easing`: Use `linear()` easing function for custom curves instead of JS animation libraries.
- `animation-sibling-index`: Use `sibling-index()` for staggered delays instead of per-item `nth-child` rules.
- `animation-scroll-state`: Use `@container scroll-state(stuck: top)` instead of JS scroll position checks.
- `animation-shape-clip-path`: Use `clip-path: shape()` with percentage values instead of pixel-based `path()`.

## How to Use

Read individual rule files for detailed explanations and code examples:

```
rules/layout-grid-centering.md
rules/workflow-cascade-layers.md
rules/animation-view-transitions.md
```

Each rule file contains:

- Brief explanation of why the modern approach is better.
- Legacy code example showing the old hack or workaround.
- Modern code example showing the clean CSS replacement.
- Browser support tier and any progressive enhancement notes.

## Full Compiled Document

For the complete guide with all rules expanded: `AGENTS.md`

## Reference

All patterns sourced from and inspired by [modern-css.com](https://modern-css.com).
