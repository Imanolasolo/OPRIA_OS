import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from auth.session import get_current_user
from services import sales_report_service
from services.company_service import get_company_id_by_name


def render():
    """Dashboard de reportes de ventas para gerentes de ventas"""
    st.header("📋 Reportes de Ventas de Neumáticos")
    
    # Obtener contexto del usuario
    current_user = get_current_user()
    if not current_user:
        st.error("Usuario no autenticado")
        return
    
    # Obtener empresa actual
    company_id = st.session_state.get("selected_company_id")
    if not company_id:
        # Si no hay empresa seleccionada, usar la primera empresa del usuario
        companies = current_user.get("companies", [])
        if not companies:
            st.warning("No tienes empresas asignadas. Contacta al administrador.")
            return
        
        # Mapear el nombre de empresa a ID
        company_id = get_company_id_by_name(companies[0])
        if not company_id:
            st.error(f"No se encontró la empresa {companies[0]}")
            return
    
    # Tabs principales
    tab1, tab2, tab3, tab4 = st.tabs([
        "📝 Nuevo Reporte",
        "📊 Mis Reportes",
        "✅ Control de Calidad",
        "📈 Análisis Semanal"
    ])
    
    # TAB 1: Crear nuevo reporte
    with tab1:
        st.subheader("Crear nuevo reporte de venta")
        
        col1, col2 = st.columns(2)
        
        with col1:
            report_date = st.date_input(
                "Fecha del reporte",
                value=datetime.now().date(),
                label_visibility="collapsed"
            )
            branch = st.text_input("Sucursal/Punto de venta", placeholder="Ej: Sucursal Centro")
            customer_name = st.text_input("Nombre del cliente", placeholder="Ej: Juan Pérez")
            tire_brand = st.text_input("Marca de neumático", placeholder="Ej: Michelin, Bridgestone, Goodyear")
        
        with col2:
            salesman_name = st.text_input("Nombre del vendedor", placeholder="Tu nombre o del vendedor")
            tire_model = st.text_input("Modelo de neumático", placeholder="Ej: Latitude Tour")
            quantity = st.number_input("Cantidad", min_value=1, value=1, step=1)
            unit_price = st.number_input("Precio unitario", min_value=0.0, value=0.0, step=0.01)
        
        col3, col4 = st.columns(2)
        
        with col3:
            payment_method = st.selectbox(
                "Método de pago",
                ["Efectivo", "Tarjeta débito", "Tarjeta crédito", "Cheque", "Transferencia", "Otro"]
            )
        
        with col4:
            # Total automático
            total_price = quantity * unit_price
            st.metric("Total", f"${total_price:,.2f}")
        
        observations = st.text_area(
            "Observaciones (opcional)",
            placeholder="Ej: Cliente requiere garantía, descuento especial, etc.",
            height=80
        )
        
        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            if st.button("💾 Guardar Reporte", use_container_width=True, type="primary"):
                if not all([report_date, branch, customer_name, tire_brand, salesman_name, tire_model, unit_price]):
                    st.error("Por favor completa todos los campos requeridos")
                else:
                    try:
                        report_id = sales_report_service.create_sales_report(
                            company_id=company_id,
                            user_id=current_user['id'],
                            report_date=str(report_date),
                            branch=branch,
                            salesman_name=salesman_name,
                            customer_name=customer_name,
                            tire_brand=tire_brand,
                            tire_model=tire_model,
                            quantity=int(quantity),
                            unit_price=float(unit_price),
                            payment_method=payment_method,
                            observations=observations
                        )
                        st.success(f"✅ Reporte guardado exitosamente (ID: {report_id})")
                        st.balloons()
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error al guardar: {str(e)}")
        
        with col_btn2:
            if st.button("🔄 Limpiar", use_container_width=True):
                st.rerun()
    
    # TAB 2: Mis reportes
    with tab2:
        st.subheader("Mis reportes de ventas")
        
        # Filtros
        col_filter1, col_filter2 = st.columns(2)
        
        with col_filter1:
            filter_date = st.date_input(
                "Filtrar por fecha",
                value=datetime.now().date(),
                label_visibility="collapsed"
            )
        
        with col_filter2:
            filter_status = st.selectbox(
                "Estado",
                ["Todos", "Pendiente", "Validado", "Rechazado"],
                label_visibility="collapsed"
            )
        
        # Obtener reportes
        status_map = {
            "Pendiente": "pending",
            "Validado": "validated",
            "Rechazado": "rejected"
        }
        
        reports = sales_report_service.list_sales_reports(
            company_id=company_id,
            user_id=current_user['id'],
            date=str(filter_date)
        )
        
        if filter_status != "Todos":
            reports = [r for r in reports if r.status == status_map.get(filter_status)]
        
        if reports:
            # Tabla de reportes
            df_data = []
            for report in reports:
                status_emoji = {
                    "pending": "⏳",
                    "validated": "✅",
                    "rejected": "❌"
                }.get(report.status, "❓")
                
                df_data.append({
                    "ID": report.id,
                    "Fecha": report.report_date,
                    "Sucursal": report.branch,
                    "Cliente": report.customer_name,
                    "Neumático": f"{report.tire_brand} {report.tire_model}",
                    "Cantidad": report.quantity,
                    "Total": f"${report.total_price:,.2f}",
                    "Estado": f"{status_emoji} {report.status}",
                    "Creado": report.created_at[:10]
                })
            
            df = pd.DataFrame(df_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            # Editar/Ver detalles
            st.subheader("Detalles del reporte")
            selected_report_id = st.selectbox(
                "Selecciona un reporte para ver detalles",
                options=[r.id for r in reports],
                format_func=lambda x: f"Reporte #{x}"
            )
            
            if selected_report_id:
                report = next((r for r in reports if r.id == selected_report_id), None)
                if report:
                    col_detail1, col_detail2 = st.columns(2)
                    
                    with col_detail1:
                        st.write(f"**Sucursal:** {report.branch}")
                        st.write(f"**Cliente:** {report.customer_name}")
                        st.write(f"**Vendedor:** {report.salesman_name}")
                        st.write(f"**Método de pago:** {report.payment_method}")
                    
                    with col_detail2:
                        st.write(f"**Marca:** {report.tire_brand}")
                        st.write(f"**Modelo:** {report.tire_model}")
                        st.write(f"**Cantidad:** {report.quantity}")
                        st.write(f"**Total:** ${report.total_price:,.2f}")
                    
                    if report.observations:
                        st.info(f"**Observaciones:** {report.observations}")
                    
                    # Opciones si está pendiente
                    if report.status == "pending":
                        col_act1, col_act2 = st.columns(2)
                        
                        with col_act1:
                            if st.button("✅ Validar", key=f"validate_{report.id}"):
                                sales_report_service.update_sales_report_status(report.id, "validated")
                                st.success("Reporte validado")
                                st.rerun()
                        
                        with col_act2:
                            if st.button("❌ Rechazar", key=f"reject_{report.id}"):
                                sales_report_service.update_sales_report_status(report.id, "rejected")
                                st.warning("Reporte rechazado")
                                st.rerun()
        else:
            st.info("No hay reportes para esta fecha")
    
    # TAB 3: Control de calidad
    with tab3:
        st.subheader("Control de calidad - Resumen diario")
        
        qc_date = st.date_input(
            "Selecciona la fecha",
            value=datetime.now().date(),
            label_visibility="collapsed"
        )
        
        # Obtener resumen del día
        daily_summary = sales_report_service.get_daily_summary(
            company_id=company_id,
            report_date=str(qc_date)
        )
        
        # Métricas
        col_m1, col_m2, col_m3 = st.columns(3)
        
        with col_m1:
            st.metric("Reportes validados", daily_summary['total_reports'])
        
        with col_m2:
            st.metric("Unidades vendidas", int(daily_summary['total_units']))
        
        with col_m3:
            st.metric("Total de ventas", f"${daily_summary['total_sales']:,.2f}")
        
        # Listado de reportes del día
        st.subheader(f"Reportes del {qc_date}")
        
        day_reports = sales_report_service.list_sales_reports(
            company_id=company_id,
            date=str(qc_date)
        )
        
        if day_reports:
            for report in day_reports:
                with st.expander(f"Reporte #{report.id} - {report.customer_name} ({report.status})"):
                    col_r1, col_r2, col_r3 = st.columns(3)
                    
                    with col_r1:
                        st.write(f"**Vendedor:** {report.salesman_name}")
                        st.write(f"**Sucursal:** {report.branch}")
                        st.write(f"**Pago:** {report.payment_method}")
                    
                    with col_r2:
                        st.write(f"**Neumático:** {report.tire_brand} {report.tire_model}")
                        st.write(f"**Cantidad:** {report.quantity}")
                        st.write(f"**P. Unitario:** ${report.unit_price:,.2f}")
                    
                    with col_r3:
                        st.write(f"**Total:** ${report.total_price:,.2f}")
                        st.write(f"**Estado:** {report.status}")
                        st.write(f"**Creado:** {report.created_at}")
        else:
            st.info("No hay reportes para esta fecha")
    
    # TAB 4: Análisis semanal
    with tab4:
        st.subheader("Análisis semanal")
        
        col_week1, col_week2 = st.columns(2)
        
        with col_week1:
            week_start = st.date_input(
                "Fecha de inicio de semana",
                value=(datetime.now() - timedelta(days=7)).date(),
                label_visibility="collapsed"
            )
        
        with col_week2:
            week_end = st.date_input(
                "Fecha de fin de semana",
                value=datetime.now().date(),
                label_visibility="collapsed"
            )
        
        # Obtener resumen semanal
        weekly_summary = sales_report_service.get_weekly_summary(
            company_id=company_id,
            start_date=str(week_start),
            end_date=str(week_end)
        )
        
        if weekly_summary:
            # Tabla de resumen
            df_weekly = pd.DataFrame(weekly_summary)
            df_weekly.columns = ["Fecha", "Reportes", "Unidades", "Total Ventas"]
            df_weekly["Total Ventas"] = df_weekly["Total Ventas"].apply(lambda x: f"${x:,.2f}")
            
            st.dataframe(df_weekly, use_container_width=True, hide_index=True)
            
            # Gráficos
            if len(weekly_summary) > 0:
                st.subheader("Tendencias")
                
                # Preparar datos para gráficos
                dates = [item['date'] for item in weekly_summary]
                units = [item['units'] for item in weekly_summary]
                sales = [item['sales'] for item in weekly_summary]
                
                col_g1, col_g2 = st.columns(2)
                
                with col_g1:
                    st.bar_chart(
                        pd.DataFrame({
                            'Fecha': dates,
                            'Unidades': units
                        }).set_index('Fecha'),
                        y_label="Unidades vendidas"
                    )
                
                with col_g2:
                    st.line_chart(
                        pd.DataFrame({
                            'Fecha': dates,
                            'Ventas': sales
                        }).set_index('Fecha'),
                        y_label="Total de ventas ($)"
                    )
        else:
            st.info("No hay datos disponibles para este período")
