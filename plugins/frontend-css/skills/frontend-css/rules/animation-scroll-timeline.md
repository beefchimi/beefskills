---
title: Scroll-Linked Animations Without a Library
impact: HIGH
impactDescription: eliminates JavaScript scroll listeners and IntersectionObserver for scroll-driven animation effects
tags: animation, scroll-timeline, scroll-driven, intersection-observer, parallax
browser: 78%
---

## Scroll-Linked Animations Without a Library

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
