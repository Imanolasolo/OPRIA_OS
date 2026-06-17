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
        "badge": "Sección 3",
        "title": "Propuesta de valor por audiencia",
        "subtitle": "Clientes, stakeholders y embajadores",
        "description": (
            "OPRIA presenta beneficios diferenciados para cada actor del ecosistema, "
            "alineando ejecución operativa con impacto estratégico y comercial."
        ),
        "directors": "## Para Dirección y Stakeholders",
        "directors_cards": [
            {"title": "Control operativo", "text": "Visibilidad completa sobre la ejecución real de los procesos."},
            {"title": "Reducción de riesgo", "text": "Menor dependencia del conocimiento individual."},
            {"title": "Escalabilidad", "text": "Crecimiento sostenible sin aumentar la complejidad al mismo ritmo."},
        ],
        "ambassadors": "## Para Embajadores Comerciales (Ventas + Consultoría)",
        "ambassadors_cards": [
            {
                "title": "Qué hace un embajador OPRIA",
                "text": "Detecta oportunidades, lidera diagnósticos y diseña propuestas de transformación operativa para cada cliente.",
            },
            {
                "title": "Valor para ventas y consultoría",
                "text": "Acorta el ciclo comercial con evidencia operativa y eleva el ticket con una oferta consultiva por fases.",
            },
            {
                "title": "Crecimiento recurrente",
                "text": "Activa planes evolutivos (implementación, producción e iteraciones) que facilitan retención y expansión de cuenta.",
            },
        ],
        "how_become": "### Cómo convertirse en embajador OPRIA",
        "how_timeline": [
            {
                "step": "Paso 1 - Aplicación y perfil",
                "text": "Postúlate con experiencia en ventas consultivas, mejora de procesos o implementación de soluciones empresariales.",
            },
            {
                "step": "Paso 2 - Certificación OPRIA",
                "text": "Completa entrenamiento en Framework OPRIA 360, discovery de procesos, diseño de roadmap y narrativa comercial.",
            },
            {
                "step": "Paso 3 - Co-ejecución de primeros casos",
                "text": "Acompaña reuniones y diagnósticos con el equipo OPRIA para dominar la metodología en escenarios reales.",
            },
            {
                "step": "Paso 4 - Activación comercial",
                "text": "Lanza oportunidades con playbooks, seguimiento en producción y esquema de crecimiento por cuenta.",
            },
        ],
        "profile": "### Perfil recomendado del embajador",
        "profile_lines": [
            "- Experiencia en ventas B2B consultivas o transformación operativa",
            "- Habilidad para mapear procesos y detectar cuellos de botella",
            "- Capacidad para traducir problemas operativos en propuestas accionables",
            "- Compromiso de acompañamiento post-venta y mejora continua",
        ],
        "info": "¿Quieres convertirte en embajador OPRIA? Agenda una sesión de onboarding para evaluar fit, certificación y plan de activación.",
        "users": "## Para Usuarios Operativos",
        "users_cards": [
            {"title": "Claridad de responsabilidades", "text": "Cada tarea tiene dueño y estado definido."},
            {"title": "Procesos guiados", "text": "Menos incertidumbre, menos tareas repetitivas."},
            {"title": "Seguimiento efectivo", "text": "Mejor comunicación y cierre de pendientes."},
        ],
        "cta_title": "Una plataforma, múltiples mensajes de valor",
        "cta_text": "Con embajadores comerciales certificados, OPRIA combina tecnología, consultoría y ejecución para generar resultados sostenibles.",
    },
    "en": {
        "badge": "Section 3",
        "title": "Value proposition by audience",
        "subtitle": "Clients, stakeholders, and ambassadors",
        "description": (
            "OPRIA delivers differentiated value for each actor in the ecosystem, "
            "aligning operational execution with strategic and commercial impact."
        ),
        "directors": "## For Leadership and Stakeholders",
        "directors_cards": [
            {"title": "Operational control", "text": "Complete visibility into real process execution."},
            {"title": "Risk reduction", "text": "Less dependency on individual knowledge."},
            {"title": "Scalability", "text": "Sustainable growth without increasing complexity at the same pace."},
        ],
        "ambassadors": "## For Commercial Ambassadors (Sales + Consulting)",
        "ambassadors_cards": [
            {
                "title": "What an OPRIA ambassador does",
                "text": "Identifies opportunities, leads diagnostics, and designs operational transformation proposals for each client.",
            },
            {
                "title": "Value for sales and consulting",
                "text": "Shortens sales cycles with operational evidence and increases deal size through phased consulting offers.",
            },
            {
                "title": "Recurring growth",
                "text": "Activates evolution plans (implementation, production, and iterations) that improve retention and account expansion.",
            },
        ],
        "how_become": "### How to become an OPRIA ambassador",
        "how_timeline": [
            {
                "step": "Step 1 - Application and profile",
                "text": "Apply with experience in consultative sales, process improvement, or enterprise solution implementation.",
            },
            {
                "step": "Step 2 - OPRIA certification",
                "text": "Complete training in the OPRIA 360 Framework, process discovery, roadmap design, and commercial narrative.",
            },
            {
                "step": "Step 3 - Co-execution of first cases",
                "text": "Join meetings and diagnostics with the OPRIA team to master the methodology in real scenarios.",
            },
            {
                "step": "Step 4 - Commercial activation",
                "text": "Launch opportunities with playbooks, production follow-up, and account growth schemes.",
            },
        ],
        "profile": "### Recommended ambassador profile",
        "profile_lines": [
            "- Experience in B2B consultative sales or operational transformation",
            "- Ability to map processes and detect bottlenecks",
            "- Ability to translate operational problems into actionable proposals",
            "- Commitment to post-sales support and continuous improvement",
        ],
        "info": "Want to become an OPRIA ambassador? Book an onboarding session to assess fit, certification, and activation plan.",
        "users": "## For Operational Users",
        "users_cards": [
            {"title": "Role clarity", "text": "Every task has an owner and a defined status."},
            {"title": "Guided processes", "text": "Less uncertainty and fewer repetitive tasks."},
            {"title": "Effective follow-up", "text": "Better communication and pending-task closure."},
        ],
        "cta_title": "One platform, multiple value messages",
        "cta_text": "With certified commercial ambassadors, OPRIA combines technology, consulting, and execution to deliver sustainable outcomes.",
    },
}


def render_value_by_audience() -> None:
    t = TEXTS[get_lang()]

    render_header_badge(t["badge"])
    render_hero(
        title=t["title"],
        subtitle=t["subtitle"],
        description=t["description"],
    )

    st.markdown(t["directors"])
    render_highlight_cards(t["directors_cards"])

    st.markdown(t["ambassadors"])
    render_highlight_cards(t["ambassadors_cards"])

    st.markdown(t["how_become"])
    render_timeline(t["how_timeline"])

    st.markdown(t["profile"])
    for line in t["profile_lines"]:
        st.markdown(line)

    st.info(t["info"])

    st.markdown(t["users"])
    render_highlight_cards(t["users_cards"])

    render_footer_cta(
        t["cta_title"],
        t["cta_text"],
    )
