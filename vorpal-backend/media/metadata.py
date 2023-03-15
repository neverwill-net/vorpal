import os
import json
import hashlib
import subprocess
from datetime import datetime
from mutagen import File
from mutagen.flac import FLAC
from mutagen.mp3 import MP3
from .models import MediaFile

def hash_file(file_path):
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            hasher.update(chunk)
    return hasher.hexdigest()
def get_metadata(file_path, debug=False):
    file_extension = os.path.splitext(file_path)[1].lower()
    if file_extension not in ['.mp3', '.m4a', '.flac', '.ogg', '.wav', '.mp4', '.mkv', '.avi', '.mov', '.wmv']:
        return None

    file_size = os.path.getsize(file_path)
    file_hash = hash_file(file_path)
    duration = None
    bit_rate = None
    sample_rate = None
    channels = None
    format_name = None
    format_long_name = None
    metadata = {}

    try:
        audio_ext = ('.mp3', '.flac', '.m4a', '.ogg', '.wav')
        video_ext = ('.mp4', '.mkv', '.avi', '.mov', '.wmv')

        if file_path.lower().endswith(audio_ext):
            audio = File(file_path)

            if isinstance(audio, FLAC) or isinstance(audio, MP3):
                duration = audio.info.length
                bit_rate = audio.info.bitrate
                sample_rate = audio.info.sample_rate
                channels = audio.info.channels
                format_name = audio.mime[0].split('/')[1]
                format_long_name = audio.mime[0]

                # Dynamically add metadata from the tags
                for key, value in audio.items():
                    metadata[key] = value

        elif file_path.lower().endswith(video_ext):
            cmd = f"ffprobe -v quiet -print_format json -show_format -show_streams -i \"{file_path}\""
            output = subprocess.check_output(cmd, shell=True).decode('utf-8')
            metadata = json.loads(output)

            # Add relevant video metadata here

        else:
            if debug:
                print(f"Unsupported file format for {file_path}")
            return None

    except Exception as e:
        if debug:
            print(f"Error reading metadata from {file_path}: {str(e)}")
        return None
    
    media_file = MediaFile(
    file_path=file_path,
    file_size=file_size,
    hash=file_hash,
    duration=duration,
    bit_rate=bit_rate,
    sample_rate=sample_rate,
    channels=channels,
    format_name=format_name,
    format_long_name=format_long_name,
    scan_date=datetime.now(),
    media_metadata=metadata  # Update the attribute name to media_metadata
    )

    return media_file


