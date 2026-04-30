import os
import subprocess

def main():
    print("--- LBP Animation Render Menu ---")
    print("1. Low Quality (480p, 15fps) - Fast preview")
    print("2. Medium Quality (720p, 30fps)")
    print("3. High Quality (1080p, 60fps) - Recommended for final")
    print("4. 4K Quality (2160p, 60fps) - Ultra HD")
    
    choice = input("\nChoose resolution (1-4): ")
    
    flags = {
        "1": "-pql",
        "2": "-pqm",
        "3": "-pqh",
        "4": "-pqk"
    }
    
    flag = flags.get(choice, "-pql")
    cmd = f"manim {flag} src/animations/lbp_animation.py LBPAnimation"
    
    print(f"\nExecuting: {cmd}")
    subprocess.run(cmd, shell=True)

if __name__ == "__main__":
    main()
