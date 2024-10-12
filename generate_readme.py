import os


icon_dir = 'Icon/Color/'
readme_file = 'README.md'

start_marker = '<!--start-icons-->'
end_marker = '<!--end-icons-->'

html_header = f'\n\n{start_marker}\n\n## 图标展示\n\n'
html_content = '''
<div style="display: flex; flex-wrap: wrap; justify-content: space-around;">
'''  # 使用 flex 布局，自动适应宽度

# 获取并排序图标文件
icon_files = [f for f in os.listdir(icon_dir) if f.endswith(('.png', '.jpg', '.jpeg', '.svg'))]
icon_files_sorted = sorted(icon_files, key=lambda x: os.path.splitext(x)[0].lower())  # 根据名称排序，忽略大小写

# 生成图标 HTML
for icon_file in icon_files_sorted:
    icon_path = os.path.join(icon_dir, icon_file)
    
    # 去除文件后缀名
    name_without_extension = os.path.splitext(icon_file)[0]

    # 处理名称，如果长度超过 10 个字符，则使用省略号
    if len(name_without_extension) > 10:
        name_display = name_without_extension[:10] + '...'
    else:
        name_display = name_without_extension
    
    print(f"Processing icon: {icon_file} -> Display name: {name_display}")  # 调试输出
    
    
    html_content += f'''
    <div style="flex: 0 0 30%; text-align: center; margin: 10px;">
        <img src="{icon_path}" alt="{icon_file}" width="100" height="100"><br>
        <span style="font-size: 8px;">{name_display}</span>
    </div>'''

# 关闭 Flexbox div
html_content += '</div>'
html_footer = f'\n\n{end_marker}\n'

# 读取现有的 README 文件内容
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
    
    new_readme_content = readme_content + html_header + html_content + html_footer


with open(readme_file, 'w') as f:
    f.write(new_readme_content)

print("图标展示已成功更新到 README.md 文件。")
