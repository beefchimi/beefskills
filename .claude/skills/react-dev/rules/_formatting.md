# Code snippet formatting (react-dev rules)

Code blocks in this folder follow a consistent style.

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
