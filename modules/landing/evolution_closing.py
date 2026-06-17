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
        "badge": "Sección 5",
        "title": "Evolución de OPRIA OS",
        "subtitle": "Plataforma modular para crecer con el negocio",
        "description": (
            "OPRIA no es una solución estática. Evoluciona por módulos y capacidades según la madurez "
            "operativa y el ritmo de crecimiento de cada organización."
        ),
        "expansion": "## Expansión por capacidades",
        "cards": [
            {"title": "Integraciones ERP y CRM", "text": "Conecta procesos operativos con sistemas de gestión empresarial."},
            {"title": "Automatizaciones", "text": "Reduce tareas manuales y acelera tiempos de respuesta."},
            {"title": "Inteligencia artificial", "text": "Prediccion de incidencias y recomendaciones de mejora."},
            {"title": "IoT y sistemas industriales", "text": "Monitoreo conectado para operaciones de alta criticidad."},
        ],
        "message": "## Mensaje de cierre",
        "message_body": """
OPRIA impulsa una transformacion operativa progresiva:

- Mejora el presente con control y trazabilidad.
- Prepara el futuro con datos, automatización e inteligencia.
- Convierte la operación en una ventaja competitiva sostenible.
        """,
        "cta_title": "Visión OPRIA",
        "cta_text": "Crear el sistema operativo digital que permita a cada empresa operar mejor hoy y evolucionar mañana.",
        "next": "### Siguiente paso sugerido",
        "next_info": "Agenda una demo guiada por industria para mapear procesos, indicadores y quick wins en menos de 2 semanas.",
    },
    "en": {
        "badge": "Section 5",
        "title": "Evolution of OPRIA OS",
        "subtitle": "A modular platform to grow with the business",
        "description": (
            "OPRIA is not a static solution. It evolves through modules and capabilities based on "
            "each organization's operational maturity and growth pace."
        ),
        "expansion": "## Capability expansion",
        "cards": [
            {"title": "ERP and CRM integrations", "text": "Connect operational processes with enterprise management systems."},
            {"title": "Automations", "text": "Reduce manual tasks and accelerate response times."},
            {"title": "Artificial intelligence", "text": "Incident prediction and improvement recommendations."},
            {"title": "IoT and industrial systems", "text": "Connected monitoring for high-criticality operations."},
        ],
        "message": "## Closing message",
        "message_body": """
OPRIA drives progressive operational transformation:

- Improves the present with control and traceability.
- Prepares the future with data, automation, and intelligence.
- Turns operations into a sustainable competitive advantage.
        """,
        "cta_title": "OPRIA Vision",
        "cta_text": "Build the digital operating system that helps every company operate better today and evolve tomorrow.",
        "next": "### Suggested next step",
        "next_info": "Book an industry-focused demo to map processes, indicators, and quick wins in less than two weeks.",
    },
}


def render_evolution_closing() -> None:
    t = TEXTS[get_lang()]

    render_header_badge(t["badge"])
    render_hero(
        title=t["title"],
        subtitle=t["subtitle"],
        description=t["description"],
    )

    st.markdown(t["expansion"])
    render_highlight_cards(t["cards"])

    st.markdown(t["message"])
    st.markdown(t["message_body"])

    render_footer_cta(
        t["cta_title"],
        t["cta_text"],
    )

    st.markdown(t["next"])
    st.info(t["next_info"])
