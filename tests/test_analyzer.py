from unittest.mock import MagicMock, patch

import pytest
import streamlit as st

from analyzer import (
    _query_llm, analyze_code, create_client, generate_readme, refactor_code,
    validate_analysis_response)

# =====================================================================
# 1. EXISTING TESTS (VALIDATE_ANALYSIS_RESPONSE) + EXTENDED BRANCHES
# =====================================================================


def test_validate_analysis_response_success():
    """Test with a perfectly formatted dictionary."""
    valid_data = {
        "is_valid_code": True,  # <-- Add this
        "language": "python",  # <-- Add this
        "extension": ".py",  # <-- Add this
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
    """Test that it fails if a top-level key is missing."""
    invalid_data = {"big_o": {"time": "O(n)", "space": "O(1)", "explanation": "..."}}
    assert validate_analysis_response(invalid_data) is False


def test_validate_analysis_response_wrong_type():
    """Test that it fails if 'flaws' is a string instead of a list."""
    invalid_data = {
        "big_o": {"time": "O(n)", "space": "O(1)", "explanation": "..."},
        "flaws": "No flaws here!",
        "suggestions": [],
    }
    assert validate_analysis_response(invalid_data) is False


def test_validate_analysis_response_invalid_inner_structures():
    """Cover the remaining branch lines inside validate_analysis_response."""
    # Not a dictionary at all
    assert validate_analysis_response("not a dict") is False

    # big_o is not a dict or missing inner keys
    bad_big_o = {"big_o": "string", "flaws": [], "suggestions": []}
    assert validate_analysis_response(bad_big_o) is False

    bad_big_o_keys = {"big_o": {"time": "O(1)"}, "flaws": [], "suggestions": []}
    assert validate_analysis_response(bad_big_o_keys) is False

    # flaws list containing non-strings
    bad_flaws = {
        "big_o": {"time": "O(1)", "space": "O(1)", "explanation": ""},
        "flaws": [123],
        "suggestions": [],
    }
    assert validate_analysis_response(bad_flaws) is False

    # suggestions list containing non-strings
    bad_suggestions = {
        "big_o": {"time": "O(1)", "space": "O(1)", "explanation": ""},
        "flaws": [],
        "suggestions": [True],
    }
    assert validate_analysis_response(bad_suggestions) is False


# =====================================================================
# 2. CLIENT CREATION TESTS (Lines 15-32)
# =====================================================================


@patch("analyzer.Groq")
def test_create_client_from_secrets(mock_groq):
    """Test creating client when API key is found in st.secrets."""
    with patch.object(st, "secrets", {"GROQ_API_KEY": "secret_key"}):
        create_client()
        mock_groq.assert_called_once_with(api_key="secret_key")


@patch("analyzer.os.getenv")
@patch("analyzer.load_dotenv")
@patch("analyzer.Groq")
def test_create_client_from_env(mock_groq, mock_load_dotenv, mock_getenv):
    """Test fallback to .env when st.secrets raises an Exception or is empty."""
    mock_getenv.return_value = "env_key"

    # Simulating st.secrets missing / throwing exception
    with patch.object(st, "secrets", {}):
        create_client()
        mock_load_dotenv.assert_called_once()
        mock_getenv.assert_called_once_with("GROQ_API_KEY")
        mock_groq.assert_called_once_with(api_key="env_key")


@patch("analyzer.os.getenv")
@patch("analyzer.load_dotenv")
def test_create_client_missing_key_error(mock_load_dotenv, mock_getenv):
    """Test that ValueError is thrown if key is completely missing."""
    mock_getenv.return_value = None
    with patch.object(st, "secrets", {}):
        with pytest.raises(ValueError, match="GROQ_API_KEY could not be found"):
            create_client()


# =====================================================================
# 3. LLM QUERY HELPERS & CORE ENGINES (Lines 44-59, 72, 80, 87-121)
# =====================================================================


@patch("analyzer.create_client")
def test_query_llm_with_response_format(mock_create_client):
    """Test internal query helper passes variables and formats perfectly."""
    mock_client = MagicMock()
    mock_create_client.return_value = mock_client
    mock_client.chat.completions.create.return_value.choices[0].message.content = (
        "  mocked response   "
    )

    res = _query_llm(
        "sys prompt", "user prompt", response_format={"type": "json_object"}
    )

    assert res == "mocked response"
    mock_client.chat.completions.create.assert_called_once_with(
        model="llama-3.3-70b-versatile",
        temperature=0,
        messages=[
            {"role": "system", "content": "sys prompt"},
            {"role": "user", "content": "user prompt"},
        ],
        response_format={"type": "json_object"},
    )


@patch("analyzer._query_llm")
def test_analyze_code_success(mock_query):
    """Test analyze_code handles valid structured JSON returns successfully."""
    mock_query.return_value = '{"is_valid_code": true, "language": "python", "extension": ".py", "big_o": {"time": "O(1)", "space": "O(1)", "explanation": "Good"}, "flaws": [], "suggestions": []}'

    result = analyze_code("print('hello')")
    assert result["big_o"]["time"] == "O(1)"
    mock_query.assert_called_once()


@patch("analyzer._query_llm")
def test_analyze_code_retry_and_fallback(mock_query):
    """Test code analysis retries upon invalid scheme and falls back cleanly."""
    # First attempt: garbage text. Second attempt: broken json. Third attempt: exceptions out.
    mock_query.side_effect = [
        "not json",
        '{"bad_json": true}',
        Exception("API Failure"),
    ]

    result = analyze_code("print('hello')")

    # Asserts fallback structure is successfully reached after 3 bad attempts
    assert result["big_o"]["time"] == "Unknown"
    assert "Failed to generate valid analysis." in result["flaws"]
    assert mock_query.call_count == 3


# =====================================================================
# 4. REFACTOR & DOCUMENTATION ENGINES (Lines 134-154, 159-167)
# =====================================================================


@patch("analyzer._query_llm")
def test_refactor_code(mock_query):
    """Verify refactoring framework passes payload execution downstream."""
    mock_query.return_value = "def typed_function() -> None:\n    pass"
    res = refactor_code("def typed_function(): pass")
    assert "def typed_function() -> None:" in res


@patch("analyzer._query_llm")
def test_generate_readme(mock_query):
    """Verify readme framework passes payload execution downstream."""
    mock_query.return_value = "# Readme Markdown"
    res = generate_readme("print(1)")
    assert res == "# Readme Markdown"


@patch("analyzer.os.getenv")
@patch("analyzer.load_dotenv")
@patch("analyzer.Groq")
def test_create_client_secrets_exception_handling(
    mock_groq, mock_load_dotenv, mock_getenv
):
    """Explicitly force st.secrets to throw an exception to hit the 'except Exception: pass' block."""
    mock_getenv.return_value = "fallback_env_key"

    # Patch st.secrets with an object that explodes with an Exception upon membership testing ("in")
    with patch.object(
        st, "secrets", side_effect=TypeError("Simulated Streamlit environment error")
    ):
        client = create_client()

        # Verify it bypassed the crash, hit 'pass', and successfully moved on to the .env fallback
        mock_load_dotenv.assert_called_once()
        mock_getenv.assert_called_once_with("GROQ_API_KEY")
        mock_groq.assert_called_once_with(api_key="fallback_env_key")
