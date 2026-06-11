import ast

import streamlit as st
from dotenv import load_dotenv

from analyzer import analyze_code, generate_readme, refactor_code

load_dotenv()

st.set_page_config(
    page_title="AI Code Profiler",
    page_icon="🚀",
    layout="wide",
)

st.title("🚀 AI-Powered Code Profiler")

st.markdown("""
Analyze Python code for:
- Big-O complexity
- Performance issues
- Security concerns
- Refactoring opportunities
- PEP 8 compliance
""")

# --- Initialize Session State ---
# This ensures our results survive a rerun triggered by download buttons
if "analysis_results" not in st.session_state:
    st.session_state.analysis_results = None

col1, col2 = st.columns(2)

with col1:
    st.subheader("Source Code")
    user_input = st.text_area(
        "Paste Python code here:",
        height=500,
        placeholder="def my_function(items):\n    for item in items:\n        print(item)", # noqa: E501
    )

    analyze_button = st.button(
        "Analyze & Refactor",
        type="primary",
        use_container_width=True,
    )


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


def render_analysis_ui(analysis: dict, refactored_code: str, readme_content: str):
    # =========================
    # Complexity
    # =========================
    big_o = analysis.get("big_o", {})
    st.info(f"""Time Complexity: {big_o.get("time", "Unknown")}
            Space Complexity: {big_o.get("space", "Unknown")}""")

    with st.expander(
        "Complexity Explanation",
        expanded=True,
    ):
        st.write(
            big_o.get(
                "explanation",
                "No explanation provided.",
            )
        )

    # =========================
    # Flaws
    # =========================

    with st.expander(
        "Identified Flaws",
        expanded=True,
    ):
        flaws = analysis.get("flaws", [])

        if flaws:
            for flaw in flaws:
                st.write(f"- {flaw}")
        else:
            st.success("No major flaws detected.")

    # =========================
    # Suggestions
    # =========================

    with st.expander(
        "Suggestions",
        expanded=True,
    ): # noqa: E501
        suggestions = analysis.get(
            "suggestions",
            [],
        )

        if suggestions:
            for suggestion in suggestions:
                st.write(f"- {suggestion}")
        else:
            st.success("No suggestions generated.")

    # =========================
    # Refactored Code
    # =========================

    st.markdown("### Refactored Code")

    st.code(
        refactored_code,
        language="python",
    )

    # =========================
    # README
    # =========================

    with st.expander(
        "Generated README",
        expanded=False,
    ):
        st.markdown(readme_content)

    # =========================
    # Downloads
    # =========================

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

            # Save the raw outputs into session state
            st.session_state.analysis_results = {
                "analysis": analysis,
                "refactored_code": refactored_code,
                "readme_content": readme_content,
            }

    except Exception as error:
        st.error(f"Analysis failed:\n{error}")


with col2:
    st.subheader("Results")

    # 1. If they hit the button, run the processing and save to session state
    if analyze_button:
        analyze(user_input)

    # 2. Check if we have saved results in session state to render (regardless of reruns) # noqa: E501
    if st.session_state.analysis_results is not None:
        results = st.session_state.analysis_results
        render_analysis_ui(
            analysis=results["analysis"],
            refactored_code=results["refactored_code"],
            readme_content=results["readme_content"],
        )
    else:
        st.write("Results will appear here after analysis.")
