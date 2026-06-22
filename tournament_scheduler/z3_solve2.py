import z3

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

teams = [f"{g}{i}" for g in "ABCDE" for i in range(1, 5)]

opt = z3.Optimize()

r1_day = [z3.Int(f"r1_day_{i}") for i in range(10)]
r1_time = [z3.Int(f"r1_time_{i}") for i in range(10)]
r2_day = [z3.Int(f"r2_day_{i}") for i in range(10)]
r2_time = [z3.Int(f"r2_time_{i}") for i in range(10)]
r3_day = [z3.Int(f"r3_day_{i}") for i in range(10)]
r3_time = [z3.Int(f"r3_time_{i}") for i in range(10)]

for i in range(10):
    opt.add(r1_day[i] >= 1, r1_day[i] <= 5)
    opt.add(r1_time[i] >= 0, r1_time[i] <= 1)
    
    opt.add(r2_day[i] >= 6, r2_day[i] <= 10)
    opt.add(r2_time[i] >= 0, r2_time[i] <= 1)
    
    opt.add(r3_day[i] >= 11, r3_day[i] <= 15)
    opt.add(r3_time[i] >= 0, r3_time[i] <= 1)

for d in range(1, 6):
    opt.add(z3.Sum([z3.If(z3.And(r1_day[i] == d, r1_time[i] == 0), 1, 0) for i in range(10)]) == 1)
    opt.add(z3.Sum([z3.If(z3.And(r1_day[i] == d, r1_time[i] == 1), 1, 0) for i in range(10)]) == 1)

for d in range(6, 11):
    opt.add(z3.Sum([z3.If(z3.And(r2_day[i] == d, r2_time[i] == 0), 1, 0) for i in range(10)]) == 1)
    opt.add(z3.Sum([z3.If(z3.And(r2_day[i] == d, r2_time[i] == 1), 1, 0) for i in range(10)]) == 1)

for d in range(11, 16):
    opt.add(z3.Sum([z3.If(z3.And(r3_day[i] == d, r3_time[i] == 0), 1, 0) for i in range(10)]) == 1)
    opt.add(z3.Sum([z3.If(z3.And(r3_day[i] == d, r3_time[i] == 1), 1, 0) for i in range(10)]) == 1)

weekend_days = [1, 2, 7, 8, 13, 14]

t_days = {t: [] for t in teams}
t_times = {t: [] for t in teams}

for i in range(10):
    for t in r1_matches[i][1]:
        t_days[t].append(r1_day[i])
        t_times[t].append(r1_time[i])
        
for i in range(10):
    for t in r2_matches[i][1]:
        t_days[t].append(r2_day[i])
        t_times[t].append(r2_time[i])

for i in range(10):
    for t in r3_matches[i][1]:
        t_days[t].append(r3_day[i])
        t_times[t].append(r3_time[i])

for t in teams:
    time_sum = z3.Sum(t_times[t])
    opt.add(time_sum >= 1, time_sum <= 2)
    
    weekend_sum = z3.Sum([z3.If(z3.Or([d == wd for wd in weekend_days]), 1, 0) for d in t_days[t]])
    opt.add(weekend_sum >= 1)

min_rest_var = z3.Int("min_rest")
max_rest_var = z3.Int("max_rest")

for t in teams:
    d1 = t_days[t][0]
    d2 = t_days[t][1]
    d3 = t_days[t][2]
    gap1 = (d2 - d1) + 1
    gap2 = (d3 - d2) + 1
    rest1 = gap1 - 1
    rest2 = gap2 - 1
    
    opt.add(min_rest_var <= rest1)
    opt.add(min_rest_var <= rest2)
    opt.add(max_rest_var >= rest1)
    opt.add(max_rest_var >= rest2)

# relax bounds
opt.add(min_rest_var >= 1)
opt.add(max_rest_var <= 10)

opt.maximize(min_rest_var)

opt.set('timeout', 120000)

print("Solving...")
if opt.check() == z3.sat:
    m = opt.model()
    print("Found solution!")
    print(f"Min rest: {m[min_rest_var]}, Max rest: {m[max_rest_var]}")
    
    with open("final_perfect_md.txt", "w") as f:
        days_dates = {
            1: '04/07/2026 (T7)', 2: '05/07/2026 (CN)', 3: '06/07/2026 (T2)', 4: '07/07/2026 (T3)', 5: '08/07/2026 (T4)',
            6: '10/07/2026 (T6)', 7: '11/07/2026 (T7)', 8: '12/07/2026 (CN)', 9: '13/07/2026 (T2)', 10: '14/07/2026 (T3)',
            11: '16/07/2026 (T5)', 12: '17/07/2026 (T6)', 13: '18/07/2026 (T7)', 14: '19/07/2026 (CN)', 15: '20/07/2026 (T2)'
        }
        schedule = {d: [] for d in range(1, 16)}
        for i in range(10):
            schedule[m[r1_day[i]].as_long()].append((m[r1_time[i]].as_long(), r1_matches[i]))
            schedule[m[r2_day[i]].as_long()].append((m[r2_time[i]].as_long(), r2_matches[i]))
            schedule[m[r3_day[i]].as_long()].append((m[r3_time[i]].as_long(), r3_matches[i]))
            
        md = ""
        for d in range(1, 16):
            r = 1 if d <= 5 else 2 if d <= 10 else 3
            schedule[d].sort(key=lambda x: x[0])
            m1 = schedule[d][0][1]
            m2 = schedule[d][1][1]
            md += f"| {r} | {days_dates[d]} | 14:30 | {m1[1][0]} | {m1[1][1]} | {m1[0]} |\n"
            md += f"| {r} | {days_dates[d]} | 16:00 | {m2[1][0]} | {m2[1][1]} | {m2[0]} |\n"
            
        f.write(md)
else:
    print("No solution found!")

