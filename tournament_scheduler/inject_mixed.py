with open('schedule_results.md', 'r') as f:
    lines = f.readlines()

start_idx = -1
end_idx = -1
for i, line in enumerate(lines):
    if line.startswith('| 1 | 04/07/2026 (T7) | 14:30 | A3 | A4 | A |'):
        start_idx = i
    if start_idx != -1 and line.startswith('| 5 | 21/07/2026 (T3) | 16:00 | A3 | A5 | A |'):
        end_idx = i
        break

with open('final_mixed_md.txt', 'r') as f:
    new_table_content = f.read()

# Make sure to append the separator logic correctly
new_lines = lines[:start_idx] + [new_table_content] + lines[end_idx+1:]

with open('schedule_results.md', 'w') as f:
    f.writelines(new_lines)

