# Beef Skills

A collection of Claude Code skills, distributed as a plugin marketplace.

## Installation

Add this repo as a marketplace in Claude Code:

```
/plugin marketplace add beefchimi/beefskills
```

Then install the plugins you want:

```
/plugin install frontend-general@beefskills
/plugin install frontend-react@beefskills
/plugin install frontend-a11y@beefskills
```

## Updating

To pull the latest changes for a specific plugin:

```
/plugin update frontend-general@beefskills
```

Or update all installed plugins at once:

```
/plugin update --all
```

## Available Plugins

### frontend-general

Based on: <https://github.com/vercel-labs/agent-skills/tree/main>
Last updated: Feb 13 2026

Frontend and TypeScript performance and best-practices guidelines. Framework-agnostic — applies to React, Vue, Svelte, vanilla JS, etc. Covers async patterns, bundle optimization, DOM performance, JS micro-optimizations, and project conventions.

### frontend-react

Based on: <https://github.com/vercel-labs/agent-skills/tree/main>
Last updated: Feb 13 2026

React-specific performance and best-practices guidelines. Covers re-render optimization, code-splitting with React.lazy/Suspense, client-side data fetching with SWR, hydration patterns, and advanced hook patterns.

### frontend-a11y

Based on: <https://mcpmarket.com/tools/skills/accessibility-compliance-expert>
Last updated: Feb 13 2026

WCAG 2.2 compliant interfaces with ARIA patterns, keyboard navigation, screen reader support, and mobile accessibility (iOS VoiceOver, Android TalkBack).

## Recommended: Shopify's skill-architect

For authoring new skills or updating existing ones, install Shopify's `skill-architect`. For now, this may be internal-only and not published to the plugin marketplace.

## Alternative: Manual Installation

You can also copy individual skills directly to your `~/.claude/skills/` directory:

```bash
# Example: install frontend-general
cp -R plugins/frontend-general/skills/frontend-general ~/.claude/skills/
```

## Development

### Adding a new skill to an existing plugin

1. Create a new `.md` file in the plugin's `skills/<plugin-name>/rules/` directory (for rule-based skills like `frontend-general`) or `skills/<plugin-name>/references/` (for reference-based skills like `frontend-a11y`).
2. Follow the template in `rules/_template.md` if applicable.
3. Add a quick reference entry in the plugin's `SKILL.md`.
4. Run `npm run build:skills` to regenerate any `AGENTS.md` files.
5. Commit and push — consumers pick up changes via `/plugin update`.

### Adding a new plugin

1. Create the plugin directory structure:

   ```
   plugins/<plugin-name>/
   ├── .claude-plugin/
   │   └── plugin.json
   └── skills/
       └── <plugin-name>/
           └── SKILL.md
   ```

2. Write `plugin.json` with name, description, and version:

   ```json
   {
     "name": "<plugin-name>",
     "description": "What this plugin does.",
     "version": "1.0.0"
   }
   ```

3. Write the `SKILL.md` with YAML frontmatter (`name`, `description`) and skill content.
4. Register the plugin in `.claude-plugin/marketplace.json` by adding an entry to the `plugins` array:

   ```json
   {
     "name": "<plugin-name>",
     "source": "./plugins/<plugin-name>",
     "description": "What this plugin does.",
     "version": "1.0.0",
     "license": "MIT",
     "keywords": []
   }
   ```

5. If the plugin has individual rule files, add a `build_agents.py` script to compile them into `AGENTS.md`. Running `npm run build:skills` will automatically find and execute it.
6. Commit and push.

### Updating a published skill

Edit the skill files directly, run `npm run build:skills` if applicable, then commit and push. Consumers update via `/plugin update`.

### Versioning

Bump the `version` field in both `plugin.json` and the corresponding entry in `marketplace.json` when making significant changes to a plugin.

### Scripts

| Command                | Description                                                          |
| ---------------------- | -------------------------------------------------------------------- |
| `npm run build:skills` | Regenerate `AGENTS.md` for all plugins that have a `build_agents.py` |
| `npm run lint`         | Run oxlint                                                           |
| `npm run format`       | Check formatting with oxfmt                                          |

## Future

I will slowly add more skills and context as time goes on. One thing I want to cover more is "guiding principals". This can perhaps be assisted by curating quotes which align nicely with the practice of pairing with AI.

> "However beautiful the strategy, you should occasionally look at the results."
> — Winston Churchill

### Composition Patterns

Consider adding something like:

- <https://github.com/vercel-labs/agent-skills/tree/main/skills/composition-patterns>
