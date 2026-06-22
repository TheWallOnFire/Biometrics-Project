import numpy as np
from manim import *

class SubtitleManager:
    """
    Class hỗ trợ quản lý việc tạo, thay thế và xóa phụ đề trong Manim.
    """
    def __init__(self, scene):
        self.scene = scene
        self.current_sub = VGroup()

    def show(self, text_str):
        if not text_str:
            return
            
        import textwrap
        wrapped_text = "\n".join(textwrap.wrap(text_str, width=50))
            
        new_sub = Text(wrapped_text, font_size=24, color=WHITE).to_edge(DOWN, buff=0.4)
        new_sub.set_z_index(100)
        
        # Thêm background mờ để dễ đọc hơn
        bg = SurroundingRectangle(new_sub, color=BLACK, fill_color=BLACK, fill_opacity=0.6, buff=0.2)
        bg.set_z_index(99)
        full_sub = VGroup(bg, new_sub)
        
        if hasattr(self, "current_full_sub") and len(self.current_full_sub) > 0:
            self.scene.play(ReplacementTransform(self.current_full_sub, full_sub), run_time=0.5)
        else:
            self.scene.play(FadeIn(full_sub), run_time=0.5)
        self.current_full_sub = full_sub

    def clear(self):
        if hasattr(self, "current_full_sub") and len(self.current_full_sub) > 0:
            self.scene.play(FadeOut(self.current_full_sub), run_time=0.5)
            self.current_full_sub = VGroup()


def calculate_lbp_pixel(img, x, y):
    '''
    Tính toán giá trị Local Binary Pattern cho một điểm ảnh tại vị trí (x, y)
    với vùng lân cận 3x3.
    '''
    center_val = img[x, y]
    val = 0
    
    # Các vị trí lân cận (hàng, cột) theo chiều kim đồng hồ bắt đầu từ góc trên bên trái
    neighbors = [
        (x-1, y-1), (x-1, y), (x-1, y+1),
        (x, y+1), (x+1, y+1), (x+1, y),
        (x+1, y-1), (x, y-1)
    ]
    
    for i, (nx, ny) in enumerate(neighbors):
        if img[nx, ny] >= center_val:
            val += (1 << (7 - i)) # Hoặc 1 << i tùy quy ước
            
    return val

def compute_lbp_image(img):
    '''
    Tính toán ma trận LBP cho toàn bộ bức ảnh grayscale.
    '''
    h, w = img.shape
    lbp_img = np.zeros((h, w), dtype=np.uint8)
    
    # Bỏ qua viền (margin) 1 pixel
    for i in range(1, h-1):
        for j in range(1, w-1):
            lbp_img[i, j] = calculate_lbp_pixel(img, i, j)
            
    return lbp_img

def compute_histogram(lbp_img, num_bins=256):
    '''
    Tính histogram cho ảnh LBP.
    '''
    hist, _ = np.histogram(lbp_img.ravel(), bins=num_bins, range=(0, num_bins))
    
    # Chuẩn hóa histogram
    hist = hist.astype("float")
    hist /= (hist.sum() + 1e-7)
    
    return hist

def extract_lbp_features(image_path, num_blocks=(8, 8)):
    '''
    Trích xuất đặc trưng LBP toàn diện: chia ảnh thành lưới, tính histogram từng ô 
    và nối lại thành vector đặc trưng (Feature Vector).
    '''
    # Đọc ảnh grayscale
    import cv2
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError(f"Không thể đọc ảnh từ {image_path}")
        
    lbp_img = compute_lbp_image(img)
    
    h, w = lbp_img.shape
    block_h = h // num_blocks[0]
    block_w = w // num_blocks[1]
    
    feature_vector = []
    
    for i in range(num_blocks[0]):
        for j in range(num_blocks[1]):
            # Lấy vùng block
            block = lbp_img[i*block_h:(i+1)*block_h, j*block_w:(j+1)*block_w]
            hist = compute_histogram(block)
            feature_vector.extend(hist)
            
    return np.array(feature_vector)

