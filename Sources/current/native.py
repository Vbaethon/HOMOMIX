#!/usr/bin/env python3
"""Deterministic optical pass. Native subject-only transforms; legacy complete
artwork uniform sampling with original white background extended only where
needed. No anisotropic stretching, recoloring or invented brand outlines.
"""
from pathlib import Path
import argparse,json,hashlib,subprocess,tempfile,sys,io,copy
import xml.etree.ElementTree as E
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent; REPO=R.parents[1]
NS='http://www.w3.org/2000/svg';E.register_namespace('',NS)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def transform(s):return f'translate(180 180) scale({s}) translate(-180 -180)'
def native(name,s):
 src=R/'assets/native-baseline'/f'{name}.svg'
 if not src.exists():return None
 raw=src.read_text()
 # Optional explicit animal geometry revision, leaving material filters intact.
 if name in {'Fish','Fish_b','Dolphin','Globefish'} and (R/'animal_redesign.py').exists():
  import author_sources
  import importlib.util
  spec=importlib.util.spec_from_file_location('animal',R/'animal_redesign.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
  original=author_sources.parts
  def parts(n):
   defs,body=original(n);return m.adjust(n,defs,body)
  author_sources.parts=parts
  raw=author_sources.svg(name);author_sources.parts=original
  s=1.0 # redesign authored directly to final optical target
 root=E.fromstring(raw)
 mask=next((e for e in root.iter() if e.attrib.get('id')=='subjectMask'),None)
 if mask is not None:
  group=E.Element(f'{{{NS}}}g',{'transform':transform(s)})
  for child in list(mask):mask.remove(child);group.append(child)
  mask.append(group) # filters do NOT scale, remain exact native 2.6/13 etc.
 else:
  fg=next((e for e in root.iter() if e.attrib.get('id')=='optical-foreground'),None)
  if fg is not None:fg.set('transform',transform(s)+' '+fg.attrib.get('transform',''))
  else:
   outer=next(e for e in list(root) if e.tag.endswith('g'))
   art=[e for e in list(outer) if not e.tag.endswith('circle')]
   group=E.Element(f'{{{NS}}}g',{'id':'optical-subject','transform':transform(s)})
   for child in art:outer.remove(child);group.append(child)
   outer.append(group)
 return E.tostring(root,encoding='unicode'),src.relative_to(REPO).as_posix()
