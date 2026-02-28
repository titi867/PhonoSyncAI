import datetime
import streamlit as st
import os
import json
import datetime

# Imports de lógica propia con manejo de errores
try:
    from src.afi_tools import texto_a_afi
    from src.engine import transcribir_audio
except ModuleNotFoundError:
    st.error("⚠️ Error crítico: No se encuentran los módulos en la carpeta /src. Revisa los nombres de los archivos.")
    st.stop()

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="IA Transcriptor Pro - TFG DAM", layout="wide")

# --- ESTILOS CUSTOM ---
st.markdown("""
    <style>
    .stButton>button {
        border-radius: 5px;
        padding: 5px 10px;
    }
    </style>
""", unsafe_allow_html=True)

# --- INICIALIZACIÓN DEL ESTADO ---
if 'transcripcion' not in st.session_state:
    st.session_state.transcripcion = [
        {"word": "Hola", "start": 0.5, "afi": "/ola/"},
        {"word": "mundo,", "start": 1.2, "afi": "/munde/"},
        {"word": "esta", "start": 1.5, "afi": "/esta/"},
        {"word": "es", "start": 1.8, "afi": "/es/"},
        {"word": "una", "start": 2.1, "afi": "/una/"},
        {"word": "interfaz", "start": 2.5, "afi": "/interfaθ/"},
        {"word": "inteligente.", "start": 3.2, "afi": "/intelixente/"},
    ]

# --- SIDEBAR (Panel de Control) ---
with st.sidebar:
    st.title("⚙️ Configuración")
    archivo_audio = st.file_uploader("1. Subir Audio", type=["wav", "mp3"])
    
    st.divider()
    modo_afi = st.toggle("🔮 Mostrar Modo Fonético (AFI)")
    
    if st.button("🚀 Procesar con IA"):
        if archivo_audio:
            with st.spinner("La IA está escuchando y transcribiendo..."):
                # 1. Guardar temporalmente
                with open("temp_audio.wav", "wb") as f:
                    f.write(archivo_audio.getbuffer())
                
                # 2. Motor Whisper
                resultado_real = transcribir_audio("temp_audio.wav")
                
                # 3. Enriquecer con AFI
                for p in resultado_real:
                    p['afi'] = texto_a_afi(p['word'])
                
                # 4. Guardar y limpiar
                st.session_state.transcripcion = resultado_real
                os.remove("temp_audio.wav")
                
                st.success("¡Análisis completado!")
                st.rerun()
        else:
            st.error("Primero debes subir un archivo de audio.")

# --- CUERPO PRINCIPAL ---
st.title("🎙️ IA Audio Editor & Phonetic Viewer")
st.info("Haz clic en las palabras para sincronizar el audio o edita el texto directamente abajo.")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📝 Editor de Transcripción")

    if archivo_audio:
        st.audio(archivo_audio)
    else:
        st.warning("Pista: Sube un audio en la izquierda para activar el reproductor.")

    st.write("---")
    
    # Contenedor de palabras (Botones)
    st.write("Visualización de segmentos:")
    espacio_texto = st.container()
    with espacio_texto:
        # Mostramos los botones en una cuadrícula fluida
        # Usamos columnas pequeñas para simular flujo de texto
        cols = st.columns(8) # Ajustable según diseño
        for idx, item in enumerate(st.session_state.transcripcion):
            mostrar = item['afi'] if modo_afi else item['word']
            # El botón se coloca en una de las 8 columnas usando módulo
            if cols[idx % 8].button(mostrar, key=f"btn_{idx}"):
                st.info(f"⏱️ Marca de tiempo: {item['start']}s | AFI: {item['afi']}")
                
    st.write("---")
    
    # --- LÓGICA DE EDICIÓN REACTIVA ---
    texto_para_editar = " ".join([w['word'] for w in st.session_state.transcripcion])
    
    nuevo_texto = st.text_area(
        "📝 Corrección manual (Edita y pulsa Ctrl+Enter para actualizar):", 
        value=texto_para_editar, 
        height=150
    )

    # Si el texto del área es diferente al que tenemos guardado, actualizamos
    if nuevo_texto != texto_para_editar:
        palabras_nuevas = nuevo_texto.split()
        nueva_lista = []
        original = st.session_state.transcripcion
        
        for i, p_word in enumerate(palabras_nuevas):
            # Lógica de asignación de tiempo:
            if i < len(original):
                # Si la palabra ya existía en esa posición, mantenemos su tiempo
                # (Nota: Esto asume corrección ortográfica, no inserción)
                st_time = original[i]['start']
            else:
                # Si es una palabra añadida al final, le damos el tiempo de la anterior + 0.3s
                st_time = nueva_lista[-1]['start'] + 0.3 if nueva_lista else 0.0
            
            nueva_lista.append({
                "word": p_word,
                "start": round(st_time, 2),
                "afi": texto_a_afi(p_word)
            })
        
        st.session_state.transcripcion = nueva_lista
        st.rerun()

with col2:
    with col2:
        st.subheader("📊 Metadatos JSON")
        st.write("Estructura de datos en tiempo real:")
        

    st.json(st.session_state.transcripcion)

    st.divider()
    st.subheader("📥 Gestión de Resultados")
    
    # 1. Preparar el nombre del archivo con fecha/hora
    timestamp_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_archivo = f"sesion_{timestamp_str}.json"
    json_string = json.dumps(st.session_state.transcripcion, indent=4, ensure_ascii=False)

    # 2. BOTÓN DE DESCARGA (Para el usuario/navegador)
    st.download_button(
        label="💾 Descargar para entregar",
        data=json_string,
        file_name=nombre_archivo,
        mime="application/json"
    )

    # 3. GUARDADO AUTOMÁTICO EN EL SERVIDOR (Copia local)
    if st.button("📁 Guardar copia local en /docs"):
        try:
            # Definimos la ruta de la subcarpeta
            subcarpeta = os.path.join("docs", "sesiones")
            
            # Verificamos/Creamos la carpeta antes de escribir
            if not os.path.exists(subcarpeta):
                os.makedirs(subcarpeta)
                st.info(f"Carpeta {subcarpeta} creada con éxito.")

            ruta_local = os.path.join(subcarpeta, nombre_archivo)
            
            with open(ruta_local, "w", encoding="utf-8") as f:
                f.write(json_string)
            
            st.success(f"✅ Guardado en: {ruta_local}")
        except Exception as e:
            st.error(f"❌ Error al guardar: {e}")
