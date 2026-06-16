import streamlit as st

from components.forms import form_header
from components.tables import render_table
from services.company_service import (
    assign_subrole_to_user,
    list_companies,
    list_company_subroles,
)
from services.role_service import assign_role, list_roles
from services.user_service import create_user, list_users, update_user, delete_user, get_user_by_id
from utils.validators import is_valid_email, is_valid_password, is_valid_username


def render_users_admin() -> None:
    st.title("Admin - Usuarios")

    companies = list_companies()
    company_map = {f"{c['id']} - {c['name']}": c["id"] for c in companies}

    with st.expander("Crear usuario", expanded=True):
        form_header("Crear usuario", "Campos basicos para alta")
        with st.form("create_user_form", clear_on_submit=True):
            username = st.text_input("Username")
            email = st.text_input("Email")
            full_name = st.text_input("Nombre completo")
            password = st.text_input("Password", type="password")
            selected_company_key = st.selectbox(
                "Empresa",
                ["Sin empresa"] + list(company_map.keys()),
            )

            selected_company_id = None
            selected_subrole_id = None
            is_company_admin = False

            if selected_company_key != "Sin empresa":
                selected_company_id = company_map[selected_company_key]
                subroles = list_company_subroles(selected_company_id)
                subrole_map = {f"{s['id']} - {s['name']}": s["id"] for s in subroles}

                if subrole_map:
                    selected_subrole_key = st.selectbox(
                        "Subrol empresa",
                        ["Sin subrol"] + list(subrole_map.keys()),
                    )
                    if selected_subrole_key != "Sin subrol":
                        selected_subrole_id = subrole_map[selected_subrole_key]

                is_company_admin = st.checkbox("Administrador de la empresa", value=False)

            submitted = st.form_submit_button("Crear")

    if submitted:
        if not is_valid_username(username):
            st.error("Username invalido.")
        elif email and not is_valid_email(email):
            st.error("Email invalido.")
        elif not is_valid_password(password):
            st.error("Password debil. Usa 8+ caracteres con mayuscula, minuscula y numero.")
        elif create_user(
            username,
            email,
            full_name,
            password,
            company_id=selected_company_id,
            subrole_id=selected_subrole_id,
            is_company_admin=is_company_admin,
        ):
            st.success("Usuario creado.")
        else:
            st.error("No se pudo crear el usuario (puede existir ya).")

    users = list_users()
    render_table("Listado de usuarios", users)

    if users:
        with st.expander("Asignar rol", expanded=False):
            st.markdown("#### Asignar rol")
            role_options = list_roles()
            if role_options:
                user_map = {f"{u['id']} - {u['username']}": u["id"] for u in users}
                role_map = {f"{r['id']} - {r['name']}": r["id"] for r in role_options}

                col1, col2 = st.columns(2)
                selected_user = col1.selectbox("Usuario", list(user_map.keys()))
                selected_role = col2.selectbox("Rol", list(role_map.keys()))
                if st.button("Asignar"):
                    if assign_role(user_map[selected_user], role_map[selected_role]):
                        st.success("Rol asignado.")
                    else:
                        st.error("No se pudo asignar rol.")

    if users and companies:
        with st.expander("Asignar subrol por empresa", expanded=False):
            st.markdown("#### Asignar subrol por empresa")
            user_map = {f"{u['id']} - {u['username']}": u["id"] for u in users}
            company_map = {f"{c['id']} - {c['name']}": c["id"] for c in companies}

            col1, col2, col3 = st.columns(3)
            selected_user_key = col1.selectbox("Usuario para subrol", list(user_map.keys()))
            selected_company_key = col2.selectbox("Empresa para subrol", list(company_map.keys()))

            selected_company_id = company_map[selected_company_key]
            subroles = list_company_subroles(selected_company_id)
            subrole_map = {f"{s['id']} - {s['name']}": s["id"] for s in subroles}

            if subrole_map:
                selected_subrole_key = col3.selectbox("Subrol", list(subrole_map.keys()))
                if st.button("Asignar subrol"):
                    if assign_subrole_to_user(
                        user_map[selected_user_key],
                        selected_company_id,
                        subrole_map[selected_subrole_key],
                    ):
                        st.success("Subrol asignado correctamente.")
                    else:
                        st.error("No se pudo asignar el subrol.")
            else:
                st.info("La empresa seleccionada no tiene subroles registrados.")

    # EDITAR USUARIOS
    if users:
        with st.expander("Editar usuario", expanded=False):
            st.markdown("### ✏️ Editar usuario")
            user_map = {f"{u['id']} - {u['username']}": u["id"] for u in users}
            selected_user_key = st.selectbox("Selecciona usuario para editar", list(user_map.keys()), key="edit_user")

            if selected_user_key:
                user_id = user_map[selected_user_key]
                user = get_user_by_id(user_id)

                if user:
                    with st.form("edit_user_form"):
                        new_email = st.text_input("Email", value=user['email'] or "")
                        new_full_name = st.text_input("Nombre completo", value=user['full_name'] or "")
                        new_password = st.text_input("Nueva contraseña (dejar vacío para no cambiar)", type="password")
                        new_is_active = st.checkbox("Activo", value=bool(user['is_active']))

                        submitted = st.form_submit_button("💾 Guardar cambios")

                        if submitted:
                            updates = {}
                            if new_email and new_email != user['email']:
                                if is_valid_email(new_email):
                                    updates['email'] = new_email
                                else:
                                    st.error("Email inválido")
                                    submitted = False

                            if new_full_name and new_full_name != user['full_name']:
                                updates['full_name'] = new_full_name

                            if new_password:
                                if is_valid_password(new_password):
                                    updates['password'] = new_password
                                else:
                                    st.error("Contraseña débil. Usa 8+ caracteres")
                                    submitted = False

                            if new_is_active != user['is_active']:
                                updates['is_active'] = 1 if new_is_active else 0

                            if submitted and updates:
                                if update_user(user_id, **updates):
                                    st.success("✅ Usuario actualizado")
                                    st.rerun()
                                else:
                                    st.error("Error al actualizar usuario")
                            elif submitted:
                                st.info("No hay cambios para guardar")
    
    # ELIMINAR USUARIOS
    if users:
        with st.expander("Eliminar usuario", expanded=False):
            st.markdown("### 🗑️ Eliminar usuario")
            st.warning("⚠️ Esta acción es irreversible")

            user_map_delete = {f"{u['id']} - {u['username']}": u["id"] for u in users}
            selected_user_key_del = st.selectbox("Selecciona usuario para eliminar", list(user_map_delete.keys()), key="delete_user")

            if selected_user_key_del:
                user_id = user_map_delete[selected_user_key_del]

                col1, col2 = st.columns(2)
                with col1:
                    if st.button("🗑️ Confirmar eliminación", key=f"del_user_{user_id}", type="secondary"):
                        if delete_user(user_id):
                            st.success("✅ Usuario eliminado")
                            st.rerun()
                        else:
                            st.error("Error al eliminar usuario")
