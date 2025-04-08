#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys, argparse

dirDeepcopyRoot = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(dirDeepcopyRoot, 'src/1_utils'))

import img_pixels


def deepcopy_main(fileList: list[str]):

    for imgPath in fileList:

        pixelsInImg, errors, warnings = img_pixels.pixels_load_from_image(imgPath)

        if warnings:
            print("Warnings:\n", "\n".join(warnings))

        if not errors:

            coords_pixelGroups_Glyphs = img_pixels.pixelGroups_active_select(pixelsInImg)

            print(f"=== Detected pixel groups (glyphs) in file {imgPath} ===")
            for (xGroupPixel, yGroupPixel), group in coords_pixelGroups_Glyphs.items():
                group.display_in_terminal()

                print(f"TODO: detect the text from the glyph")


if __name__ == '__main__':

    parser = argparse.ArgumentParser(prog="deepcopy", description="Recognize text in pixel-based images.")
    parser.add_argument("--imageFilePaths", help="comma separated image files. PNG files are preferred", action='store', required=True)
    Args = parser.parse_args()

    deepcopy_main(Args.imageFilePaths.split(","))
