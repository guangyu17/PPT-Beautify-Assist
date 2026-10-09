"""Expand a small set of semantic PPT components into editable slide-local primitives.
All expanded geometry is in inches. This is not a semantic inference engine: supplied
texts, dates, icons and relationships must already be verified against user content.
"""
from copy import deepcopy
import math
from _common import Units


def finite(value):
    result=float(value)
    if not math.isfinite(result):raise ValueError('Geometry must be finite')
    return result


def expand_spec(spec):
    result=deepcopy(spec);u=Units(spec)
    profile=spec.get('studio_profile')
    if profile is not None:
        if profile.get('tier') not in ('ultra','high','medium','low'):
            raise ValueError('studio_profile.tier: ultra/high/medium/low')
        if profile.get('backend') not in ('native','ifapi','relay'):
            raise ValueError('studio_profile.backend: native/ifapi/relay')
    result['units']='in';result['slide_size']={'width':u.sw,'height':u.sh}
    for sn,slide in enumerate(result.get('slides',[]),1):
        output=[];seen=set()
        for index,raw in enumerate(slide.get('elements',[]),1):
            e=deepcopy(raw);kind=e['type']
            if profile is not None and kind=='panel':
                if e.get('material_source')!='generated' or not e.get('texture'):
                    raise ValueError('Studio panels require a real image-generated text-free texture. Native rectangles or blur patches are not a substitute; omit the panel if no generated asset is ready.')
            key=str(e.get('id',f's{sn}-e{index}'))
            if kind=='connector':
                x1,y1,x2,y2=u.x(e['x1']),u.y(e['y1']),u.x(e['x2']),u.y(e['y2'])
                e.update(id=key,x1=x1,y1=y1,x2=x2,y2=y2,x=min(x1,x2),y=min(y1,y2),w=abs(x2-x1),h=abs(y2-y1))
                if not all(math.isfinite(v) for v in (x1,y1,x2,y2)) or math.hypot(x2-x1,y2-y1)<.00001:
                    raise ValueError('Connector must have two distinct finite endpoints')
                if e.get('route','straight') not in ('straight','elbow'):raise ValueError('route: straight or elbow')
                expanded=[e]
            else:
                x,y,w,h=u.box(e);e.update(id=key,x=x,y=y,w=w,h=h)
                if not all(math.isfinite(v) for v in (x,y,w,h)) or w<=0 or h<=0:
                    raise ValueError('Positive finite component dimensions required')
                expanded=expand_component(e) if kind in ('panel','frame','icon_badge','timeline') else [e]
            for child in expanded:
                cid=child['id']
                if cid in seen:raise ValueError('Duplicate expanded element ID: '+cid)
                seen.add(cid);output.append(child)
        slide['elements']=output
    return result


