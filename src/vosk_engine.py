import json
import logging
from vosk import Model, KaldiRecognizer
import wave

# Cargar el modelo UNA sola vez
vosk_model = Model("modelos/vosk-es")

def transcribir_vosk(ruta_audio: str) -> dict:
    """Transcripción mínima usando Vosk (offline y ligero)."""

    try:
        # Abrimos el audio SOLO UNA VEZ
        wf = wave.open(ruta_audio, "rb")

        # Inicializamos el reconocedor
        rec = KaldiRecognizer(vosk_model, wf.getframerate())

        texto = ""
        palabras = []

        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break

            if rec.AcceptWaveform(data):
                resultado = json.loads(rec.Result())
                texto += " " + resultado.get("text", "")

                if "result" in resultado:
                    for w in resultado["result"]:
                        palabras.append({
                            "word": w["word"],
                            "start": w.get("start", 0),
                            "end": w.get("end", 0)
                        })

        # resultado final
        final = json.loads(rec.FinalResult())
        texto += " " + final.get("text", "")

        print("DEBUG VOSK:", {
            "texto": texto.strip(),
            "palabras": palabras
        })

        return {
            "texto": texto.strip(),
            "palabras": palabras
        }

    except Exception as e:
        logging.error(f"Error en transcribir_vosk: {e}")
        return {"texto": "", "palabras": []}
