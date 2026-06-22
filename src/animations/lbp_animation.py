from manim import *
import json
import os
import sys
import warnings

warnings.filterwarnings("ignore")
Text.set_default(font="sans-serif")

# Thêm thư mục gốc vào path để import utils và scenes
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.utils.utils import SubtitleManager, generate_all_audio
from src.animations.scenes.intro_scene import play_intro
from src.animations.scenes.core_idea_scene import play_core_idea
from src.animations.scenes.evaluation_scene import play_evaluation

class LBPAnimation(Scene):
    def construct(self):
        # 1. Setup & Audio Generation
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        voice_data_path = os.path.join(project_root, "config", "voice_data.json")
        with open(voice_data_path, "r", encoding="utf-8") as f:
            voice_data = json.load(f)

        audio_dir = os.path.join(project_root, "media", "audio")
        generate_all_audio(voice_data, audio_dir)

        # Background music
        bg_music = os.path.join(project_root, "assets", "bg_music.mp3")
        if os.path.exists(bg_music):
            self.add_sound(bg_music, gain=-15)

        sub_manager = SubtitleManager(self)
        self.audio_end_time = 0.0

        def sub(key):
            current_time = self.renderer.time
            if current_time < self.audio_end_time:
                self.wait(self.audio_end_time - current_time)
            text_str = voice_data.get(key, "")
            if text_str:
                audio_file = os.path.join(audio_dir, f"{key}.mp3")
                if os.path.exists(audio_file) and os.path.getsize(audio_file) > 0:
                    from mutagen.mp3 import MP3
                    audio = MP3(audio_file)
                    self.add_sound(audio_file)
                    self.audio_end_time = self.renderer.time + audio.info.length
                else:
                    self.audio_end_time = self.renderer.time
            sub_manager.show(text_str)

        # Execute Scenes
        play_intro(self, sub)
        play_core_idea(self, sub, project_root)
        play_evaluation(self, sub, project_root)

        # Cleanup
        current_time = self.renderer.time
        if hasattr(self, 'audio_end_time') and current_time < self.audio_end_time:
            self.wait(self.audio_end_time - current_time + 1)
        else:
            self.wait(2)
