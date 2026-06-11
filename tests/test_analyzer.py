from analyzer import validate_analysis_response


def test_validate_analysis_response_success():
    """Test with a perfectly formatted dictionary.
    This should return true when validated"""

    valid_data = {
        "big_o": {
            "time": "O(n)",
            "space": "O(1)",
            "explanation": "Simple loop.",
        },  # noqa: E501
        "flaws": ["None"],
        "suggestions": ["Add type hints"],
    }
    assert validate_analysis_response(valid_data) is True


def test_validate_analysis_response_missing_key():
    """Test that it fails if a top-level key is missing."""
    invalid_data = {
        "big_o": {"time": "O(n)", "space": "O(1)", "explanation": "..."}
        # "flaws" and "suggestions" are missing
    }
    assert validate_analysis_response(invalid_data) is False


def test_validate_analysis_response_wrong_type():
    """Test that it fails if 'flaws' is a string instead of a list."""
    invalid_data = {
        "big_o": {"time": "O(n)", "space": "O(1)", "explanation": "..."},
        "flaws": "No flaws here!",  # Should be a list
        "suggestions": [],
    }
    assert validate_analysis_response(invalid_data) is False
