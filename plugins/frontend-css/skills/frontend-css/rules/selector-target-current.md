---
title: Scroll Spy Without IntersectionObserver
impact: MEDIUM
impactDescription: eliminates JavaScript scroll tracking and active-state management for navigation highlighting
tags: selectors, target-current, scroll-spy, intersection-observer, navigation
browser: 48%
---

## Scroll Spy Without IntersectionObserver

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
