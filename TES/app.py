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
proyectos_resp = supabase.table("proyectos") \
    .select("id, proyecto") \
    .execute()

proyectos = proyectos_resp.data


if not proyectos:
    st.warning("No hay proyectos registrados.")
    st.stop()

# -------------------------
# Formulario
# -------------------------
with st.form("form_pregunta",clear_on_submit=True):
    proyecto = st.selectbox(
        "Proyecto",
        proyectos,
        format_func=lambda p: p["proyecto"]
    )

    Proceso = st.selectbox(
        "proceso de la pregunta", ["Desviacion","Proceso","Asignado"]
    )

    Tipo = st.selectbox(
        "Tipo de la pregunta", ["Grave","Medio"]
    )

    Pregunta = st.text_area(
        "Escribe la pregunta"
    )
    Puntos = st.text_area(
        "Puntua la pregunta"
    )
    
    submitted = st.form_submit_button("Guardar datos",use_container_width=True,width=150,icon="💾")

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
