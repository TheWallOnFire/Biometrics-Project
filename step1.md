# Bước 1: Lựa chọn và Phân tích Thuật toán

Trong khuôn khổ môn học Nhận dạng và các tài liệu tham khảo cốt lõi (*Handbook of Biometrics* và *Handbook of Face Recognition 2nd Edition*), có rất nhiều thuật toán kinh điển được trình bày. Dưới đây là việc liệt kê các lựa chọn khả thi, so sánh, và lý do cuối cùng dẫn đến việc chọn **Local Binary Patterns (LBP)**.

## Giới thiệu vấn đề

### Tại sao lại cần nhận dạng khuôn mặt?

**1. Lịch sử của nhận dạng khuôn mặt:**
Nhận dạng khuôn mặt bắt đầu được nghiên cứu từ những năm 1960 với hệ thống bán tự động của Woodrow Wilson Bledsoe, yêu cầu con người đánh dấu các điểm đặc trưng (mắt, mũi, miệng) trên ảnh bằng tay. Đến những năm 1990, sự ra đời của **Eigenfaces** (Sirovich và Kirby) đã đánh dấu bước ngoặt khi hệ thống có thể tự động trích xuất đặc trưng bằng đại số tuyến tính. Sau đó, **Local Binary Patterns (LBP)** xuất hiện vào đầu những năm 2000 như một phương pháp tối ưu đặc trưng cục bộ. Đến hiện tại, với sự bùng nổ của Deep Learning (Mạng nơ-ron tích chập CNN), nhận dạng khuôn mặt đã đạt độ chính xác vượt qua khả năng của con người.

**2. Tại sao lại chọn khuôn mặt làm sinh trắc học?**
Khuôn mặt là đặc điểm sinh trắc học tự nhiên và ít mang tính xâm phạm nhất. Không giống như vân tay hay mống mắt (đòi hỏi sự hợp tác tích cực từ người dùng và thiết bị quét chuyên dụng tiếp xúc gần), khuôn mặt có thể được nhận dạng từ xa một cách thụ động bằng camera thông thường. Điều này mang lại sự tiện lợi tối đa và mô phỏng chính xác cách con người nhận diện nhau trong giao tiếp hàng ngày.

**3. Ứng dụng của nhận dạng khuôn mặt:**
Công nghệ này hiện hữu mạnh mẽ trong đời sống hiện đại:
- **Xác thực thiết bị cá nhân:** Mở khóa điện thoại (Face ID), máy tính (Windows Hello).
- **An ninh và kiểm soát ra vào:** Chấm công nhân viên, kiểm tra hành khách tại sân bay, nhận diện đối tượng theo dõi qua camera công cộng.
- **Tài chính - Ngân hàng (eKYC):** Mở tài khoản trực tuyến, xác thực thanh toán điện tử.
- **Phân tích dữ liệu & Giải trí:** Các bộ lọc (filters) AR trên mạng xã hội, phân tích cảm xúc khách hàng trong bán lẻ.

### Ưu và nhược điểm của nhận dạng khuôn mặt

**Ưu điểm:**
- **Phi tiếp xúc (Non-contact):** Vệ sinh, an toàn và thân thiện, đặc biệt hữu ích trong các bối cảnh y tế hoặc chống dịch bệnh.
- **Nhận dạng từ xa & Tự động hóa:** Có thể xử lý đồng thời nhiều đối tượng trong khung hình mà không làm gián đoạn luồng di chuyển của họ.
- **Không yêu cầu phần cứng quá đắt đỏ:** Chỉ cần một camera tiêu chuẩn (Webcam, CCTV) là đã có thể triển khai ở mức cơ bản, thay vì các cảm biến laser mống mắt đắt tiền.

**Nhược điểm:**
- **Nhạy cảm với môi trường và ngoại cảnh:** Độ chính xác dễ suy giảm nghiêm trọng khi thay đổi ánh sáng (ngược sáng, thiếu sáng), góc chụp lệch, biểu cảm khuôn mặt biến đổi, hoặc bị che khuất bởi phụ kiện (kính, khẩu trang).
- **Vấn đề Quyền riêng tư (Privacy):** Việc có thể thu thập khuôn mặt thụ động dẫn đến rủi ro lạm dụng giám sát hàng loạt (mass surveillance).
- **Rủi ro giả mạo (Spoofing):** Nếu không tích hợp công nghệ phát hiện thực thể sống (Liveness Detection), hệ thống dễ bị đánh lừa bởi ảnh in độ phân giải cao hoặc video phát lại từ điện thoại.

---

## 1. Các lựa chọn thuật toán khả thi

Dựa vào các giáo trình, ta có một số thuật toán kinh điển và phổ biến nhất có thể lựa chọn cho đồ án:

1. **Eigenfaces (Sử dụng PCA - Principal Component Analysis):**
   - *Phân loại:* Face Recognition (Holistic approach - Tiếp cận toàn cục).
   - *Nguyên lý:* Tìm ra các "khuôn mặt cơ sở" (eigenfaces) từ một tập dữ liệu bằng cách tính ma trận hiệp phương sai và trị riêng. Mỗi khuôn mặt mới sẽ được biểu diễn bằng tổ hợp tuyến tính của các eigenfaces này.

2. **Fisherfaces (Sử dụng LDA - Linear Discriminant Analysis):**
   - *Phân loại:* Face Recognition (Holistic approach).
   - *Nguyên lý:* Tương tự Eigenfaces nhưng tối ưu hóa khả năng phân lớp bằng cách làm cực đại hóa khoảng cách giữa các lớp (các người khác nhau) và cực tiểu hóa phương sai trong cùng một lớp.

3. **Minutiae Matching (Trích xuất và Khớp đặc trưng vân tay):**
   - *Phân loại:* Fingerprint Recognition.
   - *Nguyên lý:* Tìm các điểm đặc trưng (minutiae) trên vân tay như điểm rẽ nhánh (bifurcation) hoặc điểm kết thúc (ridge ending), sau đó dùng các thuật toán đối sánh không gian để so khớp hai vân tay.

4. **Iris Recognition (Thuật toán Daugman):**
   - *Phân loại:* Iris Recognition.
   - *Nguyên lý:* Sử dụng bộ lọc Gabor 2D để trích xuất đặc trưng mống mắt thành các mã nhị phân (IrisCode), sau đó so sánh bằng khoảng cách Hamming.

5. **Local Binary Patterns (LBP - Đặc trưng cục bộ):**
   - *Phân loại:* Face / Texture Recognition (Local approach - Tiếp cận cục bộ).
   - *Nguyên lý:* Rút trích đặc trưng kết cấu của ảnh bằng cách so sánh cường độ sáng của pixel trung tâm với các pixel xung quanh trong một ma trận nhỏ (thường là 3x3), từ đó tạo ra một mã nhị phân.

---

## 2. So sánh và Lý do chọn Local Binary Patterns (LBP)

So sánh các thuật toán:

| Thuật toán | Điểm mạnh | Điểm yếu | Lý do chọn |
| :--- | :--- | :--- | :--- |
| **Eigenfaces (PCA)** | Dễ cài đặt, giảm chiều dữ liệu tốt. | Bị ảnh hưởng mạnh bởi ánh sáng, góc chụp. | Khó trực quan hóa bằng Manim do liên quan nhiều đến đại số tuyến tính thay vì hình ảnh trực quan. |
| **Fisherfaces (LDA)** | Khắc phục được nhược điểm ánh sáng của PCA, phân lớp tốt hơn. | Cần nhiều dữ liệu mẫu cho mỗi lớp để huấn luyện hiệu quả. | Giống PCA, nặng về toán ma trận, khó biểu diễn bằng animation. |
| **Minutiae (Vân tay)** | Độ chính xác rất cao, chuẩn công nghiệp. | Yêu cầu thiết bị thu nhận phần cứng chuyên dụng, ảnh hưởng bởi vết xước/bẩn. | Đặc trưng vân tay khá phức tạp để vẽ và giải thích từng bước. |
| **Iris Recognition** | Không thể giả mạo, ổn định theo thời gian. | Yêu cầu camera hồng ngoại, khó lấy mẫu. | Biến đổi Gabor 2D cực kỳ khó hình dung và minh họa qua video 2D. |
| **LBP (Khuôn mặt)** | Rất nhẹ, tính toán nhanh, bất biến với thay đổi ánh sáng đơn điệu. | Nhạy cảm với nhiễu (noise), chỉ lấy được đặc trưng cục bộ hẹp. | **Được chọn.** Vì LBP rất trực quan (so sánh ma trận 3x3), dễ dàng vẽ animation bằng Manim và cực kỳ dễ hiểu cho người xem. |

### Tại sao lại chọn LBP?
- **Khả năng kể chuyện (Storytelling) cao:** LBP đi từ một bài toán vật lý rất trực quan: "Làm sao để một cái máy tính hiểu được đâu là góc cạnh, đâu là mặt phẳng trên ảnh rổ rá, da người?". Từ đó đưa ra giải pháp so sánh số lớn bé rất tự nhiên. Người xem không cần biết Toán cấp cao vẫn hiểu được.
- **Tối ưu sức mạnh của Manim:** Thư viện Manim render các hình khối hình học (`Square`, `Table`, `Grid`) và chữ số (`Text`, `MathTex`) vô cùng mượt mà. LBP là thuật toán có thể được minh họa hoàn toàn bằng các đối tượng này (cửa sổ 3x3 trượt, thay đổi màu sắc ô vuông khi thỏa mãn điều kiện, mũi tên trỏ ra chuỗi nhị phân).
- **Tính kinh điển:** Ahonen và cộng sự (2006) đã biến LBP thành một baseline xuất sắc trong Face Recognition. Nó hoàn toàn đáp ứng độ sâu học thuật yêu cầu từ giáo trình.

---

## 3. Bất lợi / Hạn chế của LBP

Dù là thuật toán phù hợp nhất để làm đồ án trực quan hóa, bản thân LBP trong thực tế cũng có những nhược điểm và hạn chế:

1. **Nhạy cảm với nhiễu ngẫu nhiên (Noise):** 
   - Vì LBP so sánh trực tiếp các pixel lân cận với pixel trung tâm một cách cứng ngắc, chỉ cần một pixel bị nhiễu (noise) làm thay đổi nhỏ cường độ sáng cũng có thể lật bit (từ 0 thành 1 hoặc ngược lại), dẫn đến mã LBP bị sai lệch hoàn toàn.
2. **Không gian quan sát quá hẹp (Local Micro-patterns):** 
   - Phiên bản LBP cơ bản (3x3) chỉ quan sát được bán kính cực nhỏ ($R=1$). Điều này khiến nó gặp khó khăn trong việc nắm bắt các đặc trưng kết cấu lớn hơn (Macro-patterns). (Để khắc phục, người ta phải dùng các biến thể như Multi-scale LBP, nhưng sẽ tốn kém chi phí tính toán hơn).
3. **Mất thông tin về cường độ sáng toàn cục:** 
   - LBP hoàn toàn loại bỏ cường độ sáng tuyệt đối (chỉ lấy chênh lệch tương đối). Ở một số bài toán, độ sáng toàn cục lại chứa thông tin quan trọng để phân loại.
4. **Kích thước Vector Đặc trưng lớn:** 
   - Khi chia ảnh ra nhiều vùng (regions) để tính Histogram, nếu chia quá nhỏ, chuỗi vector nối lại sẽ rất dài, dẫn đến tốn bộ nhớ và chậm chạp trong quá trình huấn luyện mô hình phân loại phía sau.

Thêm phần step2.md vào video: phát biểu bài toán, ý tưởng, quy trình xử lý + 2 ví dụ demo đơn giản, đánh giá + nhạn xét ưu và nhược điểm,