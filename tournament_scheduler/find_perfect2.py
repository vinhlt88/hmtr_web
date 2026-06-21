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
    
    valid = True
    for i in range(4):
        if get_calendar_gap(A_days_idx[i], A_days_idx[i+1]) < 1:
            valid = False
            break
    if not valid: continue
    
    first_6 = sum(1 for d in A_days_idx if d <= 6)
    if first_6 != 2: continue # Leaves 4 slots in first 6 days for the 4 other groups
    
    if A_days_idx[-1] not in {13, 14, 15, 16, 17}: continue
    
    A_wknds = sum(1 for d in A_days_idx if d in weekends)
    if A_wknds < 1: continue
    if 6 - A_wknds < 4: continue
    
    valid_A_days.append(A_days_idx)

best_max_rest = float('inf')
best_assignment = None
best_A = None

for A_days in valid_A_days:
    rem_days = [d for d in range(1, 18) if d not in A_days]
    
    ends = [d for d in {13, 14, 15, 16, 17} if d != A_days[-1]]
    if len(ends) != 4: continue
    
    other_days = [d for d in rem_days if d not in ends]
    if len(other_days) != 8: continue
    
    # We MUST ensure that exactly the 4 remaining days from {1,2,3,4,5,6} are assigned
    # as the FIRST element of the 4 groups.
    req_starts = [d for d in range(1, 7) if d not in A_days]
    if len(req_starts) != 4: continue
    
    # The middle elements are the remaining 4 days in other_days
    mids = [d for d in other_days if d not in req_starts]
    if len(mids) != 4: continue

    # So for each group, the assignment is [start, mid, end]
    # We just need to pair the 4 starts, 4 mids, and 4 ends.
    for mid_perm in permutations(mids):
        for end_perm in permutations(ends):
            assignment = []
            valid = True
            for i in range(4):
                if req_starts[i] >= mid_perm[i] or mid_perm[i] >= end_perm[i]:
                    valid = False
                    break
                assignment.append([req_starts[i], mid_perm[i], end_perm[i]])
            
            if not valid: continue
            
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

print(f"Best max rest: {best_max_rest}")
print("Best A:", best_A)
print("Assignment:", best_assignment)
