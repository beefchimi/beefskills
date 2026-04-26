---
title: Grouping Selectors Without Repetition
impact: HIGH
impactDescription: eliminates repetitive compound selectors and reduces stylesheet verbosity
tags: selectors, is, grouping, compound, specificity
browser: 96%
---

## Grouping Selectors Without Repetition

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
