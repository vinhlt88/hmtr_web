import itertools

block1 = [1, 2, 3, 4, 5]  # R1
block2 = [7, 8, 9, 10, 11] # R2
block3 = [13, 14, 15, 16, 17] # R3

weekends = [1, 2, 8, 9, 15, 16]

best_min_rest = -1
best_max_rest = 99
best_assignment = None

# We need to assign groups A, B, C, D, E to indices 0..4 in each round.
# For R1, A must be index 0 (Day 1). So R1 is [A, P[0], P[1], P[2], P[3]]
groups = [0, 1, 2, 3, 4] # A=0, B=1, C=2, D=3, E=4

for r1 in itertools.permutations([1, 2, 3, 4]):
    r1_assign = [0] + list(r1)
    
    for r2_assign in itertools.permutations(groups):
        for r3_assign in itertools.permutations(groups):
            
            # Check weekend counts
            valid_weekend = True
            wk_counts = [0]*5
            for g in groups:
                idx1 = r1_assign.index(g)
                idx2 = r2_assign.index(g)
                idx3 = r3_assign.index(g)
                
                d1 = block1[idx1]
                d2 = block2[idx2]
                d3 = block3[idx3]
                
                c = 0
                if d1 in weekends: c += 1
                if d2 in weekends: c += 1
                if d3 in weekends: c += 1
                
                if c < 1 or c > 2:
                    valid_weekend = False
                    break
                wk_counts[g] = c
                
            if not valid_weekend: continue
            
            # Calculate rests
            min_rest = 99
            max_rest = -1
            for g in groups:
                idx1 = r1_assign.index(g)
                idx2 = r2_assign.index(g)
                idx3 = r3_assign.index(g)
                
                d1 = block1[idx1]
                d2 = block2[idx2]
                d3 = block3[idx3]
                
                rest1 = d2 - d1 - 1
                rest2 = d3 - d2 - 1
                
                min_rest = min(min_rest, rest1, rest2)
                max_rest = max(max_rest, rest1, rest2)
                
            if max_rest < best_max_rest or (max_rest == best_max_rest and min_rest > best_min_rest):
                best_max_rest = max_rest
                best_min_rest = min_rest
                best_assignment = (r1_assign, r2_assign, r3_assign)

print(f"Best min rest: {best_min_rest}, max rest: {best_max_rest}")
print("Assignment R1:", best_assignment[0])
print("Assignment R2:", best_assignment[1])
print("Assignment R3:", best_assignment[2])

