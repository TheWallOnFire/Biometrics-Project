# Bước 4: Kịch bản Thuyết minh (Voiceover Script) & Phụ đề

Dưới đây là kịch bản thuyết minh chi tiết được thiết kế để khớp hoàn hảo với nhịp độ hình ảnh (animations) của thư viện Manim. Các câu thoại dưới đây sẽ được sử dụng làm **phụ đề (subtitle)** trực tiếp trong video để giải thích chi tiết thuật toán Local Binary Patterns (LBP).

**Mẹo thu âm/AI Voice:**
- Hãy đọc với giọng điệu kể chuyện (storytelling) tự nhiên, có sự tò mò ở phần đầu và sự hứng khởi khi giải quyết được bài toán.
- Chú ý các khoảng **[PAUSE]** - đây là lúc bạn ngừng đọc khoảng 1-2 giây để nhường sự chú ý cho hoạt ảnh Manim đang chạy trên màn hình.

---

## Cảnh 1: Đặt vấn đề (Thời lượng: ~25s)

**Giọng đọc & Phụ đề:** 
1. "Hãy tưởng tượng bạn đang xây dựng một hệ thống nhận diện khuôn mặt."
2. "Mọi thứ hoạt động hoàn hảo trong phòng thí nghiệm. Nhưng khi mang ra ngoài đời thực..."
3. "...ánh sáng từ cửa sổ hay bóng râm sẽ làm bức ảnh thay đổi hoàn toàn."
4. **[PAUSE 1s]** 
5. "Đối với máy tính, hình ảnh chỉ là một ma trận các con số biểu diễn độ sáng."
6. "Khi ánh sáng thay đổi, các con số này nhảy múa hỗn loạn."
7. "Vậy làm sao để máy tính hiểu được đâu là khuôn mặt mà không bị đánh lừa bởi ánh sáng?"
8. "Câu trả lời nằm ở một thuật toán vô cùng thanh lịch: Local Binary Patterns - LBP."

---

## Cảnh 2: Ma trận 3x3 và Ngưỡng hóa (Thời lượng: ~45s)

**Giọng đọc & Phụ đề:** 
9. "Ý tưởng cốt lõi của LBP rất đơn giản."
10. "Đừng quan tâm một điểm ảnh có độ sáng chính xác là bao nhiêu."
11. "Hãy chỉ hỏi một câu: Nó sáng hơn hay tối hơn những người hàng xóm của nó?"
12. **[PAUSE 1.5s]**
13. "Hãy trích xuất một ô vuông 3x3. Chúng ta sẽ dùng điểm ảnh ở chính giữa làm Ngưỡng."
14. "Giờ hãy quét vòng quanh. Bất kỳ điểm ảnh lân cận nào lớn hơn hoặc bằng điểm trung tâm..."
15. "...ta cho nó giá trị 1. Ngược lại, nếu nhỏ hơn, ta cho nó giá trị 0."
16. "Chú ý này, dù toàn bộ bức ảnh bị làm sáng lên..."
17. "...khoảng cách tương đối này vẫn không đổi! Đó chính là phép thuật kháng ánh sáng của LBP."
18. **[PAUSE 2s]**

---

## Cảnh 3: Chuyển đổi nhị phân (Thời lượng: ~25s)

**Giọng đọc & Phụ đề:**
19. "Tuyệt vời! Bây giờ, hãy lấy các số 0 và 1 này, đọc theo chiều kim đồng hồ."
20. "Ta sẽ có được một chuỗi nhị phân 8 bit."
21. "Dùng một chút toán học cơ bản, ta đổi chuỗi nhị phân này thành một số thập phân."
22. **[PAUSE 1s]**
23. "Con số mới này sẽ thay thế cho điểm ảnh trung tâm ban đầu."
24. "Nó không còn đại diện cho độ sáng nữa, mà là một mã tóm tắt hình dáng cục bộ."

---

## Cảnh 4: Không gian Đặc trưng (Feature Space) (Thời lượng: ~30s)

**Giọng đọc & Phụ đề:**
25. "Tất nhiên, một điểm ảnh không làm nên khuôn mặt."
26. "Ta chia bức ảnh LBP thành một tấm lưới các ô vuông nhỏ."
27. "Tại mỗi ô, ta thống kê lại tần suất xuất hiện của các mã LBP thành biểu đồ Histogram."
28. "Cuối cùng, móc nối tất cả các biểu đồ này lại với nhau..."
29. "Bùm! Ta thu được một Feature Vector khổng lồ."
30. "Đây chính là 'chữ ký' định danh độc nhất của khuôn mặt đó..."
31. "...hoàn toàn miễn nhiễm với ánh sáng, sẵn sàng cho AI nhận dạng."
32. "Đơn giản, hiệu quả và thanh lịch. Đó là Local Binary Patterns!"
