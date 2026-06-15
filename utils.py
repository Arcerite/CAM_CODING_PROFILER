import ast
from typing import Dict, Any

def get_navbar_styles() -> Dict[str, Dict[str, str]]:
    """
    Get the styles for the navbar.
    """
    return {
        "nav": {
            "background-color": "var(--primary-color)",
            "align-items": "center",
            "font-family": "Cascadia Code",
            "padding-top": "1rem",
            "padding-bottom": "1rem",
            "display": "flex",
        },
        "div": {"max-width": "100%"},
        "span": {
            "justify-content": "right",
            "color": "var(--text-color)",
            "font-weight": "normal",
            "font-size": "14px",
        },
        "img": {"height": "50px", "width": "auto"},
        "active": {"color": "var(--text-color)"},
        "hover": {"color": "var(--text-color)"},
    }

def get_navbar_options() -> Dict[str, bool]:
    """
    Get the options for the navbar.
    """
    return {"show_menu": False, "show_sidebar": False, "hide_nav": True}

def validate_user_input(user_input: str) -> tuple[bool, str]:
    """
    Validate the user input to ensure it's not empty and has valid Python syntax.

    Args:
    user_input (str): The user input to validate.

    Returns:
    bool: True if the input is valid, False otherwise.
    """
    if not user_input.strip():
        return False, "Please enter Python code."
    if len(user_input) > 15000:
        return False, "Code is too large."
    try:
        ast.parse(user_input)
    except SyntaxError as error:
        return False, f"Invalid Python syntax:\n{error}"
    return True, ""