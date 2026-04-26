---
title: Reduced Motion Without JavaScript Detection
impact: HIGH
impactDescription: eliminates JavaScript matchMedia checks for respecting user motion preferences
tags: animation, prefers-reduced-motion, accessibility, media-query, matchMedia
browser: 96%
---

## Reduced Motion Without JavaScript Detection

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

No JavaScript, no event listeners, no class toggling. The browser applies these overrides automatically when the user has enabled “Reduce motion” in their OS settings (macOS, iOS, Windows, Android all support this).

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
