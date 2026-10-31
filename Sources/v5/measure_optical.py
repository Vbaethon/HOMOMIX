#!/usr/bin/env python3
"""Read-only optical measurements; NEVER writes Icon/Color or source SVGs.

Run: python Sources/v5/measure_optical.py --output-dir /tmp/optical-audit
Pillow + numpy; existing v3 resvg renderer enables source-alpha extraction.
Geometry is a QA cue, not an instruction to equalize all logo areas.
"""
from __future__ import annotations
import argparse, concurrent.futures, copy, hashlib, io, json, math, subprocess, tempfile
from pathlib import Path
import xml.etree.ElementTree as ET
import numpy as np
from PIL import Image, ImageDraw, ImageFont
ROOT=Path(__file__).resolve().parents[2]
ICONROOT=ROOT/'Icon/Color'
FLAGS=set('China China_Taipei European_Union Hong_Kong Japan North_Korea Palestine Singapore South_Korea Taiwan_Province UK USA'.split())
FULL=set('Yin_Yang Olympics'.split())
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def metrics(weights):
    w=np.asarray(weights,dtype=float); total=float(w.sum()); mask=w>=.15; y,x=np.nonzero(mask)
    if not total or not len(x):return {'bbox':None,'area_px':0,'coverage':0,'centroid':None,'centroid_offset':None,'bbox_occupancy':None}
    yy,xx=np.indices(w.shape);cx=float(((xx+.5)*w).sum()/total);cy=float(((yy+.5)*w).sum()/total)
    box=[int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)]
    return {'bbox':box,'area_px':round(total,3),'coverage':round(total/(math.pi*(min(w.shape)/2)**2),4),'centroid':[round(cx,3),round(cy,3)],'centroid_offset':[round(cx-w.shape[1]/2,3),round(cy-w.shape[0]/2,3)],'bbox_occupancy':[round((box[2]-box[0])/w.shape[1],4),round((box[3]-box[1])/w.shape[0],4)]}
def source_mask(name,tmp):
    source=next((ROOT/'Sources'/v/'svg'/(name+'.svg') for v in ['v5','v4','v3'] if (ROOT/'Sources'/v/'svg'/(name+'.svg')).exists()),None)
    if source is None:return None,None,None
    tree=ET.fromstring(source.read_bytes()); removed=0
    for parent in tree.iter():
        for child in list(parent):
            if child.attrib.get('id')=='white-base' or (child.tag.endswith('circle') and child.attrib.get('filter')=='url(#diskShadow)'):
                parent.remove(child);removed+=1
    if not removed:return None,str(source.relative_to(ROOT)),'No separable white plate in source'
    # Subject styling stays intact except the collection's decorative finish.
    for el in tree.iter():
        if el.attrib.get('filter')=='url(#inkFinish)':del el.attrib['filter']
    sp=Path(tmp)/(name+'.svg');out=Path(tmp)/(name+'.png');sp.write_bytes(ET.tostring(tree))
    try:
        subprocess.run(['node',str(ROOT/'Sources/v3/render.cjs'),str(sp),str(out)],check=True,capture_output=True,timeout=30)
        im=Image.open(out).convert('RGBA').resize((360,360),Image.Resampling.LANCZOS)
        return np.asarray(im.getchannel('A'),dtype=float)/255,str(source.relative_to(ROOT)),None
    except Exception as e:return None,str(source.relative_to(ROOT)),type(e).__name__+': '+str(e)[:120]
def background_segment(body):
    a=np.asarray(body.convert('RGBA'),float);rgb=a[:,:,:3];alpha=a[:,:,3]/255;n=body.width
    yy,xx=np.indices((n,n));x=(xx+.5-n/2)/(n/2);y=(yy+.5-n/2)/(n/2);r=np.sqrt(x*x+y*y)
    ring=(r>.80)&(r<.91)&(alpha>.90)
    if ring.sum()<12:return np.zeros((n,n)),np.zeros((n,n)),{'model':'unavailable','residual':255,'spread':255}
    colors=rgb[ring];median=np.median(colors,axis=0);spread=float(np.percentile(np.linalg.norm(colors-median,axis=1),80))
    # Robust edge samples reject foreground touching the outer ring. Smooth
    # background fitting is intentionally marked heuristic, never exact.
    if spread<18:
        bg=np.broadcast_to(median,rgb.shape);kind='constant_edge_median';res=float(np.median(np.linalg.norm(colors-median,axis=1)))
    else:
        basis=np.stack([np.ones_like(x),x,y,x*x,x*y,y*y],axis=-1);X=basis[ring];Y=colors;keep=np.ones(len(Y),bool)
        for _ in range(3):
            coef=np.linalg.lstsq(X[keep],Y[keep],rcond=None)[0];err=np.linalg.norm(Y-X@coef,axis=1);keep=err<=max(8,float(np.percentile(err,75)))
        bg=np.clip(basis@coef,0,255);res=float(np.percentile(np.linalg.norm(Y-X@coef,axis=1),75));kind='quadratic_edge_fit'
    diff=np.linalg.norm(rgb-bg,axis=2);weights=np.clip((diff-25)/65,0,1)*alpha*(r<.96)
    contrast=np.clip(diff/255,0,1)*alpha*(weights>.05)
    return weights,contrast,{'model':kind,'residual':round(res,2),'spread':round(spread,2),'background_rgb':np.median(bg[ring],axis=0).round(1).tolist()}
