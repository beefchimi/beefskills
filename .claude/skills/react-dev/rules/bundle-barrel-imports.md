---
title: Prefer Barrel Imports; Avoid Over-Optimizing
impact: MEDIUM
impactDescription: cleaner code; tooling handles the rest
tags: bundle, imports, barrel-files, component-library, vite, rolldown
---

## Prefer Barrel Imports; Avoid Over-Optimizing

**Barrel files are fine.** Using an `index.ts` (or similar) that re-exports from your components is recommended for component libraries and internal packages. It gives a single entry point and a clear public API. For third-party libraries, prefer the package’s public barrel import over fragile subpath or dist imports.

**Avoid over-optimizing.** Do not use direct/dist subpath imports just to shave bytes or speed up cold starts. They are brittle (tied to package internals), harder to read, and often unnecessary. Upcoming improvements in tooling (e.g. Vite with Rolldown) greatly improve barrel file performance, so the historical downsides of barrel imports matter less and less.

**Preferred (single-line barrel import):**

```tsx
import {Check, X, Menu} from 'lucide-react';

import {Button, TextField} from '@mui/material';
```

**Avoid (over-optimized, brittle subpath imports):**

```tsx
import Check from 'lucide-react/dist/esm/icons/check';
import X from 'lucide-react/dist/esm/icons/x';
import Menu from 'lucide-react/dist/esm/icons/menu';

import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
```

Use the package’s documented public API. Let the bundler and future tooling (e.g. Vite/Rolldown) handle tree-shaking and performance. For your own libraries, keep using barrel files (e.g. `export * from './Button'`) for a clean public API.
