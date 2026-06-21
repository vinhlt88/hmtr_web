import json

groups = {
    'A': [
        ('D1', 'A1', 'A2'), ('D1', 'A3', 'A4'),
        ('D6', 'A2', 'A3'), ('D6', 'A5', 'A1'),
        ('D15', 'A4', 'A5'), ('D15', 'A1', 'A3'),
        ('D16', 'A5', 'A2'), ('D16', 'A4', 'A1'),
        ('D17', 'A3', 'A5'), ('D17', 'A2', 'A4')
    ],
    'B': [
        ('D2', 'B1', 'B2'), ('D2', 'B3', 'B4'),
        ('D9', 'B4', 'B2'), ('D9', 'B3', 'B1'),
        ('D13', 'B4', 'B1'), ('D13', 'B2', 'B3')
    ],
    'C': [
        ('D3', 'C3', 'C4'), ('D3', 'C1', 'C2'),
        ('D7', 'C3', 'C1'), ('D7', 'C4', 'C2'),
        ('D11', 'C4', 'C1'), ('D11', 'C2', 'C3')
    ],
    'D': [
        ('D4', 'D3', 'D4'), ('D4', 'D1', 'D2'),
        ('D8', 'D3', 'D1'), ('D8', 'D4', 'D2'),
        ('D12', 'D4', 'D1'), ('D12', 'D2', 'D3')
    ],
    'E': [
        ('D5', 'E3', 'E4'), ('D5', 'E1', 'E2'),
        ('D10', 'E3', 'E1'), ('D10', 'E4', 'E2'),
        ('D14', 'E4', 'E1'), ('D14', 'E2', 'E3')
    ]
}

def solve_group(group_matches, num_teams):
    # group_matches is list of (Day, T1, T2). It's ordered by Day.
    # Group matches into pairs by Day
    days = {}
    for m in group_matches:
        if m[0] not in days:
            days[m[0]] = []
        days[m[0]].append((m[1], m[2]))
        
    day_list = list(days.keys())
    
    best_assignment = None
    best_score = 9999
    
    # Brute force 2^(num_days) possibilities (0 = match1 is 14h30, 1 = match1 is 16h00)
    for i in range(1 << len(day_list)):
        assignment = {}
        counts = {t: {'T1': 0, 'T2': 0} for m in group_matches for t in m[1:]}
        
        for idx, day in enumerate(day_list):
            m1, m2 = days[day][0], days[day][1]
            if (i & (1 << idx)):
                # m1 is T1, m2 is T2
                counts[m1[0]]['T1'] += 1; counts[m1[1]]['T1'] += 1
                counts[m2[0]]['T2'] += 1; counts[m2[1]]['T2'] += 1
                assignment[day] = (m1, m2)
            else:
                # m1 is T2, m2 is T1
                counts[m1[0]]['T2'] += 1; counts[m1[1]]['T2'] += 1
                counts[m2[0]]['T1'] += 1; counts[m2[1]]['T1'] += 1
                assignment[day] = (m2, m1) # (T1_match, T2_match)
                
        # Calculate score (variance from ideal)
        # Ideal for 3 matches is 1.5, for 4 matches is 2.0
        score = 0
        for t, c in counts.items():
            if num_teams == 4:
                # Ideal is 1 and 2 or 2 and 1
                score += abs(c['T1'] - 1.5) + abs(c['T2'] - 1.5)
            else:
                # Ideal is 2 and 2
                score += abs(c['T1'] - 2.0) + abs(c['T2'] - 2.0)
                
        if score < best_score:
            best_score = score
            best_assignment = assignment
            
    return best_assignment, best_score

final_schedule = {}
for g, matches in groups.items():
    num = 5 if g == 'A' else 4
    ans, score = solve_group(matches, num)
    for day, (m_t1, m_t2) in ans.items():
        final_schedule[day] = {
            '14:30': m_t1,
            '16:00': m_t2
        }

print(json.dumps(final_schedule, indent=2))
