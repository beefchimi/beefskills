---
title: Identify and Avoid Circular Dependencies
impact: HIGH
impactDescription: prevents runtime errors, undefined imports, and hard-to-debug initialization order issues
tags: conventions, imports, circular-dependencies, module-structure, architecture
---

## Identify and Avoid Circular Dependencies

Circular dependencies occur when module A imports from module B, and module B (directly or transitively) imports from module A. This causes partially-initialized modules at runtime — imports resolve to `undefined`, classes are used before they're defined, and bugs surface far from their cause.

Linters like oxlint and ESLint can catch circular imports (`import/no-cycle`), but the linter only flags the symptom. This rule covers the structural patterns that **prevent** cycles from forming in the first place.

### How cycles happen

**Direct cycle — two modules import each other:**

```ts
// user.ts
import {formatEmail} from './email';
export function getUser() { /* ... */ }

// email.ts
import {getUser} from './user';
export function formatEmail() { /* ... */ }
```

**Transitive cycle — three or more modules form a chain:**

```ts
// a.ts → imports from b.ts → imports from c.ts → imports from a.ts
```

**Barrel file cycle — `index.ts` re-exports create hidden loops:**

```ts
// components/index.ts
export {Button} from './Button';
export {Modal} from './Modal';

// components/Modal.tsx — imports from its own barrel
import {Button} from '.';  // cycle: index → Modal → index
```

### Pattern 1: Enforce a dependency direction

Organize modules into layers with a clear dependency direction. Lower layers never import from higher layers.

```
shared/       ← pure utilities, types, constants (imports from nothing)
  └─ types.ts
  └─ utils.ts
domain/       ← business logic (imports from shared/)
  └─ user.ts
  └─ email.ts
features/     ← UI features (imports from domain/ and shared/)
  └─ profile/
  └─ settings/
```

**Incorrect (lower layer imports from higher layer):**

```ts
// shared/format.ts
import {getUserLocale} from '../domain/user';  // shared/ → domain/ = wrong direction
```

**Correct (extract the shared dependency):**

```ts
// shared/locale.ts
export function getLocale() { /* ... */ }

// domain/user.ts
import {getLocale} from '../shared/locale';
```

### Pattern 2: Extract shared code into a third module

When two modules need each other, the shared dependency belongs in a separate module that both import from.

**Incorrect (mutual dependency):**

```ts
// order.ts
import {getCustomer} from './customer';
export function getOrder() { /* ... */ }
export function formatOrderId(id: string) { return `ORD-${id}`; }

// customer.ts
import {formatOrderId} from './order';
export function getCustomer() { /* ... */ }
```

**Correct (extract shared utility):**

```ts
// format.ts
export function formatOrderId(id: string) { return `ORD-${id}`; }

// order.ts
import {getCustomer} from './customer';
import {formatOrderId} from './format';
export function getOrder() { /* ... */ }

// customer.ts
import {formatOrderId} from './format';
export function getCustomer() { /* ... */ }
```

### Pattern 3: Use type-only imports to break runtime cycles

If the cycle exists only because of type references, use `import type` to eliminate the runtime dependency. Type-only imports are erased at compile time and do not create module edges.

```ts
// user.ts
import type {Order} from './order';  // no runtime import — cycle broken
export interface User {
  recentOrders: Order[];
}
```

This only works when the import is used purely for type annotations. If you need the value at runtime, use Pattern 2 instead.

### Pattern 4: Avoid importing from your own barrel

Never import from a directory's `index.ts` within that same directory. Use direct relative imports instead.

**Incorrect:**

```ts
// components/Modal.tsx
import {Button} from '.';  // imports from components/index.ts — cycle
```

**Correct:**

```ts
// components/Modal.tsx
import {Button} from './Button';  // direct sibling import — no cycle
```

### When adding a new import

Before adding an import, consider: does the target module (or anything it imports) already depend on the current module? If unsure, trace the import chain or rely on the linter's `import/no-cycle` rule to catch it. Structuring code with a clear dependency direction (Pattern 1) makes this question easy to answer.