def expand_component(e):
    key=e['id'];x,y,w,h=[e[k] for k in ('x','y','w','h')];kind=e['type'];out=[]
    ink=e.get('color','#254453')
    def shape(suffix,box,shape='rect',fill=None,alpha=1,line=None,**extra):
        a,b,c,d=box
        return dict(id=key+'-'+suffix,type='shape',shape=shape,x=a,y=b,w=c,h=d,fill=fill,alpha=alpha,line=line,**extra)
    def text(suffix,value,box,size=16,**extra):
        a,b,c,d=box
        return dict(id=key+'-'+suffix,type='text',text=str(value),x=a,y=b,w=c,h=d,size=size,
                    color=extra.pop('color',ink),margin=.025,
                    **{name:e[name] for name in ('font','latin_font') if name in e},**extra)
    def connector(suffix,x1,y1,x2,y2,**extra):
        return dict(id=key+'-'+suffix,type='connector',x1=x1,y1=y1,x2=x2,y2=y2,
                    x=min(x1,x2),y=min(y1,y2),w=abs(x2-x1),h=abs(y2-y1),
                    line={'color':ink,'width_pt':e.get('line_width_pt',.8)},**extra)
    if kind in ('panel','frame'):
        geometry=e.get('shape','rounded_rect' if kind=='panel' else 'rect')
        allowed=('rect','rounded_rect','ellipse','snip_round_rect','snip_diag_rect','round_diag_rect')
        if geometry not in allowed:raise ValueError('Unsupported frame/panel shape')
        if kind=='panel':
            material=e.get('material','translucent')
            if material not in ('translucent','acrylic'):raise ValueError('Unknown panel material')
            if e.get('texture'):
                out.append(dict(id=key+'-texture',type='image',path=e['texture'],x=x,y=y,w=w,h=h,
                                fit='contain',radius=e.get('radius',.12)))
            generated=e.get('material_source')=='generated'
            alpha=finite(e.get('alpha',0 if generated else (.3 if material=='acrylic' else .7)))
            if not 0<=alpha<=1:raise ValueError('Panel alpha must be 0..1')
            out.append(shape('surface',(x,y,w,h),geometry,e.get('fill','#FFFFFF'),alpha,
                             ({'color':e.get('line_color','#D5E0E6'),'width_pt':e.get('line_width_pt',.75)}
                              if not generated or 'line_color' in e or 'line_width_pt' in e else None),
                             shadow=bool(e.get('shadow',False))))
            inset=finite(e.get('inset',0 if generated else .04))
            if material=='acrylic' and inset>0:
                if min(w,h)<=2*inset:raise ValueError('Acrylic inset consumes panel')
                out.append(shape('highlight',(x+inset,y+inset,w-2*inset,h-2*inset),geometry,None,
                                 line={'color':e.get('highlight_color','#FFFFFF'),'width_pt':.5,'alpha':.7}))
            if 'text' in e or 'paragraphs' in e:
                pad=finite(e.get('padding',.16))
                if pad<0 or min(w,h)<=2*pad:raise ValueError('Panel padding consumes text area')
                t=text('text',e.get('text',''),(x+pad,y+pad,w-2*pad,h-2*pad),e.get('size',18),
                       role=e.get('role','body'),valign=e.get('valign','top'),bold=bool(e.get('bold',False)))
                if 'paragraphs' in e:t['paragraphs']=deepcopy(e['paragraphs'])
                out.append(t)
        else:
            out.append(shape('outer',(x,y,w,h),geometry,None,line={'color':ink,'width_pt':e.get('line_width_pt',.8)}))
            if e.get('double',False):
                inset=finite(e.get('inset',.045))
                if inset<=0 or min(w,h)<=2*inset:raise ValueError('Invalid double-frame inset')
                out.append(shape('inner',(x+inset,y+inset,w-2*inset,h-2*inset),geometry,None,
                                 line={'color':ink,'width_pt':e.get('inner_width_pt',.4)}))
    elif kind=='icon_badge':
        if abs(w-h)>.01:raise ValueError('Icon badge requires square physical dimensions for a circular ring')
        pad=finite(e.get('padding',.14))
        if pad<0 or w<=2*pad:raise ValueError('Invalid badge padding')
        out.append(shape('ring',(x,y,w,h),'ellipse',e.get('fill'),e.get('alpha',1),
                         {'color':ink,'width_pt':e.get('line_width_pt',.7)}))
        if e.get('path'):
            out.append(dict(id=key+'-icon',type='image',path=e['path'],x=x+pad,y=y+pad,w=w-2*pad,h=h-2*pad,fit='contain'))
        elif e.get('symbol') in ('star4','star8','diamond'):
            out.append(shape('icon',(x+pad,y+pad,w-2*pad,h-2*pad),e['symbol'],ink,line=None))
        else:
            raise ValueError('Provide a verified icon path or supported simple symbol; no empty fake icon')
        if e.get('cardinal_marks',False):
            d=min(.06,w/12)
            for i,(cx,cy) in enumerate(((x+w/2,y),(x+w,y+h/2),(x+w/2,y+h),(x,y+h/2))):
                out.append(shape(f'mark{i}',(cx-d/2,cy-d/2,d,d),'diamond',ink))
    elif kind=='timeline':
        items=e.get('events',[])
        if not isinstance(items,list) or not 2<=len(items)<=12:raise ValueError('timeline: 2..12 verified events required')
        orientation=e.get('orientation','horizontal');spacing=e.get('spacing','sequence')
        if orientation not in ('horizontal','vertical'):raise ValueError('orientation: horizontal or vertical')
        if spacing not in ('sequence','proportional'):raise ValueError('spacing: sequence or proportional')
        if spacing=='proportional':
            times=[finite(i['time']) for i in items]
            if any(a>=b for a,b in zip(times,times[1:])):raise ValueError('Proportional times must be strictly increasing, never silently reordered')
            fractions=[(t-times[0])/(times[-1]-times[0]) for t in times]
        else:fractions=[i/(len(items)-1) for i in range(len(items))]
        radius=finite(e.get('node_radius',.045))
        if not .015<=radius<=.15:raise ValueError('Node radius .015..0.15in')
        if orientation=='horizontal':
            if h<1.1:raise ValueError('Horizontal timeline requires height >=1.1in')
            cell=min(w/len(items),finite(e.get('label_width',w/len(items))))
            if cell<=.15:raise ValueError('Timeline label width too small')
            centers=[x+cell/2+f*(w-cell) for f in fractions];line_y=y+.42
            out.append(connector('axis',centers[0],line_y,centers[-1],line_y))
            for i,(event,cx) in enumerate(zip(items,centers)):
                if 'label' not in event:raise ValueError('Every event requires a source-backed label')
                date=event.get('date')
                if date is not None:out.append(text(f'date{i}',date,(cx-cell/2,y,cell,.3),e.get('date_size',12),align='center',role='caption'))
                out.append(shape(f'node{i}',(cx-radius,line_y-radius,2*radius,2*radius),'ellipse',e.get('node_fill','#FFFFFF'),line={'color':ink,'width_pt':.8}))
                out.append(text(f'label{i}',event['label'],(cx-cell/2,y+.58,cell,.38),e.get('label_size',17),align='center',bold=True))
                if event.get('description'):
                    out.append(text(f'desc{i}',event['description'],(cx-cell/2,y+1.0,cell,h-1.0),e.get('description_size',12),align='center',role='caption'))
        else:
            if w<1:raise ValueError('Vertical timeline requires width >=1in')
            row=h/len(items);centers=[y+row*.25+f*(h-row) for f in fractions];cx=x+.12
            if row<.55:raise ValueError('Vertical timeline rows too short')
            out.append(connector('axis',cx,centers[0],cx,centers[-1]))
            for i,(event,cy) in enumerate(zip(items,centers)):
                if 'label' not in event:raise ValueError('Every event requires a source-backed label')
                out.append(shape(f'node{i}',(cx-radius,cy-radius,2*radius,2*radius),'ellipse',e.get('node_fill','#FFFFFF'),line={'color':ink,'width_pt':.8}))
                ty=cy-row*.25
                if event.get('date') is not None:out.append(text(f'date{i}',event['date'],(x+.35,ty,w-.35,.25),e.get('date_size',12),role='caption'))
                out.append(text(f'label{i}',event['label'],(x+.35,ty+.28,w-.35,.34),e.get('label_size',17),bold=True))
                if event.get('description'):
                    if row<=.75:raise ValueError('Description needs taller vertical rows')
                    out.append(text(f'desc{i}',event['description'],(x+.35,ty+.66,w-.35,row-.68),e.get('description_size',12),role='caption'))
    # No automatic broad overlap exemptions: rendered review must authorize intended layering explicitly.
    for item in out:
        item['_component_id']=key
        if e.get('allow_overlap_with'):item['allow_overlap_with']=list(e['allow_overlap_with'])
    return out


def segment_intersects_box(x1,y1,x2,y2,box):
    """Liang-Barsky clipping for straight-line / visible text-box intersection."""
    x,y,w,h=box;dx=x2-x1;dy=y2-y1;lo,hi=0.,1.
    for p,q in ((-dx,x1-x),(dx,x+w-x1),(-dy,y1-y),(dy,y+h-y1)):
        if abs(p)<1e-12:
            if q<0:return False
        else:
            t=q/p
            if p<0:lo=max(lo,t)
            else:hi=min(hi,t)
            if lo>hi:return False
    return True
