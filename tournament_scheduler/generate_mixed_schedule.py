import random
import sys

groups = {
    'A': [('A1', 'A2'), ('A3', 'A4'), ('A4', 'A2'), ('A3', 'A1'), ('A4', 'A1'), ('A2', 'A3')],
    'B': [('B1', 'B2'), ('B3', 'B4'), ('B4', 'B2'), ('B3', 'B1'), ('B4', 'B1'), ('B2', 'B3')],
    'C': [('C1', 'C2'), ('C3', 'C4'), ('C4', 'C2'), ('C3', 'C1'), ('C4', 'C1'), ('C2', 'C3')],
    'D': [('D1', 'D2'), ('D3', 'D4'), ('D4', 'D2'), ('D3', 'D1'), ('D4', 'D1'), ('D2', 'D3')],
    'E': [('E1', 'E2'), ('E3', 'E4'), ('E4', 'E2'), ('E3', 'E1'), ('E4', 'E1'), ('E2', 'E3')]
}

r1_matches = []
r2_matches = []
r3_matches = []
for g in "ABCDE":
    r1_matches.extend([(g, groups[g][0]), (g, groups[g][1])])
    r2_matches.extend([(g, groups[g][2]), (g, groups[g][3])])
    r3_matches.extend([(g, groups[g][4]), (g, groups[g][5])])

weekend_days = [1, 2, 7, 8, 13, 14]

def evaluate(schedule):
    t_1600 = {f"{g}{i}": 0 for g in "ABCDE" for i in range(1, 5)}
    t_weekend = {f"{g}{i}": 0 for g in "ABCDE" for i in range(1, 5)}
    t_days = {f"{g}{i}": [] for g in "ABCDE" for i in range(1, 5)}
    
    for day in range(15):
        m1, m2 = schedule[day]
        d_idx = day + 1
        
        for t in m1[1]:
            t_days[t].append(d_idx)
            if d_idx in weekend_days: t_weekend[t] += 1
            
        for t in m2[1]:
            t_days[t].append(d_idx)
            t_1600[t] += 1
            if d_idx in weekend_days: t_weekend[t] += 1
            
    penalty = 0
    # hard constraints
    for t, c in t_1600.items():
        if c < 1: penalty += 1000 * (1 - c)
        if c > 2: penalty += 1000 * (c - 2)
        
    for t, c in t_weekend.items():
        if c < 1: penalty += 5000
        
    min_rest = 999
    max_rest = 0
    for t, days in t_days.items():
        d1, d2, d3 = days
        gap1 = (d2 - d1) + 1
        gap2 = (d3 - d2) + 1
        rest1 = gap1 - 1
        rest2 = gap2 - 1
        
        if rest1 < 2: penalty += (2 - rest1) * 200
        if rest2 < 2: penalty += (2 - rest2) * 200
        
        min_rest = min(min_rest, rest1, rest2)
        max_rest = max(max_rest, rest1, rest2)
        
    penalty += max_rest * 10 - min_rest * 10
    return penalty, min_rest, max_rest, t_1600, t_weekend

best_schedule = None
best_penalty = 9999999
best_stats = None

for _ in range(200000):
    random.shuffle(r1_matches)
    random.shuffle(r2_matches)
    random.shuffle(r3_matches)
    
    schedule = []
    for i in range(5):
        m1, m2 = r1_matches[2*i], r1_matches[2*i+1]
        if random.random() < 0.5: m1, m2 = m2, m1
        schedule.append((m1, m2))
    for i in range(5):
        m1, m2 = r2_matches[2*i], r2_matches[2*i+1]
        if random.random() < 0.5: m1, m2 = m2, m1
        schedule.append((m1, m2))
    for i in range(5):
        m1, m2 = r3_matches[2*i], r3_matches[2*i+1]
        if random.random() < 0.5: m1, m2 = m2, m1
        schedule.append((m1, m2))
        
    pen, m_rest, x_rest, t16, twk = evaluate(schedule)
    if pen < best_penalty:
        best_penalty = pen
        best_schedule = schedule
        best_stats = (m_rest, x_rest, t16, twk)
        if pen < 50:  # meaning 0 hard constraint violations, and max_rest - min_rest is small
            pass

print(f"Best penalty: {best_penalty}, Min rest: {best_stats[0]}, Max rest: {best_stats[1]}")

# Generate MD
days_dates = {
    1: '04/07/2026 (T7)', 2: '05/07/2026 (CN)', 3: '06/07/2026 (T2)', 4: '07/07/2026 (T3)', 5: '08/07/2026 (T4)',
    6: '10/07/2026 (T6)', 7: '11/07/2026 (T7)', 8: '12/07/2026 (CN)', 9: '13/07/2026 (T2)', 10: '14/07/2026 (T3)',
    11: '16/07/2026 (T5)', 12: '17/07/2026 (T6)', 13: '18/07/2026 (T7)', 14: '19/07/2026 (CN)', 15: '20/07/2026 (T2)'
}

md = ""
for day in range(1, 16):
    m1, m2 = best_schedule[day-1]
    
    if day <= 5: r = 1
    elif day <= 10: r = 2
    else: r = 3
    
    md += f"| {r} | {days_dates[day]} | 14:30 | {m1[1][0]} | {m1[1][1]} | {m1[0]} |\n"
    md += f"| {r} | {days_dates[day]} | 16:00 | {m2[1][0]} | {m2[1][1]} | {m2[0]} |\n"

with open("final_perfect_md.txt", "w") as f:
    f.write(md)

