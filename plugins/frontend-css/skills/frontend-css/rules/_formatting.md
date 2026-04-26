# Code snippet formatting (frontend-css rules)

Code blocks in this folder follow a consistent style. **When working in a real project, the project's local Stylelint, Prettier/oxfmt, and PostCSS configs override these conventions** (see the `frontend-general` skill's `conventions-respect-local-config` rule).

## Conventions

1. **Indentation** — 2 spaces inside rule blocks.

2. **Braces** — Opening brace on the same line as the selector, closing brace on its own line:

   ```css
   .card {
     display: grid;
   }
   ```

3. **Semicolons** — Always include the trailing semicolon on the last declaration.

4. **Shorthand** — Prefer shorthand properties when all sub-values are set:
   - `inset: 0;` over `top: 0; right: 0; bottom: 0; left: 0;`
   - `gap: 16px;` over `row-gap: 16px; column-gap: 16px;`

5. **Custom properties** — Use the `--` prefix with descriptive kebab-case names:
   - `--brand-hue`, `--surface-bg`, `--space-md`

6. **Modern color syntax** — Use the space-separated functional notation (no commas):
   - `rgb(0 0 0 / 0.5)` over `rgba(0, 0, 0, 0.5)`
   - `oklch(0.7 0.15 250)` over hex when perceptual uniformity matters

7. **Logical properties** — Prefer `inline`/`block` logical equivalents over physical `left`/`right`/`top`/`bottom` for internationalization-ready code.

8. **Units** — Use `rem` for typography, `px` or relative units for borders/shadows, and viewport-relative units (`dvh`, `svh`, `lvh`) over the legacy `vh`.

9. **Comments** — Use `/* */` comments sparingly; prefer self-documenting property names and structure.

10. **Motion** — Use `ms` units instead of `s` when authoring motion durations. If multiple properties are being animated, each with the same duration and timing-function, use long-hand `transition` or `animation` syntax:

```css
.card {
  transition-property: opacity, background-color;
  transition-duration: 200ms;
  transition-timing-function: ease;
}
```
