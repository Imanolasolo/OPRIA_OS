import streamlit as st

from components.forms import form_header
from components.tables import render_table
from services.company_service import list_companies, list_company_subroles
from services.role_service import list_roles
from services.process_service import (
    VALID_PRIORITIES,
    VALID_STATUS,
    create_process_type,
    create_process,
    grant_process_type_permission,
    list_process_type_permissions,
    list_process_types,
    list_processes,
    update_process_status,
    update_process,
    delete_process,
    get_process_by_id,
)


def render_processes_admin() -> None:
    st.title("Admin - Procesos")

    tab_new, tab_legacy = st.tabs(["Workflow por Tipo (nuevo)", "Procesos legacy"])

    with tab_new:
        companies = list_companies()
        roles = list_roles()
        process_types = list_process_types()

        with st.expander("Crear tipo de proceso", expanded=True):
            form_header("Tipo de proceso", "Define la plantilla reusable del proceso")
            with st.form("create_process_type_form", clear_on_submit=True):
                p_name = st.text_input("Nombre del tipo")
                p_description = st.text_input("Descripción")
                p_category = st.text_input("Categoría", value="general")
                p_version = st.number_input("Versión", min_value=1, value=1, step=1)
                submitted_type = st.form_submit_button("Crear tipo")

            if submitted_type:
                if create_process_type(
                    name=p_name,
                    description=p_description,
                    category=p_category,
                    version=int(p_version),
                ):
                    st.success("Tipo de proceso creado.")
                    st.rerun()
                else:
                    st.error("No se pudo crear el tipo (revisa nombre/version).")

        render_table("Tipos de proceso", process_types)

        if process_types and companies:
            with st.expander("Asignar permisos por empresa/rol/subrol", expanded=False):
                st.caption("Regla: rol/subrol en 'Todos' aplica de forma global dentro de la empresa.")

                process_type_map = {f"{p['id']} - {p['name']} v{p['version']}": p["id"] for p in process_types}
                company_map = {f"{c['id']} - {c['name']}": c["id"] for c in companies}
                role_map = {"Todos": None}
                role_map.update({f"{r['id']} - {r['name']}": r["id"] for r in roles})

                col1, col2 = st.columns(2)
                selected_process_type_key = col1.selectbox("Tipo de proceso", list(process_type_map.keys()))
                selected_company_key = col2.selectbox("Empresa", list(company_map.keys()))

                selected_company_id = company_map[selected_company_key]
                subroles = list_company_subroles(selected_company_id)
                subrole_map = {"Todos": None}
                subrole_map.update({f"{s['id']} - {s['name']}": s["id"] for s in subroles})

                col3, col4 = st.columns(2)
                selected_role_key = col3.selectbox("Rol", list(role_map.keys()))
                selected_subrole_key = col4.selectbox("Subrol", list(subrole_map.keys()))

                col5, col6, col7 = st.columns(3)
                can_create = col5.checkbox("Puede crear", value=True)
                can_validate = col6.checkbox("Puede validar", value=False)
                can_close = col7.checkbox("Puede cerrar", value=False)

                if st.button("Guardar permiso"):
                    if grant_process_type_permission(
                        process_type_id=process_type_map[selected_process_type_key],
                        company_id=selected_company_id,
                        role_id=role_map[selected_role_key],
                        subrole_id=subrole_map[selected_subrole_key],
                        can_create=can_create,
                        can_validate=can_validate,
                        can_close=can_close,
                    ):
                        st.success("Permiso guardado correctamente.")
                        st.rerun()
                    else:
                        st.error("No se pudo guardar el permiso.")

        permissions = list_process_type_permissions()
        render_table("Permisos configurados", permissions)

    with tab_legacy:
        with st.expander("Crear proceso", expanded=True):
            form_header("Crear proceso")
            with st.form("create_process_form", clear_on_submit=True):
                name = st.text_input("Nombre")
                owner = st.text_input("Owner")
                status = st.selectbox("Estado", VALID_STATUS, index=0)
                priority = st.selectbox("Prioridad", VALID_PRIORITIES, index=1)
                submitted = st.form_submit_button("Crear")

        if submitted:
            if create_process(name, owner, status, priority):
                st.success("Proceso creado.")
                st.rerun()
            else:
                st.error("No se pudo crear el proceso.")

        processes = list_processes()
        render_table("Listado de procesos", processes)

        if processes:
            with st.expander("Cambiar estado", expanded=False):
                st.markdown("#### Cambiar estado")
                process_map = {f"{p['id']} - {p['name']}": p["id"] for p in processes}
                col1, col2 = st.columns(2)
                selected_process = col1.selectbox("Proceso", list(process_map.keys()))
                new_status = col2.selectbox("Nuevo estado", VALID_STATUS)

                if st.button("Actualizar estado"):
                    if update_process_status(process_map[selected_process], new_status):
                        st.success("Estado actualizado.")
                        st.rerun()
                    else:
                        st.error("No se pudo actualizar estado.")

        if processes:
            with st.expander("Editar proceso", expanded=False):
                st.markdown("### ✏️ Editar proceso")
                process_map = {f"{p['id']} - {p['name']}": p["id"] for p in processes}
                selected_process_key = st.selectbox("Selecciona proceso para editar", list(process_map.keys()), key="edit_process")

                if selected_process_key:
                    process_id = process_map[selected_process_key]
                    process = get_process_by_id(process_id)

                    if process:
                        with st.form("edit_process_form"):
                            new_name = st.text_input("Nombre", value=process['name'] or "")
                            new_owner = st.text_input("Owner", value=process['owner'] or "")
                            new_status = st.selectbox("Estado", VALID_STATUS, index=VALID_STATUS.index(process['status']))
                            new_priority = st.selectbox("Prioridad", VALID_PRIORITIES, index=VALID_PRIORITIES.index(process['priority']))

                            submitted_edit = st.form_submit_button("💾 Guardar cambios")

                            if submitted_edit:
                                updates = {}
                                if new_name and new_name != process['name']:
                                    updates['name'] = new_name
                                if new_owner and new_owner != process['owner']:
                                    updates['owner'] = new_owner
                                if new_status != process['status']:
                                    updates['status'] = new_status
                                if new_priority != process['priority']:
                                    updates['priority'] = new_priority

                                if updates:
                                    if update_process(process_id, **updates):
                                        st.success("✅ Proceso actualizado")
                                        st.rerun()
                                    else:
                                        st.error("Error al actualizar proceso")
                                else:
                                    st.info("No hay cambios para guardar")

        if processes:
            with st.expander("Eliminar proceso", expanded=False):
                st.markdown("### 🗑️ Eliminar proceso")
                st.warning("⚠️ Esta acción es irreversible")

                process_map_delete = {f"{p['id']} - {p['name']}": p["id"] for p in processes}
                selected_process_key_del = st.selectbox("Selecciona proceso para eliminar", list(process_map_delete.keys()), key="delete_process")

                if selected_process_key_del:
                    process_id = process_map_delete[selected_process_key_del]

                    if st.button("🗑️ Confirmar eliminación", key=f"del_process_{process_id}", type="secondary"):
                        if delete_process(process_id):
                            st.success("✅ Proceso eliminado")
                            st.rerun()
                        else:
                            st.error("Error al eliminar proceso")
