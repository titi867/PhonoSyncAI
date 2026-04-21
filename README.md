# PhonoSync AI 🎙️✨

> **"Voices don't lie"** – Un sistema inteligente de transcripción, sincronización y análisis fonético.

**PhonoSync AI** es una aplicación multiplataforma diseñada para cerrar la brecha entre la captura de audio y el análisis clínico/lingüístico. Desarrollada como Proyecto Final de Grado (TFG) en **Desarrollo de Aplicaciones Multiplataforma (DAM)** esta herramienta utiliza modelos de Inteligencia Artificial para ofrecer una experiencia de transcripción interactiva y precisa.

## 🚀 Características Principales

* **Transcripción Robusta:** Integración con el modelo **OpenAI Whisper** para una conversión de audio a texto de alta precisión, incluso en entornos con ruido.
* **Motor Fonético Interactivo:** Conversión automática de la transcripción al **Alfabeto Fonético Internacional (AFI)** mediante el módulo especializado `afi_tools`.
* **Sincronización Bidireccional:** Interfaz diseñada en **Streamlit** que permite la edición de texto con persistencia de metadatos temporales (*timestamps*).
* **Interoperabilidad:** Exportación de resultados en formato **JSON**, facilitando su integración en flujos de trabajo educativos, clínicos o de investigación.

## 🛠️ Stack Tecnológico

* **Lenguaje:** Python (Certificación PCAP).
* **IA/ML:** OpenAI Whisper.
* **Frontend:** Streamlit.
* **Formatos de Datos:** JSON para persistencia y metadatos.

## ⚙️ Instalación y Uso

Sigue estos pasos para ejecutar **PhonoSync AI** en tu entorno local:

### 1. Requisitos previos
Es necesario tener instalado **FFmpeg** en el sistema para que Whisper pueda procesar los archivos de audio:
* **Windows (con Chocolatey):** `choco install ffmpeg`
* **macOS (con Homebrew):** `brew install ffmpeg`
* **Linux:** `sudo apt update && sudo apt install ffmpeg`

### 2. Clonar el proyecto
git clone [https://github.com/titi867/PhonoSyncAI.git](https://github.com/titi867/PhonoSyncAI.git)
cd PhonoSyncAI

### 3. Instalar las librerías necesarias
pip install -r requirements.txt

# Asegúrate de estar en la carpeta raíz del proyecto
streamlit run app.py

## 📂 Estructura del Proyecto

El proyecto sigue una arquitectura modular para separar la lógica de negocio de la interfaz de usuario:

```text
PhonoSyncAI/
├── app.py                # Punto de entrada de la aplicación (Streamlit)
├── src/                  # Código fuente del sistema
│   ├── __init__.py       # Inicialización de módulo
│   ├── afi_tools.py      # Motor de conversión fonética (AFI)
│   ├── engine.py         # Integración con el modelo Whisper
│   └── utils.py          # Funciones auxiliares y gestión de archivos
├── docs/                 # Documentación técnica y sesiones guardadas
├── requirements.txt      # Dependencias del sistema
└── README.md             # Documentación principal
```

## 🎯 Motivación y Visión
Este proyecto nace de una trayectoria de más de 15 años en el ámbito de la Fonoaudiología y la Logopedia. PhonoSync AI busca optimizar el tiempo de los profesionales, permitiendo que la tecnología se encargue del procesamiento pesado (transcripción y fonética base) para que el experto pueda centrarse en el diagnóstico y la intervención clínica.

A futuro, el sistema está diseñado para escalar hacia la detección automática de Procesos de Simplificación Fonológica (PSF) y herramientas de análisis forense de la voz.

<https://www.linkedin.com/in/justinaaranedarodriguez/>

## ⚖️ Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.
