import random
import time

groups = {
    'A': [('A1', 'A2', 1), ('A3', 'A4', 1), ('A5', 'A1', 2), ('A2', 'A3', 2), ('A4', 'A5', 3), ('A1', 'A3', 3), ('A5', 'A2', 4), ('A4', 'A1', 4), ('A3', 'A5', 5), ('A2', 'A4', 5)],
    'B': [('B1', 'B2', 1), ('B3', 'B4', 1), ('B4', 'B2', 2), ('B3', 'B1', 2), ('B4', 'B1', 3), ('B2', 'B3', 3)],
    'C': [('C3', 'C4', 1), ('C1', 'C2', 1), ('C3', 'C1', 2), ('C4', 'C2', 2), ('C4', 'C1', 3), ('C2', 'C3', 3)],
    'D': [('D3', 'D4', 1), ('D1', 'D2', 1), ('D3', 'D1', 2), ('D4', 'D2', 2), ('D4', 'D1', 3), ('D2', 'D3', 3)],
    'E': [('E3', 'E4', 1), ('E1', 'E2', 1), ('E3', 'E1', 2), ('E4', 'E2', 2), ('E4', 'E1', 3), ('E2', 'E3', 3)]
}

matches = []
for g, m_list in groups.items():
    for m in m_list:
        matches.append({'group': g, 't1': m[0], 't2': m[1], 'round': m[2]})

weekends = {1, 2, 7, 8, 14, 15}

def solve():
    random.shuffle(matches)
    schedule = [[None, None] for _ in range(17)]
    team_days = {f"{g}{i}": [] for g in "ABCDE" for i in range(1, 6) if not (g != 'A' and i == 5)}
    team_t1 = {k: 0 for k in team_days}
    
    def is_valid(day_idx, slot_idx, match):
        t1, t2 = match['t1'], match['t2']
        
        # 1. No team twice a day
        if slot_idx == 1:
            m0 = schedule[day_idx][0]
            if m0 is not None:
                if t1 in (m0['t1'], m0['t2']) or t2 in (m0['t1'], m0['t2']):
                    return False
        if slot_idx == 0:
            m1 = schedule[day_idx][1]
            if m1 is not None:
                if t1 in (m1['t1'], m1['t2']) or t2 in (m1['t1'], m1['t2']):
                    return False
                
        # Sort days to check gaps easily
        d1_list = sorted(team_days[t1] + [day_idx])
        d2_list = sorted(team_days[t2] + [day_idx])
        
        for lst in [d1_list, d2_list]:
            for i in range(len(lst)-1):
                diff = lst[i+1] - lst[i]
                if diff < 2: return False
                if diff > 7: return False
                
        if d1_list[0] > 7: return False
        if d2_list[0] > 7: return False
        
        is_wknd = (day_idx + 1) in weekends
        if is_wknd:
            for t in (t1, t2):
                if not t.startswith('A'):
                    w_count = sum(1 for d in lst if d+1 in weekends)
                    if w_count > 1: return False
                    
        if slot_idx == 0:
            if team_t1[t1] >= 2 or team_t1[t2] >= 2: return False
            
        return True
        
    def backtrack(match_idx):
        if match_idx == 34:
            for t, days in team_days.items():
                if 17 - (days[-1]+1) > 7: return False
                w = sum(1 for d in days if d+1 in weekends)
                if t.startswith('A') and w < 1: return False
                if not t.startswith('A') and w != 1: return False
                
                t1_cnt = team_t1[t]
                if t.startswith('A') and t1_cnt != 2: return False
                if not t.startswith('A') and (t1_cnt == 0 or t1_cnt == 3): return False
            return True
            
        m = matches[match_idx]
        preferred_days = list(range(17))
        target_day = (m['round'] - 1) * 3
        preferred_days.sort(key=lambda d: abs(d - target_day))
        
        for d in preferred_days:
            for s in [0, 1]:
                if schedule[d][s] is None:
                    if is_valid(d, s, m):
                        schedule[d][s] = m
                        team_days[m['t1']].append(d)
                        team_days[m['t1']].sort()
                        team_days[m['t2']].append(d)
                        team_days[m['t2']].sort()
                        if s == 0:
                            team_t1[m['t1']] += 1
                            team_t1[m['t2']] += 1
                            
                        if backtrack(match_idx + 1):
                            return True
                            
                        schedule[d][s] = None
                        team_days[m['t1']].remove(d)
                        team_days[m['t2']].remove(d)
                        if s == 0:
                            team_t1[m['t1']] -= 1
                            team_t1[m['t2']] -= 1
        return False

    if backtrack(0):
        return schedule
    return None

start = time.time()
sol = None
for i in range(1):
    print(f"Attempt {i}...")
    sol = solve()
    if sol: break

if sol:
    import json
    with open('mixed_schedule.json', 'w') as f:
        json.dump(sol, f)
    print("FOUND!")
else:
    print("NOT FOUND")
