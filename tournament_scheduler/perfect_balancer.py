import re

# Read current schedule
with open('final_mixed_md.txt', 'r') as f:
    lines = f.readlines()

days = {}
for line in lines:
    if not line.strip() or not line.startswith('|'): continue
    cols = [c.strip() for c in line.split('|')[1:-1]]
    if len(cols) < 6: continue
    
    r, date_str, time_str, t1, t2, g = cols[:6]
    if date_str not in days:
        days[date_str] = []
    days[date_str].append((t1, t2, g))

groups_days = {g: [] for g in "ABCDE"}
for d_str, matches in days.items():
    if len(matches) == 2:
        # Assuming both matches belong to the same group since we paired them
        g = matches[0][2]
        groups_days[g].append({'date': d_str, 'matches': [(matches[0][0], matches[0][1]), (matches[1][0], matches[1][1])]})

best_assignments = {g: [] for g in "ABCDE"}

for g in "ABCDE":
    best_score = float('inf')
    best_sch = None
    g_days = groups_days[g]
    n_days = len(g_days)
    
    for i in range(1 << n_days):
        sch = []
        stats = {f"{g}{k}": {'T1': 0, 'T2': 0} for k in range(1, 5)}
        for j in range(n_days):
            m0, m1 = g_days[j]['matches']
            if (i & (1 << j)):
                t1_match, t2_match = m1, m0
            else:
                t1_match, t2_match = m0, m1
            
            sch.append((t1_match, t2_match))
            
            stats[t1_match[0]]['T1'] += 1; stats[t1_match[1]]['T1'] += 1
            stats[t2_match[0]]['T2'] += 1; stats[t2_match[1]]['T2'] += 1
            
        score = 0
        for t, s in stats.items():
            score += abs(s['T1'] - 1.5) + abs(s['T2'] - 1.5)
                
        if score < best_score:
            best_score = score
            best_sch = sch
            
    print(f"Group {g} best score: {best_score}")
    best_assignments[g] = best_sch

# Reconstruct final_mixed_md.txt
new_lines = []
for line in lines:
    if not line.strip() or not line.startswith('|'):
        new_lines.append(line)
        continue
    cols = [c.strip() for c in line.split('|')[1:-1]]
    if len(cols) < 8: continue
    
    r, date_str, time_str, t1, t2, g, r_home, r_away = cols[:8]
    # We will reconstruct day by day, so skip building here and build from days dict
    
out_lines = []
for line in lines:
    if not line.strip() or not line.startswith('|'):
        continue
    cols = [c.strip() for c in line.split('|')[1:-1]]
    if len(cols) < 8: continue
    out_lines.append(cols)

# group output lines by date
date_to_lines = {}
for i in range(0, len(out_lines), 2):
    c1 = out_lines[i]
    c2 = out_lines[i+1]
    date_str = c1[1]
    g = c1[5]
    
    # get best assignment for this day
    day_idx = next(idx for idx, d in enumerate(groups_days[g]) if d['date'] == date_str)
    best_m = best_assignments[g][day_idx]
    
    # M1
    r_home1 = c1[6] if c1[3] == best_m[0][0] else (c1[7] if c1[4] == best_m[0][0] else (c2[6] if c2[3] == best_m[0][0] else c2[7]))
    r_away1 = c1[7] if c1[4] == best_m[0][1] else (c1[6] if c1[3] == best_m[0][1] else (c2[7] if c2[4] == best_m[0][1] else c2[6]))
    
    # M2
    r_home2 = c1[6] if c1[3] == best_m[1][0] else (c1[7] if c1[4] == best_m[1][0] else (c2[6] if c2[3] == best_m[1][0] else c2[7]))
    r_away2 = c1[7] if c1[4] == best_m[1][1] else (c1[6] if c1[3] == best_m[1][1] else (c2[7] if c2[4] == best_m[1][1] else c2[6]))
    
    # construct string
    s1 = f"| {c1[0]} | {date_str} | 14:30 | {best_m[0][0]} | {best_m[0][1]} | {g} | {r_home1} | {r_away1} |\n"
    s2 = f"| {c1[0]} | {date_str} | 16:00 | {best_m[1][0]} | {best_m[1][1]} | {g} | {r_home2} | {r_away2} |\n"
    
    date_to_lines[date_str] = s1 + s2

with open('final_perfect_md.txt', 'w') as f:
    # preserve original order of dates
    seen = set()
    for cols in out_lines:
        date_str = cols[1]
        if date_str not in seen:
            f.write(date_to_lines[date_str])
            seen.add(date_str)

