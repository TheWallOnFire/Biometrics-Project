from manim import *
import os
import numpy as np

def play_evaluation(scene, sub, project_root):
    # --- Application: Real-world Recognition (Under the Hood) ---
    scene.next_section("Real-world Application")
    sub("app_title")
    app_label = Text("Ứng dụng: Under the Hood", color=YELLOW).to_edge(UP)
    scene.play(Write(app_label))
    
    # Step 1: Show the "240" code
    sub("uth_one")
    code_240 = Text("240", font_size=72, color=BLUE).move_to(ORIGIN)
    scene.play(FadeIn(code_240))
    scene.wait(1)
    
    sub("app_uth_2")
    scene.play(code_240.animate.scale(0.5).to_edge(UP, buff=1.2))
    
    # Step 2: Show a grid of many codes
    sub("app_uth_3")
    codes_grid = VGroup(*[
        Text(str(np.random.randint(0, 256)), font_size=18) 
        for _ in range(64)
    ]).arrange_in_grid(rows=8, cols=8, buff=0.4).move_to(ORIGIN)
    scene.play(LaggedStart(*[FadeIn(c) for c in codes_grid], lag_ratio=0.01))
    scene.wait(1)
    
    # Step 3: Codes flow into a Histogram
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
        
    scene.play(
        FadeIn(hist_axes), FadeIn(x_label), FadeIn(y_label),
        code_240.animate.move_to(hist_axes.c2p(240, 0), aligned_edge=DOWN).set_opacity(0),
    )
    
    scene.play(
        LaggedStart(*[
            c.animate.move_to(bars[np.random.randint(0, len(bars))].get_top()).set_opacity(0)
            for c in codes_grid
        ], lag_ratio=0.01),
        Create(bars),
        run_time=4
    )
    
    sub("uth_five")
    identity_label = Text("Identity Face Print", color=YELLOW, font_size=36).next_to(hist_axes, UP)
    scene.play(Write(identity_label))
    scene.play(Indicate(identity_label))
    scene.wait(2)
    
    # Step 4: Final Match result
    sub("match_desc")
    face_path = os.path.join(project_root, "assets", "face_portrait.png")
    face1 = ImageMobject(face_path).scale(0.4).shift(LEFT * 3)
    face2 = ImageMobject(face_path).scale(0.4).shift(RIGHT * 3)
    face2.set_opacity(0.5)
    
    scene.play(
        hist_axes.animate.scale(0.5).to_edge(DOWN),
        bars.animate.scale(0.5).move_to(hist_axes.c2p(128, 0), aligned_edge=DOWN),
        identity_label.animate.scale(0.5).next_to(hist_axes, UP, buff=0.1),
        FadeIn(face1), FadeIn(face2)
    )
    
    sub("match_robust")
    scene.play(Indicate(face1), Indicate(face2))
    scene.wait(1)
    
    sub("app_result")
    match_symbol = Text("MATCH!", color=GREEN, font_size=80).move_to(ORIGIN).set_z_index(100)
    bg_rect = SurroundingRectangle(match_symbol, color=GREEN, fill_color=BLACK, fill_opacity=0.9)
    scene.play(FadeIn(bg_rect), Write(match_symbol))
    scene.play(Indicate(match_symbol))
    scene.wait(2)
    
    scene.play(
        FadeOut(hist_axes), FadeOut(bars), FadeOut(identity_label),
        FadeOut(match_symbol), FadeOut(bg_rect), FadeOut(app_label),
        FadeOut(x_label), FadeOut(y_label), FadeOut(codes_grid),
        FadeOut(code_240), FadeOut(face1), FadeOut(face2)
    )

    # ----------------------------------------------------
    # Part 5: Ưu và Nhược điểm
    # ----------------------------------------------------
    scene.next_section("Pros and Cons")
    sub("pros_cons_title")
    pc_title = Text("Ưu và Nhược điểm", font_size=48, color=BLUE).to_edge(UP)
    scene.play(Write(pc_title))
    
    pros = VGroup(
        Text("Ưu điểm:", color=GREEN, font_size=32),
        Text("- Kháng ánh sáng đơn điệu cực tốt", font_size=24),
        Text("- Độ phức tạp tính toán rất thấp", font_size=24),
        Text("- Mô tả kết cấu (Texture) xuất sắc", font_size=24)
    ).arrange(DOWN, aligned_edge=LEFT).to_edge(LEFT, buff=0.5).shift(UP * 0.5)
    
    cons = VGroup(
        Text("Nhược điểm:", color=RED, font_size=32),
        Text("- Rất nhạy cảm với nhiễu cục bộ", font_size=24),
        Text("- Kích thước không gian quan sát quá hẹp", font_size=24),
        Text("- Mất thông tin sắc độ toàn cục", font_size=24),
        Text("- Kích thước Vector đặc trưng lớn", font_size=24)
    ).arrange(DOWN, aligned_edge=LEFT).to_edge(RIGHT, buff=0.5).shift(UP * 0.5)
    
    sub("pro_1")
    scene.play(FadeIn(pros[0], shift=RIGHT))
    scene.play(FadeIn(pros[1], shift=RIGHT))
    
    for i in range(2, len(pros)):
        sub(f"pro_{i}")
        scene.play(FadeIn(pros[i], shift=RIGHT))
        
    scene.wait(1)
    
    sub("con_1")
    scene.play(FadeIn(cons[0], shift=LEFT))
    scene.play(FadeIn(cons[1], shift=LEFT))
    
    for i in range(2, len(cons)):
        sub(f"con_{i}")
        scene.play(FadeIn(cons[i], shift=LEFT))
        
    scene.wait(2)
    scene.play(FadeOut(pros), FadeOut(cons), FadeOut(pc_title))

    # ----------------------------------------------------
    # Part 6: Kết luận
    # ----------------------------------------------------
    scene.next_section("Conclusion")
    
    # Conclusion 1
    sub("conclusion_1")
    summary_title = Text("Tổng kết", color=BLUE, font_size=48).to_edge(UP)
    scene.play(Write(summary_title))
    
    point1 = Text("- Thuật toán kinh điển & mang tính nền tảng", font_size=32).shift(UP*1)
    scene.play(FadeIn(point1, shift=RIGHT))
    scene.wait(1)
    
    # Conclusion 2
    sub("conclusion_2")
    point2 = Text("- Thanh lịch, cực nhẹ & chạy mượt trên thiết bị yếu", font_size=32).next_to(point1, DOWN, buff=0.8).align_to(point1, LEFT)
    scene.play(FadeIn(point2, shift=RIGHT))
    scene.wait(10)
    
    scene.play(FadeOut(summary_title), FadeOut(point1), FadeOut(point2))
    
    # Conclusion 3
    sub("conclusion_3")
    final_text = Text("Local Binary Patterns", font_size=60, color=BLUE)
    tagline = Text("Đơn giản - Hiệu quả - Thanh lịch", font_size=32, color=YELLOW).next_to(final_text, DOWN)
    
    scene.play(Write(final_text))
    scene.play(FadeIn(tagline, shift=UP*0.5))
    scene.wait(3)
