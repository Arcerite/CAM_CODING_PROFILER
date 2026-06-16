"""Unit tests verifying layout asset presentation matrices."""

from utils import get_navbar_styles


def test_navbar_styles_structure():
    """Verify typography configurations map accurately inside style dictionary objects."""
    styles = get_navbar_styles()
    assert isinstance(styles, dict)
    assert "nav" in styles
    assert styles["nav"]["font-family"] == "Cascadia Code"
