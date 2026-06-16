import streamlit as st

from components.forms import form_header
from components.tables import render_table
from services.company_service import (
    create_company,
    create_company_subrole,
    list_companies,
    list_company_subroles,
    update_company,
    delete_company,
    update_company_subrole,
    delete_company_subrole,
)


def render_companies_admin() -> None:
    st.title("Admin - Empresas")

    with st.expander("Crear empresa", expanded=True):
        form_header("Crear empresa")
        with st.form("create_company_form", clear_on_submit=True):
            company_name = st.text_input("Nombre empresa")
            company_slug = st.text_input("Slug (opcional)")
            submitted_company = st.form_submit_button("Crear empresa")

    if submitted_company:
        if create_company(company_name, company_slug):
            st.success("Empresa creada.")
            st.rerun()
        else:
            st.error("No se pudo crear la empresa (puede existir ya).")

    companies = list_companies()
    render_table("Listado de empresas", companies)

    # EDITAR EMPRESAS
    if companies:
        with st.expander("Editar empresa", expanded=False):
            st.markdown("### ✏️ Editar empresa")
            company_map = {f"{c['id']} - {c['name']}": c["id"] for c in companies}
            selected_company_key = st.selectbox("Selecciona empresa para editar", list(company_map.keys()), key="edit_company")
            
            if selected_company_key:
                company_id = company_map[selected_company_key]
                company = next((c for c in companies if c['id'] == company_id), None)
                
                if company:
                    with st.form("edit_company_form"):
                        new_name = st.text_input("Nombre", value=company['name'] or "")
                        new_slug = st.text_input("Slug", value=company['slug'] or "")
                        
                        submitted = st.form_submit_button("💾 Guardar cambios")
                        
                        if submitted:
                            updates = {}
                            if new_name and new_name != company['name']:
                                updates['name'] = new_name
                            if new_slug and new_slug != company['slug']:
                                updates['slug'] = new_slug
                            
                            if updates:
                                if update_company(company_id, **updates):
                                    st.success("✅ Empresa actualizada")
                                    st.rerun()
                                else:
                                    st.error("Error al actualizar empresa")
                            else:
                                st.info("No hay cambios para guardar")
    
    # ELIMINAR EMPRESAS
    if companies:
        with st.expander("Eliminar empresa", expanded=False):
            st.markdown("### 🗑️ Eliminar empresa")
            st.warning("⚠️ Esta acción es irreversible y eliminará todos los subroles asociados")
            
            company_map_delete = {f"{c['id']} - {c['name']}": c["id"] for c in companies}
            selected_company_key_del = st.selectbox("Selecciona empresa para eliminar", list(company_map_delete.keys()), key="delete_company")
            
            if selected_company_key_del:
                company_id = company_map_delete[selected_company_key_del]
                company_name = next((c['name'] for c in companies if c['id'] == company_id), "")
                
                if st.button(f"🗑️ Confirmar eliminación de '{company_name}'", key=f"del_company_{company_id}", type="secondary"):
                    if delete_company(company_id):
                        st.success("✅ Empresa eliminada")
                        st.rerun()
                    else:
                        st.error("Error al eliminar empresa")

    if companies:
        company_map = {f"{c['id']} - {c['name']}": c["id"] for c in companies}
        selected_company_key = st.selectbox("Empresa para subrol", list(company_map.keys()), key="select_company_subrole")
        selected_company_id = company_map[selected_company_key]

        with st.expander("Crear subrol de empresa", expanded=False):
            form_header("Crear subrol de empresa")
            with st.form("create_subrole_form", clear_on_submit=True):
                subrole_name = st.text_input("Nombre subrol")
                subrole_description = st.text_input("Descripcion subrol")
                submitted_subrole = st.form_submit_button("Crear subrol")

            if submitted_subrole:
                if create_company_subrole(selected_company_id, subrole_name, subrole_description):
                    st.success("Subrol creado.")
                    st.rerun()
                else:
                    st.error("No se pudo crear el subrol (puede existir ya).")

        subroles = list_company_subroles(selected_company_id)
        render_table(
            "Subroles de la empresa seleccionada",
            subroles,
        )
        
        # EDITAR SUBROLES
        if subroles:
            with st.expander("Editar subrol", expanded=False):
                st.markdown("### ✏️ Editar subrol")
                subrole_map = {f"{s['id']} - {s['name']}": s["id"] for s in subroles}
                selected_subrole_key = st.selectbox("Selecciona subrol para editar", list(subrole_map.keys()), key="edit_subrole")
                
                if selected_subrole_key:
                    subrole_id = subrole_map[selected_subrole_key]
                    subrole = next((s for s in subroles if s['id'] == subrole_id), None)
                    
                    if subrole:
                        with st.form("edit_subrole_form"):
                            new_name = st.text_input("Nombre", value=subrole['name'] or "")
                            new_description = st.text_input("Descripción", value=subrole['description'] or "")
                            
                            submitted = st.form_submit_button("💾 Guardar cambios")
                            
                            if submitted:
                                updates = {}
                                if new_name and new_name != subrole['name']:
                                    updates['name'] = new_name
                                if new_description and new_description != subrole['description']:
                                    updates['description'] = new_description
                                
                                if updates:
                                    if update_company_subrole(subrole_id, **updates):
                                        st.success("✅ Subrol actualizado")
                                        st.rerun()
                                    else:
                                        st.error("Error al actualizar subrol")
                                else:
                                    st.info("No hay cambios para guardar")
        
        # ELIMINAR SUBROLES
        if subroles:
            with st.expander("Eliminar subrol", expanded=False):
                st.markdown("### 🗑️ Eliminar subrol")
                st.warning("⚠️ Esta acción es irreversible")
                
                subrole_map_delete = {f"{s['id']} - {s['name']}": s["id"] for s in subroles}
                selected_subrole_key_del = st.selectbox("Selecciona subrol para eliminar", list(subrole_map_delete.keys()), key="delete_subrole")
                
                if selected_subrole_key_del:
                    subrole_id = subrole_map_delete[selected_subrole_key_del]
                    subrole_name = next((s['name'] for s in subroles if s['id'] == subrole_id), "")
                    
                    if st.button(f"🗑️ Confirmar eliminación de '{subrole_name}'", key=f"del_subrole_{subrole_id}", type="secondary"):
                        if delete_company_subrole(subrole_id):
                            st.success("✅ Subrol eliminado")
                            st.rerun()
                        else:
                            st.error("Error al eliminar subrol")
