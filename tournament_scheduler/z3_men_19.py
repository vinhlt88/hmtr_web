from z3 import *

groups = {
    'A': [('A1','A5'), ('A2','A4'), ('A5','A4'), ('A1','A3'), ('A4','A3'), ('A5','A2'), ('A3','A2'), ('A4','A1'), ('A2','A1'), ('A3','A5')],
    'B': [('B1','B5'), ('B2','B4'), ('B5','B4'), ('B1','B3'), ('B4','B3'), ('B5','B2'), ('B3','B2'), ('B4','B1'), ('B2','B1'), ('B3','B5')],
    'C': [('C1','C5'), ('C2','C4'), ('C5','C4'), ('C1','C3'), ('C4','C3'), ('C5','C2'), ('C3','C2'), ('C4','C1'), ('C2','C1'), ('C3','C5')],
    'D': [('D1','D4'), ('D2','D3'), ('D4','D3'), ('D1','D2'), ('D2','D4'), ('D3','D1')]
}

all_matches = []
for g, m_list in groups.items():
    for m in m_list:
        all_matches.append((g, m[0], m[1]))

num_days = 18
num_matches = len(all_matches)

s = Solver()

# D[i] is the day for match i
D = [Int(f'D_{i}') for i in range(num_matches)]
for i in range(num_matches):
    s.add(D[i] >= 0, D[i] < num_days)

# Exactly 2 matches per day
for d in range(num_days):
    s.add(Sum([If(D[i] == d, 1, 0) for i in range(num_matches)]) == 2)

# Teams
teams = list(set([m[1] for m in all_matches] + [m[2] for m in all_matches]))
team_matches = {t: [] for t in teams}
for i, m in enumerate(all_matches):
    team_matches[m[1]].append(i)
    team_matches[m[2]].append(i)

# Min rest >= 1 (no consecutive days)
# Abs(D[i] - D[j]) >= 2
for t, m_list in team_matches.items():
    for i in range(len(m_list)):
        for j in range(i+1, len(m_list)):
            m1 = m_list[i]
            m2 = m_list[j]
            # s.add(D[m1] != D[m2])
            # To ensure 1 clear rest day:
            s.add(Or(D[m1] - D[m2] >= 2, D[m2] - D[m1] >= 2))

# Weekend constraint
weekends = [0, 1, 6, 7, 13, 14]
for t, m_list in team_matches.items():
    s.add(Or([Or([D[m] == w for w in weekends]) for m in m_list]))

print("Solving...")
if s.check() == sat:
    print("SAT!")
    m = s.model()
    sched = [[] for _ in range(num_days)]
    for i in range(num_matches):
        d = m[D[i]].as_long()
        sched[d].append(all_matches[i])
        
    for d in range(num_days):
        print(f"Day {d+1}: {sched[d]}")
else:
    print("UNSAT! Rest >= 1 might be too strict.")
