import pytest

from utils import MAX_CODE_LENGTH, get_navbar_styles, validate_user_input


def test_validate_user_input_success():
    """Ensure valid code returns True and no error message."""
    is_valid, msg = validate_user_input("def test(): pass")
    assert is_valid is True
    assert msg == ""


def test_validate_python_code_empty():
    """Ensure empty or whitespace input fails correctly."""
    is_valid, msg = validate_user_input("   ")
    assert is_valid is False
    assert "Please enter Python code" in msg


def test_validate_python_code_too_large():
    """Ensure code exceeding MAX_CODE_LENGTH fails."""
    too_long_code = "a = 1\n" * (MAX_CODE_LENGTH + 100)
    is_valid, msg = validate_user_input(too_long_code)
    assert is_valid is False
    assert "Code is too large" in msg


def test_validate_python_code_syntax_error():
    """Ensure invalid syntax is caught by ast."""
    is_valid, msg = validate_user_input("def broken_function(")
    assert is_valid is False
    assert "Invalid Python syntax" in msg


def test_navbar_styles_structure():
    """Verify the styles dictionary contains required keys."""
    styles = get_navbar_styles()
    assert isinstance(styles, dict)
    assert "nav" in styles
    assert styles["nav"]["font-family"] == "Cascadia Code"
