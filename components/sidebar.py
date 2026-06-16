import streamlit as st


def render_sidebar_block(title: str, items: list[str]) -> None:
    st.sidebar.markdown(f"#### {title}")
    for item in items:
        st.sidebar.write(f"- {item}")
