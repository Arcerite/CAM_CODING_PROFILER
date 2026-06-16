"""Integration tests evaluating application view renderings, reactive elements, and lifecycle routines."""

from unittest.mock import patch

from streamlit.testing.v1 import AppTest


def test_app_renders_properly():
    """Verify that structural panels and baseline grid interfaces launch correctly."""
    at = AppTest.from_file("app.py").run()
    assert not at.exception
    assert at.subheader[0].value == "Source Code"


def test_invalid_syntax_error_handling():
    """Verify that text blocks violating security parameters abort execution flows early."""
    with patch("app.analyze_code") as mock_analyze:
        mock_analyze.return_value = {
            "is_valid_code": False,
            "language": "python",
            "extension": ".py",
            "big_o": {
                "time": "Unknown",
                "space": "Unknown",
                "explanation": "Broken syntax.",
            },
            "flaws": ["Invalid syntax."],
            "suggestions": [],
        }

        at = AppTest.from_file("app.py").run()
        at.text_area[0].input("def broken_function(").run()
        at.button[0].click().run()

        results = at.session_state["analysis_results"]
        assert results is not None
        assert "Refactoring aborted" in results["refactored_code"]


def test_analyze_exception_handling():
    """Verify backend failure exceptions translate cleanly into on-screen alerts."""
    with patch("analyzer.analyze_code") as mock_analyze:
        mock_analyze.side_effect = RuntimeError("Groq API Timeout or Connection Error")

        at = AppTest.from_file("app.py").run()
        at.text_area[0].input("print('Hello World')").run()
        at.button[0].click().run()

        assert len(at.error) > 0


def test_empty_input_guardrail():
    """Verify that executing metrics requests over purely blank records returns warnings immediately."""
    at = AppTest.from_file("app.py").run()
    at.text_area[0].input("    ").run()
    at.button[0].click().run()

    assert len(at.warning) > 0
