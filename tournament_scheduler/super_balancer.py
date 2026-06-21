import random
import json

groups = {
    'A': [('A1', 'A2'), ('A3', 'A4'), ('A5', 'A1'), ('A2', 'A3'), ('A4', 'A5'), ('A1', 'A3'), ('A5', 'A2'), ('A4', 'A1'), ('A3', 'A5'), ('A2', 'A4')],
    'B': [('B1', 'B2'), ('B3', 'B4'), ('B4', 'B2'), ('B3', 'B1'), ('B4', 'B1'), ('B2', 'B3')],
    'C': [('C3', 'C4'), ('C1', 'C2'), ('C3', 'C1'), ('C4', 'C2'), ('C4', 'C1'), ('C2', 'C3')],
    'D': [('D3', 'D4'), ('D1', 'D2'), ('D3', 'D1'), ('D4', 'D2'), ('D4', 'D1'), ('D2', 'D3')],
    'E': [('E3', 'E4'), ('E1', 'E2'), ('E3', 'E1'), ('E4', 'E2'), ('E4', 'E1'), ('E2', 'E3')]
}

day_mapping = {
    'A': [1, 3, 7, 10, 13],
    'B': [2, 9, 17],
    'C': [4, 8, 16],
    'D': [5, 11, 14],
    'E': [6, 12, 15]
}

schedule = {}
for g, days in day_mapping.items():
    if g == 'A':
        schedule[days[0]] = [('A', groups['A'][0]), ('A', groups['A'][1])]
        schedule[days[1]] = [('A', groups['A'][2]), ('A', groups['A'][3])]
        schedule[days[2]] = [('A', groups['A'][4]), ('A', groups['A'][5])]
        schedule[days[3]] = [('A', groups['A'][6]), ('A', groups['A'][7])]
        schedule[days[4]] = [('A', groups['A'][8]), ('A', groups['A'][9])]
    else:
        schedule[days[0]] = [(g, groups[g][0]), (g, groups[g][1])]
        schedule[days[1]] = [(g, groups[g][2]), (g, groups[g][3])]
        schedule[days[2]] = [(g, groups[g][4]), (g, groups[g][5])]

best_schedule = {}
for d, matches in schedule.items():
    best_schedule[d] = [matches[0], matches[1]]

days_dict = {
    1: '04/07/2026 (T7)', 2: '05/07/2026 (CN)', 3: '06/07/2026 (T2)', 4: '07/07/2026 (T3)',
    5: '09/07/2026 (T5)', 6: '10/07/2026 (T6)', 7: '11/07/2026 (T7)', 8: '12/07/2026 (CN)',
    9: '13/07/2026 (T2)', 10: '14/07/2026 (T3)', 11: '15/07/2026 (T4)', 12: '16/07/2026 (T5)',
    13: '17/07/2026 (T6)', 14: '18/07/2026 (T7)', 15: '19/07/2026 (CN)', 16: '20/07/2026 (T2)', 17: '21/07/2026 (T3)'
}

# Force perfect T1/T2 for A if possible
best_schedule[1] = [['A', ('A3', 'A4')], ['A', ('A1', 'A2')]]
best_schedule[3] = [['A', ('A5', 'A1')], ['A', ('A2', 'A3')]]
best_schedule[7] = [['A', ('A1', 'A3')], ['A', ('A4', 'A5')]]
best_schedule[10] = [['A', ('A5', 'A2')], ['A', ('A4', 'A1')]]
best_schedule[13] = [['A', ('A2', 'A4')], ['A', ('A3', 'A5')]]

md = ""
for d in range(1, 18):
    m1 = best_schedule[d][0]
    m2 = best_schedule[d][1]
    g = m1[0]
    r = day_mapping[g].index(d) + 1
    
    md += f"| {r} | {days_dict[d]} | 14:30 | {m1[1][0]} | {m1[1][1]} | {g} |\n"
    md += f"| {r} | {days_dict[d]} | 16:00 | {m2[1][0]} | {m2[1][1]} | {g} |\n"

with open("mixed_md.txt", "w") as f:
    f.write(md)

