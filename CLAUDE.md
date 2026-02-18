# Agent instructions

This repo is structured as a Claude Code plugin marketplace. Skills live under `plugins/*/skills/`.

When performing work in this codebase, you can reference these `plugins/*/skills/` skills for your own benefit. Additionally, we have some `~/.claude/` plugins and skills you may also utilize.

## Skills available

- **frontend-general**: Frontend and TypeScript performance and best practices. Framework-agnostic (React, Vue, Svelte, vanilla JS). Use when writing, reviewing, or refactoring frontend/TypeScript code (async patterns, bundle optimization, DOM performance, JS micro-optimizations, conventions).
- **frontend-react**: React-specific performance and best practices. Use when writing, reviewing, or refactoring React code (re-renders, code-splitting, SWR data fetching, hydration, hooks).
- **frontend-a11y**: WCAG 2.2 compliant interfaces with ARIA patterns, keyboard navigation, screen reader support, and mobile accessibility. Use when auditing accessibility, implementing inclusive design, or building for assistive technologies.

## How to use them

- **Read the skill** when the task matches the description above (e.g. frontend/TS work → read `frontend-general`; React work → read `frontend-react`; accessibility → read `frontend-a11y`).
- **Apply the skill’s instructions** before answering or making changes; don’t skip steps or assume the content.

## Self improvement

If any of your work leads to the realization that an existing skill could be refined, improved, or removed - or if a new skill could be formalized - please perform that work. There are some globally installed skills that could prove useful, such as: `claude-md-management` and `plugin-dev`.
