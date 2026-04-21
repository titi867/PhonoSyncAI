import whisper

def transcribir_audio(ruta_audio):
    model = whisper.load_model("base") # Carga el modelo Whisper (existen otros tamaños como "small", "medium", "large")
    result = model.transcribe(ruta_audio, word_timestamps=True, fp16=False) # Transcribe el audio y obtiene las marcas de tiempo de cada palabra. 
    # fp16=False es para evitar problemas en CPU.
    
    palabras_listas = []
    for segment in result['segments']: # Cada segmento puede contener varias palabras, iteramos sobre ellas
        for word_data in segment['words']:
            palabras_listas.append({
                "word": word_data['word'],
                "start": word_data['start'],
                "end": word_data['end'],
                "afi": "" 
            })
    return palabras_listas