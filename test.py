from dotenv import load_dotenv

load_dotenv()

from utils.audio_processor import process_input
from core.transcriber import transcribe_all

source = "https://www.youtube.com/watch?v=iVo3LfZti5w"
language = "hinglish"

chunks = process_input(source)
if not chunks:
    print("No audio chunks were produced, so transcription was skipped.")
else:
    transcript = transcribe_all(chunks, language=language)
    print(transcript)

# Run with the newer environment:
# /Users/shefaliluley/Desktop/AI-Meeting-Assistantnv-py314/bin/python test.py
