from unittest.mock import patch

import pytest
from streamlit.testing.v1 import AppTest


@pytest.fixture
def app():
    return AppTest.from_file("app.py").run()


def test_app_renders_properly(app):
    """Verify that the side-by-side layout loads up basic headers successfully."""
    assert not app.exception

    # Check that the columns and layout title subheader render properly
    assert app.subheader[0].value == "Source Code"


@patch("analyzer.generate_readme")
@patch("analyzer.refactor_code")
@patch("analyzer.analyze_code")
def test_successful_analysis_flow(mock_analyze, mock_refactor, mock_readme, app):
    """Test the end-to-end analysis workflow from button press to UI updates."""
    # Define our mocked API payloads
    mock_analyze.return_value = {
        "big_o": {
            "time": "O(1)",
            "space": "O(1)",
            "explanation": "Mocked complexity details.",
        },
        "flaws": ["A mock flaw description."],
        "suggestions": ["A mock optimization suggestion."],
    }
    mock_refactor.return_value = "def mocked_code(): pass"
    mock_readme.return_value = "# Mocked README File Content"

    # Locate the Python input box, send code, and hit run
    app.text_area[0].input("def greet():\n    print('hi')").run()
    app.button[0].click().run()

    # Check session state
    state = app.session_state
    assert "analysis_results" in state
    results = state["analysis_results"]

    # Verify the structure matches what your logic saved
    assert results["analysis"]["big_o"]["time"] == "O(1)"
    assert results["refactored_code"] == "def mocked_code(): pass"
    assert results["readme_content"] == "# Mocked README File Content"

    assert not app.exception

    # Read layout values directly from Streamlit's Markdown element array
    # because layout blocks and expanders render text inside `at.markdown`
    all_markdown_text = [md.value for md in app.markdown]

    # Assert that all the core processing data successfully reached the frontend
    assert any("Time Complexity: O(1)" in text for text in all_markdown_text)
    assert any("Space Complexity: O(1)" in text for text in all_markdown_text)
    assert any("Mocked complexity details." in text for text in all_markdown_text)


def test_invalid_syntax_error_handling(app):
    """Verify that inputting broken code breaks gracefully via ast validation."""

    # Pass in invalid, broken syntax to trigger syntax checks
    app.text_area[0].input("def broken_function(").run()
    app.button[0].click().run()

    # Verify that an error element popped up on screen to warn the developer
    assert len(app.error) > 0
    assert "Invalid Python syntax" in app.error[0].value


def test_empty_input_warning(app):
    """Ensure submitting spaces or nothing warns the developer explicitly."""

    # Send entirely blank spaces
    app.text_area[0].input("   ").run()
    app.button[0].click().run()

    # Check for the expected Streamlit warning box element
    assert len(app.error) > 0
    assert "Please enter Python code." in app.error[0].value


def test_initial_session_state(app):
    assert "analysis_results" in app.session_state
    assert app.session_state["analysis_results"] is None
