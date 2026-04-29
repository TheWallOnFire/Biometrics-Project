from manim import *
import random
import warnings
warnings.filterwarnings("ignore")

Text.set_default(font="sans-serif")

class LBPAnimation(Scene):
    def construct(self):
        # ----------------------------------------------------
        # Scene 1: Đặt vấn đề
        # ----------------------------------------------------
        try:
            face = ImageMobject("face.png").scale(1.5)
        except Exception:
            # Fallback if image not found
            face = Rectangle(width=6, height=8, fill_color=GRAY, fill_opacity=1)
        
        self.play(FadeIn(face))
        self.wait(1)
        
        # Overlay for lighting change
        lighting_overlay = Rectangle(width=14, height=8, fill_color=WHITE, fill_opacity=0)
        self.add(lighting_overlay)
        
        self.play(lighting_overlay.animate.set_fill(opacity=0.6), run_time=1)
        self.play(lighting_overlay.animate.set_fill(BLACK, opacity=0.8), run_time=1)
        self.play(lighting_overlay.animate.set_fill(WHITE, opacity=0), run_time=1)
        
        self.wait(1)
        
        # Zoom into the face
        self.play(face.animate.scale(4).shift(DOWN*4 + RIGHT*2), run_time=2)
        
        # Transition to a 8x8 Grid representing pixel values
        pixel_grid = VGroup()
        for i in range(8):
            for j in range(8):
                cell = Square(side_length=0.8, color=GRAY)
                cell.move_to(RIGHT * (j - 3.5) * 0.8 + DOWN * (i - 3.5) * 0.8)
                val = random.randint(50, 200)
                text = Text(str(val), font_size=24).move_to(cell.get_center())
                pixel_grid.add(VGroup(cell, text))
                
        self.play(FadeOut(face), FadeIn(pixel_grid))
        self.wait(2)
        
        # Highlight a 3x3 region
        region_3x3 = VGroup()
        for i in range(2, 5):
            for j in range(2, 5):
                region_3x3.add(pixel_grid[i*8 + j])
                
        self.play(
            pixel_grid.animate.set_opacity(0.1),
            region_3x3.animate.set_opacity(1)
        )
        self.wait(1)
        
        self.play(FadeOut(pixel_grid))
        
        # ----------------------------------------------------
        # Scene 2: Ma trận 3x3 và Ngưỡng hóa
        # ----------------------------------------------------
        values = [
            [120, 110, 85],
            [100, 95, 60],
            [80, 50, 90]
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
                
        self.play(ReplacementTransform(region_3x3, grid))
        self.wait(1)
        
        center_cell = cells[4]
        center_text = texts[4]
        center_val = values[1][1] # 95
        
        # Highlight center
        self.play(center_cell.animate.set_fill(YELLOW, opacity=0.5))
        
        threshold_arrow = Arrow(start=RIGHT*3 + UP*0, end=center_cell.get_right(), color=YELLOW)
        threshold_text = Text("Threshold", font_size=32, color=YELLOW).next_to(threshold_arrow, RIGHT)
        
        self.play(GrowArrow(threshold_arrow), Write(threshold_text))
        self.wait(2)
        self.play(FadeOut(threshold_arrow), FadeOut(threshold_text))
        
        # Order: Top-Left, Top-Mid, Top-Right, Right, Bottom-Right, Bottom-Mid, Bottom-Left, Left
        neighbors_indices = [0, 1, 2, 5, 8, 7, 6, 3]
        binary_values = []
        binary_texts = []
        
        for idx in neighbors_indices:
            val = int(texts[idx].text)
            bin_val = 1 if val >= center_val else 0
            binary_values.append(bin_val)
            
            # Show comparison
            comp_str = "≥" if bin_val == 1 else "<"
            comp_tex = Text(comp_str, font_size=48).move_to(cells[idx].get_center())
            self.play(FadeOut(texts[idx]), FadeIn(comp_tex), run_time=0.2)
            self.wait(0.1)
            
            self.play(cells[idx].animate.set_fill(GREEN if bin_val == 1 else RED, opacity=0.3), run_time=0.2)
            
            new_text = Text(str(bin_val), font_size=40, color=GREEN if bin_val == 1 else RED).move_to(cells[idx].get_center())
            self.play(ReplacementTransform(comp_tex, new_text), run_time=0.2)
            binary_texts.append(new_text)
            
        self.wait(2)
        
        # ----------------------------------------------------
        # Scene 3: Chuyển đổi sang thập phân
        # ----------------------------------------------------
        # Move grid up
        self.play(grid.animate.scale(0.8).shift(UP * 1.5))
        
        bin_group = VGroup()
        for i, b in enumerate(binary_values):
            t = Text(str(b), font_size=40, color=GREEN if b == 1 else RED)
            bin_group.add(t)
        
        bin_group.arrange(RIGHT, buff=0.2).next_to(grid, DOWN, buff=1)
        
        # Animate digits moving down
        moves = []
        for i, idx in enumerate(neighbors_indices):
            moves.append(ReplacementTransform(binary_texts[i].copy(), bin_group[i]))
            
        self.play(*moves)
        self.wait(1)
        
        formula_str = "1 × 2⁷ + 1 × 2⁶ + 0 × 2⁵ + 0 × 2⁴ + 0 × 2³ + 0 × 2² + 0 × 2¹ + 1 × 2⁰ = 193"
        formula_tex = Text(formula_str, font_size=32).next_to(bin_group, DOWN, buff=0.8)
        
        self.play(Write(formula_tex))
        self.wait(2)
        
        # Move result back to center
        result_text = Text("193", font_size=48, color=YELLOW)
        result_text.move_to(center_cell.get_center())
        
        self.play(
            FadeOut(bin_group),
            FadeOut(formula_tex),
            ReplacementTransform(center_text, result_text)
        )
        self.play(Flash(center_cell, color=YELLOW))
        self.wait(2)
        
        # ----------------------------------------------------
        # Scene 4: Không gian Vector
        # ----------------------------------------------------
        self.play(FadeOut(grid))
        
        large_grid = VGroup(*[Square(side_length=0.8, color=WHITE) for _ in range(16)])
        large_grid.arrange_in_grid(rows=4, cols=4, buff=0)
        large_grid.move_to(LEFT * 4)
        
        self.play(FadeIn(large_grid))
        self.wait(1)
        
        # Histogram 1
        self.play(large_grid[5].animate.set_fill(BLUE, opacity=0.5))
        chart_1 = BarChart(
            values=[15, 30, 45, 20, 10, 50],
            y_range=[0, 60, 20],
            y_length=2,
            x_length=3,
            bar_colors=[BLUE],
            y_axis_config={"label_constructor": Text}
        ).next_to(large_grid, RIGHT, buff=1).shift(UP * 1)
        self.play(Create(chart_1))
        
        # Histogram 2
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
        
        # Concatenate into Vector
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
        self.play(Write(fv_text))
        self.wait(3)

        # ----------------------------------------------------
        # End Scene
        # ----------------------------------------------------
        self.play(
            FadeOut(large_grid),
            FadeOut(feature_vector),
            FadeOut(fv_text)
        )
        end_text = Text("Cảm ơn các bạn đã theo dõi!", font_size=48, color=YELLOW)
        hashtag = Text("#LocalBinaryPatterns #AI", font_size=32, color=BLUE).next_to(end_text, DOWN, buff=0.5)
        self.play(Write(end_text))
        self.play(FadeIn(hashtag))
        self.wait(3)
