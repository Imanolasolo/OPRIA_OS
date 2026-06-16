import streamlit as st

from components.tables import render_table
from services.process_service import list_processes
from services.role_service import list_roles
from services.user_service import list_users


def render_main_dashboard() -> None:
    st.title("Dashboard Principal")

    users = list_users()
    roles = list_roles()
    processes = list_processes()

    col1, col2, col3 = st.columns(3)
    col1.metric("Usuarios", len(users))
    col2.metric("Roles", len(roles))
    col3.metric("Procesos", len(processes))

    render_table("Ultimos procesos", processes[:10])
