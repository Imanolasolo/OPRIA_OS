import streamlit as st

from landing_shared import (
    render_footer_cta,
    render_header_badge,
    render_hero,
    render_highlight_cards,
    render_timeline,
)
from modules.landing.i18n import get_lang


TEXTS = {
    "es": {
        "badge": "Sección 4",
        "title": "Segmentos objetivo y caso de uso universal",
        "subtitle": "Donde OPRIA genera mayor impacto",
        "description": (
            "OPRIA está diseñado para organizaciones donde la operación es crítica y la coordinación "
            "entre áreas determina resultados de negocio."
        ),
        "target": "## Industrias objetivo",
        "cards": [
            {"title": "Retail y cadenas", "text": "Control multisucursal, estandarización y seguimiento operativo."},
            {"title": "Logística y distribución", "text": "Trazabilidad de entregas e incidencias en tiempo real."},
            {"title": "Manufactura e industria", "text": "Producción, calidad, mantenimiento e indicadores."},
            {"title": "Servicios técnicos", "text": "Órdenes de trabajo, técnicos y tiempos de atención."},
        ],
        "uc1": "## Caso de uso comercial universal",
        "uc2": "### Gestión digital de incidencias operativas",
        "timeline": [
            {
                "step": "Paso 1",
                "text": "Un colaborador registra la incidencia con fecha, área, descripción y evidencia.",
            },
            {
                "step": "Paso 2",
                "text": "Un supervisor recibe alerta, define prioridad y asigna responsable.",
            },
            {
                "step": "Paso 3",
                "text": "El equipo ejecuta la solución y el sistema registra tiempo, responsable y resultado.",
            },
            {
                "step": "Paso 4",
                "text": "Dirección analiza volumen, áreas críticas, tiempos promedio y tendencias.",
            },
        ],
        "cta_title": "Resultado",
        "cta_text": "La incidencia deja de ser una urgencia reactiva y pasa a convertirse en aprendizaje operativo para mejora continua.",
    },
    "en": {
        "badge": "Section 4",
        "title": "Target segments and universal use case",
        "subtitle": "Where OPRIA generates the most impact",
        "description": (
            "OPRIA is designed for organizations where operations are critical and coordination "
            "across areas determines business outcomes."
        ),
        "target": "## Target industries",
        "cards": [
            {"title": "Retail and chains", "text": "Multi-branch control, standardization, and operational follow-up."},
            {"title": "Logistics and distribution", "text": "Real-time delivery and incident traceability."},
            {"title": "Manufacturing and industry", "text": "Production, quality, maintenance, and indicators."},
            {"title": "Technical services", "text": "Work orders, technicians, and response times."},
        ],
        "uc1": "## Universal commercial use case",
        "uc2": "### Digital management of operational incidents",
        "timeline": [
            {
                "step": "Step 1",
                "text": "A collaborator records the incident with date, area, description, and evidence.",
            },
            {
                "step": "Step 2",
                "text": "A supervisor receives the alert, sets priority, and assigns ownership.",
            },
            {
                "step": "Step 3",
                "text": "The team executes the solution and the system records time, owner, and outcome.",
            },
            {
                "step": "Step 4",
                "text": "Leadership analyzes volume, critical areas, average resolution time, and trends.",
            },
        ],
        "cta_title": "Outcome",
        "cta_text": "The incident stops being a reactive emergency and becomes operational learning for continuous improvement.",
    },
}


def render_segments_use_case() -> None:
    t = TEXTS[get_lang()]

    render_header_badge(t["badge"])
    render_hero(
        title=t["title"],
        subtitle=t["subtitle"],
        description=t["description"],
    )

    st.markdown(t["target"])
    render_highlight_cards(t["cards"])

    st.markdown(t["uc1"])
    st.markdown(t["uc2"])

    render_timeline(t["timeline"])

    render_footer_cta(
        t["cta_title"],
        t["cta_text"],
    )
