import yt_dlp
from pydub import AudioSegment
import os

DOWNLOAD_DIRECTORY = 'downloads'
os.makedirs(DOWNLOAD_DIRECTORY,exist_ok = True)
 
def download_yt_audio (url :str) -> str:
    output_path = os.path.join(DOWNLOAD_DIRECTORY, "%(title)s.%(ext)s")
    ydl_opts = {
        "format":"bestaudio/best",
        "outtmpl": output_path,
        "postprocessors":[
            { 
                "key": "FFmpegExtractAudio",
                "preferredcodec":"wav",
                "preferredquality": "192",
            }
        ],
        "quiet":True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url,download=True)
        filename = ydl.prepare_filename(info).replace(".webm", ".wav").replace(".m4a" , ".wav")
    return filename
    
#print(download_yt_audio("https://youtu.be/pePAAGfh-IU?si=bB21AhOLvBgRdKsr"))
#data_source = download_yt_audio("https://youtu.be/pePAAGfh-IU?si=bB21AhOLvBgRdKsr")
data_source = download_yt_audio("https://youtu.be/185XGEMefgc?si=V3-SHPvy7dpQ2bRp")

def convert_audio_to_wav(input_file:str) -> str:
    """Converting audio file to wav format using pydub library."""
    output_path = os.path.splitext(input_file)[0] + "_converted.wav"
    audio = AudioSegment.from_file(input_file)
    audio = audio.set_channels(1).set_frame_rate(16000)  # Set to mono-audio and frame rate to 16khz
    audio.export(output_path, format="wav")
    return output_path

data_final= convert_audio_to_wav(data_source)


"""Next step is to implement a function that will take the converted wav file to chunks."""
def split_audio_into_chunks(wav_path:str, chunk_duration:int=10) -> list:
    audio = AudioSegment.from_wav(wav_path)  # Loading the audio here
    
    chunk_duration_ms = chunk_duration * 60 * 1000  # Converting the chunk durations to milliseconds

    chunks = []
    for i ,start in enumerate(range(0, len(audio), chunk_duration_ms)):  # start, stop, steps
       chunk = audio[start : start + chunk_duration_ms]  # From zero ms to last ms (60,000 ms)
       chunk_path = f"{wav_path}_chunk_{i}.wav"  # Creating a path for each chunk
       chunk.export(chunk_path, format = "wav")  # Exporting the chunk to wav format
       chunks.append(chunk_path)  # Appending the chunk path to the list
    return chunks

print(split_audio_into_chunks(data_final))