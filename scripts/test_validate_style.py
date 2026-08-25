#!/usr/bin/env python3
"""Regression tests for the locked Terminal Studio style validator."""

from __future__ import annotations

import unittest
from pathlib import Path
from unittest.mock import patch

import validate_style


ROOT = Path(__file__).resolve().parents[1]
STARTER = ROOT / "assets" / "terminal-studio-16x9.html"
SQUARE_STARTER = ROOT / "assets" / "terminal-studio-1x1.html"


class StyleValidatorTests(unittest.TestCase):
    def test_canonical_starter_passes(self) -> None:
        self.assertEqual(validate_style.validate(STARTER), [])

    def test_square_starter_passes(self) -> None:
        self.assertEqual(validate_style.validate(SQUARE_STARTER), [])

    def test_positive_title_tracking_is_rejected(self) -> None:
        source = STARTER.read_text(encoding="utf-8").replace(
            "--main-title-letter-spacing: -0.045em;",
            "--main-title-letter-spacing: 0.02em;",
        )
        with patch.object(Path, "read_text", return_value=source):
            errors = validate_style.validate(Path("drifted.html"))
        self.assertTrue(any("token drift" in error for error in errors))
        self.assertTrue(any("positive or zero" in error for error in errors))

    def test_missing_font_gate_is_rejected(self) -> None:
        source = STARTER.read_text(encoding="utf-8").replace(
            "document.fonts.ready", "Promise.resolve()"
        )
        with patch.object(Path, "read_text", return_value=source):
            errors = validate_style.validate(Path("no-font-gate.html"))
        self.assertTrue(any("font readiness wait" in error for error in errors))

    def test_independent_quote_title_is_rejected(self) -> None:
        source = STARTER.read_text(encoding="utf-8").replace(
            '<h2 class="title">风格稳定', '<h2 class="quote-text">风格稳定'
        )
        with patch.object(Path, "read_text", return_value=source):
            errors = validate_style.validate(Path("quote-drift.html"))
        self.assertTrue(any("all h1/h2" in error for error in errors))
        self.assertTrue(any("quote-text" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
