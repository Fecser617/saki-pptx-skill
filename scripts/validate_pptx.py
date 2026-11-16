#!/usr/bin/env python3
"""Validate basic PPTX object, image ratio and manifest requirements.
Requires: python-pptx, Pillow
"""
import argparse
from io import BytesIO
import json
from pathlib import Path
import sys
from PIL import Image
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE

def process(path, manifest, ratio_tol):
    p = Presentation(path)
    W,H = p.slide_width,p.slide_height
    errors=[]; warnings=[]; records=[]
    texts=[]; pic_n=0; txt_n=0
    for si, slide in enumerate(p.slides,1):
        for idx,s in enumerate(slide.shapes,1):
            name=f'P{si} #{idx} {s.name}'
            # Connectors may legally have zero width or height, but no shape may be out of slide.
            if s.left < -10000 or s.top < -10000 or s.left+s.width>W+10000 or s.top+s.height>H+10000:
                errors.append(f'{name}: object outside slide boundary')
            if s.has_text_frame and s.text.strip():
                texts.append(s.text)
                txt_n+=1
            if s.shape_type == MSO_SHAPE_TYPE.PICTURE:
                pic_n +=1
                try:
                    with Image.open(BytesIO(s.image.blob)) as im:
                        iw,ih=im.size
                    visible_w=iw*(1-s.crop_left-s.crop_right)
                    visible_h=ih*(1-s.crop_top-s.crop_bottom)
                    if visible_w <=0 or visible_h <=0 or s.height<=0:
                        errors.append(f'{name}: invalid visible crop or target size')
                    else:
                        original_ratio=visible_w/visible_h
                        display_ratio=s.width/s.height
                        relative_error=abs(display_ratio/original_ratio - 1)
                        records.append({'name':name,'intrinsic_px':[iw,ih], 'display_ratio':round(display_ratio,5),'visible_source_ratio':round(original_ratio,5),'ratio_error_pct':round(relative_error*100,3)})
                        if relative_error > ratio_tol:
                            errors.append(f'{name}: image aspect ratio distortion {relative_error*100:.2f}% > {ratio_tol*100:.2f}%')
                except Exception as exc:
                    warnings.append(f'{name}: unable to inspect image: {exc}')
    full_text='\n'.join(texts)
    if manifest:
        exp_count=manifest.get('expected_slide_count')
        if exp_count is not None and len(p.slides)!=int(exp_count):
            errors.append(f'slide count {len(p.slides)} != expected {exp_count}')
        for key in ['expected_title']:
            t=str(manifest.get(key) or '').strip()
            if t and not t.startswith('<') and t not in full_text:
                errors.append(f'missing required native PPT text ({key}): {t}')
        for t in manifest.get('required_text',[]):
            if t and not str(t).startswith('<') and t not in full_text:
                errors.append(f'missing required native PPT text: {t}')
        if pic_n < int(manifest.get('min_picture_objects',0)):
            errors.append(f'picture count {pic_n} below min')
        if txt_n < int(manifest.get('min_text_shapes',0)):
            errors.append(f'native nonempty text object count {txt_n} below min')
    if pic_n==0:
        warnings.append('No picture objects. Verify whether this is expected for this particular source diagram.')
    return {'file':str(path),'slides':len(p.slides),'picture_objects':pic_n,'text_objects':txt_n,'image_checks':records,'errors':errors,'warnings':warnings,'manual_visual_checks_required':['original crop completeness','diagram technical relations','rendered text overlap','old source labels duplicated','unmodified region regression']}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('pptx',type=Path)
    ap.add_argument('--manifest',type=Path)
    ap.add_argument('--ratio-tolerance',type=float,default=0.01,help='fraction, default 0.01=1%%')
    ap.add_argument('--json-report',type=Path)
    args=ap.parse_args()
    manifest=json.loads(args.manifest.read_text(encoding='utf8')) if args.manifest else None
    result=process(args.pptx,manifest,args.ratio_tolerance)
    print(json.dumps(result,ensure_ascii=False,indent=2))
    if args.json_report: args.json_report.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
    return 2 if result['errors'] else 0
if __name__=='__main__': sys.exit(main())
