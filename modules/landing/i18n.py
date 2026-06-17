from __future__ import annotations

from typing import Any

import streamlit as st

DEFAULT_LANG = "es"
SUPPORTED_LANGS = ("es", "en")

TEXTS: dict[str, dict[str, Any]] = {
    "es": {
        "sidebar_brand": "OPRIA OS",
        "sidebar_nav": "Navegación comercial",
        "sidebar_language": "Idioma",
        "sidebar_current": "Sección actual",
        "contact_title": "Contacto directo",
        "contact_text": "Escríbeme para servicios, productos o para sumarte como embajador comercial.",
        "contact_email_label": "Enviar correo",
        "contact_whatsapp_label": "Abrir WhatsApp",
        "contact_service_title": "Servicios",
        "contact_service_text": "Consultoría, diagnóstico y acompañamiento para implementar OPRIA.",
        "contact_product_title": "Productos",
        "contact_product_text": "Hablemos de módulos, licencias y evolución de la plataforma.",
        "contact_ambassador_title": "Embajadores",
        "contact_ambassador_text": "Únete como aliado comercial y de consultoría para abrir nuevas oportunidades.",
        "contact_service_label": "Hablar por servicios",
        "contact_product_label": "Consultar productos",
        "contact_ambassador_label": "Quiero ser embajador",
        "sections": {
            "home": "Inicio",
            "framework": "Framework OPRIA 360",
            "problem": "Problema y Oportunidad",
            "how": "Cómo Funciona OPRIA",
            "value": "Valor por Audiencia",
            "segments": "Segmentos y Caso de Uso",
            "evolution": "Evolución y Cierre",
        },
    },
    "en": {
        "sidebar_brand": "OPRIA OS",
        "sidebar_nav": "Commercial navigation",
        "sidebar_language": "Language",
        "sidebar_current": "Current section",
        "contact_title": "Direct contact",
        "contact_text": "Write to me for services, products, or to join as a commercial ambassador.",
        "contact_email_label": "Send email",
        "contact_whatsapp_label": "Open WhatsApp",
        "contact_service_title": "Services",
        "contact_service_text": "Consulting, diagnosis, and support to implement OPRIA.",
        "contact_product_title": "Products",
        "contact_product_text": "Let’s talk about modules, licenses, and platform evolution.",
        "contact_ambassador_title": "Ambassadors",
        "contact_ambassador_text": "Join as a commercial and consulting partner to unlock new opportunities.",
        "contact_service_label": "Talk about services",
        "contact_product_label": "Ask about products",
        "contact_ambassador_label": "I want to be an ambassador",
        "sections": {
            "home": "Home",
            "framework": "OPRIA 360 Framework",
            "problem": "Problem and Opportunity",
            "how": "How OPRIA Works",
            "value": "Value by Audience",
            "segments": "Segments and Use Case",
            "evolution": "Evolution and Closing",
        },
    },
}


def get_lang() -> str:
    lang = st.session_state.get("landing_lang", DEFAULT_LANG)
    if lang not in SUPPORTED_LANGS:
        lang = DEFAULT_LANG
        st.session_state["landing_lang"] = lang
    return lang


def set_lang(lang: str) -> None:
    if lang in SUPPORTED_LANGS:
        st.session_state["landing_lang"] = lang


def tr(key: str, default: str = "") -> Any:
    lang = get_lang()
    current: Any = TEXTS.get(lang, {})
    for part in key.split("."):
        if isinstance(current, dict) and part in current:
            current = current[part]
        else:
            return default
    return current


def section_label(section_id: str) -> str:
    return str(tr(f"sections.{section_id}", section_id))
