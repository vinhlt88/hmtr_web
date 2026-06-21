import re
from collections import defaultdict

with open('/Users/vinhluu/vinhluu/hmtr_web/tournament_scheduler/schedule_results.md', 'r') as f:
    content = f.read()

# Extract the group stage table correctly
lines = content.split('\n')
in_table = False
table_lines = []
for line in lines:
    if line.startswith('| Vòng | Ngày'):
        in_table = True
    elif in_table and line.startswith('---'):
        break
    elif in_table and line.startswith('|') and '---' not in line:
        table_lines.append(line)

stats = defaultdict(lambda: {'total': 0, 'match1': 0, 'match2': 0, 'home': 0, 'away': 0, 'weekend': 0})

for line in table_lines:
    if not line.strip(): continue
    cols = [c.strip() for c in line.split('|')]
    if len(cols) < 7: continue
    
    date_str = cols[2]
    time_str = cols[3]
    home_team = cols[4]
    away_team = cols[5]
    
    is_weekend = '(T7)' in date_str or '(CN)' in date_str
    
    # Update Home Team
    stats[home_team]['total'] += 1
    stats[home_team]['home'] += 1
    if time_str == '14:30': stats[home_team]['match1'] += 1
    elif time_str == '16:00': stats[home_team]['match2'] += 1
    if is_weekend: stats[home_team]['weekend'] += 1
        
    # Update Away Team
    stats[away_team]['total'] += 1
    stats[away_team]['away'] += 1
    if time_str == '14:30': stats[away_team]['match1'] += 1
    elif time_str == '16:00': stats[away_team]['match2'] += 1
    if is_weekend: stats[away_team]['weekend'] += 1

print("| Đội | Tổng số trận | Trận 1 (14:30) | Trận 2 (16:00) | Đội nhà | Đội khách | Trận cuối tuần |")
print("|:---:|:---:|:---:|:---:|:---:|:---:|:---:|")
for team in sorted(stats.keys(), key=lambda x: (x[0], int(re.search(r'\d+', x).group()) if re.search(r'\d+', x) else 0)):
    s = stats[team]
    print(f"| **{team}** | {s['total']} | {s['match1']} | {s['match2']} | {s['home']} | {s['away']} | {s['weekend']} |")
