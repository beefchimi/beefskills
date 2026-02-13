# Sections

This file defines all sections, their ordering, impact levels, and descriptions.

The section ID (in parentheses) is the filename prefix used to group rules.

---

## 1. Bundle Size Optimization (bundle)

**Impact:** CRITICAL
**Description:** Reducing initial bundle size improves Time to Interactive and Largest Contentful Paint. These rules use React-specific APIs like React.lazy() and Suspense.

## 2. Client-Side Data Fetching (client)

**Impact:** MEDIUM-HIGH
**Description:** Automatic deduplication and efficient data fetching patterns using SWR and React hooks reduce redundant network requests.

## 3. Re-render Optimization (rerender)

**Impact:** MEDIUM
**Description:** Reducing unnecessary re-renders minimizes wasted computation and improves UI responsiveness.

## 4. Rendering Performance (rendering)

**Impact:** MEDIUM
**Description:** Optimizing React-specific rendering patterns including hydration, JSX, and transitions.

## 5. Advanced Patterns (advanced)

**Impact:** LOW
**Description:** Advanced patterns for specific cases that require careful implementation with React hooks and refs.
