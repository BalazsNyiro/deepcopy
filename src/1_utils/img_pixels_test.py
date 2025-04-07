#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# python3 img_pixels_test.py

import unittest, platform
import img_pixels


class TestLoadImageFile(unittest.TestCase):

    def test_load_image_file(self):
        imgPath = "../../samples/sample_abc_lower_ubuntu_light_300.png"
        pixelsInImg = img_pixels.img_load_pixels(imgPath)
        print(pixelsInImg)



if __name__ == '__main__':
    unittest.main()
