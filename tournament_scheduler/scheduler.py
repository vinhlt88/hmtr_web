import random
import datetime

# Define groups and teams
GROUPS = {
    'A': ['A1', 'A2', 'A3', 'A4', 'A5'],
    'B': ['B1', 'B2', 'B3', 'B4'],
    'C': ['C1', 'C2', 'C3', 'C4'],
    'D': ['D1', 'D2', 'D3', 'D4'],
    'E': ['E1', 'E2', 'E3', 'E4']
}

# Mathematically balanced round-robin match generator
def generate_matches():
    matches = []
    
    # Group A (5 teams - 5 rounds, 1 team rests per round)
    # Every team is home exactly twice and away exactly twice.
    # R1: A1-A2, A3-A4
    # R2: A2-A3, A4-A5
    # R3: A3-A5, A4-A1 (A4 is home)
    # R4: A1-A3, A5-A2 (A5 is home)
    # R5: A5-A1, A2-A4 (A2 is home)
    group_a_matches = [
        ('A1', 'A2', '1'),
        ('A1', 'A3', '4'),
        ('A2', 'A3', '2'),
        ('A2', 'A4', '5'),
        ('A3', 'A4', '1'),
        ('A3', 'A5', '3'),
        ('A4', 'A5', '2'),
        ('A4', 'A1', '3'),
        ('A5', 'A1', '5'),
        ('A5', 'A2', '4')
    ]
    for t1, t2, rnd in group_a_matches:
        matches.append(('A', t1, t2, rnd))
        
    # Groups B, C, D, E (4 teams - 3 rounds)
    # Balanced Home/Away: 2 teams have 2H/1A, 2 teams have 1H/2A.
    # R1: 1-2, 3-4 (3 is home)
    # R2: 1-3, 4-2 (4 is home)
    # R3: 4-1 (4 is home), 2-3 (2 is home)
    for g_label in ['B', 'C', 'D', 'E']:
        teams = GROUPS[g_label]
        group_matches = [
            (teams[0], teams[1], '1'),
            (teams[0], teams[2], '2'),
            (teams[1], teams[2], '3'),
            (teams[3], 'B1' if g_label=='B' else ('C1' if g_label=='C' else ('D1' if g_label=='D' else 'E1')), '3'),
            (teams[3], 'B2' if g_label=='B' else ('C2' if g_label=='C' else ('D2' if g_label=='D' else 'E2')), '2'),
            (teams[2], teams[3], '1')
        ]
        for t1, t2, rnd in group_matches:
            matches.append((g_label, t1, t2, rnd))
            
    return matches

# Match days (0-indexed, where 0 is July 4, 2026)
MATCH_DAYS = [0, 1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]

# Map 0-indexed day to actual date string and day of week
START_DATE = datetime.date(2026, 7, 4)
def get_date_info(day_idx):
    current_date = START_DATE + datetime.timedelta(days=day_idx)
    day_name = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"][current_date.weekday()]
    return current_date.strftime("%d/%m/%Y"), day_name, current_date.weekday() in (5, 6) # 5=Sat, 6=Sun

# Weekend days (relative to START_DATE)
WEEKEND_DAYS = set()
for d in range(18):
    _, _, is_we = get_date_info(d)
    if is_we:
        WEEKEND_DAYS.add(d)

SLOTS = []
for day in MATCH_DAYS:
    SLOTS.append((day, 0)) # 14:30 slot
    SLOTS.append((day, 1)) # 16:00 slot

def evaluate_schedule(schedule):
    hard_conflicts = 0
    soft_conflicts = 0
    
    # Track team schedules
    team_history = {}
    team_home_count = {}
    team_away_count = {}
    team_slot1_count = {}
    team_slot2_count = {}
    team_weekend_count = {}
    
    for group, teams in GROUPS.items():
        for team in teams:
            team_history[team] = []
            team_home_count[team] = 0
            team_away_count[team] = 0
            team_slot1_count[team] = 0
            team_slot2_count[team] = 0
            team_weekend_count[team] = 0
            
    for idx, match in enumerate(schedule):
        day, slot = SLOTS[idx]
        group, t1, t2, rnd = match
        
        team_history[t1].append((day, slot))
        team_history[t2].append((day, slot))
        
        team_home_count[t1] += 1
        team_away_count[t2] += 1
        
        if slot == 0:
            team_slot1_count[t1] += 1
            team_slot1_count[t2] += 1
        else:
            team_slot2_count[t1] += 1
            team_slot2_count[t2] += 1
            
        if day in WEEKEND_DAYS:
            team_weekend_count[t1] += 1
            team_weekend_count[t2] += 1

    # Hard Constraints
    for team, history in team_history.items():
        history.sort()
        for i in range(len(history) - 1):
            d1, s1 = history[i]
            d2, s2 = history[i+1]
            if d2 == d1:
                hard_conflicts += 1 # Play twice in same day
            elif d2 - d1 < 2:
                hard_conflicts += 1 # Spacing >= 1 day of rest

        if team_weekend_count[team] < 1:
            hard_conflicts += 1
        if team_slot2_count[team] < 1:
            hard_conflicts += 1

    # Soft / Balance Constraints
    for team in team_history.keys():
        # 1. Home/Away Balance (Home and Away count should be as close as possible)
        home = team_home_count[team]
        away = team_away_count[team]
        if team in GROUPS['A']: # 4 matches total
            soft_conflicts += (home - 2)**2
        else: # 3 matches total
            soft_conflicts += (abs(home - away) - 1)**2

        # 2. Slot 1 vs Slot 2 Balance (Slot 1 and Slot 2 should be balanced)
        s1 = team_slot1_count[team]
        s2 = team_slot2_count[team]
        if team in GROUPS['A']:
            soft_conflicts += (s1 - 2)**2
        else:
            soft_conflicts += (abs(s1 - s2) - 1)**2

        # 3. Weekend Match Balance (everyone should be in range [1, 2])
        we = team_weekend_count[team]
        if we > 2:
            soft_conflicts += (we - 2)**2

        # 4. Slot 2 Match Balance (everyone should be in range [1, 2])
        sl2 = team_slot2_count[team]
        if sl2 > 2:
            soft_conflicts += (sl2 - 2)**2

    return hard_conflicts, soft_conflicts

