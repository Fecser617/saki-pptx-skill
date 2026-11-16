#!/usr/bin/env python3
"""Side-by-side visual comparison. Never claim this automatically decides visual quality."""
import argparse
from pathlib import Path
from PIL import Image, ImageOps, ImageDraw

def main():
    a=argparse.ArgumentParser()
    a.add_argument('--source',required=True,type=Path)
    a.add_argument('--preview',required=True,type=Path)
    a.add_argument('--output',required=True,type=Path)
    args=a.parse_args()
    src=Image.open(args.source).convert('RGB')
    out=Image.open(args.preview).convert('RGB')
    sideW=max(src.width,out.width,1000)
    sideH=int(max(src.height,out.height)*sideW/max(src.width,out.width))
    box=(sideW,sideH)
    canvas=Image.new('RGB',(sideW*2+60,sideH+90),'white')
    a1=ImageOps.contain(src,box);a2=ImageOps.contain(out,box)
    canvas.paste(a1,((sideW-a1.width)//2,50+(sideH-a1.height)//2))
    canvas.paste(a2,(sideW+60+(sideW-a2.width)//2,50+(sideH-a2.height)//2))
    d=ImageDraw.Draw(canvas)
    d.text((20,20),'SOURCE',fill=(0,0,0));d.text((sideW+80,20),'RENDERED PPT',fill=(0,0,0))
    d.line((sideW+30,0,sideW+30,sideH+90),fill=(90,90,90),width=2)
    args.output.parent.mkdir(parents=True,exist_ok=True);canvas.save(args.output)
    print(f'Comparison at {args.output}; visually inspect original vs rendered, especially crop edges, connectors, labels.')
if __name__=='__main__':main()
