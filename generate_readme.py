import os

# 图标文件夹路径
icon_dir = 'assets/icons/'
# README 文件路径
readme_file = 'README.md'

# 定义标记，用于标识表格的起始和结束位置
start_marker = '<!--start-icons-->'
end_marker = '<!--end-icons-->'

# 生成 HTML 格式
html_header = f'\n\n{start_marker}\n\n## Preview\n\n'
html_content = '<table><tr>'

# 列数（每行显示几列）
columns = 4
col_count = 0

# 生成图标 HTML
for icon_file in os.listdir(icon_dir):
    if icon_file.endswith(('.png', '.jpg', '.jpeg', '.svg')):
        icon_path = os.path.join(icon_dir, icon_file)
        
        # 去除文件后缀名
        name_without_extension = os.path.splitext(icon_file)[0]

        # 处理名称，如果长度超过 10 个字符，则使用省略号
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

# 读取现有的 README 文件内容
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
