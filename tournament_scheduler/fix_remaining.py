weekends = {1, 2, 7, 8, 14, 15}
A_days = {1, 3, 6, 9, 14}
rem_days = [d for d in range(1, 18) if d not in A_days]

# We need to partition rem_days into 4 lists of 3 days each (for B, C, D, E)
# such that:
# 1. Each list has at least one weekend
# 2. Internal gaps are >= 2 days (i.e. diff >= 2)
# 3. Internal gaps are <= 8 days (diff <= 8)
# 4. Minimize the maximum gap at the end (from day to 17)

from itertools import permutations

best_max_end_gap = float('inf')
best_assignment = None

def solve():
    global best_max_end_gap, best_assignment
    
    assignment = [[] for _ in range(4)]
    
    def backtrack(day_idx):
        global best_max_end_gap, best_assignment
        if day_idx == 12:
            # Check weekends
            valid = True
            for g in range(4):
                if not any(d in weekends for d in assignment[g]):
                    valid = False
            if not valid: return
            
            end_gaps = [17 - assignment[g][-1] for g in range(4)]
            max_end = max(end_gaps)
            if max_end < best_max_end_gap:
                best_max_end_gap = max_end
                best_assignment = [list(a) for a in assignment]
            return
            
        d = rem_days[day_idx]
        for g in range(4):
            if len(assignment[g]) < 3:
                if assignment[g]:
                    diff = d - assignment[g][-1]
                    if diff < 2 or diff > 8:
                        continue
                assignment[g].append(d)
                backtrack(day_idx + 1)
                assignment[g].pop()
                
    backtrack(0)

solve()
print(f"Best max end gap: {best_max_end_gap}")
print("Assignment:", best_assignment)
