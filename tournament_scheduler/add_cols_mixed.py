import re
from datetime import datetime

with open('mixed_md.txt', 'r') as f:
    table_lines = f.readlines()

last_played = {}
new_table_lines = []

for line in table_lines:
    if not line.strip() or not line.startswith('|'):
        continue
    cols = [col.strip() for col in line.split('|')[1:-1]]
    if len(cols) < 6: continue
    
    round_no, date_str, time_str, home, away, group = cols[:6]
    
    # parse date
    date_part = date_str.split(' ')[0] # 04/07/2026
    dt = datetime.strptime(date_part, '%d/%m/%Y')
    
    rest_home = "-"
    if home in last_played:
        delta = (dt - last_played[home]).days - 1
        rest_home = f"{delta} ngày"
    last_played[home] = dt
    
    rest_away = "-"
    if away in last_played:
        delta = (dt - last_played[away]).days - 1
        rest_away = f"{delta} ngày"
    last_played[away] = dt
    
    new_line = f"| {round_no} | {date_str} | {time_str} | {home} | {away} | {group} | {rest_home} | {rest_away} |\n"
    new_table_lines.append(new_line)

with open('final_mixed_md.txt', 'w') as f:
    f.write("".join(new_table_lines))
