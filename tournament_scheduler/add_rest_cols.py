import re
from datetime import datetime

with open('schedule_results.md', 'r') as f:
    lines = f.readlines()

table_start = -1
table_end = -1
for i, line in enumerate(lines):
    if line.startswith('| Vòng | Ngày | Giờ | Đội Nhà | Đội Khách | Bảng |'):
        table_start = i
    elif table_start != -1 and line.strip() == '' and table_end == -1:
        table_end = i

if table_end == -1:
    table_end = len(lines)

table_lines = lines[table_start:table_end]

# Parse matches and calculate rest days
last_played = {}
new_table_lines = []

header = "| Vòng | Ngày | Giờ | Đội Nhà | Đội Khách | Bảng | Nghỉ (Nhà) | Nghỉ (Khách) |\n"
separator = "|:---:|---|---|:---:|:---:|:---:|:---:|:---:|\n"
new_table_lines.append(header)
new_table_lines.append(separator)

for line in table_lines[2:]:
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

print("".join(new_table_lines))
