"""Setup layout views and interactions for the Streamlit Website."""

from __future__ import annotations

from typing import Any, Dict, Optional

import streamlit as st
from dotenv import load_dotenv
from streamlit_navigation_bar import st_navbar

from analyzer import analyze_and_process_code
from utils import MAX_CODE_LENGTH, get_navbar_options, get_navbar_styles


def _set_page_config() -> None:
    """Sets the main configuration of the page (website name, icon, etc)."""
    st.set_page_config(
        page_title="Code Buddy",
        page_icon="Images/smile_icon.png",
        layout="wide",
        initial_sidebar_state="collapsed",
    )


def _hide_streamlit_buttons() -> None:
    """hides basic buttons."""
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


def _initialize_session_state() -> None:
    """Safely keep results across hot-reloads."""
    if (
        "analysis_results" not in st.session_state
    ):  # This preseves any data on the site if the user clicks a button
        st.session_state.analysis_results = None


def _render_complexity_section(analysis: Optional[Dict[str, Any]]) -> None:
    """Render Big-O components.

    Args:
        analysis (Optional[Dict[str, Any]]): Decoded LLM metrics map, if available.
    """
    with st.expander(
        "**Complexity**", expanded=True
    ):  # If the complexity widget is open
        if analysis is None:
            st.write(
                "Please run the code analysis to find the complexity."
            )  # if there is no result tell them to run the analyzer
        else:  # if there is code, display the resutlts
            big_o = analysis.get("big_o", {})
            st.write(
                f"Time Complexity: {big_o.get('time', 'Unknown')}  \n",
                f"Space Complexity: {big_o.get('space', 'Unknown')}  \n\n",
                big_o.get("explanation", "No explanation provided."),
            )


def _render_flaws_section(analysis: Optional[Dict[str, Any]]) -> None:
    """Render flaws found within the code.

    Args:
        analysis (Optional[Dict[str, Any]]): Decoded LLM metrics map, if available.
    """
    with st.expander(
        "**Identified Flaws**", expanded=False
    ):  # if the flaw widget is open
        if (
            analysis is None
        ):  # if they did not analyze code tell them to run the program
            st.write("Please run the code analysis to find flaws.")
        else:  # otherwise show the flaws
            flaws = analysis.get("flaws", [])
            if flaws:  # if there are any flaws display each of them
                for flaw in flaws:
                    st.write(f"- {flaw}")
            else:  # if there are no flaws, and flaws is not none... then say no flaws detected
                st.success("No major flaws detected.")


def _render_suggestions_section(analysis: Optional[Dict[str, Any]]) -> None:
    """Render the suggestions generated.

    Args:
        analysis (Optional[Dict[str, Any]]): Decoded LLM metrics map, if available.
    """
    with st.expander(
        "**Suggestions**", expanded=False
    ):  # if the suggestions widget is open
        if (
            analysis is None
        ):  # if there is no analysis to show tell the user to run the program
            st.write("Please run the code analysis to find suggestions.")
        else:  # if there is analysis to show
            suggestions = analysis.get("suggestions", [])
            if (
                suggestions
            ):  # if there are any suggestions generated show them one by one
                for suggestion in suggestions:
                    st.write(f"- {suggestion}")
            else:  # otherwise if there are no suggestions but the program was run tell the user no suggestions generated
                st.success("No suggestions generated.")


def _render_refactored_code_section(
    refactored_code: Optional[str], language: str = "python"
) -> None:
    """Render syntax highlighted refactored code.

    Args:
        refactored_code (Optional[str]): Processed optimization logic string.
        language (str): Target text syntax type parsing target used by code blocks.
    """
    with st.expander(
        "**Refactored Code**", expanded=False
    ):  # if the refactored code widget is open
        if (
            refactored_code is None
        ):  # if there is no refactored code to show as the user to run the analysis
            st.write("Please run the code analysis to get refactored code.")
        else:  # otherwise show the code in the language that was detected
            st.code(refactored_code, language=language)


def _render_readme_section(readme_content: Optional[str]) -> None:
    """Render generated readme.

    Args:
        readme_content (Optional[str]): Formatted markdown documentation block.
    """
    with st.expander(
        "**Generated README**", expanded=False
    ):  # if the readme widget is open
        if (
            readme_content is None
        ):  # if there is no readme to show ask the user to run the code analysis to generate a readme
            st.write("Please run the code analysis to get the generated README.")
        else:  # otherwise show the readme that was generated
            st.markdown(readme_content)


