"""Generate complete, accessible, unambiguous icon labels without renaming URLs."""
from html import escape
from pathlib import Path
from icon_aliases import is_hidden_alias
from icon_metadata import metadata_for

START_MARKER = '<!--start-icons-->'
END_MARKER = '<!--end-icons-->'

variant_note = '''兼容下载别名：`Zoho_old → Zoho_new`、`Download_2 → Download`、`Niche_Link → Chained_2`、`Twitter → X`、`Link → Chained_2`。默认与 Large 的旧 URL 均保留，展示区和目录只列规范名称。`Claud` 是拼写错误，已删除；请使用 `Claude`。

三个系列入口：[等高版 Color](Icon/Color) · [放大版 Large](Icon/Color/Large) · [FDS 版（未完成）](Icon/Color/FDS/README.md)。FDS 保留现有 [Netflix](Icon/Color/FDS/Netflix.png)、[YouTube](Icon/Color/FDS/YouTube.png)，不混入下方完整系列目录。

配色变体说明：bilibili 的粉/蓝/白底、Huawei 红/黑、LinkedIn 明/暗、Bahamut 两色及 Hugging Face 白/绿底保留为同主体的配色选择，不视为不同造型；Link 与 Chained_2 的微小色差也不计作独立样式。Disney 与 Disney_plus 是不同服务，使用各自官网采用的 D 短标与配色。

'''

def build_gallery(repo_root=Path('.')):
    root = Path(repo_root)
    icon_dir = root / 'Icon/Color'
    files = sorted((p for p in icon_dir.iterdir()
                    if p.suffix.lower() in {'.png', '.jpg', '.jpeg', '.svg'}
                    and not is_hidden_alias(p)), key=lambda p: (p.stem.lower(), p.name))
    content = [variant_note, '显示名称完整保留；点击图标打开原图，点击「Large」查看大尺寸。文件名与旧下载 URL 不变。官方长细标请配合标签使用，不人为拉伸。\n\n', '<table>']
    columns = 5
    for index, path in enumerate(files):
        if index % columns == 0:
            content.append('<tr>')
        rel = path.relative_to(root).as_posix()
        meta = metadata_for(path.stem)
        label = meta['display_name']
        title = label + ' · ' + path.name
        if meta.get('small_size_note'):
            title += ' · ' + meta['small_size_note']
        large = path.parent / 'Large' / ('Bilibili.png' if path.name == 'bilibili.png' else path.name)
        links = f'<a href="{escape(rel, quote=True)}"><img src="{escape(rel, quote=True)}" alt="{escape(label, quote=True)}" title="{escape(title, quote=True)}" width="60" height="60"></a>'
        if large.exists():
            large_link = f'<br><a href="{escape(large.relative_to(root).as_posix(), quote=True)}">Large</a>'
        else:
            large_link = ''
        note = '<br><small>细标：建议配合标签</small>' if meta.get('small_size_note') else ''
        content.append(f'<td align="center">{links}<br><strong>{escape(label)}</strong><br><code>{escape(path.name)}</code>{large_link}{note}</td>')
        if index % columns == columns - 1 or index == len(files) - 1:
            content.append('</tr>')
    content.append('</table>')
    return '\n'.join(content)

def write_readme(repo_root=Path('.')):
    root = Path(repo_root)
    path = root / 'README.md'
    text = path.read_text(encoding='utf-8')
    gallery = '\n\n' + build_gallery(root) + '\n\n'
    if START_MARKER in text and END_MARKER in text:
        start = text.index(START_MARKER) + len(START_MARKER)
        end = text.index(END_MARKER, start)
        text = text[:start] + gallery + text[end:]
    else:
        text += '\n\n' + START_MARKER + gallery + END_MARKER + '\n'
    path.write_text(text, encoding='utf-8')

if __name__ == '__main__':
    write_readme()
    print('README gallery updated with full display names.')
