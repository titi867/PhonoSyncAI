import datetime
import streamlit as st
import os
import json
import logging
import config

from src.utils import guardar_correccion, aplicar_correcciones
from src.afi_tools import texto_a_afi
from src.engine import transcribir_audio
from src.vosk_engine import transcribir_vosk
from PIL import Image


# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="PhonoSyncAI - TFG DAM", layout="wide")

# --- CABECERA PRINCIPAL ---
logo = Image.open("logo.png")

st.markdown(
    """
    <div style="
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin-top: -20px;
    ">
    """,
    unsafe_allow_html=True
)

st.image(logo, width=180)

st.markdown(
    """
        <h1 style="margin-bottom: 0; color: #E6EDF3;">PhonoSyncAI</h1>
        <h4 style="color: #6EA8FE; margin-top: 5px;">
            Sistema de Transcripción Fonética y Sincronización Inteligente
        </h4>
    </div>

    <hr style="margin-top: 20px; margin-bottom: 30px; border-color: #30363D;">
    """,
    unsafe_allow_html=True
)

# --- ESTILOS CUSTOM ---
st.markdown("""
<style>

    /* Botones */
    .stButton>button {
        background-color: #238636;
        color: white;
        border-radius: 6px;
        padding: 8px 18px;
        border: none;
        font-weight: 600;
        transition: 0.2s;
    }
    .stButton>button:hover {
        background-color: #2EA043;
        transform: scale(1.02);
    }

    /* Inputs */
    .stTextInput>div>div>input,
    .stTextArea textarea,
    .stSelectbox>div>div {
        background-color: #0D1117;
        color: #E6EDF3;
        border: 1px solid #30363D;
        border-radius: 6px;
    }

    /* JSON viewer */
    .stCodeBlock {
        background-color: #161B22 !important;
        border-radius: 6px;
    }

    /* Títulos */
    h1, h2, h3 {
        font-family: 'Segoe UI', sans-serif;
        font-weight: 700;
        color: #E6EDF3;
    }

    h4 {
        font-family: 'Segoe UI', sans-serif;
        font-weight: 500;
    }

</style>
""", unsafe_allow_html=True)

# --- INICIALIZACIÓN DEL ESTADO ---
if "transcripcion" not in st.session_state:
    st.session_state.transcripcion = []


# --- SIDEBAR ---
with st.sidebar:
    st.title("⚙️ Configuración")
    archivo_audio = st.file_uploader("1. Subir Audio", type=["wav", "mp3"])

    st.divider()
    modo_afi = st.toggle("🔮 Mostrar Modo Fonético (AFI)")

    opcion_modelo = st.selectbox(
    "Motor de transcripción",
    ["Whisper (preciso)", "Vosk (offline)"]
    )


    if st.button("🚀 Procesar con IA"):
        if archivo_audio:
            try:
                with st.spinner("La IA está escuchando y transcribiendo..."):
                    logging.info(f"Usuario subió archivo: {archivo_audio.name}")

                    # Guardar temporalmente
                    with open("temp_audio.wav", "wb") as f:
                        f.write(archivo_audio.getbuffer())

                    if opcion_modelo == "Whisper (preciso)":
                        resultado = transcribir_audio("temp_audio.wav")
                        texto = resultado["texto"]
                        segmentos = resultado["segmentos"]

                        # Conversión Whisper → tu formato
                        resultado_real = []
                        for seg in segmentos:
                            if "words" not in seg:
                                logging.warning("Segmento sin 'words', usando texto completo.")
                                palabras = seg["text"].split()
                                for p in palabras:
                                    resultado_real.append({
                                        "word": p,
                                        "start": round(seg["start"], 2),
                                        "afi": texto_a_afi(p)
                                    })
                                continue

                            for w in seg["words"]:
                                palabra = w["word"]
                                palabra_corregida = aplicar_correcciones(palabra)
                                resultado_real.append({
                                    "word": palabra_corregida,
                                    "start": round(w["start"], 2),
                                    "afi": texto_a_afi(palabra_corregida)
                                })

                    else:
                        from src.vosk_engine import transcribir_vosk
                        resultado = transcribir_vosk("temp_audio.wav")

                        resultado_real = []

                        if resultado["palabras"]:
                            # Caso normal (si algún día hay palabras)
                            for w in resultado["palabras"]:
                                palabra = w["word"]
                                palabra_corregida = aplicar_correcciones(palabra)
                                resultado_real.append({
                                    "word": palabra_corregida,
                                    "start": w.get("start", 0),
                                    "afi": texto_a_afi(palabra_corregida)
                                })
                        else:
                            # Fallback: dividir el texto en palabras
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
                st.rerun()

            except Exception as e:
                logging.error(f"Error procesando audio: {str(e)}")
                st.error("❌ Hubo un problema procesando el audio.")
        else:
            st.error("Primero debes subir un archivo de audio.")

# --- CUERPO PRINCIPAL ---
st.title("🎙️ IA Audio Editor & Phonetic Viewer")
st.info("Haz clic en las palabras para sincronizar el audio o edita el texto directamente abajo.")

