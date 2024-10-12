import os


icon_dir = 'Icon/Color/'
readme_file = 'README.md'

# 定义标记，用于标识表格的起始和结束位置
start_marker = '<!--start-icons-->'
end_marker = '<!--end-icons-->'


html_header = f'\n\n{start_marker}\n\n## 图标展示\n\n'
html_content = '''
<div style="display: flex; flex-wrap: wrap; justify-content: space-around;"


columns = 6
col_count = 0


icon_files = [f for f in os.listdir(icon_dir) if f.endswith(('.png', '.jpg', '.jpeg', '.svg'))]
icon_files_sorted = sorted(icon_files, key=lambda x: os.path.splitext(x)[0].lower())  # 根据名称排序，忽略大小写

# 生成图标 HTML
for icon_file in icon_files_sorted:
    icon_path = os.path.join(icon_dir, icon_file)
    
    
    name_without_extension = os.path.splitext(icon_file)[0]

   
    if len(name_without_extension) > 10:
        name_display = name_without_extension[:10] + '...'
    else:
        name_display = name_without_extension
    
    print(f"Processing icon: {icon_file} -> Display name: {name_display}")  # 调试输出
    
    
    html_content += f'''
    <td align="center" style="padding: 10px;">
        <img src="{icon_path}" alt="{icon_file}" width="100" height="100"><br>
        <span style="font-size: 8px;">{name_display}</span>
    </td>'''
    col_count += 1

   
    if col_count % columns == 0:
        html_content += '</tr><tr>'


html_content += '</tr></table>'
html_footer = f'\n\n{end_marker}\n'


with open(readme_file, 'r') as f:
    readme_content = f.read()


start_idx = readme_content.find(start_marker)
end_idx = readme_content.find(end_marker)


if start_idx != -1 and end_idx != -1:
    print("Found markers, updating table content.")
    new_readme_content = (
        readme_content[:start_idx + len(start_marker)] +  # 开始标记及之前的内容
        html_header + html_content + html_footer +  # 新的 HTML 表格
        readme_content[end_idx:]  # 结束标记及之后的内容
    )
else:
    
    print("Markers not found, adding table to the end of README.")
    new_readme_content = readme_content + html_header + html_content + html_footer


with open(readme_file, 'w') as f:
    f.write(new_readme_content)

print("图标表格已成功更新到 README.md 文件。")
