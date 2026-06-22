from manim import *
import os

def play_core_idea(scene, sub, project_root):
    # ----------------------------------------------------
    # Core Problem & Idea (Step 2.md)
    # ----------------------------------------------------
    scene.next_section("Core Problem")
    prob_title = Text("Bài toán & Ý tưởng cốt lõi", color=BLUE).to_edge(UP)
    scene.play(Write(prob_title))
    
    sub("core_problem")
    prob_desc = Text("Vấn đề: Ảnh thực tế thay đổi nhiều do ánh sáng.", font_size=32).shift(UP * 1)
    scene.play(FadeIn(prob_desc, shift=UP))
    scene.wait(1)
    
    sub("core_idea")
    idea_desc = Text("Ý tưởng: Lấy độ sáng tương đối thay vì tuyệt đối.", font_size=32, color=YELLOW).next_to(prob_desc, DOWN, buff=0.5)
    scene.play(FadeIn(idea_desc, shift=UP))
    scene.wait(10)
    
    scene.play(FadeOut(prob_desc), FadeOut(idea_desc))

    # ----------------------------------------------------
    # Part 3: Giải thích sơ về cách hoạt động
    # ----------------------------------------------------
    scene.next_section("Basic Logic")
    sub("part_3_logic")
    
    steps = VGroup(
        Text("1. Xét cửa sổ cục bộ (3x3)", font_size=28),
        Text("2. Ngưỡng hóa (Thresholding)", font_size=28),
        Text("3. Mã hóa nhị phân", font_size=28),
        Text("4. Chuyển sang thập phân", font_size=28),
        Text("5. Tính Histogram", font_size=28),
        Text("6. Xây dựng Vector đặc trưng", font_size=28)
    ).arrange(DOWN, aligned_edge=LEFT).next_to(prob_title, DOWN, buff=0.5).to_edge(LEFT, buff=1)
    
    for i, step in enumerate(steps):
        sub(f"step_{i+1}_audio")
        scene.play(FadeIn(step, shift=RIGHT))
        
    scene.wait(2)
    scene.play(FadeOut(steps), FadeOut(prob_title))

    # ----------------------------------------------------
    # Part 4: 2 Ví dụ Demo
    # ----------------------------------------------------
    scene.next_section("Demo Examples")
    from src.utils.utils import create_pixel_grid, create_3x3_grid, create_circular_lbp_grid
    
    # --- Demo 1: Detailed ---
    sub("demo_1_title")
    demo1_label = Text("Ví dụ 1: Quy trình tính toán chi tiết", color=BLUE).to_edge(UP)
    scene.play(Write(demo1_label))
    
    values1 = [[210, 215, 220], [200, 205, 215], [60, 65, 70]]
    grid1, cells1, texts1 = create_3x3_grid(values1)
    grid1.scale(0.7).shift(LEFT * 3)
    
    scene.play(Create(grid1))
    
    sub("demo_1_step_1")
    center_cell = cells1[4]
    center_cell.set_fill(YELLOW, opacity=0.5)
    scene.play(Indicate(center_cell))
    scene.wait(1)
    
    sub("demo_1_step_2")
    neighbors_indices = [0, 1, 2, 5, 8, 7, 6, 3]
    bin_vals = []
    
    for idx in neighbors_indices:
        val = values1[idx//3][idx%3]
        res = 1 if val >= 205 else 0
        bin_vals.append(res)
        
        scene.play(cells1[idx].animate.set_stroke(YELLOW, width=8), run_time=0.15)
        res_text = Text(str(res), color=GREEN if res==1 else RED, font_size=40).move_to(cells1[idx])
        scene.play(ReplacementTransform(texts1[idx], res_text), run_time=0.15)
        scene.play(cells1[idx].animate.set_stroke(WHITE, width=2), run_time=0.1)
        
    sub("demo_1_step_3")
    bin_display = Text("Binary: " + " ".join(map(str, bin_vals)), font_size=36).shift(RIGHT*3 + UP*1)
    scene.play(Write(bin_display))
    scene.wait(1)
    
    sub("demo_1_step_4")
    dec_display = Text("Decimal: 240", font_size=48, color=YELLOW).next_to(bin_display, DOWN, buff=1)
    scene.play(Write(dec_display))
    scene.play(Indicate(dec_display))
    scene.wait(2)
    
    scene.play(FadeOut(grid1), FadeOut(bin_display), FadeOut(dec_display), FadeOut(demo1_label))

    # --- Demo 2: Robustness ---
    sub("demo_2_title")
    demo2_label = Text("Ví dụ 2: Kháng ánh sáng", color=GREEN).to_edge(UP)
    scene.play(Write(demo2_label))
    
    values2 = [[min(v + 50, 255) for v in row] for row in values1]
    grid2, cells2, texts2 = create_3x3_grid(values2)
    grid2.scale(0.7).shift(LEFT * 3)
    
    sub("demo_2_step_1")
    scene.play(Create(grid2))
    cells2[4].set_fill(YELLOW, opacity=0.5)
    scene.play(Indicate(cells2[4]))
    scene.wait(1)
    
    sub("demo_2_robust_result")
    bin_vals2 = []
    for idx in neighbors_indices:
        val = values2[idx//3][idx%3]
        res = 1 if val >= 255 else 0 
        bin_vals2.append(res)
        res_text = Text(str(res), color=GREEN if res==1 else RED, font_size=40).move_to(cells2[idx])
        scene.play(ReplacementTransform(texts2[idx], res_text), run_time=0.15)

    sub("demo_2_step_3")
    bin_display2 = Text("Binary: " + " ".join(map(str, bin_vals2)), font_size=36).shift(RIGHT*3 + UP*1)
    dec_display2 = Text("Decimal: 240", font_size=48, color=YELLOW).next_to(bin_display2, DOWN, buff=1)
    
    scene.play(Write(bin_display2))
    scene.play(Write(dec_display2))
    scene.play(Circumscribe(dec_display2))
    scene.wait(3)
    
    scene.play(FadeOut(grid2), FadeOut(bin_display2), FadeOut(dec_display2), FadeOut(demo2_label))

    # ----------------------------------------------------
    # Part 4.5: Circular LBP
    # ----------------------------------------------------
    scene.next_section("Circular LBP")
    sub("circular_intro")
    
    circle_title = Text("Circular LBP (Cải tiến)", color=BLUE).to_edge(UP)
    scene.play(Write(circle_title))
    
    circ_grid_1, center_1, dots_1, circ_1 = create_circular_lbp_grid(radius=1.5, num_points=8)
    circ_grid_1.shift(LEFT * 3)
    
    sub("circular_logic")
    scene.play(Create(circ_1), FadeIn(center_1))
    scene.play(Create(dots_1))
    scene.wait(1)
    
    sub("circular_params")
    circ_grid_2, center_2, dots_2, circ_2 = create_circular_lbp_grid(radius=2.5, num_points=16)
    circ_grid_2.shift(RIGHT * 3)
    
    params_text = MathTex("R=2.5, P=16", color=YELLOW).next_to(circ_grid_2, DOWN)
    
    scene.play(
        ReplacementTransform(circ_grid_1.copy(), circ_grid_2),
        Write(params_text)
    )
    scene.wait(2)
    scene.play(FadeOut(circ_grid_1), FadeOut(circ_grid_2), FadeOut(circle_title), FadeOut(params_text))

    # ----------------------------------------------------
    # Part 4.6: Uniform Patterns
    # ----------------------------------------------------
    scene.next_section("Uniform Patterns")
    sub("uniform_intro")
    
    uni_title = Text("Uniform Patterns (Tối ưu)", color=GREEN).to_edge(UP)
    scene.play(Write(uni_title))
    
    p_val = Text("P = 8 points", font_size=36).shift(UP * 1.5)
    mã_vô_tận = Text("256 Patterns", font_size=48, color=RED).shift(UP * 0.5)
    
    scene.play(Write(p_val))
    scene.play(FadeIn(mã_vô_tận, shift=DOWN))
    scene.wait(1)
    
    sub("uniform_logic")
    # Show a uniform vs non-uniform example
    uniform_code = Text("00011100 (2 transitions)", font_size=32, color=GREEN).shift(LEFT * 3 + DOWN * 1)
    non_uniform_code = Text("01010101 (8 transitions)", font_size=32, color=RED).shift(RIGHT * 3 + DOWN * 1)
    
    scene.play(Write(uniform_code))
    scene.play(Write(non_uniform_code))
    scene.play(Indicate(uniform_code))
    scene.wait(1)
    
    sub("uniform_benefit")
    reduced_mã = Text("59 Patterns", font_size=64, color=YELLOW).move_to(mã_vô_tận)
    scene.play(ReplacementTransform(mã_vô_tận, reduced_mã))
    scene.play(FadeOut(non_uniform_code))
    scene.play(uniform_code.animate.move_to(ORIGIN + DOWN * 1))
    scene.wait(2)
    
    scene.play(FadeOut(uni_title), FadeOut(p_val), FadeOut(reduced_mã), FadeOut(uniform_code))
