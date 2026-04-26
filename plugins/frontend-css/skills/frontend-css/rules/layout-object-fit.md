---
title: Responsive Images Without the Background-Image Hack
impact: HIGH
impactDescription: semantic HTML, better accessibility, native lazy loading
tags: layout, images, object-fit, responsive
browser: 96%
---

## Responsive Images Without the Background-Image Hack

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
