# LBP Biometrics Animation

A professional, automated animation project explaining the **Local Binary Patterns (LBP)** algorithm for facial recognition. Built with Manim and Neural AI narration.

## 🚀 Features
- **6-Part Educational Flow**: From basic logic to real-world applications.
- **AI Narration**: High-quality neural voiceover unified with `vi-VN-NamMinhNeural`.
- **Dynamic Visuals**: Step-by-step 3x3 grid calculations and illumination robustness proofs.
- **Multi-Resolution Support**: Render in 480p, 1080p, or 4K.

## 📂 Project Structure
```text
Biometrics-Project/
├── assets/             # Images and media (face_portrait.png)
├── config/             # Configuration files (voice_data.json)
├── src/
│   ├── animations/     # Manim animation scripts
│   ├── scripts/        # Utility scripts (render, refresh)
│   └── utils/          # Shared helper functions
├── media/              # Rendered outputs (video, audio)
├── manim.cfg           # Manim global settings
└── README.md
```

## 🛠️ Installation
1. Install [Manim](https://docs.manim.community/en/stable/installation.html) and its dependencies (ffmpeg, latex, etc.).
2. Install Python requirements:
```bash
pip install manim edge-tts gtts mutagen numpy opencv-python
```

## 🎬 How to Use

### 1. Rendering the Video
The easiest way to render is using our interactive menu:
```powershell
python src/scripts/render.py
```
*Follow the on-screen prompts to choose Low (480p), High (1080p), or 4K resolution.*

### 2. Refreshing Audio
If you modify the narration script in `config/voice_data.json`, run this to regenerate all audio files:
```powershell
python src/scripts/refresh.py
```

## 📝 Customization
- **Narration**: Edit `config/voice_data.json` to change what the AI says.
- **Visuals**: Modify `src/animations/lbp_animation.py` to adjust the animation steps.
- **Quality**: Adjust `manim.cfg` for global frame rate and preview settings.

---
*Created for the Biometrics course - 2026*