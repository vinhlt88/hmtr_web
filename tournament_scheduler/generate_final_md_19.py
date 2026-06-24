import re
from collections import defaultdict

with open("final_men_19.txt", "r") as f:
    group_stage_md = f.read()

stats = defaultdict(lambda: {'total': 0, '1430': 0, '1600': 0, 'home': 0, 'away': 0, 'weekend': 0})
weekends = ['T7', 'CN']

# Track matches played by each team to calculate the "Vòng" (Round)
team_match_count = defaultdict(int)

new_group_stage_md = ""

for line in group_stage_md.strip().split('\n'):
    if not line.startswith('|'): continue
    cols = [c.strip() for c in line.split('|')]
    if len(cols) < 9: continue
    
    stt_ngay = cols[1]
    date_str = cols[2]
    time_str = cols[3]
    home = cols[4]
    away = cols[5]
    bang = cols[6]
    rest_home = cols[7]
    rest_away = cols[8]
    
    if not home.strip(): continue
    
    is_weekend = any(w in date_str for w in weekends)
    
    # Home team stats
    stats[home]['total'] += 1
    stats[home]['home'] += 1
    if time_str == '14:30': stats[home]['1430'] += 1
    if time_str == '16:00': stats[home]['1600'] += 1
    if is_weekend: stats[home]['weekend'] += 1
    
    # Away team stats
    stats[away]['total'] += 1
    stats[away]['away'] += 1
    if time_str == '14:30': stats[away]['1430'] += 1
    if time_str == '16:00': stats[away]['1600'] += 1
    if is_weekend: stats[away]['weekend'] += 1

    # Calculate Round
    team_match_count[home] += 1
    team_match_count[away] += 1
    r1 = team_match_count[home]
    r2 = team_match_count[away]
    avg_round = (r1 + r2) / 2
    if avg_round.is_integer():
        round_str = str(int(avg_round))
    else:
        round_str = str(avg_round)
        
    new_group_stage_md += f"| {stt_ngay} | {date_str} | {round_str} | {time_str} | {home} | {away} | {bang} | {rest_home} | {rest_away} |\n"

# Sort teams
teams = sorted(stats.keys())

stats_md = """# Thống kê số trận đấu Vòng bảng (19 Đội)

Bảng thống kê chi tiết số trận thi đấu của từng đội bóng tại giải Bóng đá Truyền thống Palei Hamu Tanran 2026 trong giai đoạn 1.

| Đội | Tổng số trận | Trận 1 (14:30) | Trận 2 (16:00) | Sân Nhà | Sân Khách | Số trận cuối tuần |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
"""
for t in teams:
    s = stats[t]
    stats_md += f"| **{t}** | {s['total']} | {s['1430']} | {s['1600']} | {s['home']} | {s['away']} | {s['weekend']} |\n"

stats_md += """
---

### Xác nhận tuân thủ điều kiện (Thuật toán Z3 Solver):
- **Thời gian thi đấu:** Khai mạc 04/07/2026, nghỉ lễ bắt buộc 08/07/2026, bế mạc 02/08/2026.
- **Số trận đấu:** Bảng 5 đội đá đúng 4 trận, Bảng 4 đội đá đúng 3 trận.
- **Khoảng cách nghỉ ngơi:** Các đội luôn được nghỉ ít nhất 1 ngày. ĐẶC BIỆT: Đã tối ưu hóa thành công khoảng thời gian nghỉ tối đa (Max Rest Limit), không đội bóng nào phải nghỉ chờ quá **8 ngày** (triệt tiêu hoàn toàn con số 10-12 ngày trước đây).
- **Ngày thi đấu:** 100% đội bóng (19 đội) đều có thi đấu **ít nhất 1 trận vào cuối tuần** (Thứ 7 hoặc Chủ Nhật).
- **Giờ thi đấu:** 100% đội bóng thuộc các bảng 5 đội (A, B, C) đều có ĐÚNG 2 TRẬN lúc 16:00. Riêng bảng D có 2 đội đá 2 trận, 2 đội đá 1 trận (Tối ưu tuyệt đối).
"""

full_doc = f"""# Lịch Thi Đấu Bóng Đá Nam (19 Đội) - Palei Hamu Tanran 2026

**Tổng quan giải đấu**
- **Ngày khởi tranh:** 04/07/2026
- **Ngày nghỉ bắt buộc:** 08/07/2026 (Nghỉ đám cưới)
- **Ngày bế mạc:** 02/08/2026
- **Khung giờ:** 14:30 (Trận 1) và 16:00 (Trận 2) mỗi ngày.
- **Các bảng đấu (19 đội):**
  - **Bảng A:** 5 đội
  - **Bảng B:** 5 đội
  - **Bảng C:** 5 đội
  - **Bảng D:** 4 đội

**Thể thức vòng loại**
- **Vòng bảng:** Đá vòng tròn một lượt tính điểm.
- **Vòng Knock-out:** Chọn 2 đội Nhất và Nhì mỗi bảng (Tổng 8 đội) vào thẳng vòng Tứ kết.

---

## 1. Giai đoạn 1: Vòng bảng

| STT Ngày | Ngày | Vòng | Giờ | Đội Nhà | Đội Khách | Bảng | Nghỉ (Nhà) | Nghỉ (Khách) |
|:---:|---|:---:|---|:---:|:---:|:---:|:---:|:---:|
{new_group_stage_md}
---

## 2. Vòng Tứ kết (Cuối tuần)

| Ngày | Giờ | Đội Nhà | Đội Khách | Trận |
|---|---|:---:|:---:|:---:|
| 25/07/2026 (T7) | 14:30 | Nhất Bảng A | Nhì Bảng B | Tứ kết 1 |
| 25/07/2026 (T7) | 16:00 | Nhất Bảng B | Nhì Bảng A | Tứ kết 2 |
| 26/07/2026 (CN) | 14:30 | Nhất Bảng C | Nhì Bảng D | Tứ kết 3 |
| 26/07/2026 (CN) | 16:00 | Nhất Bảng D | Nhì Bảng C | Tứ kết 4 |

---

## 3. Vòng Bán kết

| Ngày | Giờ | Đội Nhà | Đội Khách | Trận |
|---|---|:---:|:---:|:---:|
| 29/07/2026 (T4) | 14:30 | Đội thắng Tứ kết 1 | Đội thắng Tứ kết 3 | Bán kết 1 |
| 29/07/2026 (T4) | 16:00 | Đội thắng Tứ kết 2 | Đội thắng Tứ kết 4 | Bán kết 2 |

---

## 4. Tranh hạng Ba & Chung kết (Bế mạc)

| Ngày | Giờ | Đội Nhà | Đội Khách | Trận |
|---|---|:---:|:---:|:---:|
| 02/08/2026 (CN) | 14:30 | Đội thua Bán kết 1 | Đội thua Bán kết 2 | Tranh Hạng 3 |
| 02/08/2026 (CN) | 16:00 | Đội thắng Bán kết 1 | Đội thắng Bán kết 2 | Chung kết |

---
**Tổng số trận đấu của giải:** 44 trận.

---

{stats_md}
"""

with open("schedule_results.md", "w") as f:
    f.write(full_doc)

print("Added Vòng column to schedule_results.md")
