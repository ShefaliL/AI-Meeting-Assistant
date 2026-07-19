import os
import subprocess
import sys
from typing import List

import yt_dlp

DOWNLOAD_DIRECTORY = "downloads"
os.makedirs(DOWNLOAD_DIRECTORY, exist_ok=True)


def _run_ffmpeg(args: List[str]) -> None:
    result = subprocess.run(["ffmpeg", *args], capture_output=True, text=True)
    if result.returncode != 0:
        error_output = (result.stderr or result.stdout or "ffmpeg failed").strip()
        raise RuntimeError(error_output)


def _get_audio_duration_seconds(input_file: str) -> float:
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", input_file],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "Unable to determine audio duration")
    return float(result.stdout.strip())


def download_yt_audio(url: str) -> str:
    output_path = os.path.join(DOWNLOAD_DIRECTORY, "%(title)s.%(ext)s")
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_path,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
                "preferredquality": "192",
            }
        ],
        "quiet": True,
        "noplaylist": True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            if not info:
                raise RuntimeError("No metadata was returned for the provided URL.")

            title = info.get("title", "audio")
            sanitized_title = "".join(ch if ch.isalnum() or ch in "._- " else "_" for ch in title)
            candidates = [
                os.path.join(DOWNLOAD_DIRECTORY, f"{sanitized_title}.wav"),
                os.path.join(DOWNLOAD_DIRECTORY, f"{sanitized_title}.m4a"),
                os.path.join(DOWNLOAD_DIRECTORY, f"{sanitized_title}.webm"),
            ]
            for candidate in candidates:
                if os.path.exists(candidate):
                    return candidate

            files = [
                os.path.join(DOWNLOAD_DIRECTORY, f)
                for f in os.listdir(DOWNLOAD_DIRECTORY)
                if os.path.isfile(os.path.join(DOWNLOAD_DIRECTORY, f))
            ]
            if files:
                newest_file = max(files, key=os.path.getmtime)
                return newest_file

            raise FileNotFoundError("No downloaded audio file was found on disk.")
    except Exception as exc:
        raise RuntimeError(f"Could not download audio from YouTube URL: {exc}") from exc


def convert_audio_to_wav(input_file: str) -> str:
    """Convert an audio file to WAV format using ffmpeg."""
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file not found: {input_file}")

    output_path = os.path.splitext(input_file)[0] + "_converted.wav"
    _run_ffmpeg(["-y", "-i", input_file, "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le", output_path])
    return output_path


def split_audio_into_chunks(wav_path: str, chunk_duration: int = 10) -> List[str]:
    duration_seconds = _get_audio_duration_seconds(wav_path)
    chunk_duration_seconds = max(1, chunk_duration * 60)
    total_chunks = max(1, int(duration_seconds // chunk_duration_seconds) + (1 if duration_seconds % chunk_duration_seconds else 0))

    chunks = []
    for i in range(total_chunks):
        start_seconds = i * chunk_duration_seconds
        end_seconds = min(start_seconds + chunk_duration_seconds, duration_seconds)
        chunk_path = f"{wav_path}_chunk_{i}.wav"
        _run_ffmpeg(["-y", "-i", wav_path, "-ss", str(start_seconds), "-to", str(end_seconds), "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le", chunk_path])
        chunks.append(chunk_path)
    return chunks


def process_input(source: str) -> List[str]:
    try:
        if source.startswith("http://") or source.startswith("https://"):
            print("Detected YouTube URL. Downloading audio...")
            wav_path = download_yt_audio(source)
        else:
            print("Detected local file. Converting to WAV...")
            wav_path = convert_audio_to_wav(source)

        print("Chunking audio...")
        chunks = split_audio_into_chunks(wav_path)
        print(f"Audio ready — {len(chunks)} chunk(s) created.")
        return chunks
    except Exception as exc:
        print(f"Audio processing failed: {exc}")
        return []


if __name__ == "__main__":
    source = sys.argv[1] if len(sys.argv) > 1 else "https://youtu.be/185XGEMefgc?si=V3-SHPvy7dpQ2bRp"
    print(process_input(source))