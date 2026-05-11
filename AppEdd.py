import streamlit as st
import pandas as pd
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import io

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Mini Lienzo", page_icon="🎨", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stButton>button { width: 100%; border-radius: 5px; background-color: #ff4b4b; color: white; border: none; }
    .stDownloadButton>button { width: 100%; border-radius: 5px; background-color: #28a745; color: white; border: none; }
    [data-testid="stSidebar"] { background-color: #1a1c23; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: ESTUDIO ---
with st.sidebar:
    st.title("Dibuja algo :)")
    
    # 1. Selector de Herramienta
    herramienta = st.radio(
        "Herramienta Principal:",
        ["Dibujo Libre", "Goma", "Línea", "Rectángulo", "Círculo", "Mover/Editar"]
    )
    
    st.divider()
    
    # 2. Configuración de Colores
    st.subheader("🎨 Paleta de Colores")
    color_fondo = st.color_picker("Color del Muro (Fondo):", "#1a1c23")
    color_trazo = st.color_picker("Color del Trazo / Spray:", "#00FFCC")
    color_relleno = st.color_picker("Color de Relleno (Figuras):", "#FF4B4B")
    
    st.divider()
    
    # 3. Tipos de Pincel
    st.subheader("🖋️ Estilo de Punta")
    tipo_pincel = st.selectbox("Tipo de pincel:", ["Aerosol (Goteo)", "Marcador (Sólido)"])
    grosor = st.slider("Tamaño de punta:", 1, 150, 25)

    # Lógica de Pinceles
    if herramienta == "Goma de Borrar":
        stroke_final = color_fondo # La goma pinta del color del fondo
        fill_final = color_fondo
    elif tipo_pincel == "Aerosol (Goteo)":
        stroke_final = f"{color_trazo}AA" # Transparencia para efecto spray
        fill_final = f"{color_relleno}66"
    else:
        stroke_final = color_trazo
        fill_final = color_relleno

    if st.button("🗑️ Resetear Lienzo"):
        st.rerun()

# --- MAPEO DE MODOS ---
herramientas_map = {
    "Dibujo Libre": "freedraw",
    "Goma de Borrar": "freedraw",
    "Línea": "line",
    "Rectángulo": "rect",
    "Círculo": "circle",
    "Mover/Editar": "transform"
}
modo_actual = herramientas_map[herramienta]

# --- ESPACIO DE TRABAJO ---
col_canvas, col_export = st.columns([3, 1])

with col_canvas:
    st.markdown(f"### 🖋️ Trabajando con: **{herramienta}**")
    
    canvas_result = st_canvas(
        fill_color=fill_final,
        stroke_width=grosor,
        stroke_color=stroke_final,
        background_color=color_fondo,
        height=600,
        width=850,
        drawing_mode=modo_actual,
        key="urban_studio_v6",
    )

with col_export:
    st.subheader("💾 Exportar tu dibujo")
    
    if canvas_result.image_data is not None:
        img = Image.fromarray(canvas_result.image_data.astype('uint8'), 'RGBA')
        
        # PNG
        buf_png = io.BytesIO()
        img.save(buf_png, format="PNG")
        st.download_button(
            label="Descargar PNG",
            data=buf_png.getvalue(),
            file_name="pieza_v6.png",
            mime="image/png"
        )
        
        # PDF
        img_pdf = img.convert('RGB')
        buf_pdf = io.BytesIO()
        img_pdf.save(buf_pdf, format="PDF")
        st.download_button(
            label="Descargar PDF",
            data=buf_pdf.getvalue(),
            file_name="boceto_v6.pdf",
            mime="application/pdf"
        )

    st.divider()
    st.info("💡 **Goma:** Selecciona 'Goma de Borrar' para limpiar trazos específicos. El tamaño de la goma se ajusta con el slider de 'Tamaño de punta'.")

st.caption("Creador de dibujo | Eduardo Martínez")