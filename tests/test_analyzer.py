"""Unit tests validating core analytical models, guardrails, and structural parsing mechanisms."""

from unittest.mock import patch

import streamlit as st

from analyzer import (
    analyze_code,
    generate_readme,
    refactor_code,
    validate_analysis_response,
)


def test_validate_analysis_response_success():
    """Verify that a correctly structured payload returns True from the validator."""
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
    }
    assert validate_analysis_response(valid_data) is True


def test_validate_analysis_response_missing_key():
    """Verify that omitting required schema keys sets validation states to False."""
    invalid_data = {"big_o": {"time": "O(n)", "space": "O(1)", "explanation": "..."}}
    assert validate_analysis_response(invalid_data) is False


@patch("analyzer._query_llm")
def test_refactor_code(mock_query):
    """Verify refactoring pipeline forwards functional logic prompts into upstream network routers."""
    mock_query.return_value = "def typed_function() -> None:\n    pass"
    res = refactor_code("def typed_function(): pass")
    assert "def typed_function() -> None:" in res


@patch("analyzer._query_llm")
def test_generate_readme(mock_query):
    """Verify code structure converts smoothly down into documentation markdown outputs."""
    mock_query.return_value = "# Readme Markdown"
    res = generate_readme("print(1)")
    assert res == "# Readme Markdown"


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


@patch("analyzer._query_llm")
def test_analyze_code_invalid_structure(mock_query):
    """Verify parsing faulty configurations triggers runtime recovery schemas gracefully."""
    mock_query.return_value = '{"malformed_json":'
    res = analyze_code("some code")
    assert res["is_valid_code"] is False
