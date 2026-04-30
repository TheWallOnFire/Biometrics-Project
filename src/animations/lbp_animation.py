from manim import *
import json
import os
import sys
import warnings

warnings.filterwarnings("ignore")
Text.set_default(font="sans-serif")

# Thêm thư mục gốc vào path để import utils
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.utils.utils import SubtitleManager, create_pixel_grid, create_3x3_grid, generate_all_audio

class LBPAnimation(Scene):
    def construct(self):
        # 1. Setup & Audio Generation
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        voice_data_path = os.path.join(project_root, "config", "voice_data.json")
        with open(voice_data_path, "r", encoding="utf-8") as f:
            voice_data = json.load(f)

        audio_dir = os.path.join(project_root, "media", "audio")
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
                if os.path.exists(audio_file) and os.path.getsize(audio_file) > 0:
                    from mutagen.mp3 import MP3
                    audio = MP3(audio_file)
                    self.add_sound(audio_file)
                    self.audio_end_time = self.renderer.time + audio.info.length
                else:
                    self.audio_end_time = self.renderer.time
            sub_manager.show(text_str)

        # ----------------------------------------------------
        # Part 1: Tiêu đề và Giới thiệu
        # ----------------------------------------------------
        self.next_section("Intro")
        title_main = Text("Local Binary Patterns", font_size=64, color=BLUE)
        title_sub = Text("Trích xuất đặc trưng ảnh", font_size=32, color=LIGHT_GRAY).next_to(title_main, DOWN)
        
        sub("title_name")
        self.play(Write(title_main))
        sub("title_intro")
        self.play(FadeIn(title_sub, shift=UP*0.3))
        self.wait(2)
        self.play(FadeOut(title_main), FadeOut(title_sub))

        # ----------------------------------------------------
        # Part 2: Lựa chọn thuật toán
        # ----------------------------------------------------
        self.next_section("Algorithm Selection")
        sub("part_2_list")
        algos = VGroup(
            Text("PCA / Eigenfaces"),
            Text("HOG (Histogram of Oriented Gradients)"),
            Text("SIFT (Scale-Invariant Feature Transform)"),
            Text("LBP (Local Binary Patterns)", color=YELLOW)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        
        self.play(Create(algos), run_time=3)
        self.wait(1)
        
        sub("part_2_pick")
        self.play(
            algos[0:3].animate.set_opacity(0.2),
            algos[3].animate.scale(1.2).set_color(YELLOW).move_to(ORIGIN)
        )
        self.wait(2)
        self.play(FadeOut(algos))

        # ----------------------------------------------------
        # Part 3: Giải thích sơ về cách hoạt động
        # ----------------------------------------------------
        self.next_section("Basic Logic")
        sub("part_3_logic")
        face_path = os.path.join(project_root, "assets", "face_portrait.png")
        face_img = ImageMobject(face_path).scale(1.2).to_edge(LEFT)
        
        # Sliding window visualization
        scan_rect = Rectangle(width=0.6, height=0.6, color=YELLOW, stroke_width=4).move_to(face_img.get_corner(UL) + RIGHT*0.5 + DOWN*0.5)
        grid = create_pixel_grid().scale(0.5).to_edge(RIGHT)
        
        self.play(FadeIn(face_img, shift=RIGHT))
        self.play(Create(scan_rect))
        
        # Animate sliding window
        for _ in range(3):
            self.play(scan_rect.animate.shift(RIGHT * 0.4), run_time=0.5)
        self.play(scan_rect.animate.shift(DOWN * 0.4 + LEFT * 1.2), run_time=0.5)
        
        self.play(Create(grid))
        self.wait(2)
        self.play(FadeOut(face_img), FadeOut(grid), FadeOut(scan_rect))

        # ----------------------------------------------------
        # Part 4: 2 Ví dụ Demo
        # ----------------------------------------------------
        self.next_section("Demo Examples")
        
        # --- Demo 1: Detailed ---
        sub("demo_1_title")
        demo1_label = Text("Ví dụ 1: Quy trình tính toán chi tiết", color=BLUE).to_edge(UP)
        self.play(Write(demo1_label))
        
        values1 = [[210, 215, 220], [200, 205, 215], [60, 65, 70]]
        grid1, cells1, texts1 = create_3x3_grid(values1)
        grid1.scale(0.7).shift(LEFT * 3)
        
        self.play(Create(grid1))
        
        sub("demo_1_step_1")
        center_cell = cells1[4]
        center_cell.set_fill(YELLOW, opacity=0.5)
        self.play(Indicate(center_cell))
        self.wait(1)
        
        sub("demo_1_step_2")
        neighbors_indices = [0, 1, 2, 5, 8, 7, 6, 3]
        bin_vals = []
        
        for idx in neighbors_indices:
            val = values1[idx//3][idx%3]
            res = 1 if val >= 205 else 0
            bin_vals.append(res)
            
            self.play(cells1[idx].animate.set_stroke(YELLOW, width=8), run_time=0.15)
            res_text = Text(str(res), color=GREEN if res==1 else RED, font_size=40).move_to(cells1[idx])
            self.play(ReplacementTransform(texts1[idx], res_text), run_time=0.15)
            self.play(cells1[idx].animate.set_stroke(WHITE, width=2), run_time=0.1)
            
        sub("demo_1_step_3")
        bin_display = Text("Binary: " + " ".join(map(str, bin_vals)), font_size=36).shift(RIGHT*3 + UP*1)
        self.play(Write(bin_display))
        self.wait(1)
        
        sub("demo_1_step_4")
        dec_display = Text("Decimal: 240", font_size=48, color=YELLOW).next_to(bin_display, DOWN, buff=1)
        self.play(Write(dec_display))
        self.play(Indicate(dec_display))
        self.wait(2)
        
        self.play(FadeOut(grid1), FadeOut(bin_display), FadeOut(dec_display), FadeOut(demo1_label))

        # --- Demo 2: Robustness ---
        sub("demo_2_title")
        demo2_label = Text("Ví dụ 2: Kháng ánh sáng", color=GREEN).to_edge(UP)
        self.play(Write(demo2_label))
        
        values2 = [[min(v + 50, 255) for v in row] for row in values1]
        grid2, cells2, texts2 = create_3x3_grid(values2)
        grid2.scale(0.7).shift(LEFT * 3)
        
        sub("demo_2_step_1")
        self.play(Create(grid2))
        cells2[4].set_fill(YELLOW, opacity=0.5)
        self.play(Indicate(cells2[4]))
        self.wait(1)
        
        sub("demo_2_robust_result")
        bin_vals2 = []
        for idx in neighbors_indices:
            val = values2[idx//3][idx%3]
            res = 1 if val >= 255 else 0 
            bin_vals2.append(res)
            res_text = Text(str(res), color=GREEN if res==1 else RED, font_size=40).move_to(cells2[idx])
            self.play(ReplacementTransform(texts2[idx], res_text), run_time=0.15)

        sub("demo_2_step_3")
        bin_display2 = Text("Binary: " + " ".join(map(str, bin_vals2)), font_size=36).shift(RIGHT*3 + UP*1)
        dec_display2 = Text("Decimal: 240", font_size=48, color=YELLOW).next_to(bin_display2, DOWN, buff=1)
        
        self.play(Write(bin_display2))
        self.play(Write(dec_display2))
        self.play(Circumscribe(dec_display2))
        self.wait(3)
        
        self.play(FadeOut(grid2), FadeOut(bin_display2), FadeOut(dec_display2), FadeOut(demo2_label))

        # --- Application: Real-world Recognition (Under the Hood) ---
        self.next_section("Real-world Application")
        sub("app_title")
        app_label = Text("Ứng dụng: Under the Hood", color=YELLOW).to_edge(UP)
        self.play(Write(app_label))
        
        # Step 1: Show the "240" code
        sub("uth_one")
        code_240 = Text("240", font_size=72, color=BLUE).move_to(ORIGIN)
        self.play(FadeIn(code_240))
        self.wait(1)
        
        sub("app_uth_2")
        self.play(code_240.animate.scale(0.5).to_edge(UP, buff=1.2))
        
        # Step 2: Show a grid of many codes
        sub("app_uth_3")
        codes_grid = VGroup(*[
            Text(str(np.random.randint(0, 256)), font_size=18) 
            for _ in range(64)
        ]).arrange_in_grid(rows=8, cols=8, buff=0.4).move_to(ORIGIN)
        self.play(LaggedStart(*[FadeIn(c) for c in codes_grid], lag_ratio=0.01))
        self.wait(1)
        
        # Step 3: Codes flow into a Histogram (More Realistic)
        sub("statistic_data")
        hist_axes = Axes(
            x_range=[0, 256, 64],
            y_range=[0, 1, 0.5],
            x_length=8,
            y_length=3,
            axis_config={"include_tip": False},
            tips=False
        ).shift(DOWN * 1.5)
        
        x_label = Text("LBP Codes (0-255)", font_size=20).next_to(hist_axes.x_axis, DOWN)
        y_label = Text("Frequency", font_size=20).next_to(hist_axes.y_axis, LEFT).rotate(90*DEGREES)
        
        # More realistic histogram data (not random)
        hist_heights = [0.2, 0.4, 0.3, 0.8, 0.6, 0.4, 0.7, 0.9, 0.3, 0.5] * 3
        bars = VGroup()
        for i, h in enumerate(hist_heights):
            bar = Rectangle(
                width=0.2, 
                height=h*2, 
                fill_color=BLUE, 
                fill_opacity=0.8, 
                stroke_width=0
            ).move_to(hist_axes.c2p(i*8 + 10, 0), aligned_edge=DOWN)
            bars.add(bar)
            
        self.play(
            FadeIn(hist_axes), FadeIn(x_label), FadeIn(y_label),
            code_240.animate.move_to(hist_axes.c2p(240, 0), aligned_edge=DOWN).set_opacity(0),
        )
        
        # Animate codes "flowing" into bars
        self.play(
            LaggedStart(*[
                c.animate.move_to(bars[np.random.randint(0, len(bars))].get_top()).set_opacity(0)
                for c in codes_grid
            ], lag_ratio=0.02),
            Create(bars),
            run_time=3
        )
        
        sub("uth_five")
        identity_label = Text("Identity Fingerprint", color=YELLOW, font_size=36).next_to(hist_axes, UP)
        self.play(Write(identity_label))
        self.play(Indicate(identity_label))
        self.wait(2)
        
        # Step 4: Final Match result
        sub("match_desc")
        face1 = ImageMobject(face_path).scale(0.6).shift(LEFT * 3 + UP * 1)
        face2 = ImageMobject(face_path).scale(0.6).shift(RIGHT * 3 + UP * 1)
        face2.set_opacity(0.7) # Simulate bright/washed out image
        
        self.play(
            hist_axes.animate.scale(0.5).to_edge(DOWN),
            bars.animate.scale(0.5).move_to(hist_axes.c2p(128, 0), aligned_edge=DOWN),
            identity_label.animate.scale(0.5).next_to(hist_axes, UP, buff=0.1),
            FadeIn(face1), FadeIn(face2)
        )
        
        sub("match_robust")
        self.play(Indicate(face1), Indicate(face2))
        self.wait(1)
        
        sub("app_result")
        match_symbol = Text("MATCH!", color=GREEN, font_size=80).move_to(ORIGIN).set_z_index(100)
        bg_rect = SurroundingRectangle(match_symbol, color=GREEN, fill_color=BLACK, fill_opacity=0.9)
        self.play(FadeIn(bg_rect), Write(match_symbol))
        self.play(Indicate(match_symbol))
        self.wait(3)
        
        # Proper cleanup
        self.play(
            FadeOut(hist_axes), FadeOut(bars), FadeOut(identity_label),
            FadeOut(match_symbol), FadeOut(bg_rect), FadeOut(app_label),
            FadeOut(x_label), FadeOut(y_label), FadeOut(codes_grid),
            FadeOut(code_240), FadeOut(face1), FadeOut(face2)
        )

        # ----------------------------------------------------
        # Part 5: Ưu và Nhược điểm
        # ----------------------------------------------------
        self.next_section("Pros and Cons")
        sub("pros_cons_title")
        pc_title = Text("Ưu và Nhược điểm", font_size=48, color=BLUE).to_edge(UP)
        self.play(Write(pc_title))
        
        pros = VGroup(
            Text("Ưu điểm:", color=GREEN, font_size=36),
            Text("- Tốc độ xử lý cực nhanh", font_size=28),
            Text("- Kháng ánh sáng tốt", font_size=28)
        ).arrange(DOWN, aligned_edge=LEFT).move_to(LEFT*3 + UP*0.5)
        
        cons = VGroup(
            Text("Nhược điểm:", color=RED, font_size=36),
            Text("- Nhạy cảm với nhiễu", font_size=28),
            Text("- Vector đặc trưng lớn", font_size=28)
        ).arrange(DOWN, aligned_edge=LEFT).move_to(RIGHT*3 + UP*0.5)
        
        sub("pros_1")
        self.play(FadeIn(pros, shift=RIGHT))
        self.wait(1)
        sub("cons_1")
        self.play(FadeIn(cons, shift=LEFT))
        self.wait(2)
        self.play(FadeOut(pros), FadeOut(cons), FadeOut(pc_title))

        # ----------------------------------------------------
        # Part 6: Kết luận
        # ----------------------------------------------------
        self.next_section("Conclusion")
        sub("conclusion")
        final_text = Text("Local Binary Patterns", font_size=60, color=BLUE)
        tagline = Text("Đơn giản - Hiệu quả - Thanh lịch", font_size=32, color=YELLOW).next_to(final_text, DOWN)
        
        self.play(Write(final_text))
        self.play(FadeIn(tagline, shift=UP*0.5))
        self.wait(3)
        
        # Cleanup
        current_time = self.renderer.time
        if hasattr(self, 'audio_end_time') and current_time < self.audio_end_time:
            self.wait(self.audio_end_time - current_time + 1)
        else:
            self.wait(2)
