# Bước 3: Hướng dẫn Trực quan hóa thuật toán bằng Manim

Theo đúng yêu cầu của đồ án: *"Hạn chế tối đa việc nhồi nhét văn bản trên màn hình"*, triết lý xuyên suốt của kịch bản Manim này là **"Show, don't tell"** (Hãy cho người xem thấy, thay vì bắt họ đọc). Chúng ta sẽ dùng các chuyển động hình học (animations), sự thay đổi màu sắc, ma trận và vector để giải thích LBP.

Dưới đây là kịch bản phân rã thuật toán thành các khung hình (Scenes) trực quan:

---

## Cảnh 1 (Scene 1): Đặt vấn đề bằng hình ảnh (15 - 30 giây)

- **Mục tiêu:** Cho người xem thấy sự khó khăn của việc phân tích một bức ảnh dưới nhiều góc độ ánh sáng khác nhau.
- **Trực quan hóa (Không dùng chữ):** 
  - Đưa một bức ảnh khuôn mặt (grayscale) vào trung tâm màn hình (`ImageMobject`).
  - Dùng các bộ lọc (filter) hoặc làm mờ/chói lóa để bức ảnh thay đổi độ sáng (từ rất tối chuyển sang rất sáng chói).
  - Phóng to (`ScaleInPlace`) vào một vùng nhỏ trên khuôn mặt (ví dụ: khóe mắt hoặc góc mũi).
  - Vùng được phóng to sẽ từ từ phân rã thành một ma trận điểm ảnh (pixel grid), nơi các ô vuông chứa các con số từ 0-255 đại diện cho mức xám (Grayscale values).

---

## Cảnh 2 (Scene 2): Hoạt ảnh cốt lõi - Ma trận 3x3 và Ngưỡng hóa (1 - 2 phút)

- **Mục tiêu:** Mô phỏng quá trình tạo mã LBP từ ma trận pixel.
- **Trực quan hóa:**
  - **Trích xuất ma trận:** Vẽ một lưới ô vuông 3x3 (`Square`, `VGroup`) nằm giữa màn hình. Mỗi ô chứa một con số bất kỳ (ví dụ trung tâm là `5`, lân cận là `2, 8, 9, 3...`).
  - **Pixel trung tâm:** Ô vuông chính giữa nhấp nháy (`Indicate`) và đổi sang màu **Vàng (Yellow)**. Mũi tên trỏ vào và hiện chữ *"Threshold"* nhỏ.
  - **Quét lân cận (Chuyển động):** 
    - Bắt đầu từ góc trên bên trái, một con trỏ (hoặc đường viền highlight) sẽ chạy dọc theo chiều kim đồng hồ qua 8 ô xung quanh.
    - Tại mỗi ô, làm một animation so sánh nhanh: Văng ra dấu $\ge$ hoặc $<$.
    - **Đổi màu & Đổi số:** Nếu lớn hơn ngưỡng, ô vuông đó đổi màu viền thành **Xanh lá (Green)** và số cũ biến mất, số `1` xuất hiện. Nếu nhỏ hơn, đổi màu viền thành **Đỏ (Red)**, số `0` xuất hiện.
  - Sau khi quét xong 1 vòng, ta có một lưới $3 \times 3$ với tâm màu Vàng và xung quanh là toàn số 0 và 1 có màu Xanh/Đỏ rực rỡ. Không cần dòng chữ nào giải thích, người xem vẫn tự hiểu được quy luật!

---

## Cảnh 3 (Scene 3): Chuyển đổi sang Không gian Đặc trưng cục bộ (1 phút)

- **Mục tiêu:** Từ ma trận 3x3 tạo ra con số thập phân.
- **Trực quan hóa:**
  - **Trích xuất chuỗi nhị phân:** Các số `0` và `1` từ 8 ô xung quanh tách ra (dùng `Transform` hoặc `FadeOut`) và bay xuống dưới màn hình, xếp hàng ngang tạo thành một vector nhị phân (Ví dụ: `[1, 0, 1, 1, 0, 0, 0, 1]`).
  - Cung cấp một phương trình biến đổi nhỏ chạy mượt mà bên dưới: 
    $1 \times 2^7 + 0 \times 2^6 + ... + 1 \times 2^0 = 177$
  - Con số `177` (Màu Vàng sáng) bay ngược trở lại và "đè" lên pixel trung tâm ban đầu. Ô vuông trung tâm nháy sáng (`Flash`) báo hiệu sự hoàn tất.
  - Thu nhỏ lưới 3x3 đó lại và đẩy nó về lại bức ảnh tổng thể để ngầm ám chỉ: "Thao tác vừa rồi được lặp lại cho toàn bộ bức ảnh".

---

## Cảnh 4 (Scene 4): Không gian Vector và Biểu đồ tần suất (1.5 - 2 phút)

- **Mục tiêu:** Giải thích bước gộp các pixel thành Histogram và Feature Vector.
- **Trực quan hóa:**
  - Chia bức ảnh LBP (ảnh chứa toàn số từ 0-255) thành một mạng lưới (Grid) lớn hơn (ví dụ $4 \times 4$).
  - Mũi tên chỉ vào 1 ô lưới cụ thể. Từ ô lưới đó "nở" ra một biểu đồ cột (Bar Chart / `Axes` trong Manim) nhấp nhô đại diện cho Histogram cục bộ. Trục ngang là các giá trị từ 0-255.
  - Làm tương tự để xổ ra vài biểu đồ cột khác từ các ô khác.
  - **Concatenation (Nối Vector):** Cuối cùng, các biểu đồ cột này "móp" lại thành các thanh dài nằm ngang (Vectors 1D). Các thanh này di chuyển và **nối nối tiếp nhau** thành một thanh vector dài duy nhất vắt ngang màn hình.
  - Đóng dấu chữ **"Feature Vector"** to, rực rỡ ở cuối đoạn vector đó. Đây chính là không gian đặc trưng (Feature Space) dùng cho Machine Learning.

---

## 🚀 Một số mẹo Manim để tối ưu hóa hình ảnh
1. **Dùng màu sắc nhất quán:** Luôn dùng màu Xanh cho giá trị $\ge$ Threshold (đại diện cho 1) và Đỏ cho giá trị $<$ Threshold (đại diện cho 0) xuyên suốt video.
2. **Hạn chế dùng `Text`:** Chỉ dùng `Text` cho tiêu đề lớn chuyển cảnh. Đối với các công thức, bắt buộc phải dùng `MathTex` để đảm bảo độ sắc nét chuẩn học thuật.
3. **Điều khiển nhịp độ (Pacing):** Sử dụng `self.wait(1)` hoặc `self.wait(2)` hợp lý sau các bước biến đổi ma trận để não bộ người xem kịp xử lý thông tin hình ảnh trước khi bạn thuyết minh tiếp.
