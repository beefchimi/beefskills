---
title: Page Transitions Without a Framework
impact: HIGH
impactDescription: eliminates Barba.js and React Transition Group dependencies for animated page and state transitions
tags: animation, view-transitions, page-transitions, barba, spa, morph
browser: 89%
---

## Page Transitions Without a Framework

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