def solve():
    matches = generate_matches()
    current_schedule = list(matches)
    random.shuffle(current_schedule)
    
    best_schedule = None
    best_hard = float('inf')
    best_soft = float('inf')
    
    for restart in range(15):
        random.shuffle(current_schedule)
        hard, soft = evaluate_schedule(current_schedule)
        
        # Local search (Hill Climbing)
        for iteration in range(25000):
            if hard == 0 and soft == 0:
                print(f"Perfect solution found on restart {restart}!")
                return current_schedule
                
            if hard == 0:
                if best_schedule is None or soft < best_soft:
                    best_schedule = list(current_schedule)
                    best_hard = hard
                    best_soft = soft
            
            # Propose a swap
            i, j = random.sample(range(len(current_schedule)), 2)
            current_schedule[i], current_schedule[j] = current_schedule[j], current_schedule[i]
            
            new_hard, new_soft = evaluate_schedule(current_schedule)
            
            # Acceptance criteria
            if new_hard < hard or (new_hard == hard and new_soft <= soft):
                hard = new_hard
                soft = new_soft
            else:
                # Revert
                current_schedule[i], current_schedule[j] = current_schedule[j], current_schedule[i]
                
    if best_schedule is not None:
        print(f"Solved successfully! Hard conflicts: {best_hard}, Soft conflicts (balance deviation): {best_soft}")
        return best_schedule
    else:
        print("Failed to find a valid schedule with 0 hard conflicts.")
        return None

def format_schedule(schedule):
    lines = []
    lines.append("# Lịch Thi Đấu Bóng Đá Nam Vòng Bảng (Sân 11)")
    lines.append("")
    lines.append("| Mã trận | Ngày | Giờ bắt đầu | Đội sân nhà | Đội sân khách | Bảng | Vòng | Trùng áo? | Số ngày đội nhà nghỉ | Số ngày đội khách nghỉ | Ngày cuối tuần? |")
    lines.append("|---|---|---|---|---|---|---|---|---|---|---|")
    
    day_matches = {}
    for idx, match in enumerate(schedule):
        day, slot = SLOTS[idx]
        if day not in day_matches:
            day_matches[day] = [None, None]
        day_matches[day][slot] = match

    team_last_day = {}
    match_code = 1
    
    for day in sorted(list(set(MATCH_DAYS) | {4})):
        date_str, day_name, is_we = get_date_info(day)
        date_display = f"{day_name}, {date_str}"
        we_display = "YES" if is_we else "NO"
        
        if day == 4:
            lines.append(f"| | {date_display} | | | | | | | - | - | {we_display} |")
            lines.append(f"| | {date_display} | | | | | | | - | - | {we_display} |")
            continue
            
        for slot in [0, 1]:
            m = day_matches[day][slot]
            g, t1, t2, rnd = m
            
            # Calculate rest days
            rest_t1 = "-"
            if t1 in team_last_day:
                rest_t1 = str(day - team_last_day[t1] - 1)
                
            rest_t2 = "-"
            if t2 in team_last_day:
                rest_t2 = str(day - team_last_day[t2] - 1)
                
            time_str = "14:30" if slot == 0 else "16:00"
            
            lines.append(f"| {match_code} | {date_display} | {time_str} | {t1} | {t2} | {g} | {rnd} | NO | {rest_t1} | {rest_t2} | {we_display} |")
            
            # Update history
            team_last_day[t1] = day
            team_last_day[t2] = day
            match_code += 1

    # Play-offs
    last_group_day = 17
    po_rest_1 = last_group_day + 1
    po_rest_2 = last_group_day + 2
    po_day = last_group_day + 3
    
    d1_str, dn1, is_we1 = get_date_info(po_rest_1)
    d2_str, dn2, is_we2 = get_date_info(po_rest_2)
    dp_str, dnp, is_wep = get_date_info(po_day)
    
    we_p = "YES" if is_wep else "NO"
    
    lines.append(f"| | {dn1}, {d1_str} | | | | | | | - | - | {'YES' if is_we1 else 'NO'} |")
    lines.append(f"| | {dn2}, {d2_str} | | | | | | | - | - | {'YES' if is_we2 else 'NO'} |")
    lines.append(f"| TK1 | {dnp}, {dp_str} | 14:30 | Nhất A | Nhì B | | Play-off | | - | - | {we_p} |")
    lines.append(f"| TK2 | {dnp}, {dp_str} | 16:00 | Nhất B | Nhì A | | Play-off | | - | - | {we_p} |")
    
    return "\n".join(lines)