def measure(name, tmp):
    sm,source,error=source_mask(name,tmp);rows=[];diagnostics=[]
    for scale in ['default','Large']:
        folder=ICONROOT/('' if scale=='default' else 'Large');path=folder/(name+'.png')
        if not path.exists():
            matches=[p for p in folder.glob('*.png') if p.stem.casefold()==name.casefold()]
            if len(matches)==1:path=matches[0]
        logical_path='Icon/Color/'+('Large/' if scale=='Large' else '')+path.name
        if not path.exists():
            rows.append({'name':name,'size':scale,'path':logical_path,'status':'missing_size_variant','confidence':'unavailable'});continue
        im=Image.open(path).convert('RGBA')
        # Plate bounds are for normalization only, explicitly not foreground.
        solid=np.asarray(im.getchannel('A'))>=128;ys,xs=np.nonzero(solid)
        if not len(xs):raise ValueError('Empty icon '+str(path))
        bbox=[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)]
        expected=180 if scale=='default' else 360
        # Preserve analytic collection body normalization despite 175r plate.
        if im.size==((300,300) if scale=='default' else (360,360)):
            box=[60,60,240,240] if scale=='default' else [0,0,360,360]
        else:
            c=((bbox[0]+bbox[2])/2,(bbox[1]+bbox[3])/2);s=max(bbox[2]-bbox[0],bbox[3]-bbox[1]);box=[round(c[0]-s/2),round(c[1]-s/2),round(c[0]+s/2),round(c[1]+s/2)]
        body=im.crop(box);seg,contrast,bg=background_segment(body);notes=[]
        if sm is not None:
            w=np.asarray(Image.fromarray((sm*255).astype('uint8')).resize(body.size,Image.Resampling.LANCZOS),float)/255
            method='source_alpha_without_plate_or_collection_shadow';confidence='high';category='separable_svg_subject'
            # Contrast uses actual production pixels, never the source preview.
            contrast=contrast*(w>.02)
            visible_support=float((w*(seg>.15)).sum()/max(w.sum(),1))
            geom=metrics(w);actual=metrics(seg)
            bounds_delta=max(abs(a-b) for a,b in zip(geom['bbox'],actual['bbox']))/body.width if geom['bbox'] and actual['bbox'] else 1
            if visible_support<.60:
                confidence='low';category='source_has_low_contrast_or_embedded_plate'
                notes.append('Source alpha includes low-contrast/white material or an embedded plate; visible support '+str(round(visible_support,3))+'. Use contrast mask/manual review, not alpha area alone.')
            if bounds_delta>.07:
                confidence='low';category='source_vs_export_disagreement'
                notes.append('Source geometry and exported contrast bounds differ by '+str(round(bounds_delta*100,1))+'% of body. Production may have a later transform; source alpha is not an exact current-export measurement.')
        else:
            w=seg;method=bg['model'];confidence='medium' if bg['model']=='constant_edge_median' and bg['residual']<12 else 'low';category='legacy_flat_background' if confidence=='medium' else 'legacy_complex_background'
        if name in FLAGS:category='flag_full_bleed';confidence='low';notes.append('Flag design: no uniquely separable central foreground; numerical mask is a contrast proxy only.')
        if name in FULL:category='multicomponent_or_full_bleed';confidence='low';notes.append('Semantic subject includes multiple regions; manual interpretation required.')
        m=metrics(w)
        if m['coverage']>.70:confidence='low';notes.append('High coverage: foreground/background distinction may be ill-posed.')
        if m['coverage']<.025:confidence='low';notes.append('Very little extracted foreground; potential segmentation failure or very thin symbol.')
        if source and error:notes.append('Source fallback: '+error)
        if sm is None and bg['model']=='quadratic_edge_fit':notes.append('Smooth gradient fitted from edge; central background can be mistaken for foreground.')
        c=metrics(contrast);small=body.resize((36,36),Image.Resampling.LANCZOS);smallw=np.asarray(Image.fromarray((w*255).astype('uint8')).resize((36,36),Image.Resampling.LANCZOS),float)/255
        smallseg,smallcontrast,smallbg=background_segment(small);actual36=metrics(smallw);actual36['contrast_centroid']=metrics(smallcontrast*(smallw>.02))['centroid'];actual36['visible_core_pixels']=int((smallw>.75).sum());actual36['soft_edge_pixels']=int(((smallw>.15)&(smallw<.75)).sum())
        row={'name':name,'size':scale,'path':logical_path,'input_path':str(path),'sha256':sha(path),'image_dimensions':list(im.size),'plate_bbox_alpha128':bbox,'normalization_body_box':box,'source':source,'classification':category,'method':method,'confidence':confidence,'foreground':m,'export_contrast_foreground':metrics(seg),'contrast_centroid':c['centroid'],'contrast_centroid_offset':c['centroid_offset'],'background_model':bg,'actual36':actual36,'manual_review_reasons':notes}
        # Translate body-relative foreground box/centroids to exported canvas.
        row['foreground_canvas_bbox']=None if m['bbox'] is None else [m['bbox'][0]+box[0],m['bbox'][1]+box[1],m['bbox'][2]+box[0],m['bbox'][3]+box[1]]
        rows.append(row)
        if scale=='default':diagnostics=[small,Image.fromarray((smallw*255).astype('uint8')),row]
    return rows,diagnostics

