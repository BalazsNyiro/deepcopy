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

import unittest, img_0_pixels, img_1_pixel_select, img_2_pixelgroup_glyph_recognize_preparation_detail_detection


# python3  img_2_pixelgroup_glyph_recognize_preparation_detail_detection_test.py Test_glyph_statistics
class Test_glyph_statistics(unittest.TestCase):

    def test_glyph_stat_collect_enclosed_inactive_unavailable_segments_in_glyph(self):
        testName = "test_glyph_stat_collect_enclosed_inactive_unavailable_segments_in_glyph"
        print(f"test: {testName}")

        txt = """
          .....**....... <- only STARs and DOTs are detected, any other chars are ignored
          ....*..*......
          ...******...**  <- extra active chars, don't belong to the first group
          ..*......*....
          .*........*...
        """

        pixels, errors, warnings = img_0_pixels.pixels_load_from_string(txt, callerPlaceName=testName)
        pixelGroups_Glyphs = img_1_pixel_select.pixelGroups_active_select(pixels)

        pixelGroups_Glyphs[0].matrix_representation_refresh(addExtraEmptyBorderAroundArea=(1,1,1,1))
        img_2_pixelgroup_glyph_recognize_preparation_detail_detection.glyph_stat_collect_enclosed_inactive_unavailable_segments_in_glyph(pixelGroups_Glyphs[0].matrix_representation)


if __name__ == '__main__':
    unittest.main()
