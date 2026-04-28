# Biometrics-Project: Trực Quan Hóa Thuật Toán Với Manim

Đồ án cá nhân môn **Nhận dạng (CSC14006)** - Khoa CNTT, Trường ĐH KHTN, ĐHQG TP.HCM.

## 1. Giới thiệu

Đồ án này thực hiện việc trực quan hóa một thuật toán trong lĩnh vực sinh trắc học và nhận dạng mẫu sử dụng thư viện **Manim** (Mathematical Animation Engine). Mục tiêu của đồ án là chuyển đổi một quy trình phức tạp thành ngôn ngữ hình ảnh chuyển động có tính thẩm mỹ và dễ hiểu cho người xem.

Thuật toán được lựa chọn: **Local Binary Patterns (LBP) - Đặc trưng cục bộ**.

## 2. Phân tích thuật toán LBP

### Bài toán
Trong nhận dạng khuôn mặt (Face Recognition) hoặc phân loại kết cấu (Texture Classification), một thách thức lớn là làm sao rút trích được các đặc trưng mang tính cục bộ (local features) trên khuôn mặt nhưng lại không bị thay đổi hoặc ảnh hưởng bởi sự khác biệt của ánh sáng môi trường. LBP ra đời để giải quyết vấn đề này.

### Cốt lõi của ý tưởng
Ý tưởng cốt lõi của LBP là tóm tắt cấu trúc cục bộ trong một hình ảnh bằng cách so sánh từng điểm ảnh (pixel) với các điểm lân cận của nó. Bất kỳ giá trị lân cận nào lớn hơn hoặc bằng giá trị trung tâm sẽ được đánh giá trị là `1`, ngược lại là `0`. Sau đó, bằng cách đọc các giá trị `0` và `1` này theo chiều kim đồng hồ, ta có được một chuỗi nhị phân (binary pattern) tương ứng với giá trị lân cận cục bộ đó. 

### Quy trình xử lý
1. **Lấy cửa sổ 3x3:** Lấy một vùng ma trận 3x3 pixel trên ảnh.
2. **Ngưỡng hóa (Thresholding):** Lấy giá trị của pixel trung tâm làm ngưỡng. So sánh 8 pixel xung quanh với ngưỡng.
3. **Mã hóa nhị phân:** Nếu pixel xung quanh có giá trị $\ge$ pixel trung tâm, gán thành `1`. Nếu $<$ pixel trung tâm, gán thành `0`.
4. **Tính giá trị LBP:** Đọc chuỗi nhị phân (thường là bắt đầu từ góc trên bên trái, theo chiều kim đồng hồ) và chuyển nó thành số thập phân (từ 0 đến 255).
5. **Gán giá trị:** Thay thế pixel trung tâm ban đầu bằng giá trị thập phân vừa tính được.
6. **Histogram:** Chia ảnh LBP thu được thành các vùng (cell), tính toán biểu đồ tần suất (Histogram) cho mỗi vùng.
7. **Vector đặc trưng:** Nối (concatenate) các Histogram cục bộ này lại với nhau để tạo thành một vector đặc trưng duy nhất (Feature Vector) mô tả toàn bộ khuôn mặt.

### Ưu điểm
- **Kháng ánh sáng tốt:** Vì LBP chỉ quan tâm đến sự chênh lệch độ sáng tương đối (lớn hơn/nhỏ hơn) giữa pixel trung tâm và lân cận, nên các thay đổi ánh sáng đơn điệu không làm thay đổi giá trị LBP.
- **Tính toán nhanh:** Phép toán so sánh và dịch bit vô cùng đơn giản và tốn ít tài nguyên tính toán.
- **Biểu diễn kết cấu tốt:** LBP mô tả mạnh mẽ các đặc trưng như cạnh (edges), góc (corners), điểm đốm (spots) hoặc các vùng phẳng (flat areas).

### Hạn chế
- Nhạy cảm với nhiễu ảnh ngẫu nhiên.
- Phiên bản LBP cơ bản (3x3) chỉ quan sát được đặc trưng trong không gian rất hẹp (local micro-patterns). Để khắc phục, người ta mở rộng LBP với bán kính $R$ và số điểm lân cận $P$ linh hoạt hơn.

## 3. Cấu trúc thư mục

```text
Biometrics-Project/
│
├── source/                      # Thư mục mã nguồn Manim
│   └── lbp_animation.py         # File chứa class Scene trực quan hoá LBP
│
├── url.txt                      # Đường dẫn chia sẻ video đã xuất
├── README.md                    # File tài liệu phân tích và hướng dẫn (file này)
└── Đồ án cá nhân.pdf            # File yêu cầu đề bài
```

## 4. Hướng dẫn chạy (Export Video)

Bạn cần cài đặt thư viện **Manim** (cùng với FFmpeg và LaTeX nếu cần kết xuất công thức phức tạp) trên máy tính trước khi chạy:

```bash
pip install manim
```

Di chuyển vào thư mục `source` và chạy câu lệnh sau để render video:

```bash
manim -pqh source/lbp_animation.py LBPAnimation
```

*Giải thích cờ lệnh:*
- `-p`: Tự động phát (play) video sau khi kết xuất thành công.
- `-qh`: Quality High (Độ phân giải 1080p, 60fps). Nếu máy tính cấu hình thấp, bạn có thể thay bằng `-qm` (Medium, 720p 30fps) hoặc `-ql` (Low, 480p 15fps) để render nhanh hơn.

Sau khi hoàn tất kết xuất, video sẽ được tự động lưu trong thư mục `media/` nội bộ.