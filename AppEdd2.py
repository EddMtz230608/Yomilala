import streamlit as st
import plotly.graph_objects as go
import numpy as np
import time
import os

# --- CONFIGURACIÓN DE ESCENA ---
st.set_page_config(page_title="Cosmos Master 3D", page_icon="🌌", layout="wide")

# Estilo CSS Avanzado
st.markdown("""
    <style>
    .main { background: radial-gradient(circle, #000814 0%, #000000 100%); color: #00d4ff; }
    .stMetric { background: rgba(0, 212, 255, 0.05); border: 1px solid #00d4ff; border-radius: 15px; padding: 15px; }
    .planet-card {
        border-left: 5px solid #00d4ff;
        background: rgba(255, 255, 255, 0.03);
        padding: 20px;
        border-radius: 0 15px 15px 0;
        margin-bottom: 20px;
    }
    .stButton>button {
        background: linear-gradient(45deg, #00d4ff, #005f73);
        color: white; border: none; border-radius: 10px; transition: 0.3s;
    }
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DATOS (Distancias ajustadas para visibilidad) ---
planetas = {
    "Mercurio": {"dist": 6, "size": 8, "color": "Greys", "temp": "427°C", "lunas": 0, "vel": 4.7},
    "Venus": {"dist": 10, "size": 12, "color": "YlOrRd", "temp": "462°C", "lunas": 0, "vel": 3.5},
    "Tierra": {"dist": 14, "size": 13, "color": "Blues", "temp": "15°C", "lunas": 1, "vel": 2.9},
    "Marte": {"dist": 18, "size": 10, "color": "Reds", "temp": "-63°C", "lunas": 2, "vel": 2.4},
    "Júpiter": {"dist": 28, "size": 25, "color": "Brwnyl", "temp": "-108°C", "lunas": 79, "vel": 1.3},
    "Saturno": {"dist": 38, "size": 22, "color": "Cividis", "temp": "-138°C", "lunas": 82, "vel": 0.9},
    "Urano": {"dist": 48, "size": 18, "color": "GnBu", "temp": "-195°C", "lunas": 27, "vel": 0.6},
    "Neptuno": {"dist": 58, "size": 18, "color": "Electric", "temp": "-201°C", "lunas": 14, "vel": 0.5}
}

# --- LOGICA DE NAVEGACIÓN ---
with st.sidebar:
    st.title("🛰️ Control Center")
    modo_animado = st.toggle("Activar Órbitas", value=False)
    velocidad = st.slider("Velocidad", 0.1, 3.0, 1.0)
    st.divider()
    st.write("Eduardo Martínez Teodoro | CECYTEM")

# --- RENDERIZADO ---
st.title("🌌 Orbital Nexus: Sistema 3D Pro")

col_3d, col_info = st.columns([2, 1])

if "frame" not in st.session_state: st.session_state.frame = 0

with col_3d:
    fig = go.Figure()

    # 1. SOL (Esfera de Malla corregida)
    u, v = np.mgrid[0:2*np.pi:30j, 0:np.pi:30j]
    r_sol = 3.5
    x_sol = r_sol * np.cos(u) * np.sin(v)
    y_sol = r_sol * np.sin(u) * np.sin(v)
    z_sol = r_sol * np.cos(v)
    
    fig.add_trace(go.Surface(
        x=x_sol, y=y_sol, z=z_sol,
        colorscale='Hot', showscale=False, name="Sol",
        hovertemplate="<b>SOL</b><br>Enana Amarilla<extra></extra>"
    ))

    # 2. PLANETAS
    for p_name, p in planetas.items():
        angulo = st.session_state.frame * p['vel'] * velocidad * 0.02
        pos_x = p['dist'] * np.cos(angulo)
        pos_y = p['dist'] * np.sin(angulo)

        # Órbitas circulares
        t_orb = np.linspace(0, 2*np.pi, 100)
        fig.add_trace(go.Scatter3d(
            x=p['dist']*np.cos(t_orb), y=p['dist']*np.sin(t_orb), z=np.zeros(100),
            mode='lines', line=dict(color='rgba(255,255,255,0.1)', width=1), showlegend=False
        ))

        # Planeta (Puntos marcadores)
        fig.add_trace(go.Scatter3d(
            x=[pos_x], y=[pos_y], z=[0],
            mode='markers',
            marker=dict(
                size=p['size'], color=[0, 1], colorscale=p['color'],
                showscale=False, line=dict(color='white', width=1)
            ),
            name=p_name,
            hovertemplate=f"<b>{p_name}</b><br>Temp: {p['temp']}<extra></extra>"
        ))

    # --- CORRECCIÓN CRÍTICA DE PROPORCIÓN ---
    fig.update_layout(
        scene=dict(
            bgcolor="black",
            xaxis_visible=False, yaxis_visible=False, zaxis_visible=False,
            # ESTO EVITA QUE SE VEAN ESTIRADOS
            aspectmode='data' 
        ),
        margin=dict(l=0, r=0, b=0, t=0), height=700, paper_bgcolor="black",
        legend=dict(font=dict(color="white"))
    )
    
    st.plotly_chart(fig, use_container_width=True)

with col_info:
    st.subheader("📊 Ficha del Planeta")
    sel = st.selectbox("Seleccionar:", list(planetas.keys()))
    p = planetas[sel]
    
    st.markdown(f"""
    <div class="planet-card">
        <h3>{sel.upper()}</h3>
        <p><b>Temperatura:</b> {p['temp']}</p>
        <p><b>Satélites:</b> {p['lunas']}</p>
        <p><b>Estatus:</b> Operativo</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    st.subheader("📝 Notas de Bitácora")
    nota = st.text_area("Registrar observación:")
    if st.button("Guardar Localmente"):
        with open("bitacora.txt", "a") as f:
            f.write(f"{sel}: {nota}\n")
        st.success("Sincronizado.")

# Lógica de animación
if modo_animado:
    st.session_state.frame += 1
    time.sleep(0.01)
    st.rerun()