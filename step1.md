# Bước 1: Lựa chọn và Phân tích Thuật toán

Trong khuôn khổ môn học Nhận dạng và các tài liệu tham khảo cốt lõi (*Handbook of Biometrics* và *Handbook of Face Recognition 2nd Edition*), có rất nhiều thuật toán kinh điển được trình bày. Dưới đây là việc liệt kê các lựa chọn khả thi, so sánh, và lý do cuối cùng dẫn đến việc chọn **Local Binary Patterns (LBP)**.

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

Mục tiêu tối thượng của đồ án không chỉ là lập trình thuật toán, mà là **trực quan hóa thuật toán đó bằng thư viện Manim** thành một video mạch lạc, dễ hiểu theo phong cách 3Blue1Brown.

| Thuật toán | Mức độ phức tạp toán học | Tính khả thi khi diễn hoạt (Animation) bằng Manim | Đánh giá cho đồ án |
| :--- | :--- | :--- | :--- |
| **Eigenfaces / Fisherfaces** | Rất cao (Đại số tuyến tính phức tạp: Covariance Matrix, Eigenvectors) | Trung bình. Rất khó để minh họa quá trình tính toán PCA trên một ảnh lớn mà không làm người xem rối mắt. Cần vẽ nhiều không gian vector. | Hơi hàn lâm, khó giữ sự tập trung của khán giả đại chúng. |
| **Minutiae / Iris** | Khá cao (Bộ lọc Gabor, Xử lý hình thái học) | Khó. Manim mạnh về toán học hình học và ma trận, việc xử lý và vẽ lại đường vân tay (curves) rất tốn công và khó đẹp. | Không tối ưu cho Manim. |
| **LBP (Được chọn)** | Rất thấp (Chỉ có phép toán So sánh >, < và Đổi cơ số) | **Cực kỳ xuất sắc.** LBP vận hành ngay trên một ma trận ô vuông (Grid) 3x3 nhỏ gọn. | **Hoàn hảo.** Dễ dàng biến đổi màu sắc, dịch chuyển ô, tạo hiệu ứng đếm số nhị phân. |

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
