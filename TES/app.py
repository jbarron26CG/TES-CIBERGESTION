import streamlit as st
from supabase import create_client

# -------------------------
# Conexión a Supabase
# -------------------------
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]

supabase = create_client(url, key)

st.set_page_config(page_title="Alta de preguntas", layout="centered")
st.title("➕ Agregar pregunta a un proyecto")

# -------------------------
# Obtener proyectos
# -------------------------
proyectos_resp = supabase.table("Proyectos") \
    .select("id, Proyecto") \
    .order("Proyecto") \
    .execute()

proyectos = proyectos_resp.data

if not proyectos:
    st.warning("No hay proyectos registrados.")
    st.stop()

# -------------------------
# Formulario
# -------------------------
with st.form("form_pregunta"):
    proyecto = st.selectbox(
        "Proyecto",
        proyectos,
        format_func=lambda p: p["proyecto"]
    )

    Proceso = st.text_area(
        "proceso de la pregunta"
    )

    Tipo = st.text_area(
        "proceso de la pregunta"
    )

    Pregunta = st.text_area(
        "proceso de la pregunta"
    )
    Puntos = st.text_area(
        "proceso de la pregunta"
    )

    submitted = st.form_submit_button("Guardar pregunta")

# -------------------------
# Guardar en la base
# -------------------------
if submitted:
    if not Proceso.strip():
        st.error("El texto de la pregunta no puede estar vacío.")
    else:
        data = {
            "proyecto_id": proyecto["id"],
            "Proceso_Evaluado": Proceso,
            "Tipo_Pregunta": Tipo,
            "Pregunta": Pregunta,
            "Puntos": Puntos
        }

        response = supabase.table("preguntas").insert(data).execute()

        if response.data:
            st.success("✅ Pregunta guardada correctamente")
            st.rerun()
        else:
            st.error("❌ Ocurrió un error al guardar la pregunta")