def format_overview(schedule):
    lines = []
    lines.append("# BĐ Nam - Overview")
    lines.append("")
    lines.append("| Tên Đội | Bảng | Số trận vòng bảng | Số trận sân nhà | Số trận sân khách | Số trận 1 (14h30) | Số trận 2 (16h00) | Trận cuối tuần |")
    lines.append("|---|---|---|---|---|---|---|---|")
    
    # Calculate stats for all teams
    team_stats = {}
    for group, teams in GROUPS.items():
        for team in teams:
            team_stats[team] = {
                'name': team,
                'group': group,
                'total': 0,
                'home': 0,
                'away': 0,
                'slot1': 0,
                'slot2': 0,
                'weekend': 0
            }
            
    for idx, match in enumerate(schedule):
        day, slot = SLOTS[idx]
        group, t1, t2, rnd = match
        
        # Home/Away
        team_stats[t1]['home'] += 1
        team_stats[t2]['away'] += 1
        
        # Slots
        if slot == 0:
            team_stats[t1]['slot1'] += 1
            team_stats[t2]['slot1'] += 1
        else:
            team_stats[t1]['slot2'] += 1
            team_stats[t2]['slot2'] += 1
            
        # Weekend
        if day in WEEKEND_DAYS:
            team_stats[t1]['weekend'] += 1
            team_stats[t2]['weekend'] += 1
            
        team_stats[t1]['total'] += 1
        team_stats[t2]['total'] += 1

    # Output group by group with empty lines between groups
    for group in ['A', 'B', 'C', 'D', 'E']:
        for team in GROUPS[group]:
            s = team_stats[team]
            lines.append(f"| {s['name']} | {s['group']} | {s['total']} | {s['home']} | {s['away']} | {s['slot1']} | {s['slot2']} | {s['weekend']} |")
        lines.append("| | | | | | | | |")

    # Add settings at the bottom
    lines.append("")
    lines.append("## Cấu hình thời gian thi đấu")
    lines.append("")
    lines.append("- **Giờ bắt đầu trận 1:** 14:30")
    lines.append("- **Giờ bắt đầu trận 2:** 16:00")
    lines.append("")
    lines.append("### Khung thời gian chi tiết vòng bảng:")
    lines.append("- **Trận 1:**")
    lines.append("  - Đá 2 hiệp: 80 phút (14:30 - 15:50)")
    lines.append("  - Nghỉ giữa 2 hiệp: 10 phút")
    lines.append("  - Bù giờ cả 2 hiệp: 10 phút")
    lines.append("- **Nghỉ giữa 2 trận:** 10 phút")
    lines.append("- **Trận 2:** 100 phút (16:00 - 17:40)")
    
    return "\n".join(lines)

def print_team_verifications(schedule):
    team_history = {}
    for group, teams in GROUPS.items():
        for team in teams:
            team_history[team] = []
            
    for idx, match in enumerate(schedule):
        day, slot = SLOTS[idx]
        group, t1, t2, rnd = match
        team_history[t1].append((day, slot))
        team_history[t2].append((day, slot))
        
    print("\n=== VERIFICATION REPORT ===")
    print(f"{'Team':<6} | {'Matches':<8} | {'Weekend Matches':<15} | {'16:00 Matches':<12}")
    print("-" * 55)
    for team, history in sorted(team_history.items()):
        weekend_count = sum(1 for d, s in history if d in WEEKEND_DAYS)
        slot2_count = sum(1 for d, s in history if s == 1)
        print(f"{team:<6} | {len(history):<8} | {weekend_count:<15} | {slot2_count:<12}")

if __name__ == "__main__":
    schedule = solve()
    if schedule:
        markdown_content = format_schedule(schedule)
        with open("schedule_results.md", "w", encoding="utf-8") as f:
            f.write(markdown_content)
        print("Generated schedule_results.md successfully!")
        
        overview_content = format_overview(schedule)
        with open("scheduler_overview.md", "w", encoding="utf-8") as f:
            f.write(overview_content)
        print("Generated scheduler_overview.md successfully!")
        
        print_team_verifications(schedule)
