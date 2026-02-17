#!/usr/bin/env python3
"""
Audit .md files for docs-fancy-quotes rule:
- Prose should use "fancy" quotes (" ") and apostrophes (' ').
- Code (inline `...` or fenced ```) must use straight " and '.
"""
import re
import sys
from pathlib import Path

STRAIGHT_DOUBLE = '"'
STRAIGHT_APOSTROPHE = "'"
FANCY_OPEN_DOUBLE = "\u201c"
FANCY_CLOSE_DOUBLE = "\u201d"
FANCY_APOSTROPHE = "\u2019"


def get_prose_content(content: str) -> str:
    """Return content with fenced code blocks removed (replaced with newlines to preserve line numbers)."""
    lines = content.split("\n")
    out = []
    in_fence = False
    fence_char = None
    for line in lines:
        if not in_fence:
            if re.match(r"^\s*```", line):
                in_fence = True
                fence_char = re.match(r"^\s*(`+)", line).group(1)
                out.append("")  # keep line count
                continue
            out.append(line)
        else:
            if line.strip().startswith(fence_char) and len(line.strip()) >= len(fence_char):
                in_fence = False
                fence_char = None
            out.append("")  # blank to preserve line numbers
    return "\n".join(out)


def iter_prose_offsets(prose: str):
    """Yield (offset, char) for each character that is in prose (not inside inline `...`)."""
    i = 0
    while i < len(prose):
        if prose[i] == "`":
            backtick_run = 0
            j = i
            while j < len(prose) and prose[j] == "`":
                backtick_run += 1
                j += 1
            # Skip until we close with same run of backticks (or end of string)
            start = j
            while j <= len(prose):
                if j == len(prose):
                    i = j
                    break
                if prose[j] == "`":
                    run = 0
                    k = j
                    while k < len(prose) and prose[k] == "`":
                        run += 1
                        k += 1
                    if run >= backtick_run:
                        i = k
                        break
                    j = k
                    continue
                j += 1
            else:
                i = start
            continue
        yield i, prose[i]
        i += 1


def find_straight_quotes_in_prose(prose: str) -> list[tuple[int, str]]:
    """Return list of (offset, char) for straight " or ' in prose only (not inside inline code)."""
    return [(i, c) for i, c in iter_prose_offsets(prose) if c in (STRAIGHT_DOUBLE, STRAIGHT_APOSTROPHE)]


def find_fancy_in_code(content: str) -> list[tuple[int, str]]:
    """Return list of (offset, char) for fancy quotes inside fenced code blocks."""
    lines = content.split("\n")
    in_fence = False
    fence = None
    issues = []
    pos = 0
    for line in lines:
        if not in_fence:
            if re.match(r"^\s*```", line):
                in_fence = True
                fence = re.match(r"^\s*(`+)", line).group(1)
            pos += len(line) + 1
            continue
        if line.strip().startswith(fence) and len(line.strip()) >= len(fence):
            in_fence = False
            pos += len(line) + 1
            continue
        for j, c in enumerate(line):
            if c in (FANCY_OPEN_DOUBLE, FANCY_CLOSE_DOUBLE, FANCY_APOSTROPHE):
                issues.append((pos + j, c))
        pos += len(line) + 1
    return issues


def line_and_column(content: str, offset: int) -> tuple[int, int]:
    before = content[:offset]
    line = before.count("\n") + 1
    col = offset - before.rfind("\n") if "\n" in before else offset + 1
    return line, col


def prose_offset_set(content: str) -> set[int]:
    """Return set of character offsets that are in prose (not in fenced block, not in inline code)."""
    prose_offsets = set()
    lines = content.split("\n")
    pos = 0
    in_fence = False
    fence = None
    for line in lines:
        if not in_fence:
            if re.match(r"^\s*```", line):
                in_fence = True
                fence = re.match(r"^\s*(`+)", line).group(1)
                pos += len(line) + 1
                continue
            # This line is prose; mark positions that are not inside inline backticks
            i = 0
            while i < len(line):
                if line[i] == "`":
                    run = 0
                    j = i
                    while j < len(line) and line[j] == "`":
                        run += 1
                        j += 1
                    # Skip to closing backticks
                    while j <= len(line):
                        if j == len(line):
                            i = len(line)
                            break
                        if line[j] == "`":
                            r2 = 0
                            k = j
                            while k < len(line) and line[k] == "`":
                                r2 += 1
                                k += 1
                            if r2 >= run:
                                i = k
                                break
                            j = k
                            continue
                        j += 1
                    else:
                        i = j
                    continue
                prose_offsets.add(pos + i)
                i += 1
            pos += len(line) + 1
            continue
        if line.strip().startswith(fence) and len(line.strip()) >= len(fence):
            in_fence = False
        pos += len(line) + 1
    return prose_offsets


