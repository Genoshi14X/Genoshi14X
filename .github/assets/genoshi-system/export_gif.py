#!/usr/bin/env python3
"""Build a looping GIF from the preview's exported JSON. Requires Pillow."""
import argparse, base64, io, json
from pathlib import Path
from PIL import Image

def encode(images, destination, fps=10):
    # One shared palette avoids color flicker; no dithering keeps flat UI small.
    sheet=Image.new('RGB',(images[0].width,images[0].height*len(images[::10])))
    for i,im in enumerate(images[::10]): sheet.paste(im,(0,i*im.height))
    palette=sheet.quantize(colors=48,method=Image.Quantize.MEDIANCUT)
    frames=[im.quantize(palette=palette,dither=Image.Dither.NONE) for im in images]
    frames[0].save(destination,save_all=True,append_images=frames[1:],duration=round(1000/fps),loop=0,optimize=True,disposal=1)

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('frames',type=Path)
    parser.add_argument('-o','--output',default='genoshi-system.gif')
    args=parser.parse_args()
    data=json.loads(args.frames.read_text())
    images=[Image.open(io.BytesIO(base64.b64decode(frame))).convert('RGB') for frame in data['frames']]
    encode(images,args.output,data['fps'])
    print(f'Saved {args.output}: {Path(args.output).stat().st_size / 1024:.0f} KiB')
