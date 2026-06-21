# Phase 2: Tích hợp Backend (Ruby on Rails)

## 1. Công nghệ sử dụng
- **Framework:** Ruby on Rails (chạy ở chế độ `--api`).
- **Database:** PostgreSQL (hoặc SQLite3 cho môi trường dev).
- **Giao tiếp:** RESTful API (JSON).

## 2. Mục tiêu Phase 2
- Lưu trữ toàn bộ dữ liệu bốc thăm vào cơ sở dữ liệu để không bị mất kết quả nếu tải lại trang.
- Đặt nền móng cho các tính năng quản lý giải đấu dài hạn (Nhập kết quả tỉ số, tính điểm, xếp hạng, danh sách cầu thủ, vua phá lưới).

## 3. Thiết kế Database Schema cơ bản

Dự kiến các bảng (Tables) chính:

- **sports**
  - `id`: integer
  - `name`: string (VD: Bóng đá nam)
  - `team_count`: integer (VD: 16)
  
- **teams**
  - `id`: integer
  - `sport_id`: integer (FK)
  - `name`: string
  - `logo_url`: string
  - `representative_name`: string

- **groups**
  - `id`: integer
  - `sport_id`: integer (FK)
  - `name`: string (VD: Bảng A)

- **draw_results**
  - `id`: integer
  - `team_id`: integer (FK)
  - `group_id`: integer (FK)
  - `position`: integer (VD: 3)

*(Các bảng về `matches`, `goals` sẽ được thiết kế khi giải đấu chính thức khởi tranh).*

## 4. Các API Endpoints dự kiến

| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET | `/api/sports` | Lấy danh sách môn thi đấu. |
| GET | `/api/sports/:id/teams` | Lấy danh sách các đội tham gia môn đó. |
| GET | `/api/sports/:id/groups` | Lấy cấu trúc các bảng và danh sách các vị trí (slot) trống. |
| POST | `/api/draws/random_team` | Request backend quay ngẫu nhiên 1 đội chưa bốc thăm. |
| POST | `/api/draws/random_slot` | Request backend quay ngẫu nhiên 1 vị trí trống cho đội và lưu Database. |
| GET | `/api/teams/:id/schedule` | Trả về danh sách lịch thi đấu của đội đó. |

## 5. Danh sách công việc (Tasks Phase 2)
1. Dựng cấu trúc project `backend` bằng `rails new backend --api`.
2. Tạo các migrations và models.
3. Chèn (Seed) dữ liệu các đội làng Hamu Tanran vào DB.
4. Viết logic Random ở Controller (thay vì làm ở Frontend như Phase 1) để đảm bảo tính minh bạch và đồng bộ.
5. Sửa lại code Frontend (React) dùng `fetch` hoặc `axios` để gọi các API này thay vì dùng Mock Data.
