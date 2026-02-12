---
title: Barrel Files vs Third-Party Imports
impact: CRITICAL
impactDescription: faster builds and cold starts when consuming large libraries
tags: bundle, imports, tree-shaking, barrel-files, component-library
---

## Barrel Files vs Third-Party Imports

**Barrel files for your own code:** Using an `index.ts` (or similar) that re-exports from your components is recommended for component libraries and internal packages. It gives a single entry point and a clear public API. Consumers can import from your package root; your bundler will tree-shake based on what they use.

**Third-party libraries:** When importing from large libraries (e.g. `lucide-react`, `@mui/material`, `react-icons`), avoid importing from the package's main barrel when it pulls in many modules. Prefer direct or subpath imports so the bundler can include only what you use and cold starts stay fast.

**Incorrect (imports entire library via barrel):**

```tsx
import { Check, X, Menu } from 'lucide-react'
// Can load 1,500+ modules, slow dev and cold start

import { Button, TextField } from '@mui/material'
// Can load 2,000+ modules
```

**Correct (direct/subpath imports):**

```tsx
import Check from 'lucide-react/dist/esm/icons/check'
import X from 'lucide-react/dist/esm/icons/x'
import Menu from 'lucide-react/dist/esm/icons/menu'

import Button from '@mui/material/Button'
import TextField from '@mui/material/TextField'
```

Libraries commonly affected: `lucide-react`, `@mui/material`, `@mui/icons-material`, `@tabler/icons-react`, `react-icons`, `@headlessui/react`, `@radix-ui/react-*`, `lodash`, `date-fns`, `react-use`. For your own component library, keep using barrel files (e.g. `export * from './Button'`) for a clean public API.
