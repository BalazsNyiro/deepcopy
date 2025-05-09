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
sys.path.extend([os.path.join(dirDeepcopyRoot, 'src/p0_base'), os.path.join(dirDeepcopyRoot, 'src/p1_pixels')])
print(f"sys.path: {sys.path}")

import img_10_pixels, img_13_pixel_select
import img_15_pixelgroup_glyph_recognize_preparation_detail_detection


def deepcopy_main(fileList: list[str]):

    for imgPath in fileList:

        pixelsInImg, errors, warnings = img_10_pixels.pixels_load_from_image(imgPath)

        if warnings:
            print("Warnings:\n", "\n".join(warnings))

        if not errors:

            pixelGroups_Glyphs_all = img_13_pixel_select.pixelGroups_active_select(pixelsInImg)

            print(f"=== Detected pixel groups (glyphs) in file {imgPath} ===")
            #for groupId, group in pixelGroups_Glyphs_all.items():
            #    group.matrix_representation_display_in_terminal()

            stats = img_15_pixelgroup_glyph_recognize_preparation_detail_detection.statistics_collect_about_pixelgroups(pixelGroups_Glyphs_all)
            #print("pixelgroup statistics")
            #for pixelGroupId, statOut in stats.items():
            #    pixelGroups_Glyphs_all[pixelGroupId].matrix_representation_display_in_terminal()
            #    print(pixelGroupId, statOut)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(prog="deepcopy", description="Recognize text in pixel-based images.")
    parser.add_argument("--imageFilePaths", help="comma separated image files. PNG files are preferred",
                        action='store', required=False, default="samples/lorem_ipsum_small.png")
    Args = parser.parse_args()

    deepcopy_main(Args.imageFilePaths.split(","))
