import json

groups = {
    'A': [('A1', 'A2'), ('A3', 'A4'), ('A4', 'A2'), ('A3', 'A1'), ('A4', 'A1'), ('A2', 'A3')],
    'B': [('B1', 'B2'), ('B3', 'B4'), ('B4', 'B2'), ('B3', 'B1'), ('B4', 'B1'), ('B2', 'B3')],
    'C': [('C1', 'C2'), ('C3', 'C4'), ('C4', 'C2'), ('C3', 'C1'), ('C4', 'C1'), ('C2', 'C3')],
    'D': [('D1', 'D2'), ('D3', 'D4'), ('D4', 'D2'), ('D3', 'D1'), ('D4', 'D1'), ('D2', 'D3')],
    'E': [('E1', 'E2'), ('E3', 'E4'), ('E4', 'E2'), ('E3', 'E1'), ('E4', 'E1'), ('E2', 'E3')]
}

# The assignments from permutation:
# A=0, B=1, C=2, D=3, E=4
# R1: A B C D E
# R2: A B C D E
# R3: A B D E C

r1_order = ['A', 'B', 'C', 'D', 'E']
r2_order = ['A', 'B', 'C', 'D', 'E']
r3_order = ['A', 'B', 'D', 'E', 'C']

days_dates = {
    1: '04/07/2026 (T7)', 2: '05/07/2026 (CN)', 3: '06/07/2026 (T2)', 4: '07/07/2026 (T3)', 5: '08/07/2026 (T4)',
    6: '10/07/2026 (T6)', 7: '11/07/2026 (T7)', 8: '12/07/2026 (CN)', 9: '13/07/2026 (T2)', 10: '14/07/2026 (T3)',
    11: '16/07/2026 (T5)', 12: '17/07/2026 (T6)', 13: '18/07/2026 (T7)', 14: '19/07/2026 (CN)', 15: '20/07/2026 (T2)'
}

block1 = [1, 2, 3, 4, 5]
block2 = [6, 7, 8, 9, 10]
block3 = [11, 12, 13, 14, 15]

# Star Graph logic for 16:00
# To ensure Team 3 gets 3 matches at 16:00, and others get 1.
# R1: M1(14:30), M2(16:00) -> M2 is (T3, T4). So T3, T4 get 1.
# R2: M3(14:30), M4(16:00) -> M4 is (T3, T1). So T3 gets 1, T1 gets 1.
# R3: M5(14:30), M6(16:00) -> M6 is (T2, T3). So T3 gets 1, T2 gets 1.
# Total 16:00: T1(1), T2(1), T3(3), T4(1).
# M1=(T1, T2), M2=(T3, T4)
# M3=(T4, T2), M4=(T3, T1)
# M5=(T4, T1), M6=(T2, T3)

schedule = []
for i, g in enumerate(r1_order):
    day = block1[i]
    m1 = (g, groups[g][0]) # 14:30
    m2 = (g, groups[g][1]) # 16:00
    schedule.append((day, 1, m1, m2))

for i, g in enumerate(r2_order):
    day = block2[i]
    m1 = (g, groups[g][2]) # 14:30
    m2 = (g, groups[g][3]) # 16:00
    schedule.append((day, 2, m1, m2))

for i, g in enumerate(r3_order):
    day = block3[i]
    m1 = (g, groups[g][4]) # 14:30
    m2 = (g, groups[g][5]) # 16:00
    schedule.append((day, 3, m1, m2))

schedule.sort(key=lambda x: x[0])

# Calculate Rest
team_last_date = {}
date_to_idx = {
    1: 1, 2: 2, 3: 3, 4: 4, 5: 5,
    6: 7, 7: 8, 8: 9, 9: 10, 10: 11,
    11: 13, 12: 14, 13: 15, 14: 16, 15: 17
}

md = ""
for day, r, m1, m2 in schedule:
    idx = date_to_idx[day]
    date_str_full = days_dates[day]
    
    t1, t2 = m1[1]
    rest1_str = f"{idx - team_last_date[t1] - 1} ngày" if t1 in team_last_date else "-"
    rest2_str = f"{idx - team_last_date[t2] - 1} ngày" if t2 in team_last_date else "-"
    team_last_date[t1] = idx
    team_last_date[t2] = idx
    md += f"| {r} | {date_str_full} | 14:30 | {t1} | {t2} | {m1[0]} | {rest1_str} | {rest2_str} |\n"
    
    t3, t4 = m2[1]
    rest3_str = f"{idx - team_last_date[t3] - 1} ngày" if t3 in team_last_date else "-"
    rest4_str = f"{idx - team_last_date[t4] - 1} ngày" if t4 in team_last_date else "-"
    team_last_date[t3] = idx
    team_last_date[t4] = idx
    md += f"| {r} | {date_str_full} | 16:00 | {t3} | {t4} | {m2[0]} | {rest3_str} | {rest4_str} |\n"

with open("final_perfect_md.txt", "w") as f:
    f.write(md)

