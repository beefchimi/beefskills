# Code snippet formatting (frontend-react rules)

Code blocks in this folder follow a consistent style. **When working in a real project, the project's local ESLint/oxlint, Prettier/oxfmt, and tsconfig override these conventions** (see the `frontend-general` skill's `conventions-respect-local-config` rule).

## Conventions

1. **Braces** — No spaces inside `{}` for:
   - Imports: `import {Foo, Bar} from 'baz';`
   - Destructuring: `const {a, b} = obj;`
   - Object literals: `{passive: true}`, `return {skipped: true};`

2. **Semicolons** — Use statement-terminating semicolons.

3. **Trailing commas** — Use in multiline objects and arrays:
   - `});` with comma before `}` in the object.
   - `]);` with comma before `]` in arrays.

4. **Function/component props** — No spaces in type braces: `{onClick}: {onClick: () => void}`.

5. **Arrow function parameters** — Wrap single parameters in parentheses: `(mod) =>` not `mod =>`.
