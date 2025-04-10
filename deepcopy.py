#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2025 Balazs Nyiro
# All rights reserved.

# This source code (all file in this repo)
# is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Please read the complete LICENSE file
# in the root directory of this source tree.

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
