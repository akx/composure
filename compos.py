"""
Composite *.tif image sequences from several directories into a single PNG image sequence.
"""
import argparse
import glob
import os
from itertools import zip_longest

from PIL import Image


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", dest="dir", action="append")
    ap.add_argument("-o", dest="out_dir", required=True)
    args = ap.parse_args()
    print(args)
    files_by_dir = [sorted(glob.glob(os.path.join(dir, "*.tif"))) for dir in args.dir]
    for i, files in enumerate(zip_longest(*files_by_dir)):
        files = list(files)
        bg = files.pop(0)
        bg_img = Image.open(bg).convert("RGBA")
        for fg in files:
            fg_img = Image.open(fg).convert("RGBA")
            bg_img.alpha_composite(fg_img)
        filename = os.path.join(args.out_dir, f"frame{i:08d}.png")
        print(i, filename)
        bg_img.save(filename)


if __name__ == "__main__":
    main()
