from dotenv import load_dotenv
load_dotenv()
from utils.audio_processor import process_input
from core.transcriber import transcribe_all
import os

source = "https://www.youtube.com/watch?v=iVo3LfZti5w"
language = "hinglish"

chunks = process_input(source)
transcript = transcribe_all(chunks, language=language)

print(transcript)