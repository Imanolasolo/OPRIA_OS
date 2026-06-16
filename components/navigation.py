import streamlit as st


def render_top_navigation(current_title: str) -> None:
    st.markdown(f"### {current_title}")
