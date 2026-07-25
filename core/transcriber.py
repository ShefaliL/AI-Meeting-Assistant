import math
import os
import subprocess
import wave

import requests
import whisper

# Sarvam's sync STT-translate API rejects audio longer than 30s.
# We slice each chunk into 25s pieces (with a 5s safety margin) before sending.
SARVAM_PIECE_SECONDS = 25


WHISPER_MODEL = os.getenv("WHISPER_MODEL", "base")


SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")
SARVAM_STT_TRANSLATE_URL = "https://api.sarvam.ai/speech-to-text"
SARVAM_MODEL = os.getenv("SARVAM_STT_MODEL", "saaras:v3")

_model = None


def load_model():

    global _model  

    if _model is None: 
        print(f"Loading Whisper model: {WHISPER_MODEL} ...")
        _model = whisper.load_model(WHISPER_MODEL) 
        print("Whisper model loaded.")
    return _model 


def transcribe_chunk_whisper(chunk_path: str) -> str:

    model = load_model()  

    result = model.transcribe(
        chunk_path,
        task="transcribe",
        language="en",
    )  
    return result["text"]  


def _send_to_sarvam(piece_path: str) -> str:
    """Send one ≤30s WAV file to Sarvam and return the English transcript."""
    headers = {"api-subscription-key": SARVAM_API_KEY}

    with open(piece_path, "rb") as f:
        files = {"file": (os.path.basename(piece_path), f, "audio/wav")}
        data = {"model": SARVAM_MODEL, "mode": "translate", "with_diarization": "false"}
        response = requests.post(
            SARVAM_STT_TRANSLATE_URL,
            headers=headers,
            files=files,
            data=data,
            timeout=120,
        )

    if not response.ok:
        print(f"\n❌ Sarvam returned {response.status_code}")
        print(f"Response body: {response.text}\n")
        response.raise_for_status()

    return response.json().get("transcript", "")


def _run_ffmpeg(args):
    result = subprocess.run(["ffmpeg", *args], capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or "ffmpeg failed")


def _get_audio_duration_seconds(input_file: str) -> float:
    with wave.open(input_file, "rb") as wav_file:
        frames = wav_file.getnframes()
        rate = wav_file.getframerate()
        return frames / float(rate)


def transcribe_chunk_sarvam(chunk_path: str) -> str:
    """
    Sarvam sync API only accepts ≤30s audio. We split this chunk into
    25-second pieces, send each separately, and join the transcripts.
    """
    if not SARVAM_API_KEY:
        raise RuntimeError("SARVAM_API_KEY is not set in environment / .env")

    duration_seconds = _get_audio_duration_seconds(chunk_path)
    total_pieces = max(1, math.ceil(duration_seconds / SARVAM_PIECE_SECONDS))

    full_text = ""
    for i in range(total_pieces):
        start_seconds = i * SARVAM_PIECE_SECONDS
        end_seconds = min(start_seconds + SARVAM_PIECE_SECONDS, duration_seconds)
        piece_path = f"{chunk_path}_sv_{i}.wav"
        _run_ffmpeg(["-y", "-i", chunk_path, "-ss", str(start_seconds), "-to", str(end_seconds), "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le", piece_path])

        try:
            print(f"  → Sarvam piece {i + 1}/{total_pieces} ...")
            full_text += _send_to_sarvam(piece_path) + " "
        finally:
            if os.path.exists(piece_path):
                os.remove(piece_path)

    return full_text.strip()


def transcribe_chunk(chunk_path: str, language: str = "english") -> str:
    """
    Route one chunk to Whisper or Sarvam depending on language choice.
    - english  → Whisper (local model)
    - hinglish → Sarvam (translates to English while transcribing)
    If Sarvam is not configured, fall back to local Whisper.
    """
    if language.lower() == "hinglish":
        if not SARVAM_API_KEY:
            print("SARVAM_API_KEY not set; falling back to local Whisper transcription.")
            return transcribe_chunk_whisper(chunk_path)
        return transcribe_chunk_sarvam(chunk_path)
    return transcribe_chunk_whisper(chunk_path)


def transcribe_all(chunks: list, language: str = "english") -> str:

    full_transcript = "" 

    engine = "Sarvam AI" if language.lower() == "hinglish" else "Whisper"
    print(f"Using {engine} for transcription.")

    for i, chunk in enumerate(chunks):  

        print(f"Transcribing chunk {i + 1}/{len(chunks)}...")

        text = transcribe_chunk(chunk, language=language)  

        full_transcript += text + " "  

    print("Transcription complete.")

    return full_transcript.strip()