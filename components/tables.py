import streamlit as st


def render_table(title: str, data: list[dict]) -> None:
    st.subheader(title)
    if not data:
        st.info("Sin registros.")
        return
    st.dataframe(data, use_container_width=True)
