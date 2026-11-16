#!/usr/bin/env python3
"""Crop source-image assets and create a visual contact sheet for manual crop review.
Requires: Pillow. JSON: {source_image, crops:[{name,box:[l,t,r,b]}]}.
"""
import argparse
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps

def main():
    a=argparse.ArgumentParser()
    a.add_argument('manifest',type=Path)
    a.add_argument('--output',type=Path,default=Path('crop-review.png'))
    a.add_argument('--assets-dir',type=Path,default=Path('crops'))
    args=a.parse_args()
    d=json.loads(args.manifest.read_text(encoding='utf-8'))
    source=Path(d['source_image'])
    if not source.is_absolute():source=(args.manifest.parent/source).resolve()
    im=Image.open(source).convert('RGB')
    W,H=im.size
    args.assets_dir.mkdir(exist_ok=True,parents=True)
    sheet=Image.new('RGB',(max(1000,W),max(380,int(max(1000,W)*H/W))+1000),'white')
    outline=im.copy()
    draw=ImageDraw.Draw(outline)
    cards=[]
    for j,c in enumerate(d['crops'],1):
        name=c['name']; l,t,r,b=map(int,c['box'])
        if not (0<=l<r<=W and 0<=t<b<=H):
            raise ValueError(f'Out-of-range crop {name}: {c["box"]}, source={W}x{H}')
        img=im.crop((l,t,r,b))
        img.save(args.assets_dir/(name+'.png'))
        draw.rectangle((l,t,r,b),outline=(255,0,0),width=3)
        draw.text((l+2,t+2),f'{j}',fill=(255,0,0),stroke_width=2,stroke_fill='white')
        cards.append((name,img))
    sw=sheet.width
    leadH=int(sw*H/W)
    sheet.paste(outline.resize((sw,leadH)),(0,0))
    d2=ImageDraw.Draw(sheet)
    cols=4; pad=10; cw=(sw-pad*(cols+1))//cols; ch=175
    needed=leadH+30+((len(cards)+cols-1)//cols)*ch
    if needed>sheet.height:
        new=Image.new('RGB',(sw,needed),'white');new.paste(sheet,(0,0));sheet=new
    d2=ImageDraw.Draw(sheet)
    for i,(name,img) in enumerate(cards):
        col=i%cols; row=i//cols; x=pad+col*(cw+pad); y=leadH+20+row*ch
        thumb=ImageOps.contain(img,(cw-12,ch-42),method=Image.Resampling.LANCZOS)
        sheet.paste(thumb,(x+(cw-thumb.width)//2,y+12))
        d2.rectangle((x,y,x+cw,y+ch-3),outline=(190,190,190),width=1)
        d2.text((x+4,y+ch-26),f'{i+1}: {name} ({img.width}x{img.height})',fill='black')
    args.output.parent.mkdir(exist_ok=True,parents=True)
    sheet.save(args.output)
    print(f'Wrote {len(cards)} original-ratio crops to {args.assets_dir} and review sheet to {args.output}.')
    print('MANUAL GATE: check every image edge and bottom nodes; passing coordinate checks does NOT guarantee complete visual content.')
if __name__=='__main__':main()
