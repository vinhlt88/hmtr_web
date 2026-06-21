from itertools import combinations

weekends = {1, 2, 7, 8, 14, 15}

def solve():
    for A_days in combinations(range(1, 18), 5):
        # We want A to start on Day 1 to satisfy the user
        if A_days[0] != 1: continue
        
        valid_A = True
        for i in range(4):
            if A_days[i+1] - A_days[i] < 2:
                valid_A = False; break
            if A_days[i+1] - A_days[i] > 8: # diff 8 = 7 days rest
                valid_A = False; break
        if not valid_A: continue
        
        # Check skipped round gaps for A
        if A_days[0] - 1 > 8: continue 
        if A_days[2] - A_days[0] > 8: continue 
        if A_days[3] - A_days[1] > 8: continue 
        if A_days[4] - A_days[2] > 8: continue 
        if 17 - A_days[3] > 8: continue 
        
        if 17 - A_days[-1] > 8: continue
        
        A_weekends = sum(1 for d in A_days if d in weekends)
        if A_weekends < 1: continue
        
        rem_weekends = sum(1 for d in range(1, 18) if d not in A_days and d in weekends)
        if rem_weekends < 4: continue
        
        rem_days = [d for d in range(1, 18) if d not in A_days]
        assignment = [[] for _ in range(4)]
        
        def backtrack(day_idx):
            if day_idx == 12: return True
                
            d = rem_days[day_idx]
            for g in range(4):
                if len(assignment[g]) < 3:
                    if assignment[g] and d - assignment[g][-1] < 2: continue
                    if assignment[g] and d - assignment[g][-1] > 8: continue # diff 8 = 7 days rest
                    if d in weekends:
                        if any(x in weekends for x in assignment[g]): continue
                    
                    assignment[g].append(d)
                    
                    if len(assignment[g]) == 1 and d > 9: # wait < 8 days
                        assignment[g].pop()
                        continue
                        
                    if backtrack(day_idx + 1): return True
                    assignment[g].pop()
            return False
            
        if backtrack(0):
            valid_partition = True
            for g in range(4):
                if 17 - assignment[g][-1] > 8: valid_partition = False
                if sum(1 for d in assignment[g] if d in weekends) != 1: valid_partition = False
            if valid_partition: return A_days, assignment
                
    return None

ans = solve()
if ans:
    print("Found day partition:")
    print(f"Group A: {ans[0]}")
    for i, a in enumerate(ans[1]):
        print(f"Group {i}: {a}")
else:
    print("No partition found.")
