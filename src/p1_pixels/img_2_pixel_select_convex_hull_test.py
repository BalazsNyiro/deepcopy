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

        def get_hull_points(txt, testName):
            pixels, errors, warnings = img_0_pixels.pixels_load_from_string(txt, callerPlaceName=testName)
            pixelGroups_Glyphs_id_group_dict = img_3_pixel_select.pixelGroups_active_select(pixels)
            pixelGroups_Glyphs = list(pixelGroups_Glyphs_id_group_dict.values())
            pixelGroups_Glyphs[0].matrix_representation_refresh()

            pixelGroups_Glyphs[0].matrix_representation_display_in_terminal()
            convexHullPoints, errorsHull = img_2_pixel_select_convex_hull.convex_hull_points_collect(
                pixelGroups_Glyphs[0], {img_0_pixels.pixelsNameForegroundActive})

            print(f"Test: {testName}, convex hull points: {convexHullPoints}")
            return convexHullPoints

        txt = """
          ....***..  
          ....*.*..  
          ..**..*** 
          ..**..*..
        """
        convexHullPoints = get_hull_points(txt, testName)
        self.assertEqual(convexHullPoints, [(4, 3), (6, 2), (4, 0), (2, 0), (0, 2), (0, 3), (1, 3), (4, 3)])


        txt = """
          .**.**.  
          .*****.  
          .**.**. 
          .*...*.
        """
        convexHullPoints = get_hull_points(txt, testName)
        self.assertEqual(convexHullPoints, [(4, 3), (4, 0), (0, 0), (0, 1), (0, 2), (0, 3), (4, 3)])


        txt = """
          .............*............
          ....*........*........*...
          ....*........*........*...
          ....****.....**********...
          ....*........*............
          **************************
          ....*........*.....*......
          ....*........*...***......
          ....*........*............
          ....*........*............
          ....*........*............
          ....*.....................
        """
        convexHullPoints = get_hull_points(txt, testName)
        self.assertEqual(convexHullPoints, [(4, 11), (13, 10), (25, 5), (22, 1), (13, 0), (4, 1), (0, 5), (4, 11)])



    # python3 img_2_pixel_select_convex_hull_test.py Test_convex_hull.test_convex_hull_find_next_point_in_hull
    def test_convex_hull_find_next_point_in_hull(self):
        testName = "test_convex_hull_find_next_point_in_hull"
        print(f"Test: {testName}")

        coords: list[tuple(int, int)] = [
                    (2, 0), (3, 0),
            (1, 1), (2, 1), (3, 1),
            (1, 2), (2, 2)]


        pointStart = (3, 1)
        radianLastSelected = 0.0

        hullElemNext, radianLastSelected, minimumOneElemDetected, _ = img_2_pixel_select_convex_hull.convex_hull_next_elem_detect(pointStart, coords, radianLastSelected)
        print(f"hullElemNext 1: {hullElemNext} minimumOneSelected: {minimumOneElemDetected}")
        self.assertEqual(hullElemNext, (3, 0))
        self.assertTrue(minimumOneElemDetected)

        pointStart = hullElemNext
        hullElemNext, radianLastSelected, minimumOneElemDetected, _ = img_2_pixel_select_convex_hull.convex_hull_next_elem_detect(pointStart, coords, radianLastSelected)
        print(f"hullElemNext 2: {hullElemNext} minimumOneSelected: {minimumOneElemDetected}")
        self.assertEqual(hullElemNext, (2, 0))
        self.assertTrue(minimumOneElemDetected)

        pointStart = hullElemNext
        hullElemNext, radianLastSelected, minimumOneElemDetected, _ = img_2_pixel_select_convex_hull.convex_hull_next_elem_detect(pointStart, coords, radianLastSelected)
        print(f"hullElemNext 3: {hullElemNext} minimumOneSelected: {minimumOneElemDetected}")
        self.assertEqual(hullElemNext, (1, 1))
        self.assertTrue(minimumOneElemDetected)

        pointStart = hullElemNext
        hullElemNext, radianLastSelected, minimumOneElemDetected, _ = img_2_pixel_select_convex_hull.convex_hull_next_elem_detect(pointStart, coords, radianLastSelected)
        print(f"hullElemNext 4: {hullElemNext} minimumOneSelected: {minimumOneElemDetected}")
        self.assertEqual(hullElemNext, (1, 2))
        self.assertTrue(minimumOneElemDetected)

        pointStart = hullElemNext
        hullElemNext, radianLastSelected, minimumOneElemDetected, _ = img_2_pixel_select_convex_hull.convex_hull_next_elem_detect(pointStart, coords, radianLastSelected)
        print(f"hullElemNext 5: {hullElemNext} minimumOneSelected: {minimumOneElemDetected}")
        self.assertEqual(hullElemNext, (2, 2))
        self.assertTrue(minimumOneElemDetected)

        pointStart = hullElemNext
        hullElemNext, radianLastSelected, minimumOneElemDetected, errors = img_2_pixel_select_convex_hull.convex_hull_next_elem_detect(pointStart, coords, radianLastSelected)
        print(f"hullElemNext 6: {hullElemNext} {errors} minimumOneSelected: {minimumOneElemDetected}")
        self.assertFalse(minimumOneElemDetected)

    def test_convex_hull_find_next_point_in_hull_specials(self):
        testName = "test_convex_hull_find_next_point_in_hull_specials"
        print(f"Test: {testName}")

        coords = [ (2, 0) ]
        pointStart = (2, 0)

        # special case, there is only one elem, so the answer is
        # the start point again
        hullElemNext, errors = img_2_pixel_select_convex_hull.convex_hull_next_elem_detect(pointStart, coords)
        print(f"hullElemNext: {hullElemNext}")
        self.assertEqual(hullElemNext, pointStart)
        self.assertTrue(len(errors) == 0)

        ########## generate error: no coords, intentionally
        coords = []
        pointStart = (2, 0)

        # special case, no avaialbe coord
        hullElemNext, errors = img_2_pixel_select_convex_hull.convex_hull_next_elem_detect(pointStart, coords)
        print(f"hullElemNext: {hullElemNext}")
        self.assertTrue(len(errors) > 0)

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
