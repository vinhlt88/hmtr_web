# Phase 1: Thiết kế Hệ Frontend (Mock Data)

## 1. Công nghệ sử dụng
- **Framework:** React (khởi tạo qua Vite để có tốc độ build cực nhanh).
- **Styling:** Vanilla CSS kết hợp CSS Modules (tạo hiệu ứng chuyển động, glassmorphism, responsive).
- **Thư viện phụ trợ (dự kiến):** `react-confetti` (hiệu ứng pháo giấy), các thư viện UI cho wheel/randomizer (nếu cần).
- **Dữ liệu:** Dùng mảng Object trong JavaScript (Mock Data) để mô phỏng Database.

## 2. Sơ đồ các trang (Page Structure)

```mermaid
graph TD
    A[Trang Chủ / Chọn Môn] --> B(Bóng Đá Nam)
    A --> C(Bóng Đá Nữ)
    
    B --> D[Màn Hình Trình Chiếu Sự Kiện]
    C --> D
    
    D --> E[Trạng thái 1: Random Đội lên bốc]
    D --> F[Trạng thái 2: Random Bảng & Vị trí]
    D --> G[Trạng thái 3: Hiển thị Bảng đấu & Lịch thi đấu]
```

## 3. Kịch bản Bốc Thăm (Flow Double Random)

Quá trình trên màn hình trình chiếu (kết nối máy chiếu) diễn ra theo các bước sau:

```mermaid
sequenceDiagram
    actor MC as MC / Khán giả
    actor Rep as Đại diện Đội bóng
    participant System as Màn hình Trình Chiếu (React)

    Note over MC,System: BƯỚC 1: TÌM ĐỘI LÊN SÂN KHẤU
    MC->>System: Bấm nút "Tìm Đội Tiếp Theo"
    System-->>System: Hiệu ứng quay / xáo thẻ ngẫu nhiên (3s)
    System-->>MC: Nổi bật tên Đội trúng tuyển (VD: "ĐỘI LÀNG A")
    MC->>Rep: Mời đại diện Đội Làng A lên sân khấu
    
    Note over Rep,System: BƯỚC 2: BỐC THĂM BẢNG ĐẤU
    Rep->>System: Tự tay bấm nút "BỐC THĂM" to giữa màn hình
    System-->>System: Hiệu ứng âm thanh + Vòng quay vị trí
    System-->>MC: Vỡ oà kết quả: "BẢNG B - VỊ TRÍ SỐ 3" + Pháo giấy
    
    Note over MC,System: BƯỚC 3: XEM LỊCH THI ĐẤU
    System-->>System: Chuyển cảnh hiển thị Bảng B
    System-->>MC: Render 3 trận đấu vòng bảng của Đội Làng A (dựa trên mẫu Lịch thi đấu vị trí 3)
    
    MC->>System: Bấm "Tiếp tục" vòng lặp cho đội tiếp theo
```

## 4. Danh sách công việc (Tasks Phase 1)
1. Dựng cấu trúc project `frontend` bằng Vite.
2. Xây dựng Mock Data JSON (16 đội nam, 8 đội nữ).
3. Code layout Màn hình tổng quan (Các bảng đấu A, B, C, D).
4. Code hiệu ứng Random Đội (chọn 1 phần tử trong mảng những đội chưa bốc).
5. Code hiệu ứng Random Vị trí (chọn 1 phần tử trong mảng các slot chưa có chủ).
6. Code hiển thị Lịch thi đấu tự động dựa trên Vị trí.
7. Đóng gói và chạy thử nghiệm thực tế (Mở full screen trên browser).
