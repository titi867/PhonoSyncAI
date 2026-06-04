# PhonoSync AI 🎙️✨

## Sistema de Transcripción, Sincronización y Análisis Fonético Asistido por IA

> *"Las voces no mienten."*
> Una herramienta diseñada para transformar audio en información útil, clara y clínicamente relevante.

---

## 🌟 Descripción General

**PhonoSync AI** es una aplicación interactiva desarrollada como Trabajo Final de Grado (TFG) en **Desarrollo de Aplicaciones Multiplataforma (DAM)**.

Su objetivo es facilitar el trabajo de profesionales de la **Fonoaudiología**, **Logopedia** y **Lingüística** mediante:

* Transcripción automática de audio
* Conversión fonética al AFI
* Visualización segmentada e interactiva
* Sincronización con marcas temporales
* Análisis fonológico y prosódico *(mockups funcionales)*
* Exportación de resultados en formato JSON

El sistema combina **Inteligencia Artificial**, diseño accesible y una arquitectura modular que permite futuras ampliaciones.

---

## 🚀 Características Principales

* 🎯 Transcripción de alta precisión mediante OpenAI Whisper.
* 🔤 Conversión fonética automática con el módulo `afi_tools`.
* 🖥️ Segmentación visual interactiva usando HTML + CSS + `st.html()` para un control total del layout.
* 🔄 Modo AFI para alternar entre texto ortográfico y fonético.
* ✏️ Edición manual sincronizada con preservación de timestamps.
* 📊 Análisis fonológico y prosódico *(mockups dinámicos)*.
* 📁 Exportación JSON para uso clínico, educativo o investigativo.
* 🌐 Compatibilidad multiplataforma gracias a Streamlit.

---

## 🛠️ Stack Tecnológico

### Lenguaje

* Python 3.10+

### Inteligencia Artificial

* OpenAI Whisper
* Vosk (modo offline)

### Frontend

* Streamlit

### Procesamiento de Audio

* FFmpeg
* SoundFile

### Persistencia

* JSON

### Arquitectura

* Separación modular entre interfaz, lógica de negocio y motores de IA

---

## ⚙️ Instalación y Uso

### 1. Requisitos previos

Instalar FFmpeg:

#### Windows

```bash
choco install ffmpeg
```

#### macOS

```bash
brew install ffmpeg
```

#### Linux

```bash
sudo apt update
sudo apt install ffmpeg
```

### 2. Clonar el repositorio

```bash
git clone https://github.com/titi867/PhonoSyncAI.git
cd PhonoSyncAI
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Ejecutar la aplicación

```bash
streamlit run app.py
```

La aplicación estará disponible en:

```text
http://localhost:8501
```

---

## 📂 Estructura del Proyecto

```text
PhonoSyncAI/
├── app.py
├── src/
│   ├── afi_tools.py
│   ├── engine.py
│   ├── vosk_engine.py
│   └── utils.py
├── docs/
│   ├── sesiones/
│   └── ...
├── correcciones.json
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

### Descripción

| Archivo / Carpeta      | Función                              |
| ---------------------- | ------------------------------------ |
| `app.py`               | Interfaz principal en Streamlit      |
| `afi_tools.py`         | Conversión fonética al AFI           |
| `engine.py`            | Motor de transcripción Whisper       |
| `vosk_engine.py`       | Motor alternativo offline            |
| `utils.py`             | Utilidades y gestión de correcciones |
| `docs/`                | Documentación técnica y sesiones     |
| `correcciones.json`    | Correcciones aprendidas              |
| `requirements.txt`     | Dependencias de producción           |
| `requirements-dev.txt` | Dependencias de desarrollo           |

---

## 🧠 Nota Técnica

Para garantizar estabilidad y reproducibilidad:

* Se fijaron versiones específicas de Whisper, Torch, Streamlit y Vosk.
* Se incluyó explícitamente `soundfile` para la lectura de audio.
* Se añadió `vosk` para permitir un motor alternativo más ligero.
* Se utilizó `st.html()` para renderizar HTML puro dentro de Streamlit, evitando las limitaciones de `st.markdown()` y permitiendo un grid visual totalmente controlado para los segmentos.

---

## 🎯 Motivación y Visión

Este proyecto nace de más de **15 años de experiencia en Fonoaudiología y Logopedia**.

**PhonoSync AI** busca:

* Optimizar el tiempo de los profesionales.
* Automatizar tareas repetitivas.
* Facilitar el análisis fonético y prosódico.
* Servir como base para herramientas clínicas más avanzadas.

### Futuras líneas de desarrollo

* 🔍 Detección automática de Procesos de Simplificación Fonológica (PSF).
* 🎤 Análisis forense de la voz.
* 📈 Modelos de prosodia más precisos.
* 🗄️ Integración con bases de datos clínicas.

---

## 👩‍💻 Autora

**Justina Araneda Rodríguez**  
Fonoaudióloga · Desarrolladora DAM  
🔗 [LinkedIn](https://www.linkedin.com/in/justinaaranedarodriguez/)

---

## ⚖️ Licencia

Este proyecto se distribuye bajo la **Licencia MIT**.

Consulta el archivo `LICENSE` para más detalles.
