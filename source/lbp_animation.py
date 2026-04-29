from manim import *
from utils import SubtitleManager, create_face_icon, create_pixel_grid, create_3x3_grid, generate_all_audio
import random
import warnings
import json
import os
warnings.filterwarnings("ignore")

Text.set_default(font="sans-serif")

class LBPAnimation(Scene):
    def construct(self):
        # Load voice data
        voice_data_path = os.path.join(os.path.dirname(__file__), "voice_data.json")
        with open(voice_data_path, "r", encoding="utf-8") as f:
            voice_data = json.load(f)

        audio_dir = os.path.join(os.path.dirname(__file__), "media", "audio")
        generate_all_audio(voice_data, audio_dir)

        sub_manager = SubtitleManager(self)
        
        self.audio_end_time = 0.0
        
        def sub(key):
            current_time = self.renderer.time
            if current_time < self.audio_end_time:
                self.wait(self.audio_end_time - current_time)
                
            text_str = voice_data.get(key, "")
            
            if text_str:
                audio_file = os.path.join(audio_dir, f"{key}.mp3")
                if os.path.exists(audio_file):
                    from mutagen.mp3 import MP3
                    audio = MP3(audio_file)
                    self.add_sound(audio_file)
                    self.audio_end_time = self.renderer.time + audio.info.length
                else:
                    self.audio_end_time = self.renderer.time
            else:
                self.audio_end_time = self.renderer.time
                
            sub_manager.show(text_str)

        # ----------------------------------------------------
        # Scene 0: Title Scene
        # ----------------------------------------------------
        title_main = Text("Local Binary Patterns", font_size=64, color=BLUE)
        title_sub = Text("Trích xuất đặc trưng ảnh", font_size=36, color=LIGHT_GRAY)
        title_sub.next_to(title_main, DOWN, buff=0.5)
        
        self.play(Write(title_main), run_time=1.5)
        self.play(FadeIn(title_sub, shift=UP*0.5), run_time=1)
        self.wait(2)
        self.play(FadeOut(title_main, shift=UP*0.5), FadeOut(title_sub, shift=DOWN*0.5))

        # ----------------------------------------------------
        # Scene 1: Đặt vấn đề
        # ----------------------------------------------------
        # Tạo icon đại diện cho khuôn mặt thay vì dùng file ảnh ngoài
        face = create_face_icon()
        
        self.play(FadeIn(face))
        sub("intro_1")
        self.wait(1)
        
        sub("intro_2")
        lighting_overlay = Rectangle(width=14, height=8, fill_color=WHITE, fill_opacity=0)
        self.add(lighting_overlay)
        
        self.play(lighting_overlay.animate.set_fill(opacity=0.6), run_time=1)
        sub("intro_3")
        self.play(lighting_overlay.animate.set_fill(BLACK, opacity=0.8), run_time=1)
        self.play(lighting_overlay.animate.set_fill(WHITE, opacity=0), run_time=1)
        self.remove(lighting_overlay)
        self.wait(1)
        
        sub("intro_4")
        self.play(face.animate.scale(4).shift(DOWN*4 + RIGHT*2), run_time=2)
        
        pixel_grid = create_pixel_grid()
                
        self.play(FadeOut(face), FadeIn(pixel_grid))
        sub("intro_5")
        self.wait(2)
        
        sub("intro_6")
        region_3x3 = VGroup()
        for i in range(2, 5):
            for j in range(2, 5):
                region_3x3.add(pixel_grid[i*8 + j])
                
        self.play(
            pixel_grid.animate.set_opacity(0.1),
            region_3x3.animate.set_opacity(1)
        )
        self.wait(1)
        
        sub("intro_7")
        other_pixels = VGroup(*[p for p in pixel_grid if p not in region_3x3])
        self.play(FadeOut(other_pixels))
        pixel_grid.remove(*other_pixels)
        self.wait(1)
        
        # ----------------------------------------------------
        # Scene 2: Ma trận 3x3 và Ngưỡng hóa
        # ----------------------------------------------------
        values = [
            [120, 110, 85],
            [100, 95, 60],
            [80, 50, 90]
        ]
        
        grid, cells, texts = create_3x3_grid(values)
                
        sub("lbp_1")
        self.play(ReplacementTransform(region_3x3, grid))
        self.wait(1)
        
        sub("lbp_2")
        self.wait(1)
        
        sub("lbp_3")
        center_cell = cells[4]
        center_text = texts[4]
        center_val = values[1][1] # 95
        
        self.play(center_cell.animate.set_fill(YELLOW, opacity=0.5))
        self.wait(1)
        
        sub("lbp_4")
        threshold_arrow = Arrow(start=RIGHT*3 + UP*0, end=center_cell.get_right(), color=YELLOW)
        threshold_text = Text("Threshold", font_size=32, color=YELLOW).next_to(threshold_arrow, RIGHT)
        self.play(GrowArrow(threshold_arrow), Write(threshold_text))
        self.wait(2)
        self.play(FadeOut(threshold_arrow), FadeOut(threshold_text))
        
        sub("lbp_5")
        neighbors_indices = [0, 1, 2, 5, 8, 7, 6, 3]
        binary_values = []
        binary_texts = []
        
        for idx in neighbors_indices:
            val = int(texts[idx].text)
            bin_val = 1 if val >= center_val else 0
            binary_values.append(bin_val)
            
            comp_str = "≥" if bin_val == 1 else "<"
            comp_tex = Text(comp_str, font_size=48).move_to(cells[idx].get_center())
            self.play(FadeOut(texts[idx]), FadeIn(comp_tex), run_time=0.2)
            
            self.play(cells[idx].animate.set_fill(GREEN if bin_val == 1 else RED, opacity=0.3), run_time=0.2)
            
            if idx == 2:  # After 3 elements, show next sub
                sub("lbp_6")
                
            new_text = Text(str(bin_val), font_size=40, color=GREEN if bin_val == 1 else RED).move_to(cells[idx].get_center())
            self.play(ReplacementTransform(comp_tex, new_text), run_time=0.2)
            binary_texts.append(new_text)
            grid.remove(texts[idx])
            grid.add(new_text)
            
        sub("lbp_7")
        self.wait(1.5)
        sub("lbp_8")
        self.wait(2)
        
        # ----------------------------------------------------
        # Scene 3: Chuyển đổi sang thập phân
        # ----------------------------------------------------
        sub("dec_1")
        self.play(grid.animate.scale(0.8).shift(UP * 1.5))
        
        bin_group = VGroup()
        for i, b in enumerate(binary_values):
            t = Text(str(b), font_size=40, color=GREEN if b == 1 else RED)
            bin_group.add(t)
        
        bin_group.arrange(RIGHT, buff=0.2).next_to(grid, DOWN, buff=1)
        
        moves = []
        for i, idx in enumerate(neighbors_indices):
            moves.append(ReplacementTransform(binary_texts[i].copy(), bin_group[i]))
            
        self.play(*moves)
        sub("dec_2")
        self.wait(1.5)
        
        sub("dec_3")
        formula_str = "1×2⁷ + 1×2⁶ + 0×2⁵ + 0×2⁴ + 0×2³ + 0×2² + 0×2¹ + 1×2⁰ = 193"
        formula_tex = Text(formula_str, font_size=28).next_to(bin_group, DOWN, buff=0.8)
        
        self.play(Write(formula_tex))
        self.wait(2)
        
        result_text = Text("193", font_size=48, color=YELLOW)
        result_text.move_to(center_cell.get_center())
        
        sub("dec_4")
        self.play(
            FadeOut(bin_group),
            FadeOut(formula_tex),
            ReplacementTransform(center_text, result_text)
        )
        grid.remove(center_text)
        grid.add(result_text)
        self.play(Flash(center_cell, color=YELLOW))
        self.wait(1.5)
        
        sub("dec_5")
        self.wait(2)
        
        # ----------------------------------------------------
        # Scene 4: Không gian Vector
        # ----------------------------------------------------
        sub("vec_1")
        self.play(FadeOut(grid))
        
        large_grid = VGroup(*[Square(side_length=0.8, color=WHITE) for _ in range(16)])
        large_grid.arrange_in_grid(rows=4, cols=4, buff=0)
        large_grid.move_to(LEFT * 4)
        
        self.play(FadeIn(large_grid))
        self.wait(1)
        
        sub("vec_2")
        self.play(large_grid[5].animate.set_fill(BLUE, opacity=0.5))
        
        sub("vec_3")
        chart_1 = BarChart(
            values=[15, 30, 45, 20, 10, 50],
            y_range=[0, 60, 20],
            y_length=2,
            x_length=3,
            bar_colors=[BLUE],
            y_axis_config={"label_constructor": Text}
        ).next_to(large_grid, RIGHT, buff=1).shift(UP * 1)
        self.play(Create(chart_1))
        
        self.play(large_grid[10].animate.set_fill(GREEN, opacity=0.5))
        chart_2 = BarChart(
            values=[40, 10, 25, 35, 15, 20],
            y_range=[0, 60, 20],
            y_length=2,
            x_length=3,
            bar_colors=[GREEN],
            y_axis_config={"label_constructor": Text}
        ).next_to(large_grid, RIGHT, buff=1).shift(DOWN * 2)
        self.play(Create(chart_2))
        self.wait(1)
        
        sub("vec_4")
        vector_1 = Rectangle(width=2.5, height=0.6, color=BLUE, fill_color=BLUE, fill_opacity=0.8)
        vector_2 = Rectangle(width=2.5, height=0.6, color=GREEN, fill_color=GREEN, fill_opacity=0.8)
        dots = Text("...", font_size=48)
        
        feature_vector = VGroup(vector_1, vector_2, dots).arrange(RIGHT, buff=0).move_to(RIGHT * 2)
        fv_text = Text("Feature Vector", font_size=36, color=YELLOW).next_to(feature_vector, UP)
        
        self.play(
            ReplacementTransform(chart_1, vector_1),
            ReplacementTransform(chart_2, vector_2),
            FadeIn(dots)
        )
        
        sub("vec_5")
        self.play(Write(fv_text))
        self.wait(1.5)
        
        sub("vec_6")
        self.wait(2)
        
        sub("vec_7")
        self.wait(2)
        
        # ----------------------------------------------------
        # End Scene
        # ----------------------------------------------------
        sub("outro")
        self.play(
            FadeOut(large_grid),
            FadeOut(feature_vector),
            FadeOut(fv_text)
        )
        end_text = Text("Đơn giản, hiệu quả và thanh lịch. Đó là Local Binary Patterns!", font_size=28, color=YELLOW)
        hashtag = Text("#LocalBinaryPatterns #AI", font_size=24, color=BLUE).next_to(end_text, DOWN, buff=0.5)
        self.play(Write(end_text))
        self.play(FadeIn(hashtag))
        
        # Đảm bảo video không kết thúc trước khi audio cuối cùng chạy xong
        current_time = self.renderer.time
        if hasattr(self, 'audio_end_time') and current_time < self.audio_end_time:
            self.wait(self.audio_end_time - current_time + 1)
        else:
            self.wait(3)
