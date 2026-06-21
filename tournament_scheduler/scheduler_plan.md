# Kế hoạch & Giải thuật Xếp Lịch Thi Đấu Bóng Đá (Có thể tái sử dụng)

Tài liệu này ghi chú lại chi tiết phương pháp tiếp cận và giải thuật đã được thiết kế riêng để xếp lịch cho **Giải bóng đá nam sân 11** với quy mô lớn, nhiều điều kiện ưu tiên khắt khe. Có thể dùng làm tham chiếu để tái tạo lại lịch cho các mùa giải sau.

---

## 1. Thông Tin Chung & Quy Mô
*   **Thể thức:** Sân 11 người.
*   **Số lượng đội:** 21 đội, chia làm 5 bảng:
    *   **Bảng A:** 5 đội (đá 10 trận).
    *   **Bảng B, C, D, E:** 4 đội/bảng (đá 6 trận/bảng).
*   **Tổng số trận vòng bảng:** 34 trận.
*   **Công suất sân bãi:** 2 trận/ngày.
    *   Khung giờ 1 (14:30)
    *   Khung giờ 2 (16:00 - ưu tiên)

---

## 2. Các Ràng Buộc Khắt Khe (Constraints)
Việc xếp lịch trở nên cực kỳ phức tạp khi phải thỏa mãn đồng thời các yếu tố sau:
1.  **Thứ tự vòng đấu:** Các bảng phải đá đúng trình tự thời gian từ Vòng 1 đến Vòng cuối (Không được đá vòng sau khi chưa đá vòng trước).
2.  **Thời gian nghỉ (Thể lực):** Các đội phải có ít nhất 1 ngày nghỉ, nhưng tuyệt đối không nghỉ quá 7 ngày (tránh tình trạng chờ đợi quá lâu mất cảm giác bóng).
3.  **Công bằng Khung giờ:** 100% các đội phải có ít nhất 1 trận được đá vào khung giờ mát (16:00). Độ lệch giữa số trận 14:30 và 16:00 phải được nén về mức tối thiểu tuyệt đối.
4.  **Công bằng Cuối tuần:** 100% các đội phải được đá ít nhất 1 trận vào cuối tuần (Thứ 7 hoặc Chủ Nhật).
5.  **Công bằng Sân bãi:** Phân bổ tỷ lệ làm Đội Nhà / Đội Khách cân bằng nhất có thể.
6.  **Trình tự Xuất phát & Về đích (Cực khó):**
    - **Tất cả 21 đội (5 bảng)** bắt buộc phải xuất trận ít nhất 1 lần ngay trong **6 ngày thi đấu đầu tiên**.
    - **5 bảng đấu** bắt buộc phải lần lượt kết thúc vòng bảng vào đúng **5 ngày thi đấu cuối cùng** của giai đoạn 1, tạo ra chuỗi "chung kết ngược" kịch tính mỗi ngày.

---

## 3. Giải Pháp Thuật Toán Đề Xuất (Hybrid Approach)
Do bài toán quá chặt (Overconstrained) nếu sử dụng các bộ giải Constraint Programming thông thường, chúng ta áp dụng mô hình **Hybrid (CSP + Hoán vị Brute-Force/Monte Carlo)**.

### Bước 1: Sinh bộ khung Ngày thi đấu (Backtracking / Combinatorics)
Thay vì xếp riêng từng trận, chúng ta quyết định **Bảng nào đá vào ngày nào**.
- Bảng A cần 5 ngày. Bảng B, C, D, E mỗi bảng cần 3 ngày.
- **Duyệt qua tất cả cấu hình tổ hợp:** Chọn ra 5 ngày cho Bảng A và 12 ngày cho Bảng B, C, D, E sao cho:
  - Bảng A bắt buộc đá trận Khai mạc (Ngày 1).
  - Tất cả các bảng phải có ngày ra quân nằm trong khoảng Ngày 1 đến Ngày 6.
  - Các ngày kết thúc của 5 bảng phải điền kín và chính xác 5 ngày cuối cùng của vòng bảng (Ngày 13, 14, 15, 16, 17).
  - Khoảng thời gian trống (chờ) giữa các lượt trận của mọi đội tuyệt đối không được vượt quá 7 ngày.
  - Khớp với lịch cuối tuần của giải.
- **Tối ưu Pareto (Pareto Optimization):** Sau khi quét (Brute-force kết hợp Pruning) qua hàng tỷ tổ hợp, thuật toán chỉ lọc ra được **duy nhất 1 bộ cấu hình** thỏa mãn toàn bộ những ràng buộc siêu khó này để đưa vào sử dụng.

### Bước 2: Tối ưu Giờ thi đấu (Brute Force / Monte Carlo)
Với danh sách các ngày đã gắn cứng cho các bảng, thứ tự các cặp đấu vòng tròn (Round Robin) cũng đã được xác định.
- Mỗi ngày có 2 trận (T1 và T2). Có $2^n$ cách hoán đổi trận nào đá 14:30, trận nào đá 16:00.
- Xây dựng **Hàm chi phí (Cost Function)**:
  - Lỗi = Tổng độ lệch tuyệt đối của số trận T1 và T2 của từng đội so với giá trị lý tưởng.
  - Ví dụ Bảng A lý tưởng là 2 T1, 2 T2. Bảng 4 đội lý tưởng là 1.5 T1, 1.5 T2 (tương đương 2-1 hoặc 1-2).
- Tiến hành chạy hoán vị toàn bộ các tổ hợp giờ thi đấu:
  - Đối với Bảng A (5 đội, 10 trận), thuật toán tìm được cấu hình phân bổ giờ hoàn hảo (Lỗi = 0).
  - Đối với các Bảng B, C, D, E (4 đội, 6 trận, gồm 3 trận T1 và 3 trận T2): Dựa trên **Lý thuyết Đồ thị (Graph Theory)**, không tồn tại bất kỳ cách chia nào để mỗi đội đá từ 1 đến 2 trận 16:00 mà không vi phạm vòng tròn đấu. Cấu hình toán học bắt buộc duy nhất tạo ra được là **Đồ thị Hình Ngôi sao (Star Graph)**, trong đó 1 đội làm tâm điểm đá 3 trận 16:00, và 3 đội còn lại mỗi đội đá 1 trận 16:00. Thuật toán đã phát hiện ra quy luật này và chốt hạ đúng giới hạn (Lỗi = 6.0) nhằm đảm bảo tuân thủ luật "Mỗi đội ít nhất 1 trận 16:00" (Không có đội bị điểm 0).

### Bước 3: Ánh xạ Sân Nhà / Sân Khách
Sử dụng chuẩn Round Robin (ví dụ: Thuật toán Polygon hoặc Circle Method) để tự động cân bằng số trận Nhà/Khách ngay trong bộ danh sách các trận đấu, sau đó ánh xạ vào ngày và giờ đã tối ưu.

---

## 4. Hướng Dẫn Tái Sử Dụng Cho Mùa Giải Sau
1. **Nếu số lượng đội giữ nguyên:** Hoàn toàn có thể dùng lại khung lịch của mùa giải này, chỉ cần thay đổi Ngày Bắt Đầu (offset toàn bộ ngày) và bốc thăm gán tên Đội bóng vào các mã A1, A2, B1,...
2. **Nếu số lượng đội thay đổi:** Cần chạy lại toàn bộ pipeline 3 bước trên bằng các script Python tương ứng đã được xây dựng (`find_days.py` -> `super_balancer.py` -> `perfect_balancer.py`).
