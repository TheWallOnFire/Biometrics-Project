# Bước 2: Phân tích thuật toán Local Binary Patterns (LBP)

Dưới đây là phần phân tích chi tiết về thuật toán **Local Binary Patterns (LBP)**, đáp ứng các tiêu chí về việc trình bày rõ ràng bài toán, cốt lõi ý tưởng, quy trình xử lý, cùng với ưu điểm và hạn chế của phương pháp.

---

## 1. Phát biểu bài toán

Trong lĩnh vực Thị giác máy tính (Computer Vision) nói chung và Sinh trắc học (Biometrics - cụ thể là Nhận dạng khuôn mặt) nói riêng, hình ảnh đầu vào thường chịu tác động rất lớn bởi môi trường:
- Ánh sáng thay đổi (sáng chói, bóng râm, hướng chiếu sáng).
- Tương phản của hình ảnh kém.
- Khuôn mặt hoặc bề mặt vật thể có kết cấu (texture) phức tạp.

**Bài toán đặt ra:** Làm thế nào để máy tính có thể trích xuất được những đặc trưng mang tính **cục bộ** (local features) của hình ảnh (như cạnh, góc, điểm đốm, nếp nhăn) một cách hiệu quả, nhưng đặc trưng đó phải **không bị biến đổi** khi điều kiện ánh sáng thay đổi?

Thuật toán **Local Binary Patterns (LBP)** được Ojala et al. giới thiệu vào năm 1994 (và sau đó được Ahonen áp dụng cho Face Recognition) chính là giải pháp hoàn hảo cho bài toán này.

---

## 2. Cốt lõi của ý tưởng

Ý tưởng cốt lõi của LBP rất thanh lịch và đơn giản: **Tóm tắt cấu trúc cục bộ của hình ảnh bằng cách đo lường độ chênh lệch sáng tối tương đối giữa một điểm ảnh và các điểm lân cận của nó, thay vì sử dụng giá trị độ sáng tuyệt đối.**

Cụ thể, thuật toán không quan tâm một pixel có giá trị là 50 (tối) hay 200 (sáng). Nó chỉ quan tâm rằng: *Pixel này sáng hơn hay tối hơn các pixel xung quanh nó?* 
Bằng cách ngưỡng hóa (thresholding) các pixel xung quanh dựa trên pixel trung tâm, ta thu được một chuỗi nhị phân (0 và 1). Chuỗi nhị phân này chính là một "mã" (code) mô tả chính xác dạng kết cấu cục bộ (ví dụ: điểm kết thúc, đường thẳng, góc nhọn) tại vị trí đó.

---

## 3. Quy trình xử lý của LBP

Quy trình để trích xuất đặc trưng khuôn mặt/kết cấu bằng LBP bao gồm các bước tuần tự sau:

### Bước 3.1. Xét cửa sổ cục bộ (Local Window)
- Lấy một vùng ma trận $3 \times 3$ pixel (gồm 1 pixel trung tâm và 8 pixel lân cận xung quanh) quét qua toàn bộ bức ảnh gốc (Grayscale).

### Bước 3.2. Ngưỡng hóa (Thresholding)
- Tại mỗi ma trận $3 \times 3$, lấy giá trị cường độ sáng của **pixel trung tâm** làm ngưỡng (Threshold - ký hiệu là $T$).
- So sánh từng pixel lân cận với $T$:
  - Nếu giá trị lân cận $\ge T$, gán giá trị mới là `1`.
  - Nếu giá trị lân cận $< T$, gán giá trị mới là `0`.

### Bước 3.3. Mã hóa nhị phân
- Đọc 8 giá trị nhị phân vừa tạo theo **chiều kim đồng hồ** (thường bắt đầu từ góc trên cùng bên trái) để tạo thành một chuỗi nhị phân có độ dài 8 bit (Ví dụ: `11001011`).

### Bước 3.4. Chuyển đổi sang thập phân
- Chuyển chuỗi nhị phân 8 bit đó thành một số thập phân (có giá trị từ 0 đến 255).
- Thay thế pixel trung tâm ban đầu bằng giá trị thập phân vừa tính được.
- *Kết quả sau khi quét toàn bộ ảnh là ta thu được một "Ảnh LBP" mới.*

### Bước 3.5. Phân chia lưới (Grid Division) và Tính Histogram
- Ảnh khuôn mặt không mang ý nghĩa nếu chỉ nhìn vào từng pixel LBP. Ta tiến hành chia ảnh LBP thu được thành các ô lưới (Grid/Cells) nhỏ (ví dụ lưới $8 \times 8$).
- Tại mỗi ô, tính **Biểu đồ tần suất (Histogram)** của các giá trị LBP (đếm xem mỗi giá trị từ 0-255 xuất hiện bao nhiêu lần trong ô đó).

### Bước 3.6. Xây dựng Vector đặc trưng (Feature Vector)
- Nối (Concatenate) tất cả các Histogram của các ô lại với nhau thành một Vector dài duy nhất. 
- Vector này chính là "chữ ký" cuối cùng đại diện cho khuôn mặt, sẵn sàng để đưa vào các thuật toán Machine Learning (như SVM, KNN) để phân loại.

---

## 4. Ưu điểm của LBP

1. **Kháng sự thay đổi ánh sáng đơn điệu cực tốt (Illumination Invariance):**
   Vì LBP chỉ lấy chênh lệch tương đối. Nếu ta cộng thêm hoặc nhân một hằng số vào toàn bộ bức ảnh (mô phỏng việc ảnh sáng lên hoặc tối đi), dấu của phép trừ giữa lân cận và trung tâm không thay đổi $\rightarrow$ Mã nhị phân LBP giữ nguyên không đổi.
2. **Độ phức tạp tính toán rất thấp:**
   Chỉ bao gồm các phép toán đơn giản nhất của máy tính: So sánh lớn/nhỏ và dịch bit (Bitwise shift). Không có phép nhân, chia hay căn bậc hai, giúp LBP chạy được theo thời gian thực (Real-time) trên các thiết bị nhúng.
3. **Mô tả kết cấu (Texture) xuất sắc:**
   Mã LBP bắt giữ rất tốt các vi cấu trúc (micro-structures) như Cạnh (Edges), Góc (Corners), hay Vùng phẳng (Flat areas).

---

## 5. Hạn chế của LBP

Dù rất mạnh mẽ, LBP vẫn tồn tại các điểm yếu chí mạng:

1. **Nhạy cảm với nhiễu cục bộ (Noise Sensitivity):**
   Trong ma trận $3 \times 3$, chỉ cần một pixel lân cận bị nhiễu làm nó vượt ngưỡng hoặc rớt ngưỡng, một bit sẽ bị lật (từ 0 thành 1 hoặc ngược lại). Sự lật bit này có thể làm thay đổi hoàn toàn giá trị thập phân của toàn bộ mã LBP (ví dụ `10000000` = 128 khác hoàn toàn `00000000` = 0).
2. **Kích thước không gian quá nhỏ:**
   Ma trận $3 \times 3$ (bán kính $R=1$) chỉ nhìn thấy một vùng rất nhỏ xíu, không bắt được các đặc điểm kết cấu ở quy mô lớn (Macro-patterns). (Để giải quyết, người ta mở rộng LBP thành bán kính linh hoạt $R$ và số lân cận $P$, gọi là Extended LBP).
3. **Mất thông tin sắc độ toàn cục:**
   Vì triệt tiêu ánh sáng để chống chói, LBP vô tình vứt bỏ luôn thông tin tổng thể về độ sáng/tối của bức ảnh. Ở một số ngữ cảnh phân loại, độ sáng toàn cục lại đóng vai trò quan trọng.
4. **Vector đặc trưng quá lớn:**
   Khi chia ảnh thành lưới nhỏ (VD: $8 \times 8 = 64$ ô), mỗi ô có histogram 256 bins. Vector nối lại sẽ có kích thước $64 \times 256 = 16384$ chiều, khá lớn và cồng kềnh cho việc phân loại. (Người ta thường dùng Uniform LBP để giảm từ 256 bins xuống còn 59 bins nhằm tiết kiệm không gian).
