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
        "badge": "Sección Framework",
        "title": "Framework OPRIA 360",
        "subtitle": "No somos un SaaS más: somos un aliado integral",
        "description": (
            "OPRIA combina metodología, implementación operativa y evolución continua. "
            "Acompaña a la empresa desde el descubrimiento de procesos hasta la mejora iterativa "
            "en producción para crecer juntos con resultados medibles."
        ),
        "wheel": "## Rueda de transformación operativa",
        "timeline": [
            {
                "step": "1. Descubrir",
                "text": "Mapeamos procesos reales, puntos de fricción y cuellos de botella. Definimos prioridades de impacto y quick wins.",
            },
            {
                "step": "2. Implementar OPRIA OS",
                "text": "Configuramos gobierno organizacional, roles, flujos y trazabilidad para operar OPRIA en el día a día.",
            },
            {
                "step": "3. Pasar a producción",
                "text": "Estabilizamos ejecución, activamos reportes y medimos desempeño real de procesos con indicadores operativos.",
            },
            {
                "step": "4. Iterar y escalar",
                "text": "Aplicamos mejora continua, automatizaciones e integraciones para elevar madurez operativa y acompañar el crecimiento del negocio.",
            },
        ],
        "deliverables": "## Entregables por etapa",
        "cards": [
            {
                "title": "Diagnóstico accionable",
                "text": "Radiografía de procesos, riesgos operativos y plan de mejoras priorizadas.",
            },
            {
                "title": "Operación estandarizada",
                "text": "Flujos implementados, responsables claros y control de estados en tiempo real.",
            },
            {
                "title": "Crecimiento acompañado",
                "text": "Roadmap evolutivo por fases para escalar sin perder control operativo.",
            },
        ],
        "cta_title": "Compromiso OPRIA",
        "cta_text": "No vendemos solo tecnología. Construimos capacidad operativa sostenible junto al cliente.",
    },
    "en": {
        "badge": "Framework Section",
        "title": "OPRIA 360 Framework",
        "subtitle": "We are not just another SaaS: we are an end-to-end partner",
        "description": (
            "OPRIA combines methodology, operational implementation, and continuous evolution. "
            "It supports the company from process discovery to iterative improvement in production "
            "to grow together with measurable results."
        ),
        "wheel": "## Operational transformation wheel",
        "timeline": [
            {
                "step": "1. Discover",
                "text": "We map real processes, friction points, and bottlenecks. We define impact priorities and quick wins.",
            },
            {
                "step": "2. Implement OPRIA OS",
                "text": "We configure governance, roles, workflows, and traceability to run OPRIA in day-to-day operations.",
            },
            {
                "step": "3. Move to production",
                "text": "We stabilize execution, activate reporting, and measure real process performance with operational indicators.",
            },
            {
                "step": "4. Iterate and scale",
                "text": "We apply continuous improvement, automation, and integrations to raise operational maturity and support business growth.",
            },
        ],
        "deliverables": "## Deliverables by stage",
        "cards": [
            {
                "title": "Actionable diagnosis",
                "text": "Process snapshot, operational risks, and a prioritized improvement plan.",
            },
            {
                "title": "Standardized operations",
                "text": "Implemented workflows, clear owners, and real-time state control.",
            },
            {
                "title": "Guided growth",
                "text": "An evolutionary roadmap by phases to scale without losing operational control.",
            },
        ],
        "cta_title": "OPRIA commitment",
        "cta_text": "We do not sell only technology. We build sustainable operational capability with our clients.",
    },
}


def render_framework_cycle() -> None:
    t = TEXTS[get_lang()]

    render_header_badge(t["badge"])
    render_hero(
        title=t["title"],
        subtitle=t["subtitle"],
        description=t["description"],
    )

    st.markdown(t["wheel"])
    render_timeline(t["timeline"])

    st.markdown(t["deliverables"])
    render_highlight_cards(t["cards"])

    render_footer_cta(
        t["cta_title"],
        t["cta_text"],
    )
