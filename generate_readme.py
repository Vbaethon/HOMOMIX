import os

icon_dir = 'Icon/Color/'
readme_file = 'README.md'


start_marker = '<!--start-icons-->'
end_marker = '<!--end-icons-->'


html_header = f'\n\n{start_marker}\n\n## Preview\n\n'
html_content = '<table style="width: 100%; max-width: 800px; margin: auto;"><tr>'


columns = 6
col_count = 0

# 生成图标 HTML
for icon_file in os.listdir(icon_dir):
    if icon_file.endswith(('.png', '.jpg', '.jpeg', '.svg')):
        icon_path = os.path.join(icon_dir, icon_file)
        
        
        name_without_extension = os.path.splitext(icon_file)[0]

        
        if len(name_without_extension) > 10:
            name_display = name_without_extension[:10] + '...'
        else:
            name_display = name_without_extension
        
        print(f"Processing icon: {icon_file} -> Display name: {name_display}")  # 调试输出
        
        # 创建单元格，图标和名称
        html_content += f'''
        <td align="center" style="padding: 10px;">
            <img src="{icon_path}" alt="{icon_file}" width="60" height="60"><br>
            <span style="font-size: 8px;">{name_display}</span>
        </td>'''
        col_count += 1

        if col_count % columns == 0:
            html_content += '</tr><tr>'

# 关闭表格标签
html_content += '</tr></table>'
html_footer = f'\n\n{end_marker}\n'


with open(readme_file, 'r') as f:
    readme_content = f.read()

# 查找标记的起始和结束位置
start_idx = readme_content.find(start_marker)
end_idx = readme_content.find(end_marker)

if start_idx != -1 and end_idx != -1:
    # 替换标记之间的内容
    new_readme_content = (
        readme_content[:start_idx + len(start_marker)] +
        html_header + html_content + html_footer +
        readme_content[end_idx:]
    )
else:
    # 如果没有找到标记，默认将新表格插入到文档末尾
    new_readme_content = readme_content + html_header + html_content + html_footer

# 将更新后的内容写回 README 文件
with open(readme_file, 'w') as f:
    f.write(new_readme_content)

print("图标表格已成功更新到 README.md 文件。")
