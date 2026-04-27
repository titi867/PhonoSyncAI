import logging
import config
from typing import List


def texto_a_afi(palabra: str) -> str:
    """Convierte una palabra en su transcripción fonética AFI.

    Esta función aplica reglas fonéticas simplificadas del español
    para generar una representación aproximada en AFI.

    Args:
        palabra: Palabra en texto plano.

    Returns:
        Cadena con la transcripción AFI correspondiente.
        Si la palabra no es válida, devuelve la palabra original.
    """
    if not isinstance(palabra, str) or not palabra.strip():
        logging.warning(f"Entrada inválida en texto_a_afi: {palabra}")
        return palabra

    palabra_norm = palabra.lower().strip()

    try:
        afi = convertir_a_afi(palabra_norm)
        logging.info(f"AFI generado: {palabra_norm} → {afi}")
        return afi
    except Exception as e:
        logging.error(f"Error generando AFI para '{palabra}': {str(e)}")
        return palabra


def convertir_a_afi(palabra: str) -> str:
    """Aplica reglas fonéticas básicas del español.

    Esta función es interna y contiene las reglas de conversión.
    Se puede ampliar en el futuro para mayor precisión.

    Args:
        palabra: Palabra normalizada.

    Returns:
        Transcripción AFI aproximada.
    """
    # Reglas fonéticas mejoradas
    reglas = [
        ("ll", "ʎ"),
        ("ch", "tʃ"),
        ("rr", "r"),
        ("r", "ɾ"),

        # Nuevas reglas intermedias
        ("qu", "k"),
        ("que", "ke"),
        ("qui", "ki"),
        ("gue", "ge"),
        ("gui", "gi"),

        ("ce", "θe"),
        ("ci", "θi"),
        ("z", "θ"),

        ("j", "x"),
        ("ge", "xe"),
        ("gi", "xi"),

        ("v", "b"),
        ("h", ""),      # muda
        ("y", "ʝ"),     # consonante
        ("x", "ks"),
    ]


    afi = palabra
    for origen, destino in reglas:
        afi = afi.replace(origen, destino)

    return f"/{afi}/"
