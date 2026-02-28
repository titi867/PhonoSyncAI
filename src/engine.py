import whisper

def transcribir_audio(ruta_audio):
    model = whisper.load_model("base")
    result = model.transcribe(ruta_audio, word_timestamps=True, fp16=False)
    
    palabras_listas = []
    for segment in result['segments']:
        for word_data in segment['words']:
            palabras_listas.append({
                "word": word_data['word'],
                "start": word_data['start'],
                "end": word_data['end'],
                "afi": "" 
            })
    return palabras_listas