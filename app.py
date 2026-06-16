from __future__ import annotations

from typing import Optional

import streamlit as st
from dotenv import load_dotenv
from streamlit_navigation_bar import st_navbar

from analyzer import analyze_code, generate_readme, refactor_code
from utils import get_navbar_options, get_navbar_styles


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


def _initialize_session_state() -> None:
    """
    Initialize the session state to store analysis results.
    """
    if "analysis_results" not in st.session_state:
        st.session_state.analysis_results = None


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


def _render_refactored_code_section(
    refactored_code: Optional[str], language: str = "python"
) -> None:
    with st.expander("**Refactored Code**", expanded=False):
        if refactored_code is None:
            st.write("Please run the code analysis to get refactored code.")
        else:
            # Dynamically set syntax highlighting!
            st.code(refactored_code, language=language)


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
    extension: str = ".py",  # Pass the extension dynamically
) -> None:
    if (readme_content is not None) and (refactored_code is not None):
        st.markdown("---")
        d_col1, d_col2 = st.columns(2)
        with d_col1:
            st.download_button(
                label="💾 Download Code",
                data=refactored_code,
                file_name=f"refactored_code{extension}",  # Dynamic extension!
                mime="text/plain",
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
) -> None:
    """
    Render the analysis UI with all sections.
    """
    # 1. Extract the language and extension safely, defaulting to python if analysis is None
    if analysis:
        language = analysis.get("language", "python")
        extension = analysis.get("extension", ".py")
    else:
        language = "python"
        extension = ".py"

    # 2. Pass them into the respective sections
    _render_complexity_section(analysis)
    _render_flaws_section(analysis)
    _render_suggestions_section(analysis)

    # Pass 'language' here so syntax highlighting changes
    _render_refactored_code_section(refactored_code, language=language)

    _render_readme_section(readme_content)

    # Pass 'extension' here so the download button changes!
    _render_download_buttons(refactored_code, readme_content, extension=extension)


def analyze(user_input: str) -> None:
    try:
        with st.spinner("Analyzing code..."):
            # 1. Run the analysis engine first as a gatekeeper
            analysis = analyze_code(user_input)

            # 2. Check if the input is malicious or invalid code
            if not analysis.get("is_valid_code", True):
                st.session_state.analysis_results = {
                    # Keep the analysis so 'Identified Flaws' displays the injection warning
                    "analysis": analysis,
                    "refactored_code": "Error: Input does not appear to be valid source code. Refactoring aborted.",
                    "readme_content": "Error: Cannot generate documentation for invalid source code.",
                }
                return

            # 3. Only run these if the input safely passed validation
            refactored_code = refactor_code(user_input)
            readme_content = generate_readme(user_input)

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
        logo_path="Images/logo-cascadia.svg",
        logo_page="Home",
        urls={"About": "https://github.com/Arcerite/CAM_CODING_PROFILER"},
        styles=get_navbar_styles(),
        options=get_navbar_options(),
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
