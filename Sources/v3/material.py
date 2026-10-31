"""Centered soft inner edging; unchanged right-down diffuse cast and disk shadows."""
def filters(graphite=False,inner=True):
 innerparts=''
 merge='<feMergeNode in="cast"/><feMergeNode in="SourceGraphic"/>'
 if inner:
  innerparts='<feGaussianBlur in="SourceAlpha" stdDeviation="2.6" result="depthBlur"/><feComposite in="SourceAlpha" in2="depthBlur" operator="out" result="depthEdge"/><feFlood flood-color="#071623" flood-opacity=".12"/><feComposite in2="depthEdge" operator="in" result="depth"/><feGaussianBlur in="SourceAlpha" stdDeviation="1.1" result="lightBlur"/><feComposite in="SourceAlpha" in2="lightBlur" operator="out" result="lightEdge"/><feFlood flood-color="#FFFFFF" flood-opacity=".03"/><feComposite in2="lightEdge" operator="in" result="light"/>'
  merge+='<feMergeNode in="depth"/><feMergeNode in="light"/>'
 return f'''<filter id="diskShadow" x="-.1" y="-.1" width="1.2" height="1.2" color-interpolation-filters="sRGB"><feDropShadow dx="0" dy=".5" stdDeviation="2.5" flood-color="#172338" flood-opacity=".035"/></filter><filter id="inkFinish" x="-.25" y="-.25" width="1.5" height="1.5" color-interpolation-filters="sRGB"><feGaussianBlur in="SourceAlpha" stdDeviation="13" result="castBlur"/><feOffset in="castBlur" dx="7" dy="11" result="castOffset"/><feFlood flood-color="#102333" flood-opacity=".115"/><feComposite in2="castOffset" operator="in" result="cast"/>{innerparts}<feMerge>{merge}</feMerge></filter>'''
