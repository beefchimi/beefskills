# Sections

This file defines all sections, their ordering, impact levels, and descriptions.

The section ID (in parentheses) is the filename prefix used to group rules.

---

## 1. Project & tooling conventions (conventions)

**Impact:** HIGH
**Description:** Foundational rules for code consistency with project configuration and tooling.

## 2. Eliminating Waterfalls (async)

**Impact:** CRITICAL
**Description:** Waterfalls are the #1 performance killer. Each sequential await adds full network latency. Eliminating them yields the largest gains.

## 3. Bundle Size Optimization (bundle)

**Impact:** CRITICAL
**Description:** Reducing initial bundle size improves Time to Interactive and Largest Contentful Paint.

## 4. Client-Side Data Fetching (client)

**Impact:** MEDIUM-HIGH
**Description:** Efficient data handling and event listener patterns reduce redundant work and improve responsiveness.

## 5. Rendering Performance (rendering)

**Impact:** MEDIUM
**Description:** Optimizing the rendering process reduces the work the browser needs to do.

## 6. JavaScript Performance (js)

**Impact:** LOW-MEDIUM
**Description:** Micro-optimizations for hot paths can add up to meaningful improvements.

## 7. Documentation (docs)

**Impact:** MEDIUM
**Description:** Conventions for authoring and editing markdown documentation, including typography (quotes and apostrophes) in prose vs. code.
