import random
from collections import defaultdict

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

def solve():
    for attempt in range(1000):
        random.shuffle(all_matches)
        
        schedule = [[] for _ in range(num_days)]
        match_idx = 0
        
        # assign matches to days
        success = True
        team_last_day = {}
        
        for m in all_matches:
            g, t1, t2 = m
            # Find earliest day where t1 and t2 can play (rest >= 2 days if possible, min 1 day)
            best_day = -1
            for d in range(num_days):
                if len(schedule[d]) >= matches_per_day: continue
                # check conflicts
                conflict = False
                for existing_m in schedule[d]:
                    if t1 in existing_m or t2 in existing_m:
                        conflict = True
                        break
                if conflict: continue
                
                # check rest
                r1 = d - team_last_day.get(t1, -99)
                r2 = d - team_last_day.get(t2, -99)
                if r1 < 2 or r2 < 2:  # strict rest: at least 1 day between matches (difference >= 2)
                    continue
                    
                best_day = d
                break
                
            if best_day == -1:
                # relax rest to 1 day if needed
                for d in range(num_days):
                    if len(schedule[d]) >= matches_per_day: continue
                    conflict = False
                    for existing_m in schedule[d]:
                        if t1 in existing_m or t2 in existing_m:
                            conflict = True
                            break
                    if conflict: continue
                    r1 = d - team_last_day.get(t1, -99)
                    r2 = d - team_last_day.get(t2, -99)
                    if r1 < 1 or r2 < 1:  # Cannot play on same day!
                        continue
                    best_day = d
                    break
                    
            if best_day == -1:
                success = False
                break
                
            schedule[best_day].append(m)
            team_last_day[t1] = best_day
            team_last_day[t2] = best_day
            
        if success and all(len(day) == matches_per_day for day in schedule):
            return schedule
    return None

sched = solve()
if sched:
    print("Found schedule for Men!")
    for i, day in enumerate(sched):
        print(f"Day {i+1}: {day}")
else:
    print("Failed to find schedule for Men")
