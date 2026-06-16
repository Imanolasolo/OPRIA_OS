import streamlit as st

from auth.session import get_current_user
from components.tables import render_table
from services.process_service import (
    create_process_instance,
    list_available_process_types_for_user,
    list_process_instances,
    list_process_instances_for_validation,
    update_process_instance_status,
)


def render_personal_processes() -> None:
    st.title("Panel Personal - Mis Procesos")

    current_user = get_current_user()
    user_id = current_user.get("id")
    company_id = st.session_state.get("selected_company_id")

    if not user_id:
        st.error("No hay sesión activa.")
        return

    if not company_id:
        st.info("Selecciona una empresa en la barra lateral para continuar.")
        return

    available_types = list_available_process_types_for_user(company_id=company_id, user_id=user_id)

    tab_new, tab_my, tab_validation = st.tabs(["Nuevo proceso", "Mis instancias", "Bandeja de validación"])

    with tab_new:
        creatable = [t for t in available_types if bool(t.get("can_create"))]
        if not creatable:
            st.info("No tienes tipos de proceso habilitados para crear en esta empresa.")
        else:
            type_map = {f"{t['id']} - {t['name']} (v{t['version']})": t["id"] for t in creatable}
            selected_type_key = st.selectbox("Tipo de proceso", list(type_map.keys()))
            notes = st.text_area("Detalle / datos del proceso", height=160)

            if st.button("Crear instancia de proceso", type="primary"):
                payload = {"notes": notes.strip()}
                instance_id = create_process_instance(
                    process_type_id=type_map[selected_type_key],
                    company_id=company_id,
                    user_id=user_id,
                    payload=payload,
                )
                if instance_id:
                    st.success(f"Instancia creada correctamente. ID: {instance_id}")
                    st.rerun()
                else:
                    st.error("No se pudo crear la instancia. Revisa permisos de creación.")

    with tab_my:
        my_instances = list_process_instances(company_id=company_id, user_id=user_id, only_mine=True)
        render_table("Mis instancias de proceso", my_instances)

    with tab_validation:
        reviewable = list_process_instances_for_validation(company_id=company_id, user_id=user_id)
        render_table("Instancias para validar/cerrar", reviewable)

        if reviewable:
            instance_map = {
                f"{item['id']} - {item['process_type']} - {item['status']}": item["id"]
                for item in reviewable
            }
            selected_key = st.selectbox("Selecciona instancia", list(instance_map.keys()))
            target_status = st.selectbox(
                "Nuevo estado",
                ["validated", "rejected", "approved", "closed"],
            )
            comment = st.text_input("Comentario (opcional)")

            if st.button("Aplicar cambio de estado"):
                ok = update_process_instance_status(
                    process_instance_id=instance_map[selected_key],
                    user_id=user_id,
                    company_id=company_id,
                    to_status=target_status,
                    comment=comment,
                )
                if ok:
                    st.success("Estado actualizado correctamente.")
                    st.rerun()
                else:
                    st.error("No se pudo actualizar estado. Revisa permisos y estado objetivo.")
