from __future__ import annotations

import ast
from typing import Optional

import streamlit as st
from dotenv import load_dotenv
from streamlit_navigation_bar import st_navbar

from analyzer import analyze_code, generate_readme, refactor_code

st.set_page_config(
    page_title="Code Buddy",
    page_icon="Images/smile_icon.png",
    layout="wide",
    initial_sidebar_state="collapsed",
)

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

styles = {
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

options = {"show_menu": False, "show_sidebar": False, "hide_nav": True}

page = st_navbar(
    ["About"],
    "Home",
    logo_path="Images/logo2.svg",
    logo_page="Home",
    urls={"About": "https://github.com/Arcerite/CAM_CODING_PROFILER"},
    styles=styles,
    options=options,
    adjust=False,
)

if page == "About":
    st.switch_page("pages/about.py")
elif page == "Home":
    pass

st.write()

load_dotenv()


def validate_user_input(user_input: str) -> bool:
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


def render_analysis_ui(
    analysis: Optional[dict] = None,
    refactored_code: Optional[str] = None,
    readme_content: Optional[str] = None,
):
    # Complexity
    with st.expander(
        "**Complexity**",
        expanded=True,
    ):
        if analysis is None:
            st.write("Please run the code analysis to find the complexity.")
        else:
            big_o = analysis.get("big_o", {})
            st.write(
                f"Time Complexity: {big_o.get("time", "Unknown")}  \n",
                f"Space Complexity: {big_o.get("space", "Unknown")}  \n\n",
                big_o.get(
                    "explanation",
                    "No explanation provided.",
                ),
            )

    # Flaws
    with st.expander(
        "**Identified Flaws**",
        expanded=False,
    ):
        if analysis is None:
            st.write("Please run the code analysis to find flaws.")
        else:
            flaws = analysis.get("flaws", [])

            if flaws:
                for flaw in flaws:
                    st.write(f"- {flaw}")
            else:
                st.success("No major flaws detected.")

    # Suggestions
    with st.expander(
        "**Suggestions**",
        expanded=False,
    ):
        if analysis is None:
            st.write("Please run the code analysis to find suggestions.")
        else:
            suggestions = analysis.get(
                "suggestions",
                [],
            )

            if suggestions:
                for suggestion in suggestions:
                    st.write(f"- {suggestion}")
            else:
                st.success("No suggestions generated.")

    # Refactored Code
    with st.expander(
        "**Refactored Code**",
        expanded=False,
    ):
        if refactored_code is None:
            st.write("Please run the code analysis to get refactored code.")
        else:
            st.code(
                refactored_code,
                language="python",
            )

    # README
    with st.expander(
        "**Generated README**",
        expanded=False,
    ):
        if readme_content is None:
            st.write("Please run the code analysis to get the generated README.")
        else:
            st.markdown(readme_content)

    # Downloads
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


def analyze(user_input: str):
    if not validate_user_input(user_input):
        return

    try:
        with st.spinner("Analyzing code..."):
            analysis = analyze_code(user_input)
            refactored_code = refactor_code(user_input)
            readme_content = generate_readme(user_input)
        render_analysis_ui(analysis, refactored_code, readme_content)

    except Exception as error:
        st.error(f"Analysis failed:\n{error}")


col1, col2 = st.columns(2)

with col1:
    st.subheader("Source Code")
    user_input = st.text_area(
        "Source Code",
        height=600,
        placeholder=("Paste code here..."),
        label_visibility="collapsed",
    )

    analyze_button = st.button(
        "Analyze & Refactor",
        type="primary",
        use_container_width=True,
    )

with col2:
    st.markdown("<h3 style='text-align: center;'> Results</h3>", unsafe_allow_html=True)
    if analyze_button:
        analyze(user_input)
    else:
        render_analysis_ui(None, None, None)
