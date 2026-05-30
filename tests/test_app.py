from streamlit.testing.v1 import AppTest
from unittest.mock import patch


def test_app_renders_properly():
    at = AppTest.from_file("app.py").run()
    assert at.title[0].value == "🚀 AI-Powered Code Profiler"
    assert any("Results will appear here after analysis."
            in m.value for m in at.markdown)


# Patching the source module directly to catch the 'from analyzer import...'
@patch("analyzer.generate_readme")
@patch("analyzer.refactor_code")
@patch("analyzer.analyze_code")
def test_successful_analysis_flow(mock_analyze, mock_refactor, mock_readme):
    # Define mock behaviors
    mock_analyze.return_value = {
        "big_o": {"time": "O(1)", "space": "O(1)", "explanation": "Mocked complexity"},
        "flaws": ["None"],
        "suggestions": ["Keep it up"]
    }
    mock_refactor.return_value = "def mocked_code(): pass"
    mock_readme.return_value = "# Mocked README"

    # Start the app test
    at = AppTest.from_file("app.py").run()

    # Input valid code to satisfy ast.parse(user_input)
    at.text_area[0].input("def greet():\n    print('hi')").run()

    # Click the button
    at.button[0].click().run()

    # Verify the results in the UI
    # 1. Check Complexity Info
    assert "Time Complexity: O(1)" in at.info[0].value

    # 2. Check Refactored Code Block
    assert at.code[0].value == "def mocked_code(): pass"


def test_no_code_input_stops():
    """Verify the app stops and warns if the text area is empty."""
    at = AppTest.from_file("app.py").run()

    # 1. Leave text area empty (default state)
    # 2. Click the button
    at.button[0].click().run()

    # Verify warning appears and stop was called
    assert len(at.warning) > 0
    assert at.warning[0].value == "Please enter Python code."

    # Verify that analysis results are NOT rendered
    assert len(at.info) == 0


def test_invalid_syntax_stops():
    """Verify the app stops and errors if the Python syntax is broken."""
    at = AppTest.from_file("app.py").run()

    # 1. Input broken Python code
    at.text_area[0].input("def broken_function(:").run()

    # 2. Click the button
    at.button[0].click().run()

    # Verify error appears
    assert len(at.error) > 0
    assert "Invalid Python syntax" in at.error[0].value

    # Verify the app stopped before reaching the analysis step
    assert len(at.info) == 0
