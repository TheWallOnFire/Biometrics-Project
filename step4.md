# Bước 4: Kịch bản và Phụ đề (Final Version)

Kịch bản này đã được tối ưu hóa cho giọng đọc **NamMinhNeural** với phong cách trò chuyện tự nhiên, thân thiện.

---

## 📽️ Cấu trúc Video (6 Phần)

### 1. Tiêu đề và Giới thiệu
- **Hình ảnh**: Tiêu đề "Local Binary Patterns" và tên người thực hiện.
- **Lời dẫn**: "Chào bạn! Hôm nay chúng ta sẽ cùng nhau tìm hiểu về một thuật toán rất hay trong nhận dạng khuôn mặt, đó là LBP."
- **Visual**: Chuyển sang danh sách 6 phần chính.
- **Lời dẫn**: "Mình sẽ chia sẻ với các bạn sáu phần nội dung chính để chúng ta nắm vững kiến thức này nhé."

### 2. Liệt kê Thuật toán
- **Hình ảnh**: Danh sách các thuật toán (PCA, Eigenfaces, HOG, SIFT).
- **Lời dẫn**: "Chắc bạn đã nghe qua những cái tên như PCA hay SIFT rồi đúng không? Chúng đều rất nổi tiếng."
- **Visual**: Nhấn mạnh (Indicate) vào LBP.
- **Lời dẫn**: "But LBP lại có sức hút riêng nhờ sự đơn giản mà lại vô cùng hiệu quả."

### 3. Nguyên lý cơ bản
- **Hình ảnh**: Một tấm ảnh khuôn mặt với một ô vuông vàng quét qua (Sliding Window).
- **Lời dẫn**: "Về cơ bản, LBP sẽ so sánh từng điểm ảnh với các điểm xung quanh để tìm ra quy luật của ánh sáng."

### 4. Ví dụ Demo chi tiết
#### Ví dụ 1: Quy trình tính toán
- **Visual**: Ma trận 3x3 với các giá trị cường độ sáng.
- **Lời dẫn**: "Hãy cùng mình thực hiện một phép tính cụ thể để bạn dễ hình dung hơn nhé."
- **Step 1**: Chọn điểm trung tâm. "Đầu tiên, chúng mình sẽ lấy điểm ở chính giữa để làm chuẩn."
- **Step 2**: So sánh với 8 điểm bao quanh. "Sau đó, ta đem so sánh nó với tám điểm bao quanh."
- **Step 3**: Chuỗi nhị phân hiện ra. "Từ đó, một chuỗi số nhị phân sẽ được hình thành."
- **Step 4**: Kết quả thập phân. "Cuối cùng, kết quả là hai trăm bốn mươi."

#### Ví dụ 2: Khả năng kháng ánh sáng
- **Visual**: Ma trận 3x3 sáng hơn, nhưng kết quả LBP vẫn là 240.
- **Lời dẫn**: "Một ưu điểm tuyệt vời của LBP là nó không hề sợ ánh sáng thay đổi."
- **Lời dẫn**: "Bạn thấy đấy, dù mình có tăng độ sáng lên thì các bước so sánh vẫn diễn ra y hệt."
- **Lời dẫn**: "Kết quả vẫn không hề thay đổi so với lúc trước."
- **Lời dẫn**: "Điều này chứng tỏ mã LBP cực kỳ ổn định."

### 5. Ứng dụng: Under the Hood
- **Visual**: Con số 240 nhân bản ra hàng ngàn điểm trên toàn bộ khuôn mặt.
- **Lời dẫn**: "Hãy cùng quan sát quy trình bên trong nhé."
- **Lời dẫn**: "Con số hai trăm bốn mươi chỉ là một phần rất nhỏ thôi."
- **Lời dẫn**: "Máy tính sẽ lặp đi lặp lại việc này trên toàn bộ khuôn mặt của bạn."
- **Visual**: Biểu đồ tần suất (Histogram) được tạo ra.
- **Lời dẫn**: "Sau đó, tất cả sẽ được thống kê lại thật chi tiết."
- **Lời dẫn**: "Đây chính là mã định danh kỹ thuật số dành riêng cho bạn."
- **Lời dẫn**: "Và thế là, việc nhận diện đã thành công tốt đẹp."

### 6. Tổng kết
- **Visual**: Bảng ưu và nhược điểm.
- **Lời dẫn**: "Tất nhiên, cái gì cũng có hai mặt của nó."
- **Lời dẫn**: "Ưu điểm của LBP là nhanh và không ngại ánh sáng."
- **Lời dẫn**: "Hạn chế là nó khá nhạy cảm với nhiễu."
- **Lời dẫn**: "Cảm ơn các bạn đã dành thời gian theo dõi video về LBP của mình nhé."

---
*Kịch bản này đồng bộ hoàn toàn với file `config/voice_data.json`.*