col1, col2 = st.columns([2, 1])

# ============================
#   COLUMNA IZQUIERDA (Editor)
# ============================
with col1:
    st.subheader("📝 Editor de Transcripción")

    if archivo_audio:
        st.audio(archivo_audio)
    else:
        st.warning("Pista: Sube un audio en la izquierda para activar el reproductor.")

    st.write("---")

    # --- VISUALIZACIÓN DE PALABRAS COMO BOTONES ---
    st.write("Visualización de segmentos:")

    if st.session_state.transcripcion:
        espacio_texto = st.container()
        with espacio_texto:
            cols = st.columns(8)
            for idx, item in enumerate(st.session_state.transcripcion):
                mostrar = item["afi"] if modo_afi else item["word"]
                if cols[idx % 8].button(mostrar, key=f"btn_{idx}"):
                    st.info(f"⏱️ Marca de tiempo: {item['start']}s | AFI: {item['afi']}")
    else:
        st.info("Aún no hay transcripción disponible.")

    st.write("---")

    # --- EDICIÓN REACTIVA ---
    if st.session_state.transcripcion:
        texto_para_editar = " ".join([w["word"] for w in st.session_state.transcripcion])

        nuevo_texto = st.text_area(
            "📝 Corrección manual (Edita y pulsa Ctrl+Enter para actualizar):",
            value=texto_para_editar,
            height=150
        )

        # Si el texto cambió, procesamos la edición
        if nuevo_texto != texto_para_editar:
            palabras_nuevas = nuevo_texto.split()
            original = st.session_state.transcripcion
            nueva_lista = []

            es_seguro_entrenar = len(palabras_nuevas) == len(original)

            for i, p_word in enumerate(palabras_nuevas):
                if i < len(original):
                    st_time = original[i]["start"]

                    # ENTRENAMIENTO SEGURO
                    if es_seguro_entrenar:
                        palabra_vieja = original[i]["word"]
                        if p_word.lower() != palabra_vieja.lower():
                            guardar_correccion(palabra_vieja, p_word)
                            logging.info(f"Corrección aprendida: {palabra_vieja} → {p_word}")

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
#   COLUMNA DERECHA (JSON)
# ============================
with col2:
    st.subheader("📊 Metadatos JSON")
    st.write("Estructura de datos en tiempo real:")

    st.json(st.session_state.transcripcion)

    st.divider()
    st.subheader("📥 Gestión de Resultados")

    # 1. Nombre del archivo con timestamp
    timestamp_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_archivo = f"sesion_{timestamp_str}.json"
    json_string = json.dumps(st.session_state.transcripcion, indent=4, ensure_ascii=False)

    # 2. BOTÓN DE DESCARGA
    st.download_button(
        label="💾 Descargar para entregar",
        data=json_string,
        file_name=nombre_archivo,
        mime="application/json"
    )

    # 3. GUARDADO AUTOMÁTICO EN /docs
    if st.button("📁 Guardar copia local en /docs"):
        try:
            subcarpeta = os.path.join("docs", "sesiones")
            if not os.path.exists(subcarpeta):
                os.makedirs(subcarpeta)
                st.info(f"Carpeta {subcarpeta} creada con éxito.")

            ruta_local = os.path.join(subcarpeta, nombre_archivo)

            with open(ruta_local, "w", encoding="utf-8") as f:
                f.write(json_string)

            logging.info(f"Archivo guardado en: {ruta_local}")
            st.success(f"✅ Guardado en: {ruta_local}")

        except Exception as e:
            logging.error(f"Error guardando archivo: {str(e)}")
            st.error(f"❌ Error al guardar: {e}")

    # --- FOOTER PROFESIONAL ---
    st.markdown(
        """
        <style>

            /* Animación de brillo suave */
            @keyframes glow {
                0%   { text-shadow: 0 0 2px #6EA8FE; }
                50%  { text-shadow: 0 0 8px #6EA8FE; }
                100% { text-shadow: 0 0 2px #6EA8FE; }
            }

            .footer-phono {
                text-align: center;
                color: #8B949E;
                font-size: 14px;
                padding: 10px 0;
                margin-top: 20px;
                opacity: 0;
                animation: fadeIn 1.2s ease-out forwards;
            }

            /* Fade-in suave */
            @keyframes fadeIn {
                0% { opacity: 0; transform: translateY(5px); }
                100% { opacity: 1; transform: translateY(0); }
            }

            /* Solo el nombre y el título brillan */
            .footer-phono strong {
                color: #E6EDF3;
                animation: glow 3s ease-in-out infinite;
            }

        </style>

        <hr style="margin-top: 40px; border-color: #30363D;">

        <div class="footer-phono">
            <p style="margin: 0;">
                <strong>PhonoSyncAI</strong> · TFG DAM · 2026
            </p>
            <p style="margin: 0;">
                Desarrollado por <strong>Justina Araneda Rodríguez</strong>
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )


