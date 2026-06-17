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
        "badge": "Sección 1",
        "title": "El problema operativo del mercado",
        "subtitle": "Empresas que crecieron más rápido que sus procesos",
        "description": (
            "Muchas organizaciones operan con hojas de cálculo, mensajería, correos y sistemas "
            "aislados. Esto permite avanzar al inicio, pero se vuelve un freno cuando la operación escala."
        ),
        "frictions": "## Fricciones principales",
        "cards": [
            {
                "title": "Procesos no estandarizados",
                "text": "Cada persona resuelve distinto. Resultado: variabilidad, errores repetitivos y dependencia de talento clave.",
            },
            {
                "title": "Falta de trazabilidad",
                "text": "Preguntas críticas como quién hizo qué, cuándo y dónde se bloqueó el flujo requieren investigación manual.",
            },
            {
                "title": "Coordinación fragmentada",
                "text": "La información se pierde entre chats, reuniones y correos. Aumentan retrasos y retrabajo.",
            },
        ],
        "opportunity": "## Oportunidad",
        "metrics": {
            "m1": ("Costo oculto de la informalidad", "Alto", "Retrabajo + tiempos muertos"),
            "m2": ("Visibilidad de ejecución", "Baja", "Sin sistema de seguimiento"),
            "m3": ("Potencial de mejora", "Muy alto", "Estandarización + automatización"),
            "m4": ("Impacto en escalabilidad", "Crítico", "Crecimiento sin control"),
        },
        "cta_title": "OPRIA convierte caos operativo en sistema gobernable",
        "cta_text": "El paso de operar por memoria a operar por diseño es la ventaja competitiva real.",
    },
    "en": {
        "badge": "Section 1",
        "title": "The market's operational problem",
        "subtitle": "Companies that grew faster than their processes",
        "description": (
            "Many organizations operate with spreadsheets, messaging apps, emails, and isolated systems. "
            "This may work at first, but it becomes a bottleneck as operations scale."
        ),
        "frictions": "## Main frictions",
        "cards": [
            {
                "title": "Non-standardized processes",
                "text": "Each person solves issues differently. Result: variability, repeated errors, and dependency on key talent.",
            },
            {
                "title": "Lack of traceability",
                "text": "Critical questions like who did what, when, and where the flow got blocked require manual investigation.",
            },
            {
                "title": "Fragmented coordination",
                "text": "Information gets lost across chats, meetings, and emails. Delays and rework increase.",
            },
        ],
        "opportunity": "## Opportunity",
        "metrics": {
            "m1": ("Hidden cost of informality", "High", "Rework + dead time"),
            "m2": ("Execution visibility", "Low", "No tracking system"),
            "m3": ("Improvement potential", "Very high", "Standardization + automation"),
            "m4": ("Impact on scalability", "Critical", "Uncontrolled growth"),
        },
        "cta_title": "OPRIA turns operational chaos into a governed system",
        "cta_text": "Moving from memory-based operations to design-based operations is the real competitive advantage.",
    },
}


def render_problem_opportunity() -> None:
    t = TEXTS[get_lang()]

    render_header_badge(t["badge"])
    render_hero(
        title=t["title"],
        subtitle=t["subtitle"],
        description=t["description"],
    )

    st.markdown(t["frictions"])
    render_highlight_cards(t["cards"])

    st.markdown(t["opportunity"])
    col_left, col_right = st.columns(2)
    metrics = t["metrics"]

    with col_left:
        st.metric(*metrics["m1"])
        st.metric(*metrics["m2"])

    with col_right:
        st.metric(*metrics["m3"])
        st.metric(*metrics["m4"])

    render_footer_cta(
        t["cta_title"],
        t["cta_text"],
    )
