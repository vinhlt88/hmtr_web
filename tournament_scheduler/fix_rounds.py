with open('schedule_results.md', 'r') as f:
    lines = f.readlines()

team_counts = {f"A{i}": 0 for i in range(1, 6)}
new_lines = []

in_table = False
for line in lines:
    if line.startswith('| Vòng | Ngày'):
        in_table = True
        new_lines.append(line)
        continue
    
    if in_table and line.startswith('---'):
        in_table = False
        new_lines.append(line)
        continue
        
    if in_table and line.startswith('|'):
        cols = [c.strip() for c in line.split('|')[1:-1]]
        if len(cols) >= 6:
            r, date_str, time_str, t1, t2, g = cols[:6]
            if g == 'A':
                team_counts[t1] += 1
                team_counts[t2] += 1
                avg = (team_counts[t1] + team_counts[t2]) / 2.0
                if avg.is_integer():
                    r_str = str(int(avg))
                else:
                    r_str = str(avg)
                
                cols[0] = r_str
                # rebuild line
                new_line = "| " + " | ".join(cols) + " |\n"
                new_lines.append(new_line)
                continue
    
    new_lines.append(line)

with open('schedule_results.md', 'w') as f:
    f.writelines(new_lines)

print("Fixed A rounds")
