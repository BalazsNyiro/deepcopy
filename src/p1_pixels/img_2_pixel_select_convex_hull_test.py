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

import unittest, math

import img_0_pixels
import img_2_pixel_select_convex_hull, img_3_pixel_select

# python3 img_2_pixel_select_convex_hull_test.py Test_convex_hull
class Test_convex_hull(unittest.TestCase):

    # python3 img_2_pixel_select_convex_hull_test.py Test_convex_hull.test_convex_hull
    def test_convex_hull(self):
        testName = "test_convex_hull"

        txt = """
          ....***..  
          ....*.*..  
          ..**..*** 
          ..**..*..
        """

        pixels, errors, warnings = img_0_pixels.pixels_load_from_string(txt, callerPlaceName=testName)
        pixelGroups_Glyphs_id_group_dict = img_3_pixel_select.pixelGroups_active_select(pixels)
        pixelGroups_Glyphs = list(pixelGroups_Glyphs_id_group_dict.values())
        pixelGroups_Glyphs[0].matrix_representation_refresh()

        pixelGroups_Glyphs[0].matrix_representation_display_in_terminal()
        img_2_pixel_select_convex_hull.convex_hull_points_collect(pixelGroups_Glyphs[0], {img_0_pixels.pixelsNameForegroundActive})


    # python3 img_2_pixel_select_convex_hull_test.py Test_convex_hull.test_convex_hull_find_next_point_in_hull
    def test_convex_hull_find_next_point_in_hull(self):
        testName = "test_convex_hull_find_next_point_in_hull"
        print(f"Test: {testName}")

        coords: list[tuple(int, int)] = [
                    (2, 0), (3, 0),
            (1, 1), (2, 1), (3, 1),
                    (2, 2)]


        pointStart = (3, 1)

        hullElemNext, _ = img_2_pixel_select_convex_hull.convex_hull_next_elem_detect(pointStart, coords)
        print(f"hullElemNext: {hullElemNext}")

        pointStart = hullElemNext
        hullElemNext, _ = img_2_pixel_select_convex_hull.convex_hull_next_elem_detect(pointStart, coords)
        print(f"hullElemNext: {hullElemNext}")

        pointStart = hullElemNext
        hullElemNext, _ = img_2_pixel_select_convex_hull.convex_hull_next_elem_detect(pointStart, coords)
        print(f"hullElemNext: {hullElemNext}")

        pointStart = hullElemNext
        hullElemNext, _ = img_2_pixel_select_convex_hull.convex_hull_next_elem_detect(pointStart, coords)
        print(f"hullElemNext: {hullElemNext}")



    def test_rad_calc(self):

        testName = "test_rad_calc"
        print(f"Test: {testName}")

        radVal, err = img_2_pixel_select_convex_hull.radian_calculate_with_arctan(0, 0, 0, 0, coordinatesAreScreenZeroZeroInTopLeftRightSystem=False)
        self.assertNotEqual( err, [] )

        radVal_err = img_2_pixel_select_convex_hull.radian_calculate_with_arctan(0, 0, 10, 0, coordinatesAreScreenZeroZeroInTopLeftRightSystem=False)
        self.assertEqual( radVal_err, (0.0, []) )

        radVal_err = img_2_pixel_select_convex_hull.radian_calculate_with_arctan(0, 0, 10, 10, coordinatesAreScreenZeroZeroInTopLeftRightSystem=False)
        self.assertEqual( radVal_err, (math.pi/4, []) )

        radVal_err = img_2_pixel_select_convex_hull.radian_calculate_with_arctan(0, 0, 0, 10, coordinatesAreScreenZeroZeroInTopLeftRightSystem=False)
        self.assertEqual( radVal_err, (math.pi/2, []) )

        radVal_err = img_2_pixel_select_convex_hull.radian_calculate_with_arctan(0, 0, -10, 10, coordinatesAreScreenZeroZeroInTopLeftRightSystem=False)
        self.assertEqual( radVal_err, (3*math.pi/4, []) )

        radVal_err = img_2_pixel_select_convex_hull.radian_calculate_with_arctan(0, 0, -10, 0, coordinatesAreScreenZeroZeroInTopLeftRightSystem=False)
        self.assertEqual( radVal_err, (math.pi, []) )

        radVal_err = img_2_pixel_select_convex_hull.radian_calculate_with_arctan(0, 0, -10, -10, coordinatesAreScreenZeroZeroInTopLeftRightSystem=False)
        self.assertEqual( radVal_err, (5*math.pi/4, []) )

        radVal_err = img_2_pixel_select_convex_hull.radian_calculate_with_arctan(0, 0, 0, -10, coordinatesAreScreenZeroZeroInTopLeftRightSystem=False)
        self.assertEqual( radVal_err, (3*math.pi/2, []) )

        radVal_err = img_2_pixel_select_convex_hull.radian_calculate_with_arctan(0, 0, 10, -10, coordinatesAreScreenZeroZeroInTopLeftRightSystem=False)
        self.assertEqual( radVal_err, (7*math.pi/4, []) )

        radVal_err = img_2_pixel_select_convex_hull.radian_calculate_with_arctan(0, 0, 10, 10,
                                                                                 coordinatesAreScreenZeroZeroInTopLeftRightSystem=True)
        self.assertEqual( radVal_err, (7*math.pi/4, []) )

if __name__ == '__main__':
    unittest.main()
