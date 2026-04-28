from manim import *

class LBPAnimation(Scene):
    def construct(self):
        # 1. Introduction
        title = Text("Local Binary Patterns (LBP)", font_size=48, color=BLUE).to_edge(UP)
        subtitle = Text("Feature Extraction in Face Recognition", font_size=36).next_to(title, DOWN)
        
        self.play(Write(title))
        self.play(FadeIn(subtitle))
        self.wait(2)
        
        self.play(FadeOut(subtitle))
        
        # 2. Setup a 3x3 grid
        intro_text = Text("1. Lấy một cửa sổ 3x3 pixel", font_size=32).to_edge(UP, buff=1.5)
        self.play(Write(intro_text))
        
        values = [
            [5, 4, 3],
            [4, 3, 1],
            [2, 0, 3]
        ]
        
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
                
        self.play(Create(grid))
        self.wait(1)
        
        # 3. Highlight the center pixel
        step2_text = Text("2. Chọn pixel trung tâm làm ngưỡng (Threshold)", font_size=32).to_edge(UP, buff=1.5)
        self.play(Transform(intro_text, step2_text))
        
        center_cell = cells[4]
        center_text = texts[4]
        self.play(center_cell.animate.set_fill(YELLOW, opacity=0.5))
        self.wait(1)
        
        center_val = values[1][1]
        
        # 4. Thresholding
        step3_text = Text("3. So sánh các pixel xung quanh với trung tâm", font_size=32).to_edge(UP, buff=1.5)
        self.play(Transform(intro_text, step3_text))
        
        binary_values = []
        binary_texts = []
        
        # Order: Top-Left, Top-Mid, Top-Right, Right, Bottom-Right, Bottom-Mid, Bottom-Left, Left
        neighbors_indices = [0, 1, 2, 5, 8, 7, 6, 3]
        
        for idx in neighbors_indices:
            val = int(texts[idx].text)
            bin_val = 1 if val >= center_val else 0
            binary_values.append(bin_val)
            
            self.play(cells[idx].animate.set_fill(GREEN if bin_val == 1 else RED, opacity=0.3), run_time=0.3)
            
            new_text = Text(str(bin_val), font_size=40, color=GREEN if bin_val == 1 else RED).move_to(cells[idx].get_center())
            self.play(Transform(texts[idx], new_text), run_time=0.3)
            binary_texts.append(new_text)
            
        self.wait(1)
        
        # 5. Extracting binary sequence
        step4_text = Text("4. Đọc chuỗi nhị phân (theo chiều kim đồng hồ)", font_size=32).to_edge(UP, buff=1.5)
        self.play(Transform(intro_text, step4_text))
        
        # Move grid up to make space for sequence
        self.play(grid.animate.scale(0.6).move_to(UP * 1 + LEFT * 3))
        
        bin_str = "".join([str(b) for b in binary_values])
        
        bin_group = VGroup()
        for i, b in enumerate(binary_values):
            t = Text(str(b), font_size=40, color=GREEN if b == 1 else RED)
            bin_group.add(t)
        
        bin_group.arrange(RIGHT, buff=0.2).next_to(grid, RIGHT, buff=1.5)
        
        arrow = Arrow(start=grid.get_right(), end=bin_group.get_left(), color=WHITE)
        self.play(GrowArrow(arrow))
        
        for i, idx in enumerate(neighbors_indices):
            self.play(Indicate(texts[idx]), Indicate(bin_group[i]), run_time=0.4)
            
        self.wait(1)
        
        # 6. Convert to decimal
        step5_text = Text("5. Chuyển nhị phân sang thập phân", font_size=32).to_edge(UP, buff=1.5)
        self.play(Transform(intro_text, step5_text))
        
        decimal_val = int(bin_str, 2)
        dec_text = Text(f"= {decimal_val}", font_size=48, color=YELLOW).next_to(bin_group, DOWN, buff=0.5)
        
        self.play(Write(dec_text))
        self.wait(2)
        
        # 7. Replace center pixel
        step6_text = Text("6. Thay thế pixel trung tâm bằng giá trị mới", font_size=32).to_edge(UP, buff=1.5)
        self.play(Transform(intro_text, step6_text))
        
        new_center_text = Text(str(decimal_val), font_size=40, color=YELLOW).move_to(center_cell.get_center())
        self.play(
            FadeOut(arrow), FadeOut(bin_group), FadeOut(dec_text),
            Transform(texts[4], new_center_text),
            center_cell.animate.set_fill(PURPLE, opacity=0.8)
        )
        self.wait(2)
        
        # 8. Conclusion summary
        self.play(FadeOut(grid), FadeOut(intro_text))
        
        summary_title = Text("Đặc trưng của LBP", font_size=40, color=BLUE).to_edge(UP)
        points = VGroup(
            Text("- Tóm tắt kết cấu cục bộ (local texture).", font_size=32),
            Text("- Ít bị ảnh hưởng bởi sự thay đổi ánh sáng đơn điệu.", font_size=32),
            Text("- Phân chia ảnh thành các ô (cells) và tạo Histogram.", font_size=32),
            Text("- Ghép các Histogram thành một vector đặc trưng duy nhất.", font_size=32)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).center()
        
        self.play(Write(summary_title))
        for point in points:
            self.play(FadeIn(point, shift=RIGHT))
            self.wait(1)
            
        self.wait(3)
        self.play(FadeOut(points), FadeOut(summary_title), FadeOut(title))
        
        end_text = Text("Cảm ơn đã theo dõi!", font_size=48, color=YELLOW)
        self.play(Write(end_text))
        self.wait(2)
