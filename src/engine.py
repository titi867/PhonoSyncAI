import json
import whisper
import soundfile as sf
from typing import Dict, Any
import logging
import os


def inicializar_whisper(tipo_modelo="base"):
    # Definimos la ruta relativa exacta donde queremos que viva el modelo
    # Esto apuntará a la carpeta /modelos/whisper/ en la raíz de tu proyecto
    ruta_modelos = os.path.join(os.getcwd(), "modelos", "whisper")
    
    # Creamos la carpeta automáticamente si aún no existe
    os.makedirs(ruta_modelos, exist_ok=True)
    
    print(f"Cargando modelo '{tipo_modelo}' desde: {ruta_modelos}...")
    
    # Al pasar download_root, Whisper lo descarga ahí la primera vez.
    # Las siguientes veces, detecta que ya existe y lo carga en milisegundos de forma 100% offline.
    modelo = whisper.load_model(tipo_modelo, download_root=ruta_modelos)
    
    return modelo

# Prueba rápida
if __name__ == "__main__":
    motor = inicializar_whisper("base")
    print("✅ ¡Misión cumplida! Modelo configurado en local.")

def transcribir_audio(ruta_audio: str, modelo: str = "small") -> Dict[str, Any]:
    """Transcribe un archivo de audio y devuelve texto y marcas temporales.

    Usa el modelo Whisper especificado para procesar el archivo de audio y
    generar una transcripción segmentada con timestamps.

    Args:
        ruta_audio: Ruta al archivo de audio (.wav o .mp3).
        modelo: Nombre del modelo Whisper a utilizar.

    Returns:
        Diccionario con:
            - "texto": transcripción completa.
            - "segmentos": lista de segmentos con inicio, fin y texto.

    Raises:
        FileNotFoundError: Si el archivo no existe.
        RuntimeError: Si Whisper falla durante la transcripción.
        ValueError: Si el archivo no contiene audio válido.
    """
    logging.info(f"Validando archivo de audio: {ruta_audio}")

    # Validación del archivo
    try:
        sf.info(ruta_audio)
    except Exception:
        logging.error("El archivo no contiene audio válido o está corrupto.")
        raise ValueError("El archivo no contiene audio válido o está corrupto.")

    # Transcripción
    try:
        logging.info(f"Cargando modelo Whisper: {modelo}")
        model = inicializar_whisper(modelo)

        logging.info("Iniciando transcripción...")
        resultado = model.transcribe(
            ruta_audio,
            word_timestamps=True
        )

        logging.info("Transcripción completada correctamente.")

        return {
            "texto": resultado.get("text", "").strip(),
            "segmentos": resultado.get("segments", []),
        }

    except FileNotFoundError:
        logging.error(f"No se encontró el archivo: {ruta_audio}")
        raise

    except Exception as e:
        logging.error(f"Error durante la transcripción: {str(e)}")
        raise RuntimeError(f"Error durante la transcripción: {str(e)}")

def generar_salida_json(datos: Dict[str, Any], ruta_salida: str) -> None:
    """Genera un archivo JSON con la transcripción procesada.

    Args:
        datos: Diccionario con texto, fonética, timestamps y metadatos.
        ruta_salida: Ruta donde se guardará el archivo JSON.

    Raises:
        OSError: Si ocurre un error al escribir el archivo.
        ValueError: Si los datos no tienen el formato esperado.
    """
    logging.info(f"Generando archivo JSON en: {ruta_salida}")

    if not isinstance(datos, dict):
        logging.error("Los datos proporcionados no son un diccionario.")
        raise ValueError("Los datos deben ser un diccionario.")

    try:
        with open(ruta_salida, "w", encoding="utf-8") as f:
            json.dump(datos, f, ensure_ascii=False, indent=4)
        
        logging.info("Archivo JSON guardado correctamente.")

    except Exception as e:
        logging.error(f"No se pudo escribir el archivo JSON: {str(e)}")        
        raise OSError(f"No se pudo escribir el archivo JSON: {str(e)}")