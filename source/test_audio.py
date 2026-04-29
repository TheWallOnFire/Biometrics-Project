import json
import os
import asyncio
from utils import generate_all_audio

voice_data_path = "voice_data.json"
with open(voice_data_path, "r", encoding="utf-8") as f:
    voice_data = json.load(f)

audio_dir = "../media/audio_test"
print("Starting generation...")
generate_all_audio(voice_data, audio_dir)
print("Done.")
