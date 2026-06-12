from unittest.mock import patch

from streamlit.testing.v1 import AppTest


def test_app_renders_properly():
    """Verify that the side-by-side layout loads up basic headers successfully."""
    at = AppTest.from_file("app.py").run()
    assert not at.exception

    # Check that the columns and layout title subheader render properly
    assert at.subheader[0].value == "Source Code"


@patch("analyzer.generate_readme")
@patch("analyzer.refactor_code")
@patch("analyzer.analyze_code")
def test_successful_analysis_flow(mock_analyze, mock_refactor, mock_readme):
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

    # Spin up our simulated app environment
    at = AppTest.from_file("app.py").run()

    # Locate the Python input box, send code, and hit run
    at.text_area[0].input("def greet():\n    print('hi')").run()
    at.button[0].click().run()

    assert not at.exception

    # Read layout values directly from Streamlit's Markdown element array
    # because layout blocks and expanders render text inside `at.markdown`
    all_markdown_text = [md.value for md in at.markdown]

    # Assert that all the core processing data successfully reached the frontend
    assert any("Time Complexity: O(1)" in text for text in all_markdown_text)
    assert any("Space Complexity: O(1)" in text for text in all_markdown_text)
    assert any("Mocked complexity details." in text for text in all_markdown_text)


def test_invalid_syntax_error_handling():
    """Verify that inputting broken code breaks gracefully via ast validation."""
    at = AppTest.from_file("app.py").run()

    # Pass in invalid, broken syntax to trigger syntax checks
    at.text_area[0].input("def broken_function(").run()
    at.button[0].click().run()

    # Verify that an error element popped up on screen to warn the developer
    assert len(at.error) > 0
    assert "Invalid Python syntax" in at.error[0].value


def test_empty_input_warning():
    """Ensure submitting spaces or nothing warns the developer explicitly."""
    at = AppTest.from_file("app.py").run()

    # Send entirely blank spaces
    at.text_area[0].input("   ").run()
    at.button[0].click().run()

    # Check for the expected Streamlit warning box element
    assert len(at.warning) > 0
    assert "Please enter Python code." in at.warning[0].value
