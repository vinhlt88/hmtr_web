import json

with open('best_schedule.json', 'r') as f:
    best_schedule = json.load(f)

# Force the perfect Group A assignments
best_schedule["1"] = [['A', ('A3', 'A4')], ['A', ('A1', 'A2')]]
best_schedule["6"] = [['A', ('A5', 'A1')], ['A', ('A2', 'A3')]]
best_schedule["11"] = [['A', ('A1', 'A3')], ['A', ('A4', 'A5')]]
best_schedule["14"] = [['A', ('A5', 'A2')], ['A', ('A4', 'A1')]]
best_schedule["17"] = [['A', ('A2', 'A4')], ['A', ('A3', 'A5')]]

days = {
    1: '04/07/2026 (T7)',
    2: '05/07/2026 (CN)',
    3: '06/07/2026 (T2)',
    4: '07/07/2026 (T3)',
    5: '09/07/2026 (T5)',
    6: '10/07/2026 (T6)',
    7: '11/07/2026 (T7)',
    8: '12/07/2026 (CN)',
    9: '13/07/2026 (T2)',
    10: '14/07/2026 (T3)',
    11: '15/07/2026 (T4)',
    12: '16/07/2026 (T5)',
    13: '17/07/2026 (T6)',
    14: '18/07/2026 (T7)',
    15: '19/07/2026 (CN)',
    16: '20/07/2026 (T2)',
    17: '21/07/2026 (T3)'
}

# Define rounds roughly
# R1: Days 1-5
# R2: Days 6-10
# R3: Days 11-16
# R4: Day 14 (A only)
# R5: Day 17 (A only)

md = ""
for d in range(1, 18):
    if d <= 5: r = 1
    elif d <= 10: r = 2
    elif d in [11, 12, 13, 15, 16]: r = 3
    elif d == 14: r = 4
    elif d == 17: r = 5
    
    matches = best_schedule[str(d)]
    m1 = matches[0]
    m2 = matches[1]
    
    md += f"| {r} | {days[d]} | 14:30 | {m1[1][0]} | {m1[1][1]} | {m1[0]} |\n"
    md += f"| {r} | {days[d]} | 16:00 | {m2[1][0]} | {m2[1][1]} | {m2[0]} |\n"

print(md)
