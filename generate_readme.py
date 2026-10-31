import os
from pathlib import Path
from icon_aliases import ALIASES, is_hidden_alias

icon_dir = 'Icon/Color/'
readme_file = 'README.md'

start_marker = '<!--start-icons-->'
end_marker = '<!--end-icons-->'

html_header = f'\n\n{start_marker}\n\n## 图标展示\n\n'  
variant_note = '''兼容下载别名：`Zoho_old → Zoho_new`、`Download_2 → Download`、`Niche_Link → Chained_2`、`Twitter → X`、`Link → Chained_2`。默认与 Large 的旧 URL 均保留，展示区和目录只列规范名称。`Claud` 是拼写错误，已删除；请使用 `Claude`。

配色变体说明：bilibili 的粉/蓝/白底、Huawei 红/黑、LinkedIn 明/暗、Bahamut 两色及 Hugging Face 白/绿底保留为同主体的配色选择，不视为不同造型；Link 与 Chained_2 的微小色差也不计作独立样式。Disney 与 Disney_plus 是不同服务，使用各自官网采用的 D 短标与配色。

'''
html_content = variant_note + '<table style="width: 100%; text-align: center;"><tr>'  

columns = 7
col_count = 0


icon_files = [f for f in os.listdir(icon_dir) if f.endswith(('.png', '.jpg', '.jpeg', '.svg'))]
# 统一alias表：保留下载URL，但展示区只列规范名称。
icon_files = [f for f in icon_files if not is_hidden_alias(Path(icon_dir) / f)]
icon_files_sorted = sorted(icon_files, key=lambda x: os.path.splitext(x)[0].lower())  


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
        <img src="{icon_path}" alt="{icon_file}" width="60" height="60"><br>
        <span style="font-size: 8px;">{name_display}</span>
    </td>'''
    col_count += 1

    
    if col_count % columns == 0:
        html_content += '</tr><tr>'


html_content += '</tr></table>'
html_footer = f'\n\n{end_marker}\n\n'


with open(readme_file, 'r') as f:
    readme_content = f.read()


start_idx = readme_content.find(start_marker)
end_idx = readme_content.find(end_marker)


if start_idx != -1 and end_idx != -1:
    new_readme_content = (
        readme_content[:start_idx + len(start_marker)] +  
        '\n\n' + html_content + '\n\n' +                  
        readme_content[end_idx:]                          
    )
else:
    # 如果没有找到标记，默认将新表格插入到文档末尾
    new_readme_content = readme_content + '\n\n' + start_marker + '\n\n' + html_content + '\n\n' + end_marker + '\n\n'

with open(readme_file, 'w') as f:
    f.write(new_readme_content)

print("图标表格已成功更新到 README.md 文件。")
