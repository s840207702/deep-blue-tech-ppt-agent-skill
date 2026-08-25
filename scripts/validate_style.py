#!/usr/bin/env python3
"""Validate the locked Terminal Studio visual contract in a generated HTML deck."""

from __future__ import annotations

import argparse
import re
import sys
from html.parser import HTMLParser
from pathlib import Path


PROFILES = {"terminal-studio-16x9-v1", "terminal-studio-1x1-v1"}

REQUIRED_DECLARATIONS = {
    "--bg-primary": "#0b0f17",
    "--text-primary": "#f7f2ea",
    "--accent": "#77d7ff",
    "--line-strong": "rgba(119, 215, 255, 0.42)",
    "--main-title-weight": "900",
    "--main-title-letter-spacing": "-0.045em",
    "--main-title-line-height": "1.08",
    "--title-size": "clamp(3.7rem, 6vw, 6.4rem)",
    "--h2-size": "clamp(3rem, 5vw, 5.3rem)",
}

REQUIRED_SNIPPETS = {
    "font readiness wait": "document.fonts.ready",
    "render readiness flag": "window.__SLIDES_READY__",
    "computed-style runtime gate": "getComputedStyle",
    "loaded FontFace runtime gate": "[...document.fonts]",
    "root font-size runtime gate": "rootSize === 16",
    "accent inheritance runtime gate": "accentResults",
    "title max-width runtime gate": "maxWidthOk",
    "style-ready runtime gate": "dataset.styleReady",
    "images-ready runtime gate": "dataset.imagesReady",
    "render-ready runtime gate": "dataset.renderReady",
    "visible render failure gate": "REQUIRED STYLE, FONTS, OR IMAGES NOT READY — DO NOT EXPORT",
    "shared cover title class": ".cover-title",
    "shared content title class": ".title",
    "font family inheritance": "font-family: var(--main-title-family)",
    "font weight inheritance": "font-weight: var(--main-title-weight)",
    "tracking inheritance": "letter-spacing: var(--main-title-letter-spacing)",
    "line-height inheritance": "line-height: var(--main-title-line-height)",
    "locked root font size": "html { font-size: 16px; }",
}

FONT_SOURCE_PATTERNS = {
    "Noto Sans SC font source": re.compile(
        r"Noto\+Sans\+SC|@font-face\s*\{[^}]*font-family\s*:\s*['\"]?Noto Sans SC",
        re.IGNORECASE | re.DOTALL,
    ),
    "JetBrains Mono font source": re.compile(
        r"JetBrains\+Mono|@font-face\s*\{[^}]*font-family\s*:\s*['\"]?JetBrains Mono",
        re.IGNORECASE | re.DOTALL,
    ),
}


def declaration_values(source: str, name: str) -> list[str]:
    pattern = re.compile(rf"{re.escape(name)}\s*:\s*([^;]+);", re.IGNORECASE)
    return [match.strip() for match in pattern.findall(source)]


class HeadingContractParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.invalid_headings: list[str] = []
        self.invalid_quote_classes: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        classes = set((attributes.get("class") or "").split())
        canonical = bool(classes & {"title", "cover-title"})
        if tag in {"h1", "h2"} and not canonical:
            self.invalid_headings.append(f"<{tag} class=\"{' '.join(sorted(classes))}\">")
        if "quote-text" in classes and not canonical:
            self.invalid_quote_classes.append(f"<{tag} class=\"{' '.join(sorted(classes))}\">")


def validate(path: Path) -> list[str]:
    source = path.read_text(encoding="utf-8")
    errors: list[str] = []

    profile_match = re.search(
        r'<meta\s+name=["\']terminal-studio-profile["\']\s+content=["\']([^"\']+)["\']',
        source,
        re.IGNORECASE,
    )
    if not profile_match:
        errors.append("missing terminal-studio-profile meta marker")
    elif profile_match.group(1) not in PROFILES:
        errors.append(
            f"unknown terminal-studio profile: {profile_match.group(1)}; expected one of {sorted(PROFILES)}"
        )

    for name, expected in REQUIRED_DECLARATIONS.items():
        values = declaration_values(source, name)
        if not values:
            errors.append(f"missing locked token: {name}: {expected}")
        elif values != [expected]:
            errors.append(
                f"token drift: {name} must appear once as {expected}; found {values}"
            )

    for label, snippet in REQUIRED_SNIPPETS.items():
        if snippet not in source:
            errors.append(f"missing {label}: {snippet}")

    for label, pattern in FONT_SOURCE_PATTERNS.items():
        if not pattern.search(source):
            errors.append(f"missing {label}")

    parser = HeadingContractParser()
    parser.feed(source)
    if parser.invalid_headings:
        errors.append(
            "all h1/h2 elements must use .title or .cover-title: "
            + ", ".join(parser.invalid_headings)
        )
    if parser.invalid_quote_classes:
        errors.append(
            ".quote-text may not define an independent title system: "
            + ", ".join(parser.invalid_quote_classes)
        )

    positive_tracking = [
        value
        for value in declaration_values(source, "--main-title-letter-spacing")
        if not value.startswith("-")
    ]
    if positive_tracking:
        errors.append(f"positive or zero main-title tracking is forbidden: {positive_tracking}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate a locked Terminal Studio visual contract."
    )
    parser.add_argument("html", type=Path, help="Generated presentation HTML")
    args = parser.parse_args()

    if not args.html.is_file():
        print(f"ERROR: file not found: {args.html}", file=sys.stderr)
        return 2

    errors = validate(args.html)
    if errors:
        print(f"FAIL: {args.html} does not match a supported Terminal Studio profile", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"PASS: {args.html} matches a supported Terminal Studio profile")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