def create_face_icon():
    """Tạo biểu tượng khuôn mặt trừu tượng."""
    face_bg = Rectangle(width=5, height=6, fill_color=DARK_GRAY, fill_opacity=1, stroke_color=WHITE, stroke_width=2)
    head = Circle(radius=1.2, fill_color=LIGHT_GRAY, fill_opacity=1).move_to(face_bg.get_center() + UP*0.8)
    shoulders = Ellipse(width=3.6, height=2.5, fill_color=LIGHT_GRAY, fill_opacity=1).move_to(face_bg.get_center() + DOWN*2)
    return VGroup(face_bg, head, shoulders)

def create_pixel_grid():
    """Tạo ma trận 8x8 với các giá trị ngẫu nhiên."""
    import random
    pixel_grid = VGroup()
    for i in range(8):
        for j in range(8):
            cell = Square(side_length=0.8, color=GRAY)
            cell.move_to(RIGHT * (j - 3.5) * 0.8 + DOWN * (i - 3.5) * 0.8)
            val = random.randint(50, 200)
            text = Text(str(val), font_size=24).move_to(cell.get_center())
            pixel_grid.add(VGroup(cell, text))
    return pixel_grid

def create_3x3_grid(values):
    """Tạo lưới 3x3 LBP với giá trị cụ thể."""
    grid = VGroup()
    cells = []
    texts = []
    for i in range(3):
        for j in range(3):
            cell = Square(side_length=1.5, color=WHITE)
            cell.move_to(RIGHT * (j - 1) * 1.5 + DOWN * (i - 1) * 1.5)
            text = Text(str(values[i][j]), font_size=40).move_to(cell.get_center())
            grid.add(cell, text)
            cells.append(cell)
            texts.append(text)
    return grid, cells, texts

def create_circular_lbp_grid(radius=2, num_points=8):
    """Tạo minh họa Circular LBP với bán kính R và số điểm P."""
    grid = VGroup()
    center_dot = Dot(color=YELLOW, radius=0.1)
    circle = Circle(radius=radius, color=BLUE, stroke_width=2, stroke_opacity=0.5)
    
    dots = VGroup()
    for i in range(num_points):
        angle = i * (2 * PI / num_points)
        pos = radius * (RIGHT * np.cos(angle) + UP * np.sin(angle))
        dot = Dot(pos, color=WHITE, radius=0.08)
        dots.add(dot)
        
    grid.add(circle, center_dot, dots)
    return grid, center_dot, dots, circle

async def async_generate_all_audio(voice_data, output_dir="media/audio"):
    """Core async function to generate audio files."""
    import os
    import edge_tts
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    async def _gen_single(key, text, file_path):
        if os.path.exists(file_path):
            if os.path.getsize(file_path) > 0:
                return
            else:
                os.remove(file_path)
            
        retries = 3
        for i in range(retries):
            try:
                if i > 0:
                    print(f"Retrying {key} (Attempt {i+1})...")
                
                import asyncio
                await asyncio.sleep(0.5) # Small delay to avoid rate limiting
                
                print(f"Generating audio for: {key}...")
                communicate = edge_tts.Communicate(text, "vi-VN-NamMinhNeural")
                await communicate.save(file_path)
                
                if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                    return # Success
                
            except Exception as e:
                print(f"Attempt {i+1} failed for {key}: {e}")
                
        print(f"CRITICAL: Failed to generate {key} after {retries} attempts.")
        if os.path.exists(file_path):
            os.remove(file_path)

    tasks = []
    for key, text in voice_data.items():
        if not text:
            continue
        file_path = os.path.join(output_dir, f"{key}.mp3")
        tasks.append(_gen_single(key, text, file_path))
    
    if tasks:
        for task in tasks:
            await task

def generate_all_audio(voice_data, output_dir="media/audio"):
    """Sync wrapper for generate_all_audio."""
    import asyncio
    try:
        # Check if we are already in an event loop
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # If running, we can't use run_until_complete. 
            # This case is handled by calling async_generate_all_audio directly in async scripts.
            print("Warning: Event loop already running. Audio generation skipped in sync wrapper.")
            return
        loop.run_until_complete(async_generate_all_audio(voice_data, output_dir))
    except RuntimeError:
        asyncio.run(async_generate_all_audio(voice_data, output_dir))
