#!/usr/bin/env python3
"""Browser regression tests for CSS overrides and fake font sources."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import verify_rendered_style


ROOT = Path(__file__).resolve().parents[1]
STARTER = ROOT / "assets" / "terminal-studio-16x9.html"
SQUARE_STARTER = ROOT / "assets" / "terminal-studio-1x1.html"
VERIFIER = ROOT / "scripts" / "verify_rendered_style.py"


NODE = verify_rendered_style.find_node()


@unittest.skipUnless(
    NODE and verify_rendered_style.has_playwright(NODE),
    "Node.js and Playwright are required",
)
class RenderedStyleTests(unittest.TestCase):
    def verify(self, path: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(VERIFIER), str(path), "--slides", "1"],
            check=False,
            capture_output=True,
            text=True,
            timeout=45,
        )

    def test_canonical_profiles_pass(self) -> None:
        self.assertEqual(self.verify(STARTER).returncode, 0)
        self.assertEqual(self.verify(SQUARE_STARTER).returncode, 0)

    def test_late_css_title_override_fails(self) -> None:
        source = STARTER.read_text(encoding="utf-8").replace(
            "</style>",
            ".cover-title{font-family:Arial;font-weight:700;letter-spacing:.02em;line-height:1.3;font-size:3rem;max-width:600px}</style>",
        )
        with tempfile.TemporaryDirectory(prefix="terminal-studio-test-") as temp_dir:
            path = Path(temp_dir) / "override.html"
            path.write_text(source, encoding="utf-8")
            self.assertEqual(self.verify(path).returncode, 1)

    def test_fake_font_source_fails(self) -> None:
        source = STARTER.read_text(encoding="utf-8").replace(
            "fonts.googleapis.com", "example.invalid"
        ).replace("fonts.gstatic.com", "example.invalid")
        with tempfile.TemporaryDirectory(prefix="terminal-studio-test-") as temp_dir:
            path = Path(temp_dir) / "fake-font.html"
            path.write_text(source, encoding="utf-8")
            self.assertEqual(self.verify(path).returncode, 1)

    def test_title_accent_override_fails(self) -> None:
        source = STARTER.read_text(encoding="utf-8").replace(
            "</style>",
            ".title-accent{font-family:Arial;font-weight:500;letter-spacing:.04em}</style>",
        )
        with tempfile.TemporaryDirectory(prefix="terminal-studio-test-") as temp_dir:
            path = Path(temp_dir) / "accent-override.html"
            path.write_text(source, encoding="utf-8")
            self.assertEqual(self.verify(path).returncode, 1)

    def test_broken_image_fails(self) -> None:
        source = STARTER.read_text(encoding="utf-8").replace(
            "    <script>\n      const slides",
            '    <img src="missing-image.png" alt="broken image test">\n\n    <script>\n      const slides',
        )
        with tempfile.TemporaryDirectory(prefix="terminal-studio-test-") as temp_dir:
            path = Path(temp_dir) / "broken-image.html"
            path.write_text(source, encoding="utf-8")
            self.assertEqual(self.verify(path).returncode, 1)


if __name__ == "__main__":
    unittest.main()
