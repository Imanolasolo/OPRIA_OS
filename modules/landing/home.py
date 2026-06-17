import streamlit as st

from landing_shared import (
    render_footer_cta,
    render_header_badge,
    render_hero,
    render_highlight_cards,
    render_quote,
)
from modules.landing.i18n import get_lang


TEXTS = {
    "es": {
        "badge": "Presentación Comercial",
        "subtitle": "Plataforma Operativa Inteligente para Empresas",
        "description": (
            "Transforma operaciones dispersas en un sistema gobernable, medible y escalable. "
            "OPRIA conecta personas, equipos, roles, procesos, sistemas e información operativa "
            "en una sola capa inteligente."
        ),
        "quote": (
            "Las empresas no crecen solamente agregando más personas o herramientas; "
            "crecen cuando sus operaciones pueden repetirse, medirse y mejorarse."
        ),
        "cards": [
            {
                "title": "Control real de la operación",
                "text": "Cada actividad tiene responsable, flujo, estado e historial verificable.",
            },
            {
                "title": "Integración sin fricción",
                "text": "No reemplaza todo lo existente; se integra como capa operativa entre sistemas.",
            },
            {
                "title": "Decisión basada en datos",
                "text": "Dashboards e indicadores para detectar cuellos de botella y priorizar mejoras.",
            },
        ],
        "overview": "## Qué encontrarás en esta presentación",
        "left": [
            "- Framework OPRIA 360: descubrir, implementar, producir, iterar",
            "- Problema del mercado y oportunidad",
            "- Cómo funciona OPRIA en 3 capas",
            "- Valor para clientes, stakeholders y embajadores",
        ],
        "right": [
            "- Segmentos objetivo y propuesta por industria",
            "- Caso de uso comercial universal",
            "- Evolución modular de la plataforma",
        ],
        "cta_title": "Usa el menú lateral para explorar secciones",
        "cta_text": "Cada bloque está pensado para una conversación comercial clara y accionable con tu audiencia.",
    },
    "en": {
        "badge": "Commercial Presentation",
        "subtitle": "Intelligent Operating Platform for Businesses",
        "description": (
            "Transforms scattered operations into a governed, measurable, and scalable system. "
            "OPRIA connects people, teams, roles, processes, existing systems, and operational "
            "information in one intelligent layer."
        ),
        "quote": (
            "Companies do not grow only by adding more people or tools; "
            "they grow when operations can be repeated, measured, and improved."
        ),
        "cards": [
            {
                "title": "Real operational control",
                "text": "Every activity has an owner, a workflow, a known status, and a verifiable history.",
            },
            {
                "title": "Seamless integration",
                "text": "It does not replace everything you already have; it acts as an operational layer across systems.",
            },
            {
                "title": "Data-driven decisions",
                "text": "Dashboards and indicators to detect bottlenecks and prioritize improvements.",
            },
        ],
        "overview": "## What you will find in this presentation",
        "left": [
            "- OPRIA 360 Framework: discover, implement, produce, iterate",
            "- Market problem and opportunity",
            "- How OPRIA works in 3 layers",
            "- Value for clients, stakeholders, and ambassadors",
        ],
        "right": [
            "- Target segments and industry value proposition",
            "- Universal commercial use case",
            "- Modular platform evolution",
        ],
        "cta_title": "Use the sidebar menu to explore sections",
        "cta_text": "Each block is designed for a clear, actionable commercial conversation with your audience.",
    },
}


def render_home() -> None:
    t = TEXTS[get_lang()]

    render_header_badge(t["badge"])
    render_hero(
        title="OPRIA OS",
        subtitle=t["subtitle"],
        description=t["description"],
    )

    render_quote(t["quote"])

    render_highlight_cards(t["cards"])

    st.markdown(t["overview"])
    col1, col2 = st.columns(2)

    with col1:
        for line in t["left"]:
            st.markdown(line)

    with col2:
        for line in t["right"]:
            st.markdown(line)

    render_footer_cta(
        t["cta_title"],
        t["cta_text"],
    )
