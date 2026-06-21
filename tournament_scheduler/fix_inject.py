with open('schedule_results.md', 'r') as f:
    lines = f.readlines()

with open('final_perfect_md.txt', 'r') as f:
    new_table_content = f.read()

start_idx = -1
end_idx = -1
for i, line in enumerate(lines):
    if line.startswith('| Vòng | Ngày | Giờ | Đội Nhà |'):
        start_idx = i + 2
    if start_idx != -1 and i > start_idx and line.startswith('---'):
        end_idx = i - 1
        break

if start_idx != -1 and end_idx != -1:
    new_lines = lines[:start_idx] + [new_table_content] + lines[end_idx:]
    with open('schedule_results.md', 'w') as f:
        f.writelines(new_lines)
    print("Injected successfully!")
else:
    print(f"Failed! start={start_idx}, end={end_idx}")
