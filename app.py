import datetime
import streamlit as st
import os
import json
import logging
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

from src.utils import guardar_correccion, aplicar_correcciones
from src.afi_tools import texto_a_afi
from src.engine import transcribir_audio
from src.vosk_engine import transcribir_vosk


# ============================
#   CARGAR CORRECCIONES
# ============================
try:
    with open("correcciones.json", "r", encoding="utf-8") as f:
        correcciones = json.load(f)
except:
    correcciones = {}
    logging.warning("No se encontró 'correcciones.json', iniciando vacío.")


# ============================
#   CONFIGURACIÓN DE PÁGINA
# ============================
st.set_page_config(page_title="PhonoSyncAI - TFG DAM", layout="wide")


# ============================
#   CABECERA PRINCIPAL
# ============================
st.markdown('<div class="header-container">', unsafe_allow_html=True)
st.image("logo.png", width=180)
st.markdown("""
    <h1 class="header-title">PhonoSyncAI</h1>
    <h4 class="header-subtitle">Sistema de Transcripción Fonética y Sincronización Inteligente</h4>
</div>
<hr class="header-divider">
""", unsafe_allow_html=True)


# ============================
#   CSS DEFINITIVO
# ============================
st.markdown("""
<style>

    /* CABECERA */
    .header-container {
        margin-top: 20px !important;
        margin-bottom: 10px !important;
        text-align: center;
    }

    .header-title {
        margin-bottom: 0;
        color: #E6EDF3;
        font-family: 'Segoe UI', sans-serif;
        font-weight: 700;
    }

    .header-subtitle {
        color: #6EA8FE;
        margin-top: 5px;
        font-family: 'Segoe UI', sans-serif;
        font-weight: 500;
    }

    .header-divider {
        margin-top: 20px;
        margin-bottom: 30px;
        border-color: #30363D;
    }

    /* ESPACIADO GLOBAL */
    .block-container {
        padding-top: 2.5rem !important;
    }

    /* GRID FLEX */
    .segment-grid {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin-top: 10px;
    }

    /* CAJA DE PALABRA */
    .segment-box {
        flex: 0 0 calc(12.5% - 8px); /* 8 por fila */
        padding: 6px 10px;
        border-radius: 6px;
        font-size: 0.9rem;
        font-weight: 600;
        color: white;
        text-align: center;
        cursor: pointer;
    }

    /* COLORES POR TIPO */
    .word-noun { background-color: #4C8BF5; }
    .word-verb { background-color: #A855F7; }
    .word-adj { background-color: #F59E0B; }
    .word-error { background-color: #EF4444; }
    .word-unknown { background-color: #6B7280; }

    /* HOVER */
    .segment-box:hover {
        opacity: 0.85;
        transform: scale(1.03);
        transition: 0.1s ease-in-out;
    }

</style>
""", unsafe_allow_html=True)


# ============================
#   ESTADO
# ============================
if "transcripcion" not in st.session_state:
    st.session_state.transcripcion = []

if "modo_afi" not in st.session_state:
    st.session_state.modo_afi = False


# ============================
#   SIDEBAR
# ============================
with st.sidebar:
    st.title("⚙️ Configuración")

    st.subheader("📁 Subir Audio")
    archivo_audio = st.file_uploader("Selecciona un archivo", type=["wav", "mp3"])

    st.divider()

    # MICRÓFONO MOCKUP
    st.subheader("🎤 Grabación por micrófono (Mockup)")

    if "grabando" not in st.session_state:
        st.session_state.grabando = False

    if st.button("🎙️ Iniciar grabación (simulada)"):
        st.session_state.grabando = True

    if st.session_state.grabando:
        st.markdown("""
        <div style="width:40px;height:40px;background:#FF4B4B;border-radius:50%;margin:auto;
        animation:pulso 1s infinite;"></div>
        <style>
        @keyframes pulso {
            0% { transform:scale(1); opacity:0.8; }
            50% { transform:scale(1.3); opacity:1; }
            100% { transform:scale(1); opacity:0.8; }
        }
        </style>
        """, unsafe_allow_html=True)

        if st.button("⏹️ Detener grabación"):
            st.session_state.grabando = False
            st.info("📁 Audio simulado listo para procesar")

    st.divider()

    st.subheader("🔡 Opciones")
    st.session_state.modo_afi = st.toggle("🧠 Mostrar AFI", value=st.session_state.modo_afi)

    opcion_modelo = st.selectbox("Motor de transcripción", ["Whisper (preciso)", "Vosk (offline)"])

    st.divider()

    if st.button("⚡ Procesar con IA"):
        st.session_state.procesar_ia = True


