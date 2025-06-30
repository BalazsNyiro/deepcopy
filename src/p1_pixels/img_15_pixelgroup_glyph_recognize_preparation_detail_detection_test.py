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

import unittest, img_10_pixels, img_13_pixel_select, img_15_pixelgroup_glyph_recognize_preparation_detail_detection

# python3  img_15_pixelgroup_glyph_recognize_preparation_detail_detection_test.py Test_glyph_statistics_collect_all
class Test_glyph_statistics_collect_all(unittest.TestCase):
    """give back a global status about the complete collector"""

    def test_glyph_stats_collect_all(self):
        testName = "test_glyph_stats_collect_all"

        txt = """
          ***........**.........****..
          *..*......*..*.......*......
          ****.....*....*......*......
          *...*...********.....*......
          ****...*........*.....****..
        """

        pixels, errors, warnings = img_10_pixels.pixels_load_from_string(txt, callerPlaceName=testName)
        pixelGroups_Glyphs_id_group_dict = img_13_pixel_select.pixelGroups_active_select(pixels)

        stats_pixelGroupId_statNames_values = img_15_pixelgroup_glyph_recognize_preparation_detail_detection.statistics_collect_about_pixelgroups(
            pixelGroups_Glyphs_id_group_dict)

        print("keys in stats:", stats_pixelGroupId_statNames_values.keys())
        self.assertTrue(stats_pixelGroupId_statNames_values[0]["glyph_stat_collect_enclosed_inactive_unavailable_segments_in_glyph"], 2)
        self.assertTrue(stats_pixelGroupId_statNames_values[1]["glyph_stat_collect_enclosed_inactive_unavailable_segments_in_glyph"], 1)
        self.assertTrue(stats_pixelGroupId_statNames_values[2]["glyph_stat_collect_enclosed_inactive_unavailable_segments_in_glyph"], 0)

        for pixelGroupId, statsAll in stats_pixelGroupId_statNames_values.items():
            print(f"\n\n========= pixelGroupId in statistic collector test - {pixelGroupId} =========")
            for statName, stat in statsAll.items():
                print(f"{statName:>10}: {stat}")




# cd src/p1_pixels
# python3  img_15_pixelgroup_glyph_recognize_preparation_detail_detection_test.py Test_glyph_statistics_one_by_one
class Test_glyph_statistics_one_by_one(unittest.TestCase):
    """test one stat collector in one test, to see are they correct or not"""

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

        pixels, errors, warnings = img_10_pixels.pixels_load_from_string(txtB, callerPlaceName=testName)
        print(pixels)
        pixelGroups_Glyphs_id_group_dict = img_13_pixel_select.pixelGroups_active_select(pixels)
        pixelGroups_Glyphs = list(pixelGroups_Glyphs_id_group_dict.values())
        print(pixelGroups_Glyphs[0].pixels)

        print("==== txtB matrix representation in terminal: ======")
        pixelGroups_Glyphs[0].matrix_representation_refresh(addExtraEmptyBorderAroundArea=(1, 1, 1, 1))
        pixelGroups_Glyphs[0].matrix_representation_display_in_terminal(refreshTheMatrix=False)

        print("txtB closed inactive segment detect:")
        enclosedInactiveSegmentsNum, errors = img_15_pixelgroup_glyph_recognize_preparation_detail_detection.glyph_stat_collect_enclosed_inactive_unavailable_segments_in_glyph__emptyBorderHasToBePreparedAroundMatrix(pixelGroups_Glyphs[0])
        self.assertEqual(len(enclosedInactiveSegmentsNum), 2)



if __name__ == '__main__':  # pragma: no cover
    unittest.main()         # pragma: no cover