def fix_prose_quotes(content: str, skip_avoid_examples: bool = False) -> str:
    """
    In prose only: replace straight " with “/” (alternating) and ' with ’.
    skip_avoid_examples: if True, do not replace in lines that look like "Avoid: ..." (for docs-fancy-quotes.md).
    """
    prose = prose_offset_set(content)
    result = []
    double_quote_count = 0
    i = 0
    while i < len(content):
        if i not in prose:
            result.append(content[i])
            i += 1
            continue
        c = content[i]
        if c == STRAIGHT_DOUBLE:
            if skip_avoid_examples:
                # Check if this line is an "Avoid:" example (starts with - Avoid: or **Avoid**)
                line_start = content.rfind("\n", 0, i) + 1
                line_end = content.find("\n", i)
                if line_end == -1:
                    line_end = len(content)
                line = content[line_start:line_end]
                if re.match(r"^[\s\-]*\*?Avoid\*?:", line) or "- Avoid:" in line[:20]:
                    result.append(c)
                    i += 1
                    continue
            double_quote_count += 1
            result.append(FANCY_CLOSE_DOUBLE if double_quote_count % 2 == 0 else FANCY_OPEN_DOUBLE)
            i += 1
            continue
        if c == STRAIGHT_APOSTROPHE:
            if skip_avoid_examples:
                line_start = content.rfind("\n", 0, i) + 1
                line_end = content.find("\n", i)
                if line_end == -1:
                    line_end = len(content)
                line = content[line_start:line_end]
                if re.match(r"^[\s\-]*\*?Avoid\*?:", line) or "- Avoid:" in line[:20]:
                    result.append(c)
                    i += 1
                    continue
            result.append(FANCY_APOSTROPHE)
            i += 1
            continue
        result.append(c)
        i += 1
    return "".join(result)


def audit_file(path: Path) -> dict:
    try:
        content = path.read_text(encoding="utf-8")
    except Exception as e:
        return {"error": str(e)}

    prose = get_prose_content(content)
    straight = find_straight_quotes_in_prose(prose)
    fancy_in_code = find_fancy_in_code(content)

    straight_with_loc = [(line_and_column(prose, off), char) for off, char in straight]
    fancy_with_loc = [(line_and_column(content, off), c) for off, c in fancy_in_code]

    return {
        "straight_in_prose": straight_with_loc,
        "fancy_in_code": fancy_with_loc,
        "ok": not straight_with_loc and not fancy_with_loc,
    }


def main():
    root = Path(__file__).resolve().parent.parent
    md_files = sorted(root.rglob("*.md"))
    md_files = [f for f in md_files if "node_modules" not in str(f) and ".git" not in str(f)]

    if "--fix" in sys.argv:
        # Fix mode: rewrite prose quotes in place. Skip AGENTS.md (generated).
        fixed_count = 0
        for path in md_files:
            rel = path.relative_to(root)
            if path.name == "AGENTS.md":
                continue
            try:
                content = path.read_text(encoding="utf-8")
            except Exception as e:
                print(f"{rel}: skip ({e})", file=sys.stderr)
                continue
            skip_avoid = "docs-fancy-quotes.md" in str(path)
            new_content = fix_prose_quotes(content, skip_avoid_examples=skip_avoid)
            if new_content != content:
                path.write_text(new_content, encoding="utf-8")
                fixed_count += 1
                print(f"Fixed: {rel}")
        print(f"\nFixed {fixed_count} file(s). Regenerate AGENTS.md in plugins that use build_agents.py.")
        return 0

    violations = []
    for path in md_files:
        rel = path.relative_to(root)
        r = audit_file(path)
        if "error" in r:
            print(f"{rel}: ERROR {r['error']}", file=sys.stderr)
            continue
        if not r["ok"]:
            # Exclude intentional straight quotes (Avoid examples in docs-fancy-quotes + compiled AGENTS.md)
            rel_str = str(rel)
            if "docs-fancy-quotes.md" in rel_str or (
                rel_str.endswith("AGENTS.md") and "frontend-general" in rel_str
            ):
                continue
            violations.append((rel, r))

    if not violations:
        print("All .md files are faithful to the fancy-quotes rule.")
        return 0

    print("Files with potential violations of docs-fancy-quotes:\n")
    for rel, r in violations:
        print(f"  {rel}")
        if r["straight_in_prose"]:
            for (line, col), c in r["straight_in_prose"][:20]:
                print(f"    Prose: straight {repr(c)} at line {line}, col {col}")
            if len(r["straight_in_prose"]) > 20:
                print(f"    ... and {len(r['straight_in_prose']) - 20} more")
        if r["fancy_in_code"]:
            for (line, col), c in r["fancy_in_code"][:10]:
                print(f"    Code:  fancy {repr(c)} at line {line}, col {col}")
            if len(r["fancy_in_code"]) > 10:
                print(f"    ... and {len(r['fancy_in_code']) - 10} more")
        print()
    return 1


if __name__ == "__main__":
    sys.exit(main())
