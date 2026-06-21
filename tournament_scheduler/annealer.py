import random
import math
import copy

groups = {
    'A': [('A1', 'A2', 1), ('A3', 'A4', 1), ('A5', 'A1', 2), ('A2', 'A3', 2), ('A4', 'A5', 3), ('A1', 'A3', 3), ('A5', 'A2', 4), ('A4', 'A1', 4), ('A3', 'A5', 5), ('A2', 'A4', 5)],
    'B': [('B1', 'B2', 1), ('B3', 'B4', 1), ('B4', 'B2', 2), ('B3', 'B1', 2), ('B4', 'B1', 3), ('B2', 'B3', 3)],
    'C': [('C3', 'C4', 1), ('C1', 'C2', 1), ('C3', 'C1', 2), ('C4', 'C2', 2), ('C4', 'C1', 3), ('C2', 'C3', 3)],
    'D': [('D3', 'D4', 1), ('D1', 'D2', 1), ('D3', 'D1', 2), ('D4', 'D2', 2), ('D4', 'D1', 3), ('D2', 'D3', 3)],
    'E': [('E3', 'E4', 1), ('E1', 'E2', 1), ('E3', 'E1', 2), ('E4', 'E2', 2), ('E4', 'E1', 3), ('E2', 'E3', 3)]
}

all_matches = []
for g, matches in groups.items():
    for m in matches:
        all_matches.append({'group': g, 'teams': (m[0], m[1]), 'round': m[2]})

weekends = {1, 2, 7, 8, 14, 15}

def evaluate(state):
    # state is a list of 34 matches.
    # index 0,1 -> day 1 (T1, T2)
    # index 2,3 -> day 2 (T1, T2)
    cost = 0
    
    team_days = {f"{g}{i}": [] for g in "ABCDE" for i in range(1, 6) if not (g != 'A' and i == 5)}
    team_t1 = {k: 0 for k in team_days}
    
    for i in range(17):
        m1 = state[i*2]
        m2 = state[i*2+1]
        t1, t2 = m1['teams']
        t3, t4 = m2['teams']
        
        # constraint 2: no team plays twice on same day
        if len({t1, t2, t3, t4}) < 4:
            cost += 1000000
            
        team_days[t1].append(i+1); team_days[t2].append(i+1)
        team_days[t3].append(i+1); team_days[t4].append(i+1)
        
        team_t1[t1] += 1; team_t1[t2] += 1
        
    for t, days in team_days.items():
        days.sort()
        for i in range(len(days)-1):
            diff = days[i+1] - days[i]
            if diff < 2:
                cost += 100000 * (2 - diff)
            if diff > 7:
                cost += 1000 * (diff - 7)
                
        if days[0] > 8:
            cost += 1000 * (days[0] - 8)
        if 17 - days[-1] > 7:
            cost += 1000 * (17 - days[-1] - 7)
            
        w = sum(1 for d in days if d in weekends)
        if t.startswith('A'):
            if w < 1: cost += 50000 * (1 - w)
            if team_t1[t] != 2: cost += 10000 * abs(team_t1[t] - 2)
        else:
            if w != 1: cost += 50000 * abs(w - 1)
            if team_t1[t] == 0 or team_t1[t] == 3: cost += 10000
            
    # round order
    for g in "ABCDE":
        g_matches = [m for m in state if m['group'] == g]
        for m1 in g_matches:
            for m2 in g_matches:
                if m1['round'] < m2['round']:
                    d1 = state.index(m1) // 2 + 1
                    d2 = state.index(m2) // 2 + 1
                    if d1 > d2:
                        cost += 10 * (d1 - d2)
                        if set(m1['teams']).intersection(set(m2['teams'])):
                            cost += 500 * (d1 - d2)
                            
    return cost

def solve():
    best_state = list(all_matches)
    random.shuffle(best_state)
    best_cost = evaluate(best_state)
    
    state = list(best_state)
    cost = best_cost
    
    T = 10000.0
    T_min = 0.001
    alpha = 0.99995
    
    iterations = 0
    while T > T_min:
        i, j = random.sample(range(34), 2)
        state[i], state[j] = state[j], state[i]
        
        new_cost = evaluate(state)
        
        if new_cost < cost or random.random() < math.exp((cost - new_cost) / T):
            cost = new_cost
            if cost < best_cost:
                best_cost = cost
                best_state = list(state)
                if best_cost == 0:
                    break
        else:
            state[i], state[j] = state[j], state[i] # backtrack
            
        T *= alpha
        iterations += 1
        
    print(f"Iterations: {iterations}, Best Cost: {best_cost}")
    return best_state, best_cost

final_state, final_cost = solve()
if final_cost < 1000:
    import json
    with open('optimized_state.json', 'w') as f:
        json.dump(final_state, f, indent=2)
else:
    print("Failed to find a completely valid schedule. Trying again...")
    final_state, final_cost = solve()
    import json
    with open('optimized_state.json', 'w') as f:
        json.dump(final_state, f, indent=2)