# ============================
#   PROCESAMIENTO IA
# ============================
if st.session_state.get("procesar_ia", False):

    if archivo_audio:
        try:
            with st.spinner("Procesando audio..."):

                with open("temp_audio.wav", "wb") as f:
                    f.write(archivo_audio.getbuffer())

                if opcion_modelo == "Whisper (preciso)":
                    resultado = transcribir_audio("temp_audio.wav")
                    segmentos = resultado["segmentos"]

                    resultado_real = []
                    for seg in segmentos:
                        if "words" not in seg:
                            for p in seg["text"].split():
                                resultado_real.append({
                                    "word": p,
                                    "start": round(seg["start"], 2),
                                    "afi": texto_a_afi(p)
                                })
                            continue

                        for w in seg["words"]:
                            palabra = w["word"].lower()
                            palabra_corregida = correcciones.get(palabra, palabra)
                            resultado_real.append({
                                "word": palabra_corregida,
                                "start": round(w["start"], 2),
                                "afi": texto_a_afi(palabra_corregida)
                            })

                else:
                    resultado = transcribir_vosk("temp_audio.wav")
                    resultado_real = []

                    if resultado["palabras"]:
                        for w in resultado["palabras"]:
                            palabra = w["word"].lower()
                            palabra_corregida = correcciones.get(palabra, palabra)
                            resultado_real.append({
                                "word": palabra_corregida,
                                "start": w.get("start", 0),
                                "afi": texto_a_afi(palabra_corregida)
                            })
                    else:
                        for p in resultado["texto"].split():
                            palabra_corregida = aplicar_correcciones(p)
                            resultado_real.append({
                                "word": palabra_corregida,
                                "start": 0,
                                "afi": texto_a_afi(palabra_corregida)
                            })

                st.session_state.transcripcion = resultado_real
                os.remove("temp_audio.wav")

            st.success("¡Análisis completado!")

        except Exception as e:
            st.error(f"Error: {e}")

    else:
        st.error("Sube un archivo primero.")

    st.session_state.procesar_ia = False
    st.rerun()


# ============================
#   CUERPO PRINCIPAL
# ============================
st.title("🎙️ IA Audio Editor & Phonetic Viewer")
st.info("Haz clic en las palabras para sincronizar el audio o edita el texto abajo.")

col1, col2 = st.columns([2, 1])


