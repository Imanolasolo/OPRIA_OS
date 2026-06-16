import streamlit as st


SESSION_USER_KEY = "opria_current_user"


def set_current_user(user: dict) -> None:
    st.session_state[SESSION_USER_KEY] = user


def get_current_user() -> dict:
    return st.session_state.get(SESSION_USER_KEY, {})


def is_authenticated() -> bool:
    return bool(st.session_state.get(SESSION_USER_KEY))


def clear_session() -> None:
    if SESSION_USER_KEY in st.session_state:
        del st.session_state[SESSION_USER_KEY]
