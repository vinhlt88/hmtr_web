import random
from collections import defaultdict
from datetime import datetime, timedelta

teams = {
    'A': ['A1', 'A2', 'A3', 'A4', 'A5'],
    'B': ['B1', 'B2', 'B3', 'B4'],
    'C': ['C1', 'C2', 'C3', 'C4'],
    'D': ['D1', 'D2', 'D3', 'D4'],
    'E': ['E1', 'E2', 'E3', 'E4']
}

# Define rounds
rounds_matches = {
    1: [('A', 'A1', 'A2'), ('A', 'A3', 'A4'), ('B', 'B1', 'B2'), ('B', 'B3', 'B4'), ('C', 'C1', 'C2'), ('C', 'C3', 'C4'), ('D', 'D1', 'D2'), ('D', 'D3', 'D4'), ('E', 'E1', 'E2'), ('E', 'E3', 'E4')],
    2: [('A', 'A5', 'A1'), ('A', 'A2', 'A3'), ('B', 'B1', 'B3'), ('B', 'B4', 'B2'), ('C', 'C1', 'C3'), ('C', 'C4', 'C2'), ('D', 'D1', 'D3'), ('D', 'D4', 'D2'), ('E', 'E1', 'E3'), ('E', 'E4', 'E2')],
    3: [('A', 'A4', 'A5'), ('A', 'A1', 'A3'), ('B', 'B1', 'B4'), ('B', 'B2', 'B3'), ('C', 'C1', 'C4'), ('C', 'C2', 'C3'), ('D', 'D1', 'D4'), ('D', 'D2', 'D3'), ('E', 'E1', 'E4'), ('E', 'E2', 'E3')],
    4: [('A', 'A2', 'A5'), ('A', 'A4', 'A1')],
    5: [('A', 'A3', 'A5'), ('A', 'A2', 'A4')]
}

start_date = datetime(2026, 7, 4)
rest_date = datetime(2026, 7, 8)
match_days = []
current_date = start_date
while len(match_days) < 17:
    if current_date != rest_date:
        match_days.append(current_date)
    current_date += timedelta(days=1)

# We need to assign matches to match_days such that:
# 1. Rounds are sequential (all R1, then R2, then R3, then R4, then R5)
# 2. Every team plays at least one weekend match.
# 3. Every team plays at least one 16:00 match.
# 4. No team plays 2 days in a row (if possible, definitely not same day).
# 5. Balance Home/Away. (The pairs already define home/away roughly, we can swap within pair).

def is_weekend(d):
    return d.weekday() >= 5

def solve():
    for _ in range(10000):
        schedule = []
        team_weekend = defaultdict(int)
        team_16h00 = defaultdict(int)
        team_last_played = {}
        
        day_idx = 0
        valid = True
        
        for r in range(1, 6):
            matches = rounds_matches[r][:]
            random.shuffle(matches)
            
            while matches:
                if len(schedule) % 2 == 0:
                    # Need a pair of matches for the day
                    m1 = matches.pop(0)
                    m2 = None
                    for i, m in enumerate(matches):
                        # Ensure teams don't play on the same day (not possible anyway since different groups mostly, but check within group A)
                        if m[1] not in (m1[1], m1[2]) and m[2] not in (m1[1], m1[2]):
                            m2 = matches.pop(i)
                            break
                    if not m2 and matches:
                        valid = False; break
                    
                    if m2 is None:
                        # Only 1 match left? Not possible if we grouped correctly, wait, round 4 and 5 have 2 matches, so 1 pair.
                        day_matches = [m1]
                    else:
                        day_matches = [m1, m2]
                    
                    random.shuffle(day_matches) # random 14:30 and 16:00
                    
                    date = match_days[day_idx]
                    for slot, match in enumerate(day_matches):
                        time_str = '14:30' if slot == 0 else '16:00'
                        grp, t1, t2 = match
                        
                        # Swap home/away randomly
                        if random.choice([True, False]):
                            t1, t2 = t2, t1
                            
                        schedule.append({
                            'round': r,
                            'date': date,
                            'time': time_str,
                            'home': t1,
                            'away': t2,
                            'group': grp
                        })
                        if is_weekend(date):
                            team_weekend[t1] += 1
                            team_weekend[t2] += 1
                        if time_str == '16:00':
                            team_16h00[t1] += 1
                            team_16h00[t2] += 1
                        
                        # Check rest
                        if t1 in team_last_played and (date - team_last_played[t1]).days < 1:
                            valid = False
                        if t2 in team_last_played and (date - team_last_played[t2]).days < 1:
                            valid = False
                            
                        team_last_played[t1] = date
                        team_last_played[t2] = date
                        
                    day_idx += 1
                if not valid: break
            if not valid: break
            
        if not valid: continue
        
        # Check constraints
        all_weekend = all(v >= 1 for v in team_weekend.values()) and len(team_weekend) == 21
        all_16h = all(v >= 1 for v in team_16h00.values()) and len(team_16h00) == 21
        if all_weekend and all_16h:
            return schedule
    return None

sched = solve()
if sched:
    with open('schedule_results.md', 'w') as f:
        f.write("# Lịch Thi Đấu Giải Bóng Đá Truyền Thống Palei Hamu Tanran 2026\n\n")
        f.write("**Tổng quan giải đấu**\n")
        f.write("- **Ngày bắt đầu:** 2026-07-04\n")
        f.write("- **Ngày nghỉ vòng bảng:** 2026-07-08\n")
        f.write("- **Quy định cuối tuần:** Mỗi đội phải đá ít nhất 1 trận vào Thứ 7 hoặc Chủ Nhật.\n")
        f.write("- **Khung giờ:** 14:30 (Trận 1) và 16:00 (Trận 2) mỗi ngày.\n")
        f.write("- **Các bảng đấu:**\n")
        f.write("  - **Bảng A** – 5 đội (A1 … A5)\n")
        f.write("  - **Bảng B** – 4 đội (B1 … B4)\n")
        f.write("  - **Bảng C** – 4 đội (C1 … C4)\n")
        f.write("  - **Bảng D** – 4 đội (D1 … D4)\n")
        f.write("  - **Bảng E** – 4 đội (E1 … E4)\n")
        f.write("- **Thể thức xét Nhì bảng:** So sánh 5 đội Nhì bảng (không tính kết quả với đội bét bảng A). Chọn 1 đội xuất sắc nhất vào thẳng Tứ kết. 4 đội còn lại đá Play-off tranh 2 vé.\n\n")
        
        f.write("## 1. Giai đoạn 1: Vòng bảng\n\n")
        f.write("| Vòng | Ngày | Giờ | Đội Nhà | Đội Khách | Bảng |\n")
        f.write("|---|---|---|---|---|---|\n")
        for m in sched:
            f.write(f"| {m['round']} | {m['date'].strftime('%Y-%m-%d')} | {m['time']} | {m['home']} | {m['away']} | {m['group']} |\n")
        
        f.write("\n## 2. Giai đoạn 2: Đá Play-off\n\n")
        f.write("*(Diễn ra sau vòng bảng, dành cho 4 đội nhì bảng xếp thứ 2 đến thứ 5)*\n\n")
        f.write("| Trận | Giờ | Đội Nhà | Đội Khách | Vòng |\n")
        f.write("|---|---|---|---|---|\n")
        f.write("| Play-off 1 | 14:30 | Đội nhì tốt thứ 2 | Đội nhì tốt thứ 5 | Play-off |\n")
        f.write("| Play-off 2 | 16:00 | Đội nhì tốt thứ 3 | Đội nhì tốt thứ 4 | Play-off |\n\n")
        
        f.write("## 3. Các vòng đấu loại trực tiếp (Tứ kết, Bán kết, Chung kết)\n\n")
        f.write("- **Tứ kết:** 5 đội Nhất bảng + 1 đội Nhì xuất sắc nhất + 2 đội thắng Play-off (Tổng 8 đội, 4 trận).\n")
        f.write("- **Bán kết:** 4 đội thắng Tứ kết (2 trận).\n")
        f.write("- **Tranh hạng Ba & Chung kết:** (2 trận).\n")
        
    print("SUCCESS")
else:
    print("FAILED")
