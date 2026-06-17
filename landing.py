import streamlit as st

from landing_shared import (
    load_landing_css,
    render_contact_block,
)
from modules.landing.evolution_closing import render_evolution_closing
from modules.landing.framework_cycle import render_framework_cycle
from modules.landing.home import render_home
from modules.landing.how_it_works import render_how_it_works
from modules.landing.problem_opportunity import render_problem_opportunity
from modules.landing.segments_use_case import render_segments_use_case
from modules.landing.value_by_audience import render_value_by_audience
from modules.landing.i18n import get_lang, section_label, set_lang, tr


st.set_page_config(
    page_title="OPRIA OS | Plataforma Operativa Inteligente",
    page_icon="OP",
    layout="wide",
)
load_landing_css()

SECTIONS = {
    "home": render_home,
    "framework": render_framework_cycle,
    "problem": render_problem_opportunity,
    "how": render_how_it_works,
    "value": render_value_by_audience,
    "segments": render_segments_use_case,
    "evolution": render_evolution_closing,
}

if "landing_section" not in st.session_state:
    st.session_state["landing_section"] = "home"

if "landing_lang" not in st.session_state:
    st.session_state["landing_lang"] = "es"

lang = get_lang()

st.sidebar.markdown(f"## {tr('sidebar_brand', 'OPRIA OS')}")
st.sidebar.caption(str(tr("sidebar_nav", "Navegación comercial")))
st.sidebar.markdown(f"**{tr('sidebar_language', 'Idioma')}**")

col_es, col_en = st.sidebar.columns(2)
if col_es.button("ES", use_container_width=True, type="primary" if lang == "es" else "secondary"):
    set_lang("es")
    st.rerun()

if col_en.button("EN", use_container_width=True, type="primary" if lang == "en" else "secondary"):
    set_lang("en")
    st.rerun()

st.sidebar.divider()

for section_id in SECTIONS:
    if st.sidebar.button(section_label(section_id), use_container_width=True):
        st.session_state["landing_section"] = section_id

st.sidebar.divider()
st.sidebar.write(
    f"{tr('sidebar_current', 'Sección actual')}: {section_label(st.session_state['landing_section'])}"
)

SECTIONS[st.session_state["landing_section"]]()

st.divider()
render_contact_block()
