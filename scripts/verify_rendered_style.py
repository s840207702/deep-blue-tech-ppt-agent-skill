#!/usr/bin/env python3
"""Run the Playwright rendered-style verifier with a predictable CLI."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path


def find_node() -> str | None:
    return os.environ.get("NODE_PATH_EXECUTABLE") or shutil.which("node")


def has_playwright(node: str) -> bool:
    skill_root = Path(__file__).resolve().parents[1]
    try:
        result = subprocess.run(
            [node, "-e", "require.resolve('playwright')"],
            check=False,
            capture_output=True,
            text=True,
            timeout=8,
            env=os.environ.copy(),
            cwd=skill_root,
        )
    except (OSError, subprocess.TimeoutExpired):
        return False
    return result.returncode == 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Verify every slide's computed title styles and real loaded FontFace state."
    )
    parser.add_argument("html", type=Path, help="Generated presentation HTML")
    parser.add_argument("--browser", help="Path to Chrome, Chromium, or Edge")
    parser.add_argument("--timeout", type=int, default=30, help="Per-slide timeout in seconds")
    parser.add_argument("--slides", help="Comma-separated slide numbers; default verifies all")
    args = parser.parse_args()

    html_path = args.html.resolve()
    if not html_path.is_file():
        print(f"ERROR: file not found: {html_path}", file=sys.stderr)
        return 2

    node = find_node()
    if not node:
        print("ERROR: Node.js not found", file=sys.stderr)
        return 2
    if not has_playwright(node):
        print(
            "ERROR: Playwright not found. Run `npm install` in the Skill directory or expose it through NODE_PATH.",
            file=sys.stderr,
        )
        return 2

    verifier = Path(__file__).with_name("verify_rendered_style.cjs")
    command = [
        node,
        str(verifier),
        str(html_path),
        "--timeout",
        str(args.timeout),
    ]
    if args.browser:
        command.extend(["--browser", args.browser])
    if args.slides:
        command.extend(["--slides", args.slides])

    return subprocess.run(command, check=False, env=os.environ.copy()).returncode


if __name__ == "__main__":
    raise SystemExit(main())
