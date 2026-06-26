# Đồ án cá nhân môn học Nhận dạng
- MSSV: 23120105
- Tên: Huỳnh Mạnh Tường
- Lớp: 23CTT2

# Video
https://youtu.be/coH1ep8uJEk


# Thư viện
```bash
pip install -r requirements.txt
```

# Hướng dẫn cách chạy
1. Mở Terminal/Command Prompt tại thư mục giải nén (thư mục đang chứa file `url.txt` này).
2. Chạy lệnh sau để xuất video (chất lượng 1080p, 60fps):
```bash
manim -pqh src/animations/lbp_animation.py LBPAnimation
```

- Nếu gặp lỗi "Manim command not found", hãy đảm bảo rằng bạn đã kích hoạt môi trường ảo `manim` bằng lệnh `conda activate manim` (hoặc `source manim/bin/activate` trên Windows/Linux).
- Nếu gặp lỗi về đường dẫn hoặc file không tồn tại, hãy kiểm tra lại thư mục hiện tại trong Terminal đã trỏ đúng vào thư mục chứa file này chưa.
