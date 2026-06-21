weekends = {1, 2, 7, 8, 14, 15}
A_days = {1, 3, 6, 9, 14}
rem_days = [d for d in range(1, 18) if d not in A_days]

# We want the ends to be exactly 13, 15, 16, 17
from itertools import permutations

best_max_rest = float('inf')
best_assignment = None

def get_calendar_gap(d1, d2):
    return d2 - d1 - 1

def solve():
    global best_max_rest, best_assignment
    
    # Generate all combinations of 3 days for B, C, D, E
    # We have 12 remaining days. The last elements of each group must be 13, 15, 16, 17
    # So we need to distribute the 8 early days: 2, 4, 5, 7, 8, 10, 11, 12
    # into 4 pairs (B1,B2), (C1,C2), (D1,D2), (E1,E2)
    early_days = [2, 4, 5, 7, 8, 10, 11, 12]
    ends = [13, 15, 16, 17]
    
    def backtrack(idx, current_pairs):
        global best_max_rest, best_assignment
        if idx == 8:
            # We have 4 pairs
            # Pair them with the 4 ends
            for end_perm in permutations(ends):
                assignment = []
                for i in range(4):
                    assignment.append(current_pairs[i] + [end_perm[i]])
                
                # Check weekends
                valid = True
                for g in range(4):
                    if not any(d in weekends for d in assignment[g]):
                        valid = False
                        break
                if not valid: continue
                
                # Calculate max internal rest
                max_rest = 0
                for g in range(4):
                    r1 = get_calendar_gap(assignment[g][0], assignment[g][1])
                    r2 = get_calendar_gap(assignment[g][1], assignment[g][2])
                    max_rest = max(max_rest, r1, r2)
                
                if max_rest < best_max_rest:
                    best_max_rest = max_rest
                    best_assignment = assignment
            return
            
        d = early_days[idx]
        for p in range(4):
            if len(current_pairs[p]) < 2:
                if current_pairs[p]:
                    # enforce ascending
                    if d <= current_pairs[p][-1]:
                        continue
                current_pairs[p].append(d)
                
                # Symmetry breaking for pairs
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

solve()
print(f"Best max internal rest: {best_max_rest}")
print("Assignment:", best_assignment)

