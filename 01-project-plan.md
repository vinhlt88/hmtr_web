# Kế hoạch phát triển Website Bốc thăm Làng Hamu Tanran

## 1. Mục tiêu (Goal)
Xây dựng một hệ thống website phục vụ sự kiện lễ bốc thăm chia bảng các môn thể thao của làng Hamu Tanran. 
Website không chỉ đóng vai trò là một công cụ chia bảng mà còn là một phần trình diễn trên sân khấu (trình chiếu lên màn hình lớn), mang lại cảm giác hồi hộp, chuyên nghiệp và phấn khích (Wow Effect) cho toàn bộ khán giả và các đội tham gia.

## 2. Yêu cầu hệ thống (Requirements)
- **Môn thể thao ưu tiên:**
  - Bóng đá nam: 16 đội, chia thành 4 bảng (A, B, C, D), mỗi bảng 4 đội.
  - Bóng đá nữ: 8 đội, chia thành 2 bảng (A, B), mỗi bảng 4 đội.
  - *(Bóng chuyền nam sẽ được bổ sung sau).*
- **Logic bốc thăm (Double Random Hồi hộp):**
  - Danh sách đội lên bốc thăm được chọn ngẫu nhiên.
  - Vị trí và bảng đấu của đội đó cũng được bốc ngẫu nhiên.
- **Tính năng mở rộng:**
  - Ngay sau khi bốc được vị trí (VD: Bảng B - Vị trí 3), hệ thống lập tức hiển thị Lịch thi đấu vòng bảng của đội đó (sẽ gặp ai ở các lượt trận).
  - Có thể tổng hợp và in ra bảng đấu, lịch thi đấu cuối cùng.
- **Nền tảng công nghệ:** 
  - Frontend: React (Vite).
  - Backend: Ruby on Rails.

## 3. Lộ trình triển khai (Phases)
Dự án được chia làm 2 giai đoạn chính để có thể nhanh chóng có bản demo trực quan nhất.

- **[Phase 1: Thiết kế hệ Frontend (Mock Data)](./02-phase-1-frontend.md)**
  - Tập trung 100% vào UI/UX và các hiệu ứng animation (Spinning wheel, Confetti, Flip cards).
  - Sử dụng dữ liệu giả (Mock data) để chạy toàn bộ kịch bản bốc thăm mượt mà trên trình duyệt.
  - Có thể dùng ngay cho buổi lễ thực tế (nếu không yêu cầu lưu trữ dữ liệu phức tạp trên server).

- **[Phase 2: Tích hợp Backend (Rails API)](./03-phase-2-backend.md)**
  - Xây dựng database để lưu trữ danh sách đội vĩnh viễn.
  - Xây dựng API và nối với Frontend.
  - Hỗ trợ các tính năng trong tương lai: Cập nhật tỉ số trận đấu, bảng xếp hạng tự động, danh sách vua phá lưới.
