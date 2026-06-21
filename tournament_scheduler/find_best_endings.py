weekends = {1, 2, 7, 8, 14, 15}
A_days = {1, 3, 6, 9, 14}
rem_days = [d for d in range(1, 18) if d not in A_days]

days_dict = {
    1: 4, 2: 5, 3: 6, 4: 7, 
    5: 9, 6: 10, 7: 11, 8: 12, 9: 13, 10: 14, 11: 15, 12: 16, 13: 17, 14: 18, 15: 19, 16: 20, 17: 21
}

from itertools import permutations

def get_calendar_gap(d1, d2):
    return days_dict[d2] - days_dict[d1] - 1

valid_assignments = []

early_days = [2, 4, 5, 7, 8, 10, 11, 12]
ends = [13, 15, 16, 17]

def backtrack(idx, current_pairs):
    if idx == 8:
        for end_perm in permutations(ends):
            assignment = []
            for i in range(4):
                assignment.append(current_pairs[i] + [end_perm[i]])
            
            valid = True
            for g in range(4):
                if not any(d in weekends for d in assignment[g]):
                    valid = False
                    break
                r1 = get_calendar_gap(assignment[g][0], assignment[g][1])
                r2 = get_calendar_gap(assignment[g][1], assignment[g][2])
                if r1 < 1 or r2 < 1 or r1 > 7 or r2 > 7:
                    valid = False
                    break
            if not valid: continue
            
            max_start = max(assignment[g][0] for g in range(4))
            valid_assignments.append({
                'max_start': max_start,
                'assignment': assignment
            })
        return
        
    d = early_days[idx]
    for p in range(4):
        if len(current_pairs[p]) < 2:
            if current_pairs[p]:
                if d <= current_pairs[p][-1]:
                    continue
            current_pairs[p].append(d)
            
            if len(current_pairs[p]) == 1:
                is_valid = True
                for prev_p in range(p):
                    if not current_pairs[prev_p]:
                        is_valid = False
                        break
                if not is_valid:
                    current_pairs[p].pop()
                    continue
            
            backtrack(idx + 1, current_pairs)
            current_pairs[p].pop()

backtrack(0, [[], [], [], []])

for s in sorted(valid_assignments, key=lambda x: x['max_start']):
    print(f"Max start: {s['max_start']}, Assignment: {s['assignment']}")

