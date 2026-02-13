#!/usr/bin/env python3
"""Compile rules/*.md into AGENTS.md. Excludes _sections.md and _template.md."""

from pathlib import Path

RULES_DIR = Path(__file__).parent / "rules"
OUTPUT = Path(__file__).parent / "AGENTS.md"

SECTION_ORDER = [
    ("bundle", "Bundle Size Optimization", "CRITICAL"),
    ("client", "Client-Side Data Fetching", "MEDIUM-HIGH"),
    ("rerender", "Re-render Optimization", "MEDIUM"),
    ("rendering", "Rendering Performance", "MEDIUM"),
    ("advanced", "Advanced Patterns", "LOW"),
]


def strip_frontmatter(content: str) -> tuple[str, str]:
    """Return (title, body). Title is from first ## line after frontmatter."""
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            body = parts[2].lstrip("\n")
        else:
            body = content
    else:
        body = content
    lines = body.split("\n")
    title = ""
    rest_lines = []
    for line in lines:
        if line.startswith("## ") and not title:
            title = line[3:].strip()
        else:
            rest_lines.append(line)
    body = "\n".join(rest_lines).strip()
    return title, body


def main():
    by_prefix = {}
    for f in RULES_DIR.iterdir():
        if not f.suffix == ".md" or f.name.startswith("_"):
            continue
        name = f.stem
        if "-" in name:
            prefix = name.split("-", 1)[0]
            by_prefix.setdefault(prefix, []).append(f)
    for prefix in by_prefix:
        by_prefix[prefix].sort(key=lambda p: p.name)

    out = []
    out.append("# React Best Practices")
    out.append("")
    out.append("**Version 1.0.0**")
    out.append("React")
    out.append("")
    out.append("> **Note:**")
    out.append(
        "> This document is for agents and LLMs when maintaining, generating, or refactoring"
    )
    out.append(
        "> React codebases. For framework-agnostic patterns, see the `frontend-general` skill."
    )
    out.append("")
    out.append("---")
    out.append("")
    out.append("## Abstract")
    out.append("")
    out.append("React-specific performance and best-practices guide.")
    out.append(
        "Rules across 5 categories: bundle optimization with React.lazy/Suspense, client-side"
    )
    out.append(
        "data fetching with SWR, re-render optimization, React rendering patterns, and advanced"
    )
    out.append("hook patterns. Each rule includes incorrect vs. correct examples.")
    out.append("")
    out.append("---")
    out.append("")
    out.append("## Table of Contents")
    out.append("")

    for sec_num, (prefix, section_title, impact) in enumerate(SECTION_ORDER, 1):
        files = by_prefix.get(prefix, [])
        if not files:
            continue
        out.append(
            f"{sec_num}. [{section_title}](#{sec_num}-{section_title.lower().replace(' ', '-')}) — **{impact}**"
        )
        for r_num, f in enumerate(files, 1):
            content = f.read_text(encoding="utf-8")
            title, _ = strip_frontmatter(content)
            out.append(f"   - {sec_num}.{r_num} {title}")
        out.append("")

    out.append("---")
    out.append("")

    for sec_num, (prefix, section_title, _) in enumerate(SECTION_ORDER, 1):
        files = by_prefix.get(prefix, [])
        if not files:
            continue
        out.append(f"## {sec_num}. {section_title}")
        out.append("")
        for r_num, f in enumerate(files, 1):
            content = f.read_text(encoding="utf-8")
            title, body = strip_frontmatter(content)
            out.append(f"### {sec_num}.{r_num} {title}")
            out.append("")
            out.append(body)
            out.append("")
        out.append("")

    OUTPUT.write_text("\n".join(out), encoding="utf-8")
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    main()