# ============================
#   COLUMNA IZQUIERDA
# ============================
with col1:

    st.subheader("🎧 Reproductor de Audio")
    if archivo_audio:
        st.audio(archivo_audio)
    else:
        st.warning("Sube un audio para activar el reproductor.")

    st.write("---")

    # ============================
    #   SEGMENTOS DETECTADOS
    # ============================
    st.subheader("🧩 Segmentos Detectados")

    if st.session_state.transcripcion:

        html_segmentos = '<div class="segment-grid">'

        for item in st.session_state.transcripcion:
            mostrar = item["afi"] if st.session_state.modo_afi else item["word"]
            palabra = item["word"].lower()

            if palabra.endswith("o"):
                clase = "word-noun"
            elif palabra.endswith(("ar", "er", "ir")):
                clase = "word-verb"
            elif palabra.endswith("a"):
                clase = "word-adj"
            elif "r" not in palabra and len(palabra) > 3:
                clase = "word-error"
            else:
                clase = "word-unknown"

            html_segmentos += f'<div class="segment-box {clase}">{mostrar}</div>'

        html_segmentos += '</div>'

        st.html(html_segmentos)

    else:
        st.info("Aún no hay transcripción disponible.")

    # ============================
    #   EDITOR
    # ============================
    st.subheader("📝 Editor de Transcripción")

    if st.session_state.transcripcion:

        texto_para_editar = " ".join([w["word"] for w in st.session_state.transcripcion])

        nuevo_texto = st.text_area(
            "Corrección manual:",
            value=texto_para_editar,
            height=150
        )

        if nuevo_texto != texto_para_editar:
            palabras_nuevas = nuevo_texto.split()
            original = st.session_state.transcripcion
            nueva_lista = []

            es_seguro = len(palabras_nuevas) == len(original)

            for i, p_word in enumerate(palabras_nuevas):
                if i < len(original):
                    st_time = original[i]["start"]

                    if es_seguro:
                        palabra_vieja = original[i]["word"]
                        if p_word.lower() != palabra_vieja.lower():
                            guardar_correccion(palabra_vieja, p_word)

                else:
                    st_time = nueva_lista[-1]["start"] + 0.3 if nueva_lista else 0.0

                nueva_lista.append({
                    "word": p_word,
                    "start": round(st_time, 2),
                    "afi": texto_a_afi(p_word)
                })

            st.session_state.transcripcion = nueva_lista
            st.rerun()

    # ============================
    #   ANÁLISIS FONOLÓGICO
    # ============================
    st.subheader("🧠 Análisis Fonológico (Mockup)")

    edad = st.number_input("Edad del niño", 2, 12, 5)

    if st.button("🔍 Analizar PSF"):
        palabras = [w["word"] for w in st.session_state.transcripcion]

        errores_detectados = sum(
            (("r" not in p and len(p) > 3) or (p.endswith("o") and len(p) <= 3))
            for p in palabras
        )

        esperados = {2:12,3:10,4:8,5:6,6:4,7:3,8:2,9:1,10:1,11:0,12:0}[edad]

        fig, ax = plt.subplots(figsize=(6,4))
        ax.bar(["Esperados","Detectados"], [esperados, errores_detectados],
               color=["#4ECDC4","#FF6B6B"])
        ax.set_title(f"Perfil Fonológico (Edad {edad})")
        st.pyplot(fig)

    st.subheader("📋 Resumen de Errores")

    if st.session_state.transcripcion:
        errores = {"Omisiones":0,"Sustituciones":0,"Simplificaciones":0,"Rotacismo":0,"Otros":0}

        for w in [x["word"] for x in st.session_state.transcripcion]:
            if "r" not in w and len(w)>3: errores["Rotacismo"]+=1
            if w.endswith("o") and len(w)<=3: errores["Simplificaciones"]+=1
            if w.startswith("m") and "p" in w: errores["Sustituciones"]+=1
            if len(w)<=2: errores["Omisiones"]+=1

        st.table(errores)

    # ============================
    #   ANÁLISIS PROSÓDICO
    # ============================
    st.subheader("🎵 Análisis Prosódico (Mockup)")

    if st.button("🎚️ Analizar Prosodia"):
        palabras = len(st.session_state.transcripcion)
        pitch = 180 + (palabras % 20) * 2
        var = 20 + (palabras % 5) * 3
        dur = palabras * 0.45

        st.info(f"Pitch promedio: {pitch} Hz")
        st.info(f"Variabilidad: {var} Hz")
        st.info(f"Duración estimada: {dur} s")

        t = np.linspace(0, dur, 100)
        curva = pitch + np.sin(t*3)*var

        fig2, ax2 = plt.subplots(figsize=(6,4))
        ax2.plot(t, curva, color="#6EA8FE")
        st.pyplot(fig2)


# ============================
#   COLUMNA DERECHA
# ============================
with col2:

    st.subheader("📊 Metadatos JSON")
    st.json(st.session_state.transcripcion)

    st.divider()

    st.subheader("📥 Guardar Resultados")

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_archivo = f"sesion_{timestamp}.json"
    json_string = json.dumps(st.session_state.transcripcion, indent=4, ensure_ascii=False)

    st.download_button("💾 Descargar JSON", json_string, nombre_archivo)

    if st.button("📁 Guardar en /docs/sesiones"):
        carpeta = "docs/sesiones"
        os.makedirs(carpeta, exist_ok=True)
        ruta = os.path.join(carpeta, nombre_archivo)
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(json_string)
        st.success(f"Guardado en {ruta}")


# ============================
#   FOOTER
# ============================
st.markdown("""
<hr style="margin-top:40px; border-color:#30363D;">
<div style="text-align:center; color:#8B949E;">
    <strong style="color:#E6EDF3;">PhonoSyncAI</strong> · TFG DAM · 2026<br>
    Desarrollado por <strong style="color:#E6EDF3;">Justina Araneda Rodríguez</strong>
</div>
""", unsafe_allow_html=True)
