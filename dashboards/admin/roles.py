import streamlit as st

from components.forms import form_header
from components.tables import render_table
from services.role_service import create_role, list_roles, update_role, delete_role, get_role_by_id


def render_roles_admin() -> None:
    st.title("Admin - Roles")

    with st.expander("Crear rol", expanded=True):
        form_header("Crear rol")
        with st.form("create_role_form", clear_on_submit=True):
            name = st.text_input("Nombre")
            description = st.text_input("Descripcion")
            submitted = st.form_submit_button("Crear")

    if submitted:
        if create_role(name, description):
            st.success("Rol creado.")
            st.rerun()
        else:
            st.error("No se pudo crear el rol (puede existir ya o nombre vacio).")

    roles = list_roles()
    render_table("Listado de roles", roles)
    
    # EDITAR ROLES
    if roles:
        with st.expander("Editar rol", expanded=False):
            st.markdown("### ✏️ Editar rol")
            role_map = {f"{r['id']} - {r['name']}": r["id"] for r in roles}
            selected_role_key = st.selectbox("Selecciona rol para editar", list(role_map.keys()), key="edit_role")
            
            if selected_role_key:
                role_id = role_map[selected_role_key]
                role = get_role_by_id(role_id)
                
                if role:
                    with st.form("edit_role_form"):
                        new_name = st.text_input("Nombre", value=role['name'] or "")
                        new_description = st.text_input("Descripción", value=role['description'] or "")
                        
                        submitted = st.form_submit_button("💾 Guardar cambios")
                        
                        if submitted:
                            updates = {}
                            if new_name and new_name != role['name']:
                                updates['name'] = new_name
                            if new_description and new_description != role['description']:
                                updates['description'] = new_description
                            
                            if updates:
                                if update_role(role_id, **updates):
                                    st.success("✅ Rol actualizado")
                                    st.rerun()
                                else:
                                    st.error("Error al actualizar rol")
                            else:
                                st.info("No hay cambios para guardar")
    
    # ELIMINAR ROLES
    if roles:
        with st.expander("Eliminar rol", expanded=False):
            st.markdown("### 🗑️ Eliminar rol")
            st.warning("⚠️ Esta acción es irreversible")
            
            role_map_delete = {f"{r['id']} - {r['name']}": r["id"] for r in roles}
            selected_role_key_del = st.selectbox("Selecciona rol para eliminar", list(role_map_delete.keys()), key="delete_role")
            
            if selected_role_key_del:
                role_id = role_map_delete[selected_role_key_del]
                
                if st.button("🗑️ Confirmar eliminación", key=f"del_role_{role_id}", type="secondary"):
                    if delete_role(role_id):
                        st.success("✅ Rol eliminado")
                        st.rerun()
                    else:
                        st.error("Error al eliminar rol")
