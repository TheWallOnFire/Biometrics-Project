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
            self.clear()
            return
            
        import textwrap
        wrapped_text = "\n".join(textwrap.wrap(text_str, width=60))
            
        new_sub = Text(wrapped_text, font_size=24, color=WHITE).to_edge(DOWN, buff=0.3)
        new_sub.add_background_rectangle(color=DARK_GRAY, opacity=1.0, buff=0.15)
        
        if len(self.current_sub) > 0:
            self.scene.play(ReplacementTransform(self.current_sub, new_sub), run_time=0.5)
        else:
            self.scene.play(FadeIn(new_sub), run_time=0.5)
        self.current_sub = new_sub

    def clear(self):
        if len(self.current_sub) > 0:
            self.scene.play(FadeOut(self.current_sub), run_time=0.5)
            self.current_sub = VGroup()


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

def generate_all_audio(voice_data, output_dir="media/audio"):
    """
    Generate audio files for all strings in voice_data using edge-tts (Microsoft Neural).
    Higher quality and more natural than gTTS. Parallel generation for speed.
    """
    import os
    import asyncio
    import edge_tts
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    async def _gen_single(key, text, file_path):
        # Chỉ tạo nếu chưa có hoặc có thể ghi đè tùy ý
        # Ở đây ta giữ nguyên logic kiểm tra tồn tại để tránh gọi API quá nhiều
        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            return
            
        try:
            print(f"Generating audio for: {key}...")
            communicate = edge_tts.Communicate(text, "vi-VN-NamMinhNeural")
            await communicate.save(file_path)
        except Exception as e:
            print(f"Error generating {key}: {e}")

    async def _generate():
        tasks = []
        for key, text in voice_data.items():
            if not text:
                continue
            file_path = os.path.join(output_dir, f"{key}.mp3")
            tasks.append(_gen_single(key, text, file_path))
        
        if tasks:
            await asyncio.gather(*tasks)

    try:
        # Chạy loop mới
        asyncio.run(_generate())
    except RuntimeError:
        # Nếu đã có loop đang chạy (trong một số môi trường đặc biệt)
        try:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(_generate())
        except Exception as e:
            print(f"Could not start asyncio: {e}")
        except Exception as e:
            print(f"General error: {e}")
