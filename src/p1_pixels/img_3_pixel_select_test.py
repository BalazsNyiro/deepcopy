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

import unittest
import img_3_pixel_select, img_0_pixels

# python3 img_3_pixel_select_test.py



# python3 img_3_pixel_select_test.py Test_pixelGroups_active_select
class Test_pixelGroups_active_select(unittest.TestCase):

    def test_pixelGroups_active_select(self):
        testName = "test_base1 in test_pixelGroups_active_select"

        txt = """
          .....**....... <- only STARs and DOTs are detected, any other chars are ignored
          ....*..*......
          ...******...**  <- extra active chars, don't belong to the first group
          ..*......*....
          .*........*...
        """

        pixels, errors, warnings = img_0_pixels.pixels_load_from_string(
            txt, callerPlaceName=testName)

        print(pixels)

        pixelGroups_Glyphs_id_group_dict = img_3_pixel_select.pixelGroups_active_select(pixels)
        pixelGroups_Glyphs = list(pixelGroups_Glyphs_id_group_dict.values())

        print(f"=== Detected pixel groups (glyphs),  ===")
        for pixelGroup in pixelGroups_Glyphs:
            pixelGroup.matrix_representation_display_in_terminal()


        print(" are these x,y coords in the detected pixels?")
        for wanted in [(5, 0), ( 6, 0),
                       (4, 1), ( 7, 1),
                       (3, 2), ( 4, 2), (5, 2), (6, 2), (7, 2), (8, 2),
                       (2, 3), ( 9, 3),
                       (1, 4), (10, 4)
                      ]:
            self.assertIn(wanted, pixelGroups_Glyphs[0].pixels )

        self.assertTrue(
            len(pixelGroups_Glyphs[0].pixels) == txt.count("*")-2)


# python3 img_3_pixel_select_test.py  Test_isActive_checkAllSelectors
class Test_isActive_checkAllSelectors(unittest.TestCase):

    def test_isActive_all_selector(self):

        onePixelRgb = (200, 244, 199)  # too bright pixel

        isActive = img_3_pixel_select.isActive_checkAllSelectors(
            onePixelRgb,
            [
                (img_3_pixel_select.pixelGroupSelector_default,
                {"rMax_toSelect": 100, "gMax_toSelect": 100, "bMax_toSelect": 100})
            ] )

        self.assertFalse(isActive)



        isActive = img_3_pixel_select.isActive_checkAllSelectors(
            onePixelRgb,
            [
                (img_3_pixel_select.pixelGroupSelector_default,
                 {"rMax_toSelect": 222, "gMax_toSelect": 222, "bMax_toSelect": 222})
            ] )

        self.assertTrue(isActive)

        ############### separated R, G, B channel selector
        for onePixelRgb in [(0, 255, 255), (255, 0, 255), (255, 255, 0) ]:

            isActive = img_3_pixel_select.isActive_checkAllSelectors(
                onePixelRgb,
                [
                    (img_3_pixel_select.pixelGroupSelector_default,
                     {"rMax_toSelect": 100, "gMax_toSelect": 100, "bMax_toSelect": 100})
                ] )

            self.assertTrue(isActive)


# python3 img_3_pixel_select_test.py
class Test_coords_neighbour(unittest.TestCase):

    def test_find_neighbours_basic(self):

        neighbours = img_3_pixel_select.coords_neighbours(3, 3, 0, 0, 6, 6)
        self.assertTrue(len(neighbours) == 8)

        neighbours = img_3_pixel_select.coords_neighbours(x=3, y=3,
                                                        xMinValidPossibleCoordValue=0, yMinValidPossibleCoordValue=0,
                                                        xMaxValidPossibleCoordValue=6, yMaxValidPossibleCoordValue=6,
                                                        allowedDirections={1}
                                                        )
        self.assertTrue(len(neighbours) == 1)


        neighbours = img_3_pixel_select.coords_neighbours(x=3, y=3,
                                                        xMinValidPossibleCoordValue=0, yMinValidPossibleCoordValue=3,
                                                        xMaxValidPossibleCoordValue=6, yMaxValidPossibleCoordValue=6,
                                                        allowedDirections={1}
                                                        )
        self.assertTrue(len(neighbours) == 0)


        neighbours = img_3_pixel_select.coords_neighbours(x=3, y=3,
                                                        xMinValidPossibleCoordValue=0, yMinValidPossibleCoordValue=3,
                                                        xMaxValidPossibleCoordValue=6, yMaxValidPossibleCoordValue=6
                                                        )
        self.assertTrue(len(neighbours) == 5)


        neighbours = img_3_pixel_select.coords_neighbours(x=3, y=3,
                                                        xMinValidPossibleCoordValue=0, yMinValidPossibleCoordValue=0,
                                                        xMaxValidPossibleCoordValue=3, yMaxValidPossibleCoordValue=3
                                                        )
        self.assertTrue(len(neighbours) == 3)
        self.assertEqual(neighbours, sorted([(3, 2), (2, 3), (2, 2)]))



if __name__ == '__main__':  # pragma: no cover
    unittest.main()         # pragma: no cover
