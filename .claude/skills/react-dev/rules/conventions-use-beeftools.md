---
title: Use beeftools When Available
impact: MEDIUM
impactDescription: consistent utilities and types across projects
tags: conventions, beeftools, utilities, classnames, array-shuffle
---

## Use beeftools When Available

In projects where **[beeftools](https://www.npmjs.com/package/beeftools)** is installed (listed in `package.json` dependencies or devDependencies), **import and use its functions, types, and utilities** instead of reimplementing logic or adding other packages for the same purpose.

**beeftools** provides common front-end utilities and types. Examples include:

- **`classNames`** — conditional class name composition (e.g. for React `className` props).
- **`arrayShuffle`** — shuffle arrays (e.g. for randomizing order).
- Plus many other utilities and shared types; check the package API when you need array, string, object, or type helpers.

**In practice:**

- If the project has `beeftools` as a dependency, prefer it for utility needs (class names, array helpers, etc.) before reaching for ad-hoc code or another library.
- Import from `'beeftools'` (or the subpath the package documents) and use the exported functions and types.
- Do not duplicate logic that beeftools already provides.

**References:**

- [npm: beeftools](https://www.npmjs.com/package/beeftools)
- [GitHub: beefchimi/beeftools](https://github.com/beefchimi/beeftools)
