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
    # Limpiamos ambas palabras antes de guardarlas
    original = limpiar_palabra(palabra_original)
    corregida = limpiar_palabra(palabra_corregida)
    
    # Si alguna se quedó vacía al limpiar, no hacemos nada
    if not original or not corregida:
        return
    
    correcciones = cargar_correcciones()
    correcciones[original] = corregida
    
    with open(ARCHIVO_CORRECCIONES, "w", encoding="utf-8") as f:
        json.dump(correcciones, f, indent=4, ensure_ascii=False) # Guarda con formato legible y soporte para caracteres especiales.

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