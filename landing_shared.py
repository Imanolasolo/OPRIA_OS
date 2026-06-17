from __future__ import annotations

from pathlib import Path
from urllib.parse import quote

import streamlit as st


LANDING_CSS_PATH = Path("assets/landing.css")


def load_landing_css() -> None:
    if LANDING_CSS_PATH.exists():
        css = LANDING_CSS_PATH.read_text(encoding="utf-8")
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def render_header_badge(text: str) -> None:
    st.caption(text)


def render_hero(title: str, subtitle: str, description: str) -> None:
    st.subheader(subtitle)
    st.title(title)
    st.write(description)


def render_highlight_cards(items: list[dict[str, str]]) -> None:
    if not items:
        return

    column_count = min(3, len(items))
    columns = st.columns(column_count)

    for index, item in enumerate(items):
        with columns[index % column_count]:
            with st.expander(item["title"], expanded=False):
                st.write(item["text"])


def render_quote(quote: str) -> None:
    st.info(quote)


def render_timeline(steps: list[dict[str, str]]) -> None:
    for step in steps:
        with st.expander(step["step"], expanded=False):
            st.write(step["text"])


def render_footer_cta(title: str, text: str) -> None:
    st.success(f"{title}\n\n{text}")


def render_contact_block() -> None:
    from modules.landing.i18n import tr

    email_address = "jjusturi@gmail.com"
    whatsapp_url = "https://wa.me/593993513082"
    service_message = quote("Hola, quiero información sobre servicios de OPRIA.")
    product_message = quote("Hola, quiero consultar productos o módulos de OPRIA.")
    ambassador_message = quote("Hola, quiero saber cómo puedo convertirme en embajador OPRIA.")

    st.markdown(f"### {tr('contact_title', 'Contacto directo')}")
    st.write(tr('contact_text', 'Escríbeme para servicios, productos o para sumarte como embajador comercial.'))

    col_services, col_products, col_ambassadors = st.columns(3)

    with col_services:
        with st.expander(tr('contact_service_title', 'Servicios'), expanded=False):
            st.write(tr('contact_service_text', 'Consultoría, diagnóstico y acompañamiento para implementar OPRIA.'))
            st.link_button(
                tr('contact_service_label', 'Hablar por servicios'),
                f"{whatsapp_url}?text={service_message}",
                use_container_width=True,
            )
            st.caption(email_address)

    with col_products:
        with st.expander(tr('contact_product_title', 'Productos'), expanded=False):
            st.write(tr('contact_product_text', 'Hablemos de módulos, licencias y evolución de la plataforma.'))
            st.link_button(
                tr('contact_product_label', 'Consultar productos'),
                f"{whatsapp_url}?text={product_message}",
                use_container_width=True,
            )
            st.caption(email_address)

    with col_ambassadors:
        with st.expander(tr('contact_ambassador_title', 'Embajadores'), expanded=False):
            st.write(tr('contact_ambassador_text', 'Únete como aliado comercial y de consultoría para abrir nuevas oportunidades.'))
            st.link_button(
                tr('contact_ambassador_label', 'Quiero ser embajador'),
                f"{whatsapp_url}?text={ambassador_message}",
                use_container_width=True,
            )
            st.link_button(
                tr('contact_whatsapp_label', 'Abrir WhatsApp'),
                whatsapp_url,
                use_container_width=True,
            )
