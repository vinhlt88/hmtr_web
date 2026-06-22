import sys

groups = {
    'A': [('A1', 'A2'), ('A3', 'A4'), ('A4', 'A2'), ('A3', 'A1'), ('A4', 'A1'), ('A2', 'A3')],
    'B': [('B1', 'B2'), ('B3', 'B4'), ('B4', 'B2'), ('B3', 'B1'), ('B4', 'B1'), ('B2', 'B3')],
    'C': [('C1', 'C2'), ('C3', 'C4'), ('C4', 'C2'), ('C3', 'C1'), ('C4', 'C1'), ('C2', 'C3')],
    'D': [('D1', 'D2'), ('D3', 'D4'), ('D4', 'D2'), ('D3', 'D1'), ('D4', 'D1'), ('D2', 'D3')],
    'E': [('E1', 'E2'), ('E3', 'E4'), ('E4', 'E2'), ('E3', 'E1'), ('E4', 'E1'), ('E2', 'E3')]
}

r1_matches = []
r2_matches = []
r3_matches = []
for g in "ABCDE":
    r1_matches.extend([(g, groups[g][0]), (g, groups[g][1])])
    r2_matches.extend([(g, groups[g][2]), (g, groups[g][3])])
    r3_matches.extend([(g, groups[g][4]), (g, groups[g][5])])

all_matches = r1_matches + r2_matches + r3_matches
# Total 30 matches.

def solve():
    assignment = [0]*30
    
    def backtrack(idx, r1_sum, r2_sum, r3_sum, team_sums):
        if idx == 30:
            return r1_sum == 5 and r2_sum == 5 and r3_sum == 5
            
        m = all_matches[idx]
        t1, t2 = m[1][0], m[1][1]
        
        for val in (0, 1):
            # Check limits
            if val == 1:
                if idx < 10 and r1_sum == 5: continue
                if 10 <= idx < 20 and r2_sum == 5: continue
                if 20 <= idx < 30 and r3_sum == 5: continue
                if team_sums[t1] == 2 or team_sums[t2] == 2: continue
                
            assignment[idx] = val
            
            # bounds check for lower bound (must be at least 1)
            # if we assign 0, check if remaining matches can satisfy the lower bound
            if val == 0:
                pass # Can be pruned, but 30 vars is fast enough
                
            if val == 1:
                team_sums[t1] += 1
                team_sums[t2] += 1
                
            if idx < 10:
                res = backtrack(idx+1, r1_sum+val, r2_sum, r3_sum, team_sums)
            elif idx < 20:
                res = backtrack(idx+1, r1_sum, r2_sum+val, r3_sum, team_sums)
            else:
                res = backtrack(idx+1, r1_sum, r2_sum, r3_sum+val, team_sums)
                
            if res:
                # final check on team_sums
                if idx == 29:
                    valid = True
                    for k, v in team_sums.items():
                        if v < 1 or v > 2:
                            valid = False
                            break
                    if valid:
                        return True
                else:
                    return True
                    
            if val == 1:
                team_sums[t1] -= 1
                team_sums[t2] -= 1
                
        return False

    team_sums = {f"{g}{i}": 0 for g in "ABCDE" for i in range(1, 5)}
    if backtrack(0, 0, 0, 0, team_sums):
        print("Found valid 16:00 assignment!")
        print(assignment)
    else:
        print("No valid assignment exists.")

solve()
