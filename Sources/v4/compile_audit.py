"""Build exhaustive path coverage from the independently reviewed evidence rows."""
from pathlib import Path
import json,collections
R=Path(__file__).resolve().parent;P=R.parents[1]
def read(p):return json.loads(p.read_text())
def main():
    evidence={}
    for f in ['a-m.json','n-z.json','supplement.json','a-m-supplement.json','claude-supplement.json']:
        if not (R/'audit-inputs'/f).exists():continue
        for row in read(R/'audit-inputs'/f)['rows']:evidence[row['name']]=row
    ai={'ChatGPT':('https://openai.com/brand/','官方Blossom结绳形状对应，保留。'), 'Claud':('https://www.anthropic.com/legal/trademark-guidelines','Claude兼容别名。放射花形可辨，精确官方素材取得受限，保留不猜。'), 'Claude':('https://www.anthropic.com/legal/trademark-guidelines','放射花形可辨，精确官方素材取得受限，保留不猜。'), 'Microsoft_Copilot':('https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks','官方彩带基本形对应，保留。'), 'Perplexity':('https://www.perplexity.ai/favicon.svg','官方线框几何对应，保留黑底变体。'), 'Hugging_face':('https://huggingface.co/brand','官方拥抱笑脸形状对应，保留。'), 'Hugging_face_g':('https://huggingface.co/brand','官方拥抱笑脸形状对应，保留项目绿色背景变体。')}
    generic=set((P/'Sources/v3/generic-names.txt').read_text().split())
    changes={'Panda','Panda_ai','Load_balancing_2','Load_balancing_3'}
    corrected={'AdblockPlus_2','Microsoft','Disney_Channel','UBISOFT','Peacook','Scholar'}
    resampled={'Disney','Disney_plus'}
    new={a['name']:a for a in read(R/'AI-OFFICIAL-SOURCES.json')['assets'] if a['name'] in {'Grok','Gemini','DeepSeek'}}
    items=[]
    defaults=sorted((P/'Icon/Color').glob('*.png'),key=lambda p:p.stem.casefold())
    for f in defaults+sorted((P/'Icon/Color/FDS').glob('*.png')):
        n=f.stem if f.parent.name!='FDS' else 'FDS/'+f.stem
        paths=[f.relative_to(P).as_posix()]
        if f.parent.name!='FDS':
            large=next(x for x in (P/'Icon/Color/Large').glob('*.png') if x.name.casefold()==f.name.casefold());paths.append(large.relative_to(P).as_posix())
        e=evidence.get(n,{})
        status=e.get('status','非品牌类别，不适用');note=e.get('note',e.get('visual_observation','原创功能图形、地域图案或已命名主题，不冒充官方服务标识。'));source=e.get('source',e.get('official_source'))
        if n in ai:source,note=ai[n];status='无法完全确认' if n in {'Claude','Claud'} else '已正确'
        if n in {'Claude','Claud'} and n in evidence and '已正确' in evidence[n]['status']:
            status=evidence[n]['status'];note=evidence[n]['note'];source=evidence[n]['source']
        if n in generic:status='原创已修正' if n in changes else '非品牌类别，不适用';source=None;note='原创通用图形，无官方商标可替换。'+('本轮熊猫解剖/负载均衡构图修正。' if n in changes else '')
        if n in corrected:status='已修正为官方标识';note+=' 本轮使用确证官方素材适配，未手绘替代。'
        if n in resampled:status='官方compact忠实重采样';note='单独D具有官方compact来源，原先不是因缺少完整字标而错误。本轮改用确证源，保留几何/颜色；Disney公司暖白背景铺满圆形，Disney+透明SVG用白盘。';source='https://thewaltdisneycompany.com/' if n=='Disney' else 'https://www.disneyplus.com/'
        if n in new:status='新增官方标识';source=new[n]['source'];note=new[n]['note']
        if n in {'AI','AI_bot','AI_Tree','AI_voice'}:status='非品牌类别，不适用'
        category='未完全确认' if '确认' in status else ('官方已修正' if n in corrected else ('官方新增' if n in new else ('官方重采样' if n in resampled else ('原创修正' if n in changes else ('非品牌' if '不适用' in status or '通用' in status or '地域' in status or '角色' in status else '官方形状已对应')))))
        items.append({'name':n,'paths':paths,'status':status,'category':category,'finding':note,'official_source':source,'action':'updated' if n in corrected|resampled|changes else ('added' if n in new else 'retained')})
    counts=dict(collections.Counter(x['category'] for x in items))
    data={'checked_at':'2026-10-31','scope':'All default icons, matching Large paths, Claud compatibility alias, and both FDS variants. Identity/geometry audit, not trademark licensing clearance or proof of original historical byte provenance.','counts':counts,'items':items}
    (R/'OFFICIAL-AUDIT.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    lines=['# HOMOMIX 全量官方标识审查','', '本清单记录已验证构建，发布状态以Git提交为准。覆盖所有默认/Large路径、Claud别名和FDS两款；官方身份核验不等于商标使用许可。','', '分类统计：'+ '；'.join(f'{k} {v}' for k,v in counts.items())+'。','', '## 逐项结果','']
    for row in items:
        lines += [f"- **{row['name']} · {row['status']}**：{row['finding']}" + (f" [官方来源]({row['official_source']})" if row['official_source'] else '')]
    (R/'OFFICIAL-AUDIT.md').write_text('\n'.join(lines)+'\n')
    print(len(items),counts)
if __name__=='__main__':main()
