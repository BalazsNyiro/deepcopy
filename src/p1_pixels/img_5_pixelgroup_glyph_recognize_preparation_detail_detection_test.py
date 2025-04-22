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

import unittest, img_0_pixels, img_3_pixel_select, img_5_pixelgroup_glyph_recognize_preparation_detail_detection


# python3  img_5_pixelgroup_glyph_recognize_preparation_detail_detection_test.py Test_glyph_statistics
class Test_glyph_statistics(unittest.TestCase):

    def test_glyph_stat_collect_enclosed_inactive_unavailable_segments_in_glyph(self):
        testName = "test_glyph_stat_collect_enclosed_inactive_unavailable_segments_in_glyph"
        print(f"test: {testName}")


        txtB = """
          ***..
          *..*.
          ****.
          *...*
          ****.
        """

        pixels, errors, warnings = img_0_pixels.pixels_load_from_string(txtB, callerPlaceName=testName)
        print(pixels)
        pixelGroups_Glyphs_id_group_dict = img_3_pixel_select.pixelGroups_active_select(pixels)
        pixelGroups_Glyphs = list(pixelGroups_Glyphs_id_group_dict.values())
        print(pixelGroups_Glyphs[0].pixels)

        print("txtB matrix representation:")
        pixelGroups_Glyphs[0].matrix_representation_refresh(addExtraEmptyBorderAroundArea=(1,1,1,1))
        print("=========")
        print(pixelGroups_Glyphs[0].matrix_representation)
        print("=========")
        pixelGroups_Glyphs[0].matrix_representation_display_in_terminal(refreshTheMatrix=False)

        print("txtB closed inactive segment detect:")
        enclosedInactiveSegmentsNum, errors = img_5_pixelgroup_glyph_recognize_preparation_detail_detection.glyph_stat_collect_enclosed_inactive_unavailable_segments_in_glyph__emptyBorderHasToBePreparedAroundMatrix(pixelGroups_Glyphs[0])
        self.assertEqual(len(enclosedInactiveSegmentsNum), 2)



if __name__ == '__main__':  # pragma: no cover
    unittest.main()         # pragma: no cover
