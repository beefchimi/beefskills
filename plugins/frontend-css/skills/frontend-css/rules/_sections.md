# Sections

This file defines all sections, their ordering, impact levels, and descriptions.

The section ID (in parentheses) is the filename prefix used to group rules.

---

## 1. Layout (layout)

**Impact:** CRITICAL
**Description:** Modern layout primitives replace fragile hacks (transform centering, padding aspect-ratios, JS scroll handlers) with declarative, resilient CSS. These patterns eliminate JavaScript dependencies, prevent layout shift, and drastically reduce code complexity.

## 2. Workflow (workflow)

**Impact:** HIGH
**Description:** Native CSS features that replace preprocessors, JavaScript feature-detection, and naming methodologies. Custom properties, nesting, cascade layers, @scope, and @supports let you write maintainable, scalable CSS without a build step.

## 3. Typography (typo)

**Impact:** HIGH
**Description:** Modern typography controls for fluid sizing, text wrapping, font loading, variable fonts, and text truncation — replacing media-query breakpoints, JavaScript resizing, and float hacks with single-property solutions.

## 4. Color (color)

**Impact:** MEDIUM-HIGH
**Description:** Wide-gamut color spaces, perceptually uniform palettes, relative color syntax, and native dark-mode primitives. Replace Sass color functions, manual contrast checks, and duplicated dark-mode values with built-in CSS capabilities.

## 5. Selectors (selector)

**Impact:** MEDIUM-HIGH
**Description:** Modern pseudo-classes and pseudo-elements that eliminate JavaScript for parent selection, form validation styling, focus management, and DOM manipulation. Cleaner selectors with lower specificity and better intent.

## 6. Animation (animation)

**Impact:** MEDIUM
**Description:** CSS-native animation capabilities that replace JavaScript animation libraries, IntersectionObserver scroll tracking, and manual transition orchestration. Individual transforms, scroll-driven animations, view transitions, and display-none transitions — all GPU-accelerated.
