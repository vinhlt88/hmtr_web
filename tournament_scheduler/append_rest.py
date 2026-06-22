import re

with open("final_perfect_md.txt", "r") as f:
    lines = f.readlines()

team_last_date = {}

# Map dates to calendar index to calculate rest
date_to_idx = {
    '04/07/2026': 1, '05/07/2026': 2, '06/07/2026': 3, '07/07/2026': 4, '08/07/2026': 5,
    '10/07/2026': 7, '11/07/2026': 8, '12/07/2026': 9, '13/07/2026': 10, '14/07/2026': 11,
    '16/07/2026': 13, '17/07/2026': 14, '18/07/2026': 15, '19/07/2026': 16, '20/07/2026': 17
}

out_lines = []
for line in lines:
    if not line.strip() or not line.startswith('|'):
        continue
    cols = [c.strip() for c in line.split('|')[1:-1]]
    if len(cols) < 6: continue
    
    r, date_str_full, time_str, t1, t2, g = cols[:6]
    date_str = date_str_full.split(' ')[0]
    
    idx = date_to_idx[date_str]
    
    # Calculate rest
    if t1 in team_last_date:
        rest1 = (idx - team_last_date[t1]) - 1
        rest1_str = f"{rest1} ngày"
    else:
        rest1_str = "-"
        
    if t2 in team_last_date:
        rest2 = (idx - team_last_date[t2]) - 1
        rest2_str = f"{rest2} ngày"
    else:
        rest2_str = "-"
        
    # update last date
    team_last_date[t1] = idx
    team_last_date[t2] = idx
    
    new_line = f"| {r} | {date_str_full} | {time_str} | {t1} | {t2} | {g} | {rest1_str} | {rest2_str} |\n"
    out_lines.append(new_line)

with open("final_perfect_md.txt", "w") as f:
    f.writelines(out_lines)

