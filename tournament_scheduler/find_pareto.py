weekends = {1, 2, 7, 8, 14, 15}
A_days = {1, 3, 6, 9, 14}
rem_days = [d for d in range(1, 18) if d not in A_days]

solutions = []

assignment = [[] for _ in range(4)]

def backtrack(day_idx):
    if day_idx == 12:
        valid = True
        for g in range(4):
            if not any(d in weekends for d in assignment[g]):
                valid = False
        if not valid: return
        
        max_start = max(assignment[g][0] for g in range(4))
        max_end_gap = max(17 - assignment[g][-1] for g in range(4))
        max_internal_gap = max(assignment[g][1] - assignment[g][0] for g in range(4))
        max_internal_gap2 = max(assignment[g][2] - assignment[g][1] for g in range(4))
        max_gap = max(max_internal_gap, max_internal_gap2) - 1 # Rest days
        
        solutions.append({
            'max_start': max_start,
            'max_end_gap': max_end_gap,
            'max_rest': max_gap,
            'assignment': [list(a) for a in assignment]
        })
        return
        
    d = rem_days[day_idx]
    for g in range(4):
        if len(assignment[g]) < 3:
            if assignment[g]:
                diff = d - assignment[g][-1]
                if diff < 2 or diff > 8:
                    continue
            assignment[g].append(d)
            # Symmetry breaking: first elements must be ordered
            if len(assignment[g]) == 1:
                # find if there's any empty group before this one
                is_valid = True
                for prev_g in range(g):
                    if not assignment[prev_g]:
                        is_valid = False
                        break
                if not is_valid:
                    assignment[g].pop()
                    continue
            
            backtrack(day_idx + 1)
            assignment[g].pop()

backtrack(0)

print(f"Found {len(solutions)} solutions.")

# Find Pareto frontier
pareto = []
for s in solutions:
    is_dominated = False
    for other in solutions:
        if other['max_start'] <= s['max_start'] and \
           other['max_end_gap'] <= s['max_end_gap'] and \
           other['max_rest'] <= s['max_rest']:
               if other['max_start'] < s['max_start'] or \
                  other['max_end_gap'] < s['max_end_gap'] or \
                  other['max_rest'] < s['max_rest']:
                   is_dominated = True
                   break
    if not is_dominated:
        pareto.append(s)

print("Pareto optimal solutions:")
for s in pareto:
    print(f"Max Start: {s['max_start']}, Max End Gap: {s['max_end_gap']}, Max Rest: {s['max_rest']}, Assignment: {s['assignment']}")
