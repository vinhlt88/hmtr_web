from itertools import permutations, combinations

weekends = {1, 2, 7, 8, 14, 15}
days_dict = {
    1: 4, 2: 5, 3: 6, 4: 7, 
    5: 9, 6: 10, 7: 11, 8: 12, 9: 13, 10: 14, 11: 15, 12: 16, 13: 17, 14: 18, 15: 19, 16: 20, 17: 21
}

def get_calendar_gap(d1, d2):
    return days_dict[d2] - days_dict[d1] - 1

valid_A_days = []
for A_days_idx in combinations(range(1, 18), 5):
    if A_days_idx[0] != 1: continue
    
    # Check internal gaps >= 1 day rest
    valid = True
    for i in range(4):
        if get_calendar_gap(A_days_idx[i], A_days_idx[i+1]) < 1:
            valid = False
            break
    if not valid: continue
    
    # Must have exactly 2 days in first 6 days
    first_6 = sum(1 for d in A_days_idx if d <= 6)
    if first_6 != 2: continue
    
    # End day must be among 13, 14, 15, 16, 17
    if A_days_idx[-1] not in {13, 14, 15, 16, 17}: continue
    
    # Weekends
    A_wknds = sum(1 for d in A_days_idx if d in weekends)
    if A_wknds < 1: continue
    if 6 - A_wknds < 4: continue # Leave at least 4 weekends for B,C,D,E
    
    valid_A_days.append(A_days_idx)

print(f"Found {len(valid_A_days)} valid A days")

best_max_rest = float('inf')
best_assignment = None
best_A = None

for A_days in valid_A_days:
    rem_days = [d for d in range(1, 18) if d not in A_days]
    
    early_days = [d for d in rem_days if d not in {13, 14, 15, 16, 17} or d == rem_days[-4]] 
    # Actually, let's just use permutations to partition rem_days
    # rem_days has exactly 12 days.
    # We want 4 groups of 3 days.
    # And their last days must exactly be the 4 days from {13,14,15,16,17} that A didn't take.
    ends = [d for d in {13, 14, 15, 16, 17} if d != A_days[-1]]
    if len(ends) != 4: continue
    
    other_days = [d for d in rem_days if d not in ends]
    if len(other_days) != 8: continue
    
    # Partition other_days into 4 pairs
    def backtrack(idx, current_pairs):
        global best_max_rest, best_assignment, best_A
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
                
                # Check A max rest
                rA = [get_calendar_gap(A_days[i], A_days[i+1]) for i in range(4)]
                if max(rA) > 7: continue
                
                max_rest = 0
                for g in range(4):
                    r1 = get_calendar_gap(assignment[g][0], assignment[g][1])
                    r2 = get_calendar_gap(assignment[g][1], assignment[g][2])
                    max_rest = max(max_rest, r1, r2)
                
                max_rest = max(max_rest, max(rA))
                
                if max_rest < best_max_rest:
                    best_max_rest = max_rest
                    best_assignment = assignment
                    best_A = A_days
            return
            
        d = other_days[idx]
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

print(f"Best max rest: {best_max_rest}")
print("Best A:", best_A)
print("Assignment:", best_assignment)
