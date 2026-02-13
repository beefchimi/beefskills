# Beef Skills

This is my own personal collection of Claude Skills (`.claude/skills/`).

## Future

I will slowly add more skills and `AGENTS` context as time goes on. One thing I want to cover more is “guiding principals”. This can perhaps be assisted by curating quotes which align nicely with the practice of pairing with AI.

> “However beautiful the strategy, you should occasionally look at the results.”
> — Winston Churchill

## Usage: Git submodules

Use this repo as a submodule so each project gets the same skills and you can update them with `git submodule update`.

**One-time setup in a project that uses Claude and expects skills in `.claude/skills/`:**

1. Ensure the project has a `.claude` directory _(create it if needed)_.
2. Add this repo as a submodule **into** `.claude` so that this repo’s `.claude/skills` becomes the project’s skills:

   ```bash
   cd /path/to/your-project
   git submodule add https://github.com/YOUR_USERNAME/beefskills.git .claude/beefskills
   ```

3. From the **project root**, symlink the submodule’s skills into `.claude/skills`:

   ```bash
   ln -s .claude/beefskills/.claude/skills .claude/skills
   ```

   Result: `your-project/.claude/skills/*` resolve into the submodule.

4. When cloning the project later, init submodules:

   ```bash
   git clone --recurse-submodules <your-project-url>
   # or after a plain clone:
   git submodule update --init --recursive
   ```

To pull the latest skills in all projects: `git submodule update --remote .claude/beefskills` (or whatever path you used).
