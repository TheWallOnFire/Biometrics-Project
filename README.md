# LBP Animation Project (Biometrics)

Dự án trực quan hóa thuật toán **Local Binary Patterns (LBP)** sử dụng thư viện **Manim**. Video được thiết kế theo phong cách giáo dục hiện đại (tương tự 3Blue1Brown) nhằm giải thích cơ chế trích xuất đặc trưng khuôn mặt một cách trực quan và sinh động.

## 🚀 Tính năng nổi bật
- **Nội dung chuyên sâu**: Bao gồm LBP cơ bản, Circular LBP và Uniform Patterns.
- **Thời lượng tối ưu**: Đảm bảo trên 5 phút theo yêu cầu đồ án.
- **Thuyết minh AI**: Giọng đọc `NamMinhNeural` tự nhiên và chuyên nghiệp.
- **Phụ đề tự động**: Phụ đề tiếng Việt xuyên suốt video, hỗ trợ tiếp cận tốt hơn.

## 🛠️ Hướng dẫn cài đặt

Đảm bảo bạn đã cài đặt Python 3.8+ và Manim. Sau đó cài đặt các thư viện cần thiết:
```bash
pip install manim edge-tts mutagen numpy opencv-python
```

## 🎬 Cách chạy và Xuất video

### 1. Render Video
Để xuất video chất lượng cao (1080p, 60fps), sử dụng lệnh:
```bash
manim -pkh src/animations/lbp_animation.py LBPAnimation
```
- `-p`: Xem ngay sau khi render xong.
- `-k`: Giữ lại các file trung gian.
- `-h`: Chất lượng High (1080p). Nếu muốn render nhanh bản nháp, dùng `-ql` (Low Quality).

### 2. Chuẩn bị nộp bài (Submission)
Dự án đã tích hợp sẵn công cụ đóng gói theo đúng yêu cầu trong PDF:
```bash
python src/scripts/submission_prepare.py
```
- Công cụ sẽ tạo một thư mục mang tên MSSV (ví dụ: `22127000`).
- Bên trong chứa folder `source` (mã nguồn) và file `url.txt`.
- **Lưu ý**: Hãy sửa MSSV của bạn trong file `src/scripts/submission_prepare.py` trước khi chạy.

## 📌 Hashtags bắt buộc
Khi đăng tải video, vui lòng sử dụng các hashtag sau để đảm bảo tính lan tỏa:
`#fithcmus #patternrecognition #ai #ml`

## 📁 Cấu trúc thư mục
- `src/animations/`: Chứa kịch bản Manim chính (`lbp_animation.py`).
- `src/utils/`: Chứa các hàm bổ trợ vẽ lưới, xử lý âm thanh và phụ đề.
- `config/`: Chứa file `voice_data.json` (nội dung thuyết minh).
- `assets/`: Hình ảnh và tài nguyên sử dụng trong video.
- `media/`: Kết quả render (video và audio).

---
*Dự án được thực hiện cho môn học Nhận dạng (Biometrics) - 2026*