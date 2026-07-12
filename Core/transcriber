from numba import none
import whisper
import os


WHISPER_MODEL = os.getenv("WHISPER_MODEL", "base")  # Default to "base" if not set
_model = none

def load_model():
    global _model
    if _model is none: #if model is not loaded yet, then load it
        print(f"Loading model...")
        _model = whisper.load_model(WHISPER_MODEL)
        print(f"Whisper Model loaded successfully.")
    return _model

def transcribe_chunk(chunk_path:str ,translate:bool=False) -> str: #transcribe the audio chunk using whisper model into transribtion text
    model = load_model()
    task = "translate" if translate else "transcribe" #turnary operator to check if translate is true or false, if true then translate else transcribe
    result = model.transcribe(chunk_path)
    return result["text"]

# def transcribe_all(chunks:list ,translate:bool=False) -> str:
#     fulltranscriptions = []
#     for chunk in chunks:
#         transcription = transcribe_chunk(chunk, translate)
#         fulltranscriptions.append(transcription)
#     return " ".join(fulltranscriptions)