from __future__ import annotations

import ast
from typing import Dict, Optional

import streamlit as st
from dotenv import load_dotenv
from streamlit_navigation_bar import st_navbar

from analyzer import analyze_code, generate_readme, refactor_code


def _set_page_config() -> None:
    """
    Set the page configuration for the Streamlit app.
    """
    st.set_page_config(
        page_title="Code Buddy",
        page_icon="Images/smile_icon.png",
        layout="wide",
        initial_sidebar_state="collapsed",
    )


def _hide_streamlit_buttons() -> None:
    """
    Hide the Streamlit buttons and add custom styles.
    """
    st.markdown(
        """
    .stAppDeployButton {
        display: none;
    }
    <style>
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        padding-left: 1rem;
        padding-right: 1rem;
    },
    [data-testid="st-navbar"] > div {
    display: flex !important;
    justify-content: space-between !important;
    align-items: center !important;
    max-width: 100% !important;
    padding-left: 2rem;
    padding-right: 2rem;
    },
    [data-testid="st-navbar"] > div > div {
        flex: 0 1 auto !important;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )


def _get_navbar_styles() -> Dict[str, Dict[str, str]]:
    """
    Get the styles for the navbar.
    """
    return {
        "nav": {
            "background-color": "#60A54D",
            "align-items": "center",
            "font-family": "sans-serif",
            "padding-top": "1rem",
            "padding-bottom": "1rem",
            "display": "flex",
        },
        "div": {"max-width": "100%"},
        "span": {
            "justify-content": "right",
            "color": "#FFFFFF",
            "font-weight": "normal",
            "font-size": "14px",
        },
        "img": {"height": "50px", "width": "auto"},
        "active": {"color": "#FFFFFF"},
        "hover": {"color": "#FFFFFF"},
    }


def _get_options() -> Dict[str, bool]:
    """
    Get the options for the navbar.
    """
    return {"show_menu": False, "show_sidebar": False, "hide_nav": True}


def _initialize_session_state() -> None:
    """
    Initialize the session state to store analysis results.
    """
    if "analysis_results" not in st.session_state:
        st.session_state.analysis_results = None


def _validate_user_input(user_input: str) -> bool:
    """
    Validate the user input to ensure it's not empty and has valid Python syntax.

    Args:
    user_input (str): The user input to validate.

    Returns:
    bool: True if the input is valid, False otherwise.
    """
    if not user_input.strip():
        st.warning("Please enter Python code.")
        st.stop()
    if len(user_input) > 15000:
        st.error("Code is too large.")
        return False
    try:
        ast.parse(user_input)
    except SyntaxError as error:
        st.error(f"Invalid Python syntax:\n{error}")
        return False
    return True


def _render_complexity_section(analysis: Optional[dict]) -> None:
    """
    Render the complexity analysis section.

    Args:
        analysis (Optional[dict]): The analysis results.
    """
    with st.expander("**Complexity**", expanded=True):
        if analysis is None:
            st.write("Please run the code analysis to find the complexity.")
        else:
            big_o = analysis.get("big_o", {})
            st.write(
                f"Time Complexity: {big_o.get('time', 'Unknown')}  \n",
                f"Space Complexity: {big_o.get('space', 'Unknown')}  \n\n",
                big_o.get("explanation", "No explanation provided."),
            )


def _render_flaws_section(analysis: Optional[dict]) -> None:
    """
    Render the identified flaws section.

    Args:
        analysis (Optional[dict]): The analysis results.
    """
    with st.expander("**Identified Flaws**", expanded=False):
        if analysis is None:
            st.write("Please run the code analysis to find flaws.")
        else:
            flaws = analysis.get("flaws", [])
            if flaws:
                for flaw in flaws:
                    st.write(f"- {flaw}")
            else:
                st.success("No major flaws detected.")


def _render_suggestions_section(analysis: Optional[dict]) -> None:
    """
    Render the suggestions section.

    Args:
        analysis (Optional[dict]): The analysis results.
    """
    with st.expander("**Suggestions**", expanded=False):
        if analysis is None:
            st.write("Please run the code analysis to find suggestions.")
        else:
            suggestions = analysis.get("suggestions", [])
            if suggestions:
                for suggestion in suggestions:
                    st.write(f"- {suggestion}")
            else:
                st.success("No suggestions generated.")


def _render_refactored_code_section(refactored_code: Optional[str]) -> None:
    """
    Render the refactored code section.

    Args:
        refactored_code (Optional[str]): The refactored code.
    """
    with st.expander("**Refactored Code**", expanded=False):
        if refactored_code is None:
            st.write("Please run the code analysis to get refactored code.")
        else:
            st.code(refactored_code, language="python")


def _render_readme_section(readme_content: Optional[str]) -> None:
    """
    Render the generated README section.

    Args:
        readme_content (Optional[str]): The generated README content.
    """
    with st.expander("**Generated README**", expanded=False):
        if readme_content is None:
            st.write("Please run the code analysis to get the generated README.")
        else:
            st.markdown(readme_content)


def _render_download_buttons(
    refactored_code: Optional[str],
    readme_content: Optional[str],
) -> None:
    """
    Render download buttons for code and README.

    Args:
        refactored_code (Optional[str]): The refactored code.
        readme_content (Optional[str]): The generated README content.
    """
    if (readme_content is not None) and (refactored_code is not None):
        st.markdown("---")
        d_col1, d_col2 = st.columns(2)
        with d_col1:
            st.download_button(
                label="💾 Download Code",
                data=refactored_code,
                file_name="refactored_code.py",
                mime="text/x-python",
                use_container_width=True,
            )
        with d_col2:
            st.download_button(
                label="📖 Download README",
                data=readme_content,
                file_name="README.md",
                mime="text/markdown",
                use_container_width=True,
            )


def render_analysis_ui(
    analysis: Optional[dict] = None,
    refactored_code: Optional[str] = None,
    readme_content: Optional[str] = None,
):
    """
    Render the analysis UI with all sections.

    Args:
        analysis (Optional[dict]): The analysis results.
        refactored_code (Optional[str]): The refactored code.
        readme_content (Optional[str]): The generated README content.
    """
    _render_complexity_section(analysis)
    _render_flaws_section(analysis)
    _render_suggestions_section(analysis)
    _render_refactored_code_section(refactored_code)
    _render_readme_section(readme_content)
    _render_download_buttons(refactored_code, readme_content)


def analyze(user_input: str):
    """
    Analyze the user input code.

    Args:
        user_input (str): The user input code.
    """
    if not _validate_user_input(user_input):
        return

    try:
        with st.spinner("Analyzing code..."):
            analysis = analyze_code(user_input)
            refactored_code = refactor_code(user_input)
            readme_content = generate_readme(user_input)

            # Save the raw outputs into session state
            st.session_state.analysis_results = {
                "analysis": analysis,
                "refactored_code": refactored_code,
                "readme_content": readme_content,
            }

    except Exception as error:
        st.error(f"Analysis failed:\n{error}")


def main() -> None:
    """
    Create the home page.
    """
    _set_page_config()
    _hide_streamlit_buttons()
    st_navbar(
        ["About"],
        "Home",
        logo_path="Images/logo2.svg",
        logo_page="Home",
        urls={"About": "https://github.com/Arcerite/CAM_CODING_PROFILER"},
        styles=_get_navbar_styles(),
        options=_get_options(),
        adjust=False,
    )

    load_dotenv()
    _initialize_session_state()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Source Code")
        user_input = st.text_area(
            "Source Code",
            height=600,
            placeholder="Paste code here...",
            label_visibility="collapsed",
        )

        analyze_button = st.button(
            "Analyze & Refactor",
            type="primary",
            use_container_width=True,
        )

    with col2:
        st.markdown(
            "<h3 style='text-align: center;'> Results</h3>",
            unsafe_allow_html=True,
        )
        if analyze_button:
            analyze(user_input)

        # Check if we have saved results in session state to render
        if st.session_state.analysis_results is not None:
            results = st.session_state.analysis_results
            render_analysis_ui(
                analysis=results["analysis"],
                refactored_code=results["refactored_code"],
                readme_content=results["readme_content"],
            )
        else:
            render_analysis_ui(None, None, None)


if __name__ == "__main__":
    main()
