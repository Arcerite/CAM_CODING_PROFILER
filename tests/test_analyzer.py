"""Unit tests validating unified analytical models, guardrails, and structural parsing mechanisms."""

from unittest.mock import patch

import streamlit as st

from analyzer import analyze_and_process_code, validate_analysis_response


def test_validate_analysis_response_success():
    """Verify that a correctly structured single-call payload returns True from the validator."""
    valid_data = {
        "is_valid_code": True,
        "language": "python",
        "extension": ".py",
        "big_o": {
            "time": "O(n)",
            "space": "O(1)",
            "explanation": "Simple loop.",
        },
        "flaws": ["None"],
        "suggestions": ["Add type hints"],
        "refactored_code": "def typed_function() -> None:\n    pass",
        "readme_content": "# Readme Markdown",
    }
    assert validate_analysis_response(valid_data) is True


def test_validate_analysis_response_missing_key():
    """Verify that omitting required schema keys sets validation states to False."""
    invalid_data = {"big_o": {"time": "O(n)", "space": "O(1)", "explanation": "..."}}
    assert validate_analysis_response(invalid_data) is False


def test_create_client_secrets_exception_handling():
    """Ensure unexpected secrets mapping formats prompt immediate environmental variable fallbacks."""
    with patch("analyzer.load_dotenv"), patch(
        "analyzer.os.getenv"
    ) as mock_getenv, patch("analyzer.Groq"), patch.object(
        st, "secrets", side_effect=TypeError("Simulated error")
    ):

        mock_getenv.return_value = "fallback_env_key"

        from analyzer import create_client

        client = create_client()
        assert client is not None


@patch("analyzer.Groq")
def test_analyze_code_invalid_structure(mock_groq_class):
    """Verify parsing faulty configurations triggers runtime recovery schemas gracefully."""
    mock_client = mock_groq_class.return_value
    mock_chat = mock_client.chat.completions.create
    mock_chat.return_value.choices = [
        type(
            "Choice",
            (object,),
            {
                "message": type(
                    "Message", (object,), {"content": '{"malformed_json":'}
                )()
            },
        )()  # noqa: E501
    ]

    res = analyze_and_process_code("some code")
    assert res["is_valid_code"] is False