def main():
    global ROOT, ICONROOT
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output-dir',required=True,type=Path)
    p.add_argument('--jobs',type=int,default=4)
    p.add_argument('--repo',type=Path,default=ROOT,help='Repository containing Sources; default script repository')
    p.add_argument('--icon-root',type=Path,help='Alternate Icon/Color directory, or export directory containing Icon/Color')
    args=p.parse_args();ROOT=args.repo.resolve();ICONROOT=(args.icon_root.resolve() if args.icon_root else ROOT/'Icon/Color')
    if (ICONROOT/'Icon/Color').is_dir():ICONROOT=ICONROOT/'Icon/Color'
    out=args.output_dir.resolve()
    if out==ICONROOT or ICONROOT in out.parents or out==ROOT/'Icon' or ROOT/'Icon' in out.parents:raise ValueError('Output directory cannot be production Icon tree')
    out.mkdir(parents=True,exist_ok=True);names=sorted(p.stem for p in ICONROOT.glob('*.png'))
    paths=[p for p in ICONROOT.rglob('*.png')];before={str(p):sha(p) for p in paths}
    with tempfile.TemporaryDirectory(prefix='homomix-optical-') as tmp:
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as pool:results=list(pool.map(lambda n:measure(n,tmp),names))
    rows=[r for a,_ in results for r in a];review=[r['name'] for r in rows if r['size']=='default' and r['confidence']=='low']
    report={'schema':1,'read_only':True,'source_repo':str(ROOT),'icon_root':str(ICONROOT),'names':len(names),'png_measured':sum('foreground' in r for r in rows),'missing_variants':[r['path'] for r in rows if r.get('status')=='missing_size_variant'],'definitions':{'coverage':'Soft foreground area divided by analytic circular body area, NOT all-image alpha area.','centroid':'Alpha-weighted (SVG) or edge-background-difference weighted (legacy), body pixel coordinates.','contrast_centroid':'Actual exported pixel contrast against inferred background, auxiliary optical cue.','36px':'Full circular icon body reduced to 36px (default 300px canvas at60px has180px body at36px).','limitations':'SVG alpha is exact geometry without collection shadows but not perceived optical weight. Legacy extraction is heuristic. Flags/full-bleed/low-confidence rows must not drive automatic normalization. Preserve shape-specific optical correction.'},'manual_segmentation_review':review,'rows':rows}
    (out/'optical-measurements.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    cols=6;cw=195;ch=78;sheet=Image.new('RGB',(cols*cw,math.ceil(len(results)/cols)*ch),'#ededed');draw=ImageDraw.Draw(sheet)
    for i,(_,diag) in enumerate(results):
        small,mask,row=diag;x=(i%cols)*cw;y=(i//cols)*ch;sheet.paste(small,(x+8,y+23),small);sheet.paste(mask.convert('RGB'),(x+55,y+23));draw.text((x+8,y+5),row['name'][:27],fill='black');draw.text((x+99,y+24),row['confidence'],fill='#aa3333' if row['confidence']=='low' else '#333333');draw.text((x+99,y+40),'area '+str(round(row['foreground']['coverage']*100,1))+'%',fill='#333333');draw.text((x+8,y+62),'36px actual | mask',fill='#555555')
    sheet.save(out/'optical-36px-contact.png')
    changed=[s for s,h in before.items() if sha(Path(s))!=h]
    if changed:raise RuntimeError('Production was modified concurrently: '+str(changed))
    print(json.dumps({'names':len(names),'png_measured':sum('foreground' in r for r in rows),'missing_variants':[r['path'] for r in rows if r.get('status')=='missing_size_variant'],'manual_review':len(review),'production_unchanged':True,'output':str(out)}))
if __name__=='__main__':main()