def _render_download_buttons(
    refactored_code: Optional[str],
    readme_content: Optional[str],
    extension: str = ".py",
) -> None:
    """Render the download buttons underneath the columns.

    Args:
        refactored_code (Optional[str]): Source asset string bound for download.
        readme_content (Optional[str]): Documentation string asset bound for download.
        extension (str): Target filesystem text type suffix.
    """
    if (readme_content is not None) and (
        refactored_code is not None
    ):  # if both the readme and the refactored code exsists
        st.markdown("---")
        d_col1, d_col2 = st.columns(2)
        with (
            d_col1
        ):  # on the left have a collumn with a button to download refactored code
            st.download_button(
                label="💾 Download Code",
                data=refactored_code,
                file_name=f"refactored_code{extension}",
                mime="text/plain",
                use_container_width=True,
            )
        with d_col2:  # on the right, have a collumn with a button to download readme.md
            st.download_button(
                label="📖 Download README",
                data=readme_content,
                file_name="README.md",
                mime="text/markdown",
                use_container_width=True,
            )


def render_analysis_ui(
    analysis: Optional[Dict[str, Any]] = None,
    refactored_code: Optional[str] = None,
    readme_content: Optional[str] = None,
) -> None:
    """render the full ui

    Args:
        analysis (Optional[Dict[str, Any]]): Decoded structural analytics map.
        refactored_code (Optional[str]): Complete logic optimization code string.
        readme_content (Optional[str]): Renderable markdown project summary text block.
    """
    if (
        analysis
    ):  # if the code was analyzed succesfully, try and get the language and extension. defaults are python and .py if it fails
        language = analysis.get("language", "python")
        extension = analysis.get("extension", ".py")
    else:  # if the code was not analyzed set the language and extension to python and .py
        language = "python"
        extension = ".py"

    _render_complexity_section(analysis)
    _render_flaws_section(analysis)
    _render_suggestions_section(analysis)
    _render_refactored_code_section(refactored_code, language=language)
    _render_readme_section(readme_content)
    _render_download_buttons(refactored_code, readme_content, extension=extension)


def analyze(user_input: str) -> None:
    """run the analysis
    Args:
        user_input (str): Target text block pulled from active browser text area frame.
    """
    if not user_input.strip():  # if the user inputs a blank string
        st.warning("Please provide valid code input before running diagnostics.")
        return

    try:  # attempt to run the analyzer
        with st.spinner(
            "Analyzing, refactoring, and documenting code..."
        ):  # "loading" analyzis
            combined_results = analyze_and_process_code(user_input)  # run the analyzer

            if not combined_results.get(
                "is_valid_code", True
            ):  # if the ai returns that the provided input was not valid code or if there was an error, abort
                st.session_state.analysis_results = {
                    "analysis": combined_results,
                    "refactored_code": "Error: Input does not appear to be valid source code. Refactoring aborted.",  # noqa: E501
                    "readme_content": "Error: Cannot generate documentation for invalid source code.",  # noqa: E501
                }
                return
            # set the state of the analysis so that it doesnt reset on button press
            st.session_state.analysis_results = {
                "analysis": combined_results,
                "refactored_code": combined_results.get("refactored_code", ""),
                "readme_content": combined_results.get("readme_content", ""),
            }

    except Exception as error:  # in the event of any errors report an error
        st.error(f"Analysis failed:\n{error}")


def main() -> None:
    """Build structure of the website."""
    # sets up the bones of the website
    _set_page_config()
    _hide_streamlit_buttons()
    st_navbar(
        ["About"],
        "Home",
        logo_path="Images/logo-cascadia.svg",
        logo_page="Home",
        urls={"About": "https://github.com/Arcerite/CAM_CODING_PROFILER"},
        styles=get_navbar_styles(),
        options=get_navbar_options(),
        adjust=False,
    )

    load_dotenv()
    _initialize_session_state()

    col1, col2 = st.columns(2)  # seperate the website into two sections
    # in the left section have the source code portion
    with col1:
        st.subheader("Source Code")
        user_input = st.text_area(
            "Source Code",
            max_chars=MAX_CODE_LENGTH,
            height=600,
            placeholder="Paste code here...",
            label_visibility="collapsed",
        )

        analyze_button = st.button(
            "Analyze & Refactor",
            type="primary",
            use_container_width=True,
        )
    # in the right section have all the widgets
    with col2:
        st.markdown(
            "<h3 style='text-align: center;'> Results</h3>",
            unsafe_allow_html=True,
        )
        if analyze_button:
            analyze(user_input)

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
