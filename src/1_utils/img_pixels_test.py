#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# python3 img_pixels_test.py

import unittest, platform, sys
import img_pixels

from unittest.mock import Mock
from unittest.mock import patch
import PIL

class FakePixel_channel_2():
    """return with 2 channel information, simulate grayscale + alpha"""
    def __init__(self):
        self.size = (1, 1)

    def getpixel(self, coord=(0,0)):
        """coord is not important, always return with these values"""
        return (1,2)  # return with 0 channel values, which is invalid, minimum 1 is necessary



class TestLoadImageFile(unittest.TestCase):

    def test_load_image_file__check_memory_usage(self):
        imgPath = "../../samples/lorem_ipsum.png"

        print(f"this is a large image - to process every pixel, the for loop needs 10+ seconds")
        pixelsInImg, errors, warnings = img_pixels.img_load_pixels(imgPath)


    def test_load_image_file_incorrect_channel_number(self):
        imgPath = "../../samples/sample_abc_lower_ubuntu_light_300_grayscale.png"

        with patch("PIL.Image.open") as mocked_fun:
            mocked_fun.return_value = FakePixel_channel_2()

            pixelsInImg, errors, warnings = img_pixels.img_load_pixels(imgPath)
            self.assertTrue(len(warnings) == 1)
            self.assertIn("probably Alpha channel is detected", str(warnings))




    def test_load_image_file_grayscale(self):
        imgPath = "../../samples/sample_abc_lower_ubuntu_light_300_grayscale.png"
        pixelsInImg, errors, warnings = img_pixels.img_load_pixels(imgPath)
        self.assertTrue(len(pixelsInImg[0][0]) == 3)
        self.assertTrue(warnings == list())
        # 3 values are in the pixel, rgb is created from one grayscale value


    def test_load_image_file_rgb(self):
        imgPath = "../../samples/sample_abc_lower_ubuntu_light_300.png"
        pixelsInImg, errors, warnings = img_pixels.img_load_pixels(imgPath)
        print(f"pixel 0, 0:")
        print(pixelsInImg[0][0])  # 3 values are in the pixel
        self.assertTrue(len(pixelsInImg[0][0]) == 3)  # 3 values are in the pixel
        self.assertTrue(warnings == list())


    def test_load_image_file__missing_file(self):
        imgPath = "unknown_file.png"
        pixelsInImg, errors, warnings = img_pixels.img_load_pixels(imgPath)
        self.assertTrue(len(errors) == 1)
        self.assertTrue(len(pixelsInImg) == 0)
        self.assertTrue(warnings == list())


if __name__ == '__main__':
    unittest.main()
