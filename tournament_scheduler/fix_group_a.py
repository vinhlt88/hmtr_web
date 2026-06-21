matches = [
    [('A1', 'A2'), ('A3', 'A4')], # D1
    [('A2', 'A3'), ('A5', 'A1')], # D6
    [('A4', 'A5'), ('A1', 'A3')], # D15
    [('A5', 'A2'), ('A4', 'A1')], # D16
    [('A3', 'A5'), ('A2', 'A4')]  # D17
]

for i in range(32):
    counts = {f'A{j}': {'T1': 0, 'T2': 0} for j in range(1, 6)}
    assignment = []
    for day in range(5):
        if i & (1 << day):
            t1_match = matches[day][0]
            t2_match = matches[day][1]
        else:
            t1_match = matches[day][1]
            t2_match = matches[day][0]
            
        counts[t1_match[0]]['T1'] += 1; counts[t1_match[1]]['T1'] += 1
        counts[t2_match[0]]['T2'] += 1; counts[t2_match[1]]['T2'] += 1
        assignment.append((t1_match, t2_match))
        
    valid = True
    for k, v in counts.items():
        if v['T1'] != 2 or v['T2'] != 2:
            valid = False
            break
            
    if valid:
        print("FOUND PERFECT MATCH FOR A!")
        for day in range(5):
            print(f"Day {day+1}: 14:30 {assignment[day][0]} | 16:00 {assignment[day][1]}")
        break
