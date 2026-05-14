import yt_dlp
import os
import subprocess
import glob

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def download_youtube_audio(url: str) -> str:
    output_path = os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s")

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_path,

        #  FIXED PATH (IMPORTANT)
        

        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
                "preferredquality": "192",
            }
        ],
        "quiet": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info).replace(".webm", ".wav").replace(".m4a", ".wav")

    return filename

# data = download_youtube_audio("https://www.youtube.com/watch?v=mtiOK2QG9Q0")


def convert_to_wav(input_path: str) -> str:
    output_path = os.path.splitext(input_path)[0] + "_converted.wav"

    # Use FFmpeg directly (NO pydub)
    subprocess.run([
        "ffmpeg",
        "-y",
        "-i", input_path,
        "-ac", "1",
        "-ar", "16000",
        output_path
    ], check=True)

    return output_path

# data_final = convert_to_wav(data)



def chunk_audio(wav_path: str, chunk_minutes: int = 10) -> list:
    chunk_seconds = chunk_minutes * 60

    base_path = os.path.splitext(wav_path)[0]

    output_pattern = f"{base_path}_chunk_%03d.wav"

    subprocess.run([
        "ffmpeg",
        "-y",
        "-i", wav_path,
        "-f", "segment",
        "-segment_time", str(chunk_seconds),
        "-c", "copy",
        output_pattern
    ], check=True)

    chunks = sorted(
        glob.glob(f"{base_path}_chunk_*.wav")
    )

    return chunks


# print(chunk_audio(data_final))

def process_input(source: str) -> list:
    if source.startswith("http://") or source.startswith("https://"):
        print("Detected YouTube URL. Downloading audio...")
        wav_path = download_youtube_audio(source)
    else:
        print("Detected local file. Converting to WAV...")
        wav_path = convert_to_wav(source)

    print("Chunking audio...")
    chunks = chunk_audio(wav_path)
    print(f"Audio ready — {len(chunks)} chunk(s) created.")
    return chunks
