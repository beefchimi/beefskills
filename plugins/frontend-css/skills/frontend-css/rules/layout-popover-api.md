---
title: Dropdown Menus Without JavaScript Toggles
impact: HIGH
impactDescription: eliminates JS open/close/outside-click/ESC/aria logic for popup content
tags: layout, popover, dropdown, menu, toggle, javascript
browser: 86%
---

## Dropdown Menus Without JavaScript Toggles

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
