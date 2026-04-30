import json
import os
import sys
import asyncio

# Thêm thư mục gốc vào path để import utils
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(project_root)

from src.utils.utils import async_generate_all_audio

async def main():
    voice_data_path = os.path.join(project_root, "config", "voice_data.json")
    with open(voice_data_path, "r", encoding="utf-8") as f:
        voice_data = json.load(f)

    audio_dir = os.path.join(project_root, "media", "audio")
    
    # Xóa audio cũ để đảm bảo đổi giọng đồng bộ
    if os.path.exists(audio_dir):
        import shutil
        print("Cleaning old audio for consistent voice...")
        shutil.rmtree(audio_dir)
        
    print(f"Generating audio in {audio_dir}...")
    await async_generate_all_audio(voice_data, audio_dir)
    print("Done.")

if __name__ == "__main__":
    asyncio.run(main())
