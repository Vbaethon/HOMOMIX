import os

icon_dir = 'Icon/Color/'
readme_file = 'README.md'

start_marker = '<!--start-icons-->'
end_marker = '<!--end-icons-->'

html_header = f'\n\n{start_marker}\n\n## Preview\n\n'
html_content = '<table><tr>'

columns = 4
col_count = 0

for icon_file in os.listdir(icon_dir):
    if icon_file.endswith(('.png', '.jpg', '.jpeg', '.svg')):
        icon_path = os.path.join(icon_dir, icon_file)
        
        html_content += f'''
        <td align="center" style="padding: 10px;">
            <img src="{icon_path}" alt="{icon_file}" width="60" height="60"><br>
            <span style="font-size: 6px;">{icon_file}</span>
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
    new_readme_content = (
        readme_content[:start_idx + len(start_marker)] +
        html_header + html_content + html_footer +
        readme_content[end_idx:]
    )

else:
    new_re
    adme_content = readme_content + html_header + html_content + html_footer

with open(readme_file, 'w') as f:
    f.write(new_readme_content)

print("图标表格已成功更新到 README.md 文件。")
