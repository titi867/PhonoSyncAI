import json
import os
import re

ARCHIVO_CORRECCIONES = "correcciones.json"

def limpiar_palabra(palabra):
    """
    Quita espacios, comas, puntos y símbolos raros a los lados de la palabra.
    Así guardamos 'paco' puro, en lugar de 'paco,' o ' paco '.
    """
    return palabra.lower().strip(" .,;!?\n\r")

def cargar_correcciones():
    if not os.path.exists(ARCHIVO_CORRECCIONES):
        return {}
    
    with open(ARCHIVO_CORRECCIONES, "r", encoding="utf-8") as f:
        return json.load(f)

def guardar_correccion(palabra_original, palabra_corregida):
    # Limpiar
    original = limpiar_palabra(palabra_original)
    corregida = limpiar_palabra(palabra_corregida)

    # 1. No guardar si están vacías
    if not original or not corregida:
        return

    # 2. No guardar si son iguales
    if original == corregida:
        return

    # 3. No guardar palabras funcionales
    palabras_funcionales = {"la", "el", "de", "que", "y", "a", "en", "un", "una", "se"}
    if original in palabras_funcionales:
        return

    # 4. No guardar si la corrección cambia demasiado la palabra
    # (evita cosas como "pio" → "rápido")
    if abs(len(original) - len(corregida)) > 3:
        return

    # 5. No guardar si la corrección no parece un error ortográfico
    # (evita errores fonológicos infantiles)
    if original[0] != corregida[0]:
        return

    # 6. Cargar correcciones existentes
    try:
        correcciones = cargar_correcciones()
    except:
        correcciones = {}

    # 7. Guardar corrección segura
    correcciones[original] = corregida

    with open(ARCHIVO_CORRECCIONES, "w", encoding="utf-8") as f:
        json.dump(correcciones, f, indent=4, ensure_ascii=False)


def aplicar_correcciones(palabra_whisper):
    correcciones = cargar_correcciones()
    if not correcciones:
        return palabra_whisper
    
    # Limpiamos la palabra que viene de Whisper para buscarla en el diccionario
    limpia = limpiar_palabra(palabra_whisper)
    
    if limpia in correcciones:
        palabra_nueva = correcciones[limpia]
        
        # Hacemos el reemplazo manteniendo cualquier coma o punto que tuviera la original.
        # Por ejemplo, si Whisper trajo "Paco," y la IA sabe que es "pato", devuelve "pato,"
        patron = re.compile(re.escape(limpia), re.IGNORECASE)
        return patron.sub(palabra_nueva, palabra_whisper)
        
    return palabra_whisper