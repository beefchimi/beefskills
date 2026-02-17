#!/usr/bin/env python3
"""
Bump the version for a plugin in plugin.json and marketplace.json.
Usage: python3 scripts/bump_plugin_version.py <plugin-name> <new-version>
Example: python3 scripts/bump_plugin_version.py frontend-general 1.1.0
"""
import json
import sys
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    if len(sys.argv) != 3:
        print("Usage: bump_plugin_version.py <plugin-name> <new-version>", file=sys.stderr)
        print("Example: bump_plugin_version.py frontend-general 1.1.0", file=sys.stderr)
        return 1

    name = sys.argv[1]
    new_version = sys.argv[2].strip()

    plugin_dir = root / "plugins" / name
    plugin_json = plugin_dir / ".claude-plugin" / "plugin.json"
    marketplace_json = root / ".claude-plugin" / "marketplace.json"

    if not plugin_json.exists():
        print(f"Not found: {plugin_json}", file=sys.stderr)
        return 1
    if not marketplace_json.exists():
        print(f"Not found: {marketplace_json}", file=sys.stderr)
        return 1

    # Update plugin.json
    data = json.loads(plugin_json.read_text(encoding="utf-8"))
    old = data.get("version", "")
    data["version"] = new_version
    plugin_json.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(f"Updated {plugin_json.relative_to(root)}: {old!r} -> {new_version!r}")

    # Update marketplace.json
    data = json.loads(marketplace_json.read_text(encoding="utf-8"))
    for p in data.get("plugins", []):
        if p.get("name") == name:
            old = p.get("version", "")
            p["version"] = new_version
            print(f"Updated marketplace entry for {name}: {old!r} -> {new_version!r}")
            break
    else:
        print(f"Warning: no plugin named {name!r} in marketplace.json", file=sys.stderr)
    marketplace_json.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

    return 0


if __name__ == "__main__":
    sys.exit(main())
