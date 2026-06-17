import streamlit as st

from landing_shared import (
    render_footer_cta,
    render_header_badge,
    render_hero,
    render_highlight_cards,
)
from modules.landing.i18n import get_lang


TEXTS = {
    "es": {
        "badge": "Sección 2",
        "title": "ómo funciona OPRIA OS",
        "subtitle": "Tres capas para diseñar la operación",
        "description": (
            "OPRIA digitaliza la forma real en que opera una empresa. No impone un modelo rígido; "
            "ordena y conecta lo que ya existe para hacerlo medible y escalable."
        ),
        "l1": "## Capa 1 - Gobierno Organizacional",
        "l1_cards": [
            {"title": "Empresas y unidades", "text": "Cada organización define su propio espacio operativo."},
            {"title": "Usuarios", "text": "Identidad, accesos, responsabilidades y actividad histórica por colaborador."},
            {"title": "Roles y subroles", "text": "Permisos precisos para que cada perfil reciba solo las herramientas necesarias."},
        ],
        "l2": "## Capa 2 - Orquestación de Procesos",
        "l2_cards": [
            {"title": "Inicio y responsable", "text": "Cada proceso arranca con contexto y propietario claro."},
            {"title": "Pasos, validaciones y estados", "text": "El flujo deja de ser informal y pasa a ser verificable."},
            {"title": "Cierre y trazabilidad", "text": "Se registra qué pasó, quién actuó y cuánto tiempo tomó."},
        ],
        "l3": "## Capa 3 - Inteligencia Operativa",
        "l3_cards": [
            {"title": "Dashboards", "text": "Visibilidad de avance en tiempo real."},
            {"title": "Indicadores y reportes", "text": "Detección de cuellos de botella y oportunidades de mejora."},
            {"title": "Alertas e historial", "text": "Seguimiento continuo para decisiones basadas en evidencia."},
        ],
        "cta_title": "De la pregunta al diagnóstico accionable",
        "cta_text": "La operación deja de preguntar qué está pasando y empieza a responder dónde mejorar y cómo hacerlo.",
    },
    "en": {
        "badge": "Section 2",
        "title": "How OPRIA OS works",
        "subtitle": "Three layers to design operations",
        "description": (
            "OPRIA digitizes how a company actually operates. It does not impose a rigid model; "
            "it organizes and connects what already exists to make it measurable and scalable."
        ),
        "l1": "## Layer 1 - Organizational Governance",
        "l1_cards": [
            {"title": "Companies and units", "text": "Each organization defines its own operational space."},
            {"title": "Users", "text": "Identity, access, responsibilities, and historical activity per collaborator."},
            {"title": "Roles and subroles", "text": "Precise permissions so each profile gets only the tools they need."},
        ],
        "l2": "## Layer 2 - Process Orchestration",
        "l2_cards": [
            {"title": "Start and owner", "text": "Each process starts with clear context and ownership."},
            {"title": "Steps, validations, and states", "text": "The flow moves from informal to verifiable."},
            {"title": "Closure and traceability", "text": "It records what happened, who acted, and how long it took."},
        ],
        "l3": "## Layer 3 - Operational Intelligence",
        "l3_cards": [
            {"title": "Dashboards", "text": "Real-time visibility into execution progress."},
            {"title": "Indicators and reports", "text": "Bottleneck detection and improvement opportunities."},
            {"title": "Alerts and history", "text": "Continuous tracking for evidence-based decisions."},
        ],
        "cta_title": "From questions to actionable diagnosis",
        "cta_text": "Operations stop asking what is happening and start answering where to improve and how.",
    },
}


def render_how_it_works() -> None:
    t = TEXTS[get_lang()]

    render_header_badge(t["badge"])
    render_hero(
        title=t["title"],
        subtitle=t["subtitle"],
        description=t["description"],
    )

    st.markdown(t["l1"])
    render_highlight_cards(t["l1_cards"])

    st.markdown(t["l2"])
    render_highlight_cards(t["l2_cards"])

    st.markdown(t["l3"])
    render_highlight_cards(t["l3_cards"])

    render_footer_cta(
        t["cta_title"],
        t["cta_text"],
    )
