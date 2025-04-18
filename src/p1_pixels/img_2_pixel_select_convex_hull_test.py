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
import img_2_pixel_select_convex_hull

# python3 img_2_pixel_select_convex_hull_test.py Test_convex_hull
class Test_convex_hull(unittest.TestCase):

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
