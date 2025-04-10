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



# python3 img_pixels_test.py
# python3 img_pixels_test.py  Test_active_pixel_group_detection.test_active_pixel_group_detection

import unittest, platform, sys, os, time
import img_pixels, img_pixel_select

from unittest.mock import Mock
from unittest.mock import patch
import PIL


def path_abs_to_testfile(pathRelative: str):
    """with absolute path the test """
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), pathRelative)



# python3 img_pixels_test.py  Test_active_pixel_group_detection.test_active_pixel_group_detection
class Test_active_pixel_group_detection(unittest.TestCase):


    def test_active_pixel_group_detection(self):

        imgPath = path_abs_to_testfile("../../samples/sample_abc_lower_ubuntu_light_300_grayscale.png")
        pixelsInImg, _errors, _warnings = img_pixels.pixels_load_from_image(imgPath)

        pixelGroups = img_pixel_select.pixelGroups_active_select(pixelsInImg)

        self.assertTrue(len(pixelGroups) == 28)  # 26 letters + 2 accents


        for group in pixelGroups:
            group.display_in_terminal()

        areaWithAllPixelGroups = img_pixels.matrix_representation_shared_for_more_pixelgroups(pixelGroups)

        img_pixels.pixel_group_matrix_representation_print(areaWithAllPixelGroups)





class FakePixel_channel_2():
    """return with 2 channel information, simulate grayscale + alpha"""
    def __init__(self):
        self.size = (1, 1)

    def getpixel(self, coord=(0,0)):
        """coord is not important, always return with these values"""
        return (1,2)  # return with 0 channel values, which is invalid, minimum 1 is necessary



class TestLoadImageFile(unittest.TestCase):


    def test_load_image_file__check_memory_usage_and_speed_manually(self):
        """manual image load test - native Python is maybe a little slow to read a huge PNG, pixel by pixel"""
        # A4 white based page with 300dpi pixel text
        imgPath = path_abs_to_testfile("../../samples/lorem_ipsum.png")
        if os.path.isfile(imgPath): # big binary file, used only for speed test, don't insert into git
            print(f"this is a large image - to process every pixel, the for loop needs ~8 seconds")

            pixelsInImg, errors, warnings = img_pixels.pixels_load_from_image(imgPath)
            "testResult: only the PNG -> python reading is slow, the in-memory loop is relatively fast, 0.1 sec in the huge lorem ipsum"

            timeStartLoop = time.time()
            for rowNum, row in enumerate(pixelsInImg):
                # print("pixelReadRow:", rowNum)
                for pixelOne in row:
                    pass
            print(f"loop time over pixels: {time.time() - timeStartLoop}")



    def test_load_image_file_incorrect_channel_number(self):
        imgPath = path_abs_to_testfile("../../samples/sample_abc_lower_ubuntu_light_300_grayscale.png")

        with patch("PIL.Image.open") as mocked_fun:
            mocked_fun.return_value = FakePixel_channel_2()

            _pixelsInImg, errors, warnings = img_pixels.pixels_load_from_image(imgPath)
            self.assertTrue(len(warnings) == 1)
            self.assertIn("probably Alpha channel is detected", str(warnings))




    def test_load_image_file_grayscale(self):
        imgPath = path_abs_to_testfile("../../samples/sample_abc_lower_ubuntu_light_300_grayscale.png")
        pixelsInImg, errors, warnings = img_pixels.pixels_load_from_image(imgPath)
        self.assertTrue(len(pixelsInImg[0][0]) == 3)
        self.assertTrue(warnings == list())
        # 3 values are in the pixel, rgb is created from one grayscale value


    def test_load_image_file_rgb(self):
        imgPath = path_abs_to_testfile("../../samples/sample_abc_lower_ubuntu_light_300.png")
        pixelsInImg, errors, warnings = img_pixels.pixels_load_from_image(imgPath)
        print(f"pixel 0, 0:")
        print(pixelsInImg[0][0])  # 3 values are in the pixel
        self.assertTrue(len(pixelsInImg[0][0]) == 3)  # 3 values are in the pixel
        self.assertTrue(warnings == list())


    def test_load_image_file__missing_file(self):
        imgPath = "unknown_file.png"
        pixelsInImg, errors, warnings = img_pixels.pixels_load_from_image(imgPath)
        self.assertTrue(len(errors) == 1)
        self.assertTrue(len(pixelsInImg) == 0)
        self.assertTrue(warnings == list())


if __name__ == '__main__':
    unittest.main()
