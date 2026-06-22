from manim import *

def play_intro(scene, sub):
    scene.next_section("Intro")
    title_main = Text("Local Binary Patterns", font_size=64, color=BLUE)
    title_sub = Text("Trích xuất đặc trưng ảnh", font_size=32, color=LIGHT_GRAY).next_to(title_main, DOWN)
    
    sub("title_name")
    scene.play(Write(title_main))
    sub("title_intro")
    scene.play(FadeIn(title_sub, shift=UP*0.3))
    scene.wait(2)
    scene.play(FadeOut(title_main), FadeOut(title_sub))

    # ----------------------------------------------------
    # Part 1.5: Giới thiệu vấn đề
    # ----------------------------------------------------
    scene.next_section("Problem Introduction")
    prob_title = Text("Tại sao cần nhận dạng khuôn mặt?", color=BLUE).to_edge(UP)
    scene.play(Write(prob_title))
    
    sub("intro_prob_1")
    hist_text = Text("1. Lịch sử: 1960s (Thủ công) -> 1990s (PCA) -> Nay (Deep Learning)", font_size=28).shift(UP * 1.5)
    scene.play(FadeIn(hist_text, shift=UP))
    
    sub("intro_prob_2")
    why_text = Text("2. Ưu điểm: Phi tiếp xúc, Tự nhiên, Tiện lợi", font_size=28).next_to(hist_text, DOWN, buff=0.5).align_to(hist_text, LEFT)
    scene.play(FadeIn(why_text, shift=UP))
    
    sub("intro_prob_3")
    app_text = Text("3. Ứng dụng: Face ID, eKYC, CCTV", font_size=28).next_to(why_text, DOWN, buff=0.5).align_to(why_text, LEFT)
    scene.play(FadeIn(app_text, shift=UP))
    scene.wait(10)
    
    scene.play(FadeOut(prob_title), FadeOut(hist_text), FadeOut(why_text), FadeOut(app_text))

    # ----------------------------------------------------
    # Part 2: Lựa chọn thuật toán
    # ----------------------------------------------------
    scene.next_section("Algorithm Selection")
    sub("algo_compare_1")
    algo_title = Text("So sánh thuật toán", color=BLUE).to_edge(UP)
    scene.play(Write(algo_title))
    
    table = Table(
        [["Eigenfaces", "Dễ cài đặt", "Nhạy cảm ánh sáng"],
         ["Fisherfaces", "Phân lớp tốt", "Cần nhiều dữ liệu"],
         ["Minutiae", "Độ chính xác cao", "Cần phần cứng riêng"],
         ["Iris", "Không thể giả mạo", "Camera hồng ngoại"],
         ["LBP", "Nhanh, kháng ánh sáng", "Nhạy cảm nhiễu"]],
        col_labels=[Text("Thuật toán"), Text("Điểm mạnh"), Text("Điểm yếu")],
        include_outer_lines=True,
        line_config={"stroke_width": 1, "color": GRAY}
    ).scale(0.5).move_to(ORIGIN)
    
    scene.play(Create(table))
    scene.wait(1)
    
    sub("algo_compare_2")
    row_eigen = table.get_rows()[1]
    scene.play(row_eigen.animate.set_color(RED))
    scene.wait(1)
    scene.play(row_eigen.animate.set_color(WHITE))
    
    sub("algo_compare_3")
    row_lbp = table.get_rows()[5]
    scene.play(row_lbp.animate.set_color(YELLOW))
    scene.wait(1)
    
    sub("algo_compare_4")
    lbp_box = SurroundingRectangle(row_lbp, color=YELLOW)
    scene.play(Create(lbp_box))
    
    scene.wait(2)
    
    scene.play(FadeOut(algo_title), FadeOut(table), FadeOut(lbp_box))
