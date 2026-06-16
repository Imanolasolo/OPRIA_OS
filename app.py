import streamlit as st

from auth.session import clear_session, get_current_user, is_authenticated, set_current_user
from dashboards.admin.companies import render_companies_admin
from dashboards.admin.processes import render_processes_admin
from dashboards.admin.roles import render_roles_admin
from dashboards.admin.users import render_users_admin
from dashboards.main_dashboard import render_main_dashboard
from dashboards.personal_processes import render_personal_processes
from dashboards import sales_reports
from database.init_db import ensure_database
from services.user_service import authenticate_user
from services.company_service import get_company_id_by_name


def _load_css() -> None:
	try:
		with open("assets/styles.css", "r", encoding="utf-8") as css_file:
			st.markdown(f"<style>{css_file.read()}</style>", unsafe_allow_html=True)
	except FileNotFoundError:
		pass


def _render_login() -> None:
	st.markdown(
		"""
<h1>
  OPR<span style='color:#d32f2f;'>IA</span>
  <span style='color:#1565c0;'>OS</span>
</h1>
		""",
		unsafe_allow_html=True,
	)
	st.caption("MVP - Panel operativo")

	col_about, col_login, col_help = st.columns([1, 1, 1])

	with col_login:
		with st.form("login_form", clear_on_submit=False):
			username = st.text_input("Usuario")
			password = st.text_input("Password", type="password")
			submitted = st.form_submit_button("Entrar")

	with col_about:
		with st.expander("¿Qué es OPRIA?", expanded=True):
			st.markdown(
				"""
**OPRIA es una plataforma inteligente de operación empresarial que conecta personas, procesos y tecnología para ayudar a las empresas a crecer y operar mejor.**

Identifica oportunidades de mejora, digitaliza procesos, automatiza tareas repetitivas y transforma la información de la empresa en decisiones más rápidas y eficientes.

Con OPRIA puedes gestionar usuarios, equipos, procesos, indicadores y flujos de trabajo desde un único entorno adaptable a las necesidades de cada organización.

**Menos tareas manuales. Más control. Mejores decisiones.**
				"""
			)

	with col_help:
		with st.expander("Instrucciones básicas de manejo", expanded=False):
			st.markdown(
				"""
1. Inicia sesión con tu usuario y contraseña.
2. Revisa el Dashboard para ver el resumen de usuarios, roles y procesos.
3. Si tienes rol admin, usa el menú lateral para entrar a módulos de administración.
4. En Admin Usuarios puedes crear cuentas y asignar roles.
5. En Admin Roles puedes crear nuevos perfiles de acceso.
6. En Admin Procesos puedes registrar procesos y actualizar su estado.
7. Usa Cerrar sesión al finalizar para proteger tu acceso.
				"""
			)

	if submitted:
		user = authenticate_user(username, password)
		if user:
			set_current_user(user)
			st.success("Sesion iniciada.")
			st.rerun()
		else:
			st.error("Credenciales invalidas.")

	st.info("Usuario inicial: admin | Password: Admin123!")


def _render_sidebar() -> str:
	current_user = get_current_user()
	st.sidebar.subheader("Sesion")
	st.sidebar.write(f"Usuario: {current_user.get('username', '-')}")
	st.sidebar.write(f"Roles: {', '.join(current_user.get('roles', [])) or '-'}")
	st.sidebar.write(f"Empresas: {', '.join(current_user.get('companies', [])) or '-'}")
	st.sidebar.write(f"Subroles: {', '.join(current_user.get('subroles', [])) or '-'}")

	is_admin = "admin" in current_user.get("roles", [])
	options = ["Dashboard"]
	
	# Reportes de Ventas solo para paneles personales (no admin general)
	companies = current_user.get("companies", [])
	if companies:
		options.append("Mis Procesos")

	if companies and not is_admin:
		options.append("Reportes de Ventas")
	
	if is_admin:
		options.extend(["Admin Empresas", "Admin Usuarios", "Admin Roles", "Admin Procesos"])

	selected = st.sidebar.radio("Navegacion", options)

	# Selector de empresa si hay más de una
	if companies and len(companies) > 1:
		st.sidebar.divider()
		st.sidebar.write("**Empresa actual:**")
		selected_company = st.sidebar.selectbox(
			"Selecciona empresa",
			options=companies,
			label_visibility="collapsed"
		)
		st.session_state["selected_company"] = selected_company
		company_id = get_company_id_by_name(selected_company)
		st.session_state["selected_company_id"] = company_id
	elif companies:
		st.session_state["selected_company"] = companies[0]
		company_id = get_company_id_by_name(companies[0])
		st.session_state["selected_company_id"] = company_id

	if st.sidebar.button("Cerrar sesion"):
		clear_session()
		st.rerun()

	return selected


def main() -> None:
	st.set_page_config(page_title="OPRIA OS", page_icon="OP", layout="wide")
	_load_css()
	ensure_database()

	if not is_authenticated():
		_render_login()
		return

	selected_view = _render_sidebar()

	if selected_view == "Dashboard":
		render_main_dashboard()
	elif selected_view == "Mis Procesos":
		render_personal_processes()
	elif selected_view == "Reportes de Ventas":
		sales_reports.render()
	elif selected_view == "Admin Empresas":
		render_companies_admin()
	elif selected_view == "Admin Usuarios":
		render_users_admin()
	elif selected_view == "Admin Roles":
		render_roles_admin()
	elif selected_view == "Admin Procesos":
		render_processes_admin()


if __name__ == "__main__":
	main()
