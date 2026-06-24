import random

groups = {
    'A': [('A1','A6'), ('A2','A5'), ('A3','A4'), 
          ('A6','A4'), ('A5','A3'), ('A1','A2'),
          ('A2','A6'), ('A3','A1'), ('A4','A5'),
          ('A6','A5'), ('A1','A4'), ('A2','A3'),
          ('A3','A6'), ('A4','A2'), ('A5','A1')],
    'B': [('B1','B5'), ('B2','B4'), ('B5','B4'), ('B1','B3'), ('B4','B3'), ('B5','B2'), ('B3','B2'), ('B4','B1'), ('B2','B1'), ('B3','B5')]
}

all_matches = []
for g, m_list in groups.items():
    for m in m_list:
        all_matches.append((g, m[0], m[1]))

num_days = 13
matches_per_day = [2]*12 + [1]

def solve():
    for attempt in range(2000):
        random.shuffle(all_matches)
        
        schedule = [[] for _ in range(num_days)]
        
        success = True
        team_last_day = {}
        
        for m in all_matches:
            g, t1, t2 = m
            best_day = -1
            
            # try to find a day with rest >= 2
            for d in range(num_days):
                if len(schedule[d]) >= matches_per_day[d]: continue
                conflict = False
                for existing_m in schedule[d]:
                    if t1 in existing_m or t2 in existing_m:
                        conflict = True
                        break
                if conflict: continue
                r1 = d - team_last_day.get(t1, -99)
                r2 = d - team_last_day.get(t2, -99)
                if r1 < 2 or r2 < 2:
                    continue
                best_day = d
                break
                
            # relax to rest >= 1
            if best_day == -1:
                for d in range(num_days):
                    if len(schedule[d]) >= matches_per_day[d]: continue
                    conflict = False
                    for existing_m in schedule[d]:
                        if t1 in existing_m or t2 in existing_m:
                            conflict = True
                            break
                    if conflict: continue
                    r1 = d - team_last_day.get(t1, -99)
                    r2 = d - team_last_day.get(t2, -99)
                    if r1 < 1 or r2 < 1:
                        continue
                    best_day = d
                    break
                    
            if best_day == -1:
                success = False
                break
                
            schedule[best_day].append(m)
            team_last_day[t1] = best_day
            team_last_day[t2] = best_day
            
        if success:
            return schedule
    return None

sched = solve()
if sched:
    print("Found schedule for Women!")
    for i, day in enumerate(sched):
        print(f"Day {i+1}: {day}")
else:
    print("Failed to find schedule for Women")
