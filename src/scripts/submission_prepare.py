import os
import shutil

def prepare_submission(mssv="22127000"):
    # 1. Setup paths
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    submission_dir = os.path.join(project_root, mssv)
    source_dir = os.path.join(submission_dir, "source")
    
    # 2. Create directories
    if os.path.exists(submission_dir):
        shutil.rmtree(submission_dir)
    os.makedirs(source_dir)
    
    print(f"Creating submission folder for {mssv}...")
    
    # 3. Define files to copy (maintaining relative structure within source/)
    # For Manim, it's often easier to put everything in a flat structure or keep the src/ structure
    # The PDF says "Thư mục mã nguồn Manim chứa các file .py", so we'll keep the logic.
    
    to_copy = [
        ("src", "src"),
        ("config", "config"),
        ("assets", "assets"),
        ("README.md", "README.md"),
        ("manim.cfg", "manim.cfg")
    ]
    
    for item_src, item_dest in to_copy:
        src_path = os.path.join(project_root, item_src)
        dest_path = os.path.join(source_dir, item_dest)
        
        if os.path.isdir(src_path):
            shutil.copytree(src_path, dest_path, ignore=shutil.ignore_patterns('__pycache__', 'media', '.git'))
        elif os.path.isfile(src_path):
            shutil.copy2(src_path, dest_path)
            
    # 4. Copy url.txt to the MSSV root
    url_src = os.path.join(project_root, "url.txt")
    url_dest = os.path.join(submission_dir, "url.txt")
    if os.path.exists(url_src):
        shutil.copy2(url_src, url_dest)
    else:
        with open(url_dest, "w") as f:
            f.write("https://your-video-link-here.com")
            
    print(f"Submission folder ready at: {submission_dir}")
    print("Please rename the folder to your actual Student ID (MSSV) and zip it.")

if __name__ == "__main__":
    # You can change this to your actual Student ID
    prepare_submission("22127000")
