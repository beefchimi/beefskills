---
title: Preventing Layout Shift From Scrollbar Appearance
impact: HIGH
impactDescription: eliminates content reflow when scrollbar appears or disappears
tags: layout, scrollbar, scrollbar-gutter, layout-shift
browser: 90%
---

## Preventing Layout Shift From Scrollbar Appearance

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
