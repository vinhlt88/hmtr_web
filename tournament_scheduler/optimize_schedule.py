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

all_matches = r1_matches + r2_matches + r3_matches
assignment = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0]

r1_1430 = [all_matches[i] for i in range(10) if assignment[i] == 0]
r1_1600 = [all_matches[i] for i in range(10) if assignment[i] == 1]

r2_1430 = [all_matches[i] for i in range(10, 20) if assignment[i] == 0]
r2_1600 = [all_matches[i] for i in range(10, 20) if assignment[i] == 1]

r3_1430 = [all_matches[i] for i in range(20, 30) if assignment[i] == 0]
r3_1600 = [all_matches[i] for i in range(20, 30) if assignment[i] == 1]

weekend_days = [1, 2, 7, 8, 13, 14]

def evaluate(r1_14, r1_16, r2_14, r2_16, r3_14, r3_16):
    t_weekend = {f"{g}{i}": 0 for g in "ABCDE" for i in range(1, 5)}
    t_days = {f"{g}{i}": [] for g in "ABCDE" for i in range(1, 5)}
    
    # R1
    for i in range(5):
        day = i + 1
        for t in r1_14[i][1]:
            t_days[t].append(day)
            if day in weekend_days: t_weekend[t] += 1
        for t in r1_16[i][1]:
            t_days[t].append(day)
            if day in weekend_days: t_weekend[t] += 1
            
    # R2
    for i in range(5):
        day = i + 6
        for t in r2_14[i][1]:
            t_days[t].append(day)
            if day in weekend_days: t_weekend[t] += 1
        for t in r2_16[i][1]:
            t_days[t].append(day)
            if day in weekend_days: t_weekend[t] += 1
            
    # R3
    for i in range(5):
        day = i + 11
        for t in r3_14[i][1]:
            t_days[t].append(day)
            if day in weekend_days: t_weekend[t] += 1
        for t in r3_16[i][1]:
            t_days[t].append(day)
            if day in weekend_days: t_weekend[t] += 1
            
    penalty = 0
    # hard constraint
    for t, c in t_weekend.items():
        if c < 1: penalty += 10000
        
    min_rest = 999
    max_rest = 0
    for t, days in t_days.items():
        d1, d2, d3 = days
        gap1 = (d2 - d1) + 1
        gap2 = (d3 - d2) + 1
        rest1 = gap1 - 1
        rest2 = gap2 - 1
        
        # we want rest to be between 2 and 6
        if rest1 < 2: penalty += (2 - rest1) * 200
        if rest2 < 2: penalty += (2 - rest2) * 200
        if rest1 > 6: penalty += (rest1 - 6) * 100
        if rest2 > 6: penalty += (rest2 - 6) * 100
        
        min_rest = min(min_rest, rest1, rest2)
        max_rest = max(max_rest, rest1, rest2)
        
    penalty += max_rest * 10 - min_rest * 10
    return penalty, min_rest, max_rest

best_penalty = 999999
best_sched = None

for _ in range(200000):
    random.shuffle(r1_1430)
    random.shuffle(r1_1600)
    random.shuffle(r2_1430)
    random.shuffle(r2_1600)
    random.shuffle(r3_1430)
    random.shuffle(r3_1600)
    
    pen, min_r, max_r = evaluate(r1_1430, r1_1600, r2_1430, r2_1600, r3_1430, r3_1600)
    if pen < best_penalty:
        best_penalty = pen
        best_sched = (list(r1_1430), list(r1_1600), list(r2_1430), list(r2_1600), list(r3_1430), list(r3_1600))
        if pen < 20:
            break

print(f"Best pen: {best_penalty}, Min rest: {min_r}, Max rest: {max_r}")

days_dates = {
    1: '04/07/2026 (T7)', 2: '05/07/2026 (CN)', 3: '06/07/2026 (T2)', 4: '07/07/2026 (T3)', 5: '08/07/2026 (T4)',
    6: '10/07/2026 (T6)', 7: '11/07/2026 (T7)', 8: '12/07/2026 (CN)', 9: '13/07/2026 (T2)', 10: '14/07/2026 (T3)',
    11: '16/07/2026 (T5)', 12: '17/07/2026 (T6)', 13: '18/07/2026 (T7)', 14: '19/07/2026 (CN)', 15: '20/07/2026 (T2)'
}

r1_14, r1_16, r2_14, r2_16, r3_14, r3_16 = best_sched
md = ""

for i in range(5):
    day = i + 1
    m1 = r1_14[i]
    m2 = r1_16[i]
    md += f"| 1 | {days_dates[day]} | 14:30 | {m1[1][0]} | {m1[1][1]} | {m1[0]} |\n"
    md += f"| 1 | {days_dates[day]} | 16:00 | {m2[1][0]} | {m2[1][1]} | {m2[0]} |\n"

for i in range(5):
    day = i + 6
    m1 = r2_14[i]
    m2 = r2_16[i]
    md += f"| 2 | {days_dates[day]} | 14:30 | {m1[1][0]} | {m1[1][1]} | {m1[0]} |\n"
    md += f"| 2 | {days_dates[day]} | 16:00 | {m2[1][0]} | {m2[1][1]} | {m2[0]} |\n"

for i in range(5):
    day = i + 11
    m1 = r3_14[i]
    m2 = r3_16[i]
    md += f"| 3 | {days_dates[day]} | 14:30 | {m1[1][0]} | {m1[1][1]} | {m1[0]} |\n"
    md += f"| 3 | {days_dates[day]} | 16:00 | {m2[1][0]} | {m2[1][1]} | {m2[0]} |\n"

with open("final_perfect_md.txt", "w") as f:
    f.write(md)

