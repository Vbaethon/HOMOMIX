import os

icon_dir = 'Icon/Color/'
readme_file = 'README.md'

html_header = '\n\n## Preview\n\n'
html_content = '<table><tr>'


columns = 4
col_count = 0

for icon_file in os.listdir(icon_dir):
    if icon_file.endswith(('.png', '.jpg', '.jpeg', '.svg')):
        icon_path = os.path.join(icon_dir, icon_file)
        # 创建单元格，图标和名称
        html_content += f'''
        <td align="center" style="padding: 10px;">
            <img src="{icon_path}" alt="{icon_file}" width="80" height="80"><br>
            <b>{icon_file}</b>
        </td>'''
        col_count += 1

        
        if col_count % columns == 0:
            html_content += '</tr><tr>'


html_content += '</tr></table>'


with open(readme_file, 'r') as f:
    existing_content = f.read()

# 将 HTML 内容添加到 README 文件末尾
with open(readme_file, 'w') as f:
    f.write(existing_content + html_header + html_content)

print("图标表格已成功添加到 README.md 文件末尾。")
