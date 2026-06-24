import random

groups = {
    'A': [('A1','A5'), ('A2','A4'), ('A5','A4'), ('A1','A3'), ('A4','A3'), ('A5','A2'), ('A3','A2'), ('A4','A1'), ('A2','A1'), ('A3','A5')],
    'B': [('B1','B5'), ('B2','B4'), ('B5','B4'), ('B1','B3'), ('B4','B3'), ('B5','B2'), ('B3','B2'), ('B4','B1'), ('B2','B1'), ('B3','B5')],
    'C': [('C1','C5'), ('C2','C4'), ('C5','C4'), ('C1','C3'), ('C4','C3'), ('C5','C2'), ('C3','C2'), ('C4','C1'), ('C2','C1'), ('C3','C5')],
    'D': [('D1','D4'), ('D2','D3'), ('D4','D3'), ('D1','D2'), ('D2','D4'), ('D3','D1')]
}

all_matches = []
for g, m_list in groups.items():
    for m in m_list:
        all_matches.append((g, m[0], m[1]))

num_days = 18
matches_per_day = 2
weekend_days = {0, 1, 6, 7, 13, 14} # 0-indexed days (1, 2, 7, 8, 14, 15)

def solve():
    for attempt in range(5000):
        random.shuffle(all_matches)
        
        schedule = [[] for _ in range(num_days)]
        team_last_day = {}
        team_weekends = {f"{g}{i}": 0 for g in "ABC" for i in range(1,6)}
        team_weekends.update({f"D{i}": 0 for i in range(1,5)})
        
        success = True
        
        for m in all_matches:
            g, t1, t2 = m
            valid_days = []
            
            for d in range(num_days):
                if len(schedule[d]) >= matches_per_day: continue
                # conflict check
                conflict = False
                for existing_m in schedule[d]:
                    if t1 in existing_m or t2 in existing_m:
                        conflict = True
                        break
                if conflict: continue
                
                # check consecutive days (rest >= 1)
                r1 = d - team_last_day.get(t1, -99)
                r2 = d - team_last_day.get(t2, -99)
                if r1 < 2 or r2 < 2:  # Try strictly rest >= 1 clear day between
                    pass # We will try rest >= 2 first, then fallback to >= 1
                    
                valid_days.append(d)
                
            if not valid_days:
                success = False
                break
                
            # Heuristic: Prefer weekend days for teams with 0 weekends
            best_day = -1
            
            # Sort valid days: 
            # 1. Prioritize rest >= 2
            # 2. Prioritize weekends if t1 or t2 need weekend
            
            needs_weekend = team_weekends[t1] == 0 or team_weekends[t2] == 0
            
            valid_days.sort(key=lambda d: (
                (d - team_last_day.get(t1, -99) < 2 or d - team_last_day.get(t2, -99) < 2), # False is better (rest >= 2)
                -(d in weekend_days) if needs_weekend else 0
            ))
            
            best_day = valid_days[0]
            
            if best_day - team_last_day.get(t1, -99) < 2 or best_day - team_last_day.get(t2, -99) < 2:
                # If we must play with 1 day rest, ensure it's at least 1 day!
                if best_day - team_last_day.get(t1, -99) < 1 or best_day - team_last_day.get(t2, -99) < 1:
                    success = False # Cannot play on same day
                    break

            schedule[best_day].append(m)
            team_last_day[t1] = best_day
            team_last_day[t2] = best_day
            if best_day in weekend_days:
                team_weekends[t1] += 1
                team_weekends[t2] += 1
                
        if success:
            # Check if everyone got a weekend
            all_weekend = all(v > 0 for v in team_weekends.values())
            if all_weekend:
                return schedule
    return None

sched = solve()
if sched:
    print("Found schedule!")
    # Now assign 14:30 and 16:00
    # Every team must get at least one 16:00
    # For each day, one match is 14:30, one is 16:00
    # We can randomly swap them and check
    import copy
    for attempt in range(1000):
        time_sched = []
        team_1600 = {f"{g}{i}": 0 for g in "ABC" for i in range(1,6)}
        team_1600.update({f"D{i}": 0 for i in range(1,5)})
        
        for d in range(num_days):
            m1, m2 = sched[d]
            if random.choice([True, False]):
                time_sched.append((m1, m2))
                team_1600[m2[1]] += 1
                team_1600[m2[2]] += 1
            else:
                time_sched.append((m2, m1))
                team_1600[m1[1]] += 1
                team_1600[m1[2]] += 1
                
        if all(v > 0 for v in team_1600.values()):
            print("Found time assignment!")
            
            # Print to md format
            days_dates = [
                '04/07/2026 (T7)', '05/07/2026 (CN)', '06/07/2026 (T2)', '07/07/2026 (T3)', 
                '09/07/2026 (T5)', '10/07/2026 (T6)', '11/07/2026 (T7)', '12/07/2026 (CN)', 
                '13/07/2026 (T2)', '14/07/2026 (T3)', '15/07/2026 (T4)', '16/07/2026 (T5)', 
                '17/07/2026 (T6)', '18/07/2026 (T7)', '19/07/2026 (CN)', '20/07/2026 (T2)', 
                '21/07/2026 (T3)', '22/07/2026 (T4)'
            ]
            
            md = ""
            for i, (m1, m2) in enumerate(time_sched):
                md += f"| {i+1} | {days_dates[i]} | 14:30 | {m1[1]} | {m1[2]} | {m1[0]} | - | - |\n"
                md += f"| {i+1} | {days_dates[i]} | 16:00 | {m2[1]} | {m2[2]} | {m2[0]} | - | - |\n"
                
            with open("new_men_schedule.txt", "w") as f:
                f.write(md)
            break
else:
    print("Failed")
