import re

def texto_a_afi(texto):
    """
    Convierte texto en español a una representación fonética básica (AFI).
    """
    if not texto:
        return ""
    
    # Convertimos a minúsculas para procesar
    fon = texto.lower()
    
    # --- Reglas de Sustitución Fonética ---
    # (El orden importa para no romper diígrafos)
    
    # Consonantes complejas
    fon = fon.replace('ll', 'ʎ')
    fon = fon.replace('ch', 'tʃ')
    fon = fon.replace('qu', 'k')
    fon = fon.replace('que', 'ke').replace('qui', 'ki')
    fon = fon.replace('gu', 'g')
    
    # Grafemas con sonidos específicos
    fon = fon.replace('v', 'b')
    fon = fon.replace('z', 'θ')
    fon = re.sub(r'c([eiéí])', r'θ\1', fon) # c ante e, i
    fon = fon.replace('c', 'k') # resto de c
    
    fon = fon.replace('h', '') # la h es muda
    fon = fon.replace('j', 'x')
    fon = re.sub(r'g([eiéí])', r'x\1', fon) # g ante e, i
    
    fon = fon.replace('y', 'j') # y como semiconsonante
    fon = fon.replace('ñ', 'ɲ')

    # El sonido /b/ (v y b son iguales en AFI para español)
    fon = fon.replace('v', 'b')
    fon = fon.replace('b', 'b')
    
    # La r fuerte (al principio o rr)
    fon = re.sub(r'^r', 'r̄', fon)
    fon = fon.replace('rr', 'r̄')
    
    return f"/{fon}/"