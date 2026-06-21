from itertools import combinations

weekends = {1, 2, 7, 8, 14, 15}
days_dict = {
    1: 4, 2: 5, 3: 6, 4: 7, # 04/07 to 07/07
    # Day 8/07 is rest
    5: 9, 6: 10, 7: 11, 8: 12, 9: 13, 10: 14, 11: 15, 12: 16, 13: 17, 14: 18, 15: 19, 16: 20, 17: 21
}

playoff_date = 23

best_max_gap = float('inf')
best_days = None

for A_days_idx in combinations(range(1, 18), 5):
    if A_days_idx[0] != 1: continue # Must start on Day 1
    
    A_days = [days_dict[i] for i in A_days_idx]
    
    # Internal gaps must be >= 2 days (>= 1 day rest)
    valid = True
    for i in range(4):
        if A_days[i+1] - A_days[i] < 2:
            valid = False
            break
    if not valid: continue
    
    # A_weekends >= 1
    wknds = sum(1 for d in A_days_idx if d in weekends)
    if wknds < 1: continue
    
    # Rest gaps for teams
    # A5 rests R1: starts on A_days[1]. Gap from start of tournament (04/07)? No, wait before first match.
    # Actually wait before first match doesn't break rhythm as much, but let's count it.
    gap_A5 = A_days[1] - 4 - 1
    
    # A4 rests R2: plays R1 and R3
    gap_A4 = A_days[2] - A_days[0] - 1
    
    # A2 rests R3: plays R2 and R4
    gap_A2 = A_days[3] - A_days[1] - 1
    
    # A3 rests R4: plays R3 and R5
    gap_A3 = A_days[4] - A_days[2] - 1
    
    # A1 rests R5: plays R4, waits for playoff
    gap_A1 = playoff_date - A_days[3] - 1
    
    # All teams wait for playoff after their last match
    gap_A5_end = playoff_date - A_days[4] - 1
    gap_A4_end = playoff_date - A_days[4] - 1
    gap_A2_end = playoff_date - A_days[4] - 1
    gap_A3_end = playoff_date - A_days[4] - 1
    
    max_gap = max(gap_A5, gap_A4, gap_A2, gap_A3, gap_A1, 
                  gap_A5_end, gap_A4_end, gap_A2_end, gap_A3_end)
                  
    if max_gap < best_max_gap:
        best_max_gap = max_gap
        best_days = A_days_idx

print(f"Best max gap: {best_max_gap}")
print(f"Best A days (indices): {best_days}")
print(f"Dates: {[days_dict[i] for i in best_days]}")
