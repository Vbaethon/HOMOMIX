import os

icon_dir = 'Icon/Color/'
readme_file = 'README.md'

table_header = '\n\n## 图标展示\n\n| 图标名称  | 预览    |\n| -------- | -------- |\n'

table_rows = ""
for icon_file in os.listdir(icon_dir):
    if icon_file.endswith(('.png')):  
        icon_path = os.path.join(icon_dir, icon_file)
        table_rows += f'| {icon_file} | ![{icon_file}]({icon_path}) |\n'

with open(readme_file, 'r') as f:
    existing_content = f.read()

with open(readme_file, 'w') as f:
    f.write(existing_content + table_header + table_rows)

print("图标表格已成功添加到 README.md 文件末尾。")
