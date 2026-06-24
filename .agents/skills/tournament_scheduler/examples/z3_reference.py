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

def try_solve(max_rest_limit):
    print(f"\n--- Trying max_rest_limit = {max_rest_limit} ---")
    s = Solver()
    
    # Optional timeout to avoid hanging too long on UNSAT
    s.set("timeout", 10000)

    D = [Int(f'D_{i}') for i in range(num_matches)]
    T = [Int(f'T_{i}') for i in range(num_matches)]

    for i in range(num_matches):
        s.add(D[i] >= 0, D[i] < num_days)
        s.add(T[i] >= 0, T[i] <= 1)

    for d in range(num_days):
        s.add(Sum([If(D[i] == d, 1, 0) for i in range(num_matches)]) == 2)
        s.add(Sum([If(And(D[i] == d, T[i] == 0), 1, 0) for i in range(num_matches)]) == 1)
        s.add(Sum([If(And(D[i] == d, T[i] == 1), 1, 0) for i in range(num_matches)]) == 1)

    teams = list(set([m[1] for m in all_matches] + [m[2] for m in all_matches]))
    team_matches = {t: [] for t in teams}
    for i, m in enumerate(all_matches):
        team_matches[m[1]].append(i)
        team_matches[m[2]].append(i)

    # Min rest >= 1
    for t, m_list in team_matches.items():
        for i in range(len(m_list)):
            for j in range(i+1, len(m_list)):
                m1 = m_list[i]
                m2 = m_list[j]
                s.add(Or(D[m1] - D[m2] >= 2, D[m2] - D[m1] >= 2))

    # Max rest limit using sorted variables
    for t, m_list in team_matches.items():
        K = len(m_list)
        S = [Int(f'S_{t}_{k}') for k in range(K)]
        for k in range(K):
            s.add(S[k] >= 0, S[k] < num_days)
            s.add(Or([S[k] == D[m] for m in m_list]))
            
        for k in range(K-1):
            s.add(S[k] < S[k+1])
            s.add(S[k+1] - S[k] <= max_rest_limit + 1)

    # Weekend constraint
    weekends = [0, 1, 6, 7, 13, 14]
    for t, m_list in team_matches.items():
        s.add(Or([Or([D[m] == w for w in weekends]) for m in m_list]))

    # 16:00 constraint
    for t, m_list in team_matches.items():
        if t.startswith('A') or t.startswith('B') or t.startswith('C'):
            s.add(Sum([T[m] for m in m_list]) == 2)
        else:
            s.add(Sum([T[m] for m in m_list]) >= 1)
            s.add(Sum([T[m] for m in m_list]) <= 2)

    # Early start constraint
    # Every team must play its first match within the first 6 days (index <= 5)
    for t, m_list in team_matches.items():
        s.add(Or([D[m] <= 5 for m in m_list]))

    res = s.check()
    if res == sat:
        print("SAT!")
        m = s.model()
        return m, D, T
    else:
        print(res)
        return None, None, None

best_m = None
best_D = None
best_T = None

# Binary search or linear scan for best max_rest_limit
for limit in [7, 6, 5, 4]:
    m, D, T = try_solve(limit)
    if m:
        best_m = m
        best_D = D
        best_T = T
        print(f"Success with max_rest_limit = {limit}")
    else:
        print(f"Failed with max_rest_limit = {limit}")
        break

if best_m:
    print("Writing best model to file...")
    days_dates = [
        '04/07/2026 (T7)', '05/07/2026 (CN)', '06/07/2026 (T2)', '07/07/2026 (T3)', 
        '09/07/2026 (T5)', '10/07/2026 (T6)', '11/07/2026 (T7)', '12/07/2026 (CN)', 
        '13/07/2026 (T2)', '14/07/2026 (T3)', '15/07/2026 (T4)', '16/07/2026 (T5)', 
        '17/07/2026 (T6)', '18/07/2026 (T7)', '19/07/2026 (CN)', '20/07/2026 (T2)', 
        '21/07/2026 (T3)', '22/07/2026 (T4)'
    ]
    
    cal_days = [
        4, 5, 6, 7,
        9, 10, 11, 12,
        13, 14, 15, 16,
        17, 18, 19, 20,
        21, 22
    ]
    
    schedule = [None] * num_days
    for d in range(num_days):
        schedule[d] = [None, None]
        
    for i in range(num_matches):
        d = best_m[best_D[i]].as_long()
        t = best_m[best_T[i]].as_long()
        schedule[d][t] = all_matches[i]
        
    md = ""
    team_last_date = {}
    
    for d in range(num_days):
        cal_date = cal_days[d]
        date_str_full = days_dates[d]
        
        # 14:30
        g1, t1, t2 = schedule[d][0]
        rest1 = f"{cal_date - team_last_date[t1] - 1} ngày" if t1 in team_last_date else "-"
        rest2 = f"{cal_date - team_last_date[t2] - 1} ngày" if t2 in team_last_date else "-"
        team_last_date[t1] = cal_date
        team_last_date[t2] = cal_date
        md += f"| {d+1} | {date_str_full} | 14:30 | {t1} | {t2} | {g1} | {rest1} | {rest2} |\n"
        
        # 16:00
        g2, t3, t4 = schedule[d][1]
        rest3 = f"{cal_date - team_last_date[t3] - 1} ngày" if t3 in team_last_date else "-"
        rest4 = f"{cal_date - team_last_date[t4] - 1} ngày" if t4 in team_last_date else "-"
        team_last_date[t3] = cal_date
        team_last_date[t4] = cal_date
        md += f"| {d+1} | {date_str_full} | 16:00 | {t3} | {t4} | {g2} | {rest3} | {rest4} |\n"
        
    with open("final_men_19.txt", "w") as f:
        f.write(md)

