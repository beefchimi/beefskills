---
title: Aspect Ratios Without the Padding Hack
impact: HIGH
impactDescription: eliminates wrapper elements and unintuitive percentage padding
tags: layout, aspect-ratio, responsive, video, images
browser: 93%
---

## Aspect Ratios Without the Padding Hack

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
