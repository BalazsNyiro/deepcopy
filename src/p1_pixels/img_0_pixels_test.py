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



# python3 img_0_pixels_test.py
# python3 img_0_pixels_test.py  Test_active_pixel_group_detection.test_active_pixel_group_detection

import unittest, platform, sys, os, time
import img_0_pixels, img_3_pixel_select

from unittest.mock import Mock
from unittest.mock import patch
import PIL


def path_abs_to_testfile(pathRelative: str):
    """with absolute path the test """
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), pathRelative)


# python3 img_0_pixels_test.py Test_pixelgroup_matrix_repr_select_corner
class Test_pixelgroup_matrix_repr_select_corner(unittest.TestCase):

    def test_select_top_left_coord(self):
        testName = "select_corner_coord_in_matrix_representation"

        # two left empty column are NOT in matrix representation!
        # so as a human, the top-left is (2, 0)
        txt = """
          .........  
          ....*.*..  
          ...*.**..  
          ..*....*. 
          ..*****..
          .........
        """

        pixels, errors, warnings = img_0_pixels.pixels_load_from_string(txt, callerPlaceName=testName)
        pixelGroups_Glyphs_id_group_dict = img_3_pixel_select.pixelGroups_active_select(pixels)
        pixelGroups_Glyphs = list(pixelGroups_Glyphs_id_group_dict.values())

        pixelGroups_Glyphs[0].matrix_representation_refresh()
        pixelGroups_Glyphs[0].matrix_representation_display_in_terminal(refreshTheMatrix=False)

        coordSelected, _err = img_0_pixels.pixelgroup_matrix_repr_select_corner_coord(
            pixelGroups_Glyphs[0], wantedCorner=("top", "left"))
        print(f"topLeft relative coord: {coordSelected}")
        self.assertEqual(coordSelected, [(2, 0)])

        emptyGrp = img_0_pixels.PixelGroup_Glyph()
        coordSelected, err = img_0_pixels.pixelgroup_matrix_repr_select_corner_coord(emptyGrp)
        self.assertEqual(err, ["ERROR in '' no rows in matrix representation"])

        emptyGrp.matrix_representation = [[]]
        coordSelected, err = img_0_pixels.pixelgroup_matrix_repr_select_corner_coord(emptyGrp)
        self.assertEqual(err, ["ERROR in '' missing characters in matrix row in a representation (the row is empty)"])



        #### ABS top-left:
        coordSelected, _err = img_0_pixels.pixelgroup_matrix_repr_select_corner_coord(
            pixelGroups_Glyphs[0], wantedCorner=("top", "left"), wantedCoordType="absInPage")
        print(f"topLeft absolute coord: {coordSelected}")
        self.assertEqual(coordSelected, [(4, 1)])

        #### ABS top-right:
        coordSelected, _err = img_0_pixels.pixelgroup_matrix_repr_select_corner_coord(
            pixelGroups_Glyphs[0], wantedCorner=("top", "right"), wantedCoordType="absInPage")
        print(f"topRight absolute coord: {coordSelected}")
        self.assertEqual(coordSelected, [(6, 1)])

        #### ABS bottom-left:
        coordSelected, _err = img_0_pixels.pixelgroup_matrix_repr_select_corner_coord(
            pixelGroups_Glyphs[0], wantedCorner=("bottom", "left"), wantedCoordType="absInPage")
        print(f"bottomLeft absolute coord: {coordSelected}")
        self.assertEqual(coordSelected, [(2, 4)])

        #### ABS bottom-right:
        coordSelected, _err = img_0_pixels.pixelgroup_matrix_repr_select_corner_coord(
            pixelGroups_Glyphs[0], wantedCorner=("bottom", "right"), wantedCoordType="absInPage")
        print(f"bottomRight absolute coord: {coordSelected}")
        self.assertEqual(coordSelected, [(6, 4)])

        #### REL bottom-right:
        coord, _err = img_0_pixels.pixelgroup_matrix_repr_select_corner_coord(
            pixelGroups_Glyphs[0], wantedCorner=("bottom", "right"), wantedCoordType="relativeInMatrix")
        print(f"bottomRight rel coord: {coord}")
        self.assertEqual(coord, [(4, 3)])



        # no selection
        coordSelected, _err = img_0_pixels.pixelgroup_matrix_repr_select_corner_coord(
            pixelGroups_Glyphs[0], wantedCorner=("top", "left"),
            wantedCoordType="absInPage", wantedRepresentedNames={"unknown"}
        )
        self.assertEqual(coordSelected, [])

# python3 img_0_pixels_test.py  Test_drop_group_collector
class Test_drop_group_collector(unittest.TestCase):
    """connected pixels detection"""

    def test_drop_collector_simple(self):

        testName = "test_drop_collector_simple"
        print(f"Test: {testName}")

        txt = """
          ************
          ***........*     Dot/ by default the {1,3,5,7} directions
          **.*********    Dot/ cannot detect this diagonal
          *.*........*   Dot/
          *.*.******.*
          *.*......*.*
          *.********.*
          *..........*
          ************
        """

        pixels, errors, warnings = img_0_pixels.pixels_load_from_string(txt, callerPlaceName=testName)
        pixelGroups_Glyphs_id_group_dict = img_3_pixel_select.pixelGroups_active_select(pixels)
        pixelGroups_Glyphs = list(pixelGroups_Glyphs_id_group_dict.values())

        pixelGroups_Glyphs[0].matrix_representation_refresh()


        # {1, 3, 5, 7}: can detect horzontal or vertical connections,
        # so diagonal is not detected
        emptyGroup = img_3_pixel_select.coords_drop_collect_pixelgroups_from_starting_point(
            pixelGroups_Glyphs[0].matrix_representation,
            allowedDirections={1, 3, 5, 7},
            wantedRepresentedPixelGroupNames={img_0_pixels.pixelsNameBackgroundInactive},
            xStartInMatrix=3, yStartInMatrix=1
        )

        emptyGroup.matrix_representation_display_in_terminal()
        self.assertTrue(len(emptyGroup.pixels) == 8)

        # detect all way:
        """
        total * 41, . 29 
                       1
              1234567890
           1: ..********
           2: .*........
           3: *.********
           4: *.*......*
           5: *.******.*
           6: *........*
           7: **********
        """
        emptyGroup = img_3_pixel_select.coords_drop_collect_pixelgroups_from_starting_point(
            pixelGroups_Glyphs[0].matrix_representation,
            allowedDirections={1, 2, 3, 4, 5, 6, 7, 8},
            wantedRepresentedPixelGroupNames={img_0_pixels.pixelsNameBackgroundInactive},
            xStartInMatrix=3, yStartInMatrix=1
        )

        emptyGroup.matrix_representation_display_in_terminal()
        self.assertTrue(len(emptyGroup.pixels) == 41)


        ###### only special directions are allowed:
        """
        total * 7, . 14 
              123
           1: ..*
           2: .*.
           3: *..
           4: *..
           5: *..
           6: *..
           7: *..
        """
        emptyGroup = img_3_pixel_select.coords_drop_collect_pixelgroups_from_starting_point(
            pixelGroups_Glyphs[0].matrix_representation,
            allowedDirections={5, 6},
            wantedRepresentedPixelGroupNames={img_0_pixels.pixelsNameBackgroundInactive},
            xStartInMatrix=3, yStartInMatrix=1
        )

        emptyGroup.matrix_representation_display_in_terminal()
        self.assertTrue(len(emptyGroup.pixels) == 7)


# python3 img_0_pixels_test.py Test_collect_relative_matrix_coords
class Test_collect_relative_matrix_coords(unittest.TestCase):

    def test_collect_relative_matrix_coords(self):
        testName = "test_active_pixel_group_detection"
        print(f"Test: {testName}")

        txt = """
          ....
          ..*.
          .***
          ..*.
        """

        pixels, errors, warnings = img_0_pixels.pixels_load_from_string(txt, callerPlaceName=testName)
        pixelGroups_Glyphs_id_group_dict = img_3_pixel_select.pixelGroups_active_select(pixels)
        pixelGroups_Glyphs = list(pixelGroups_Glyphs_id_group_dict.values())

        pixelGroups_Glyphs[0].matrix_representation_refresh()

        # with relative coords
        coordsInactiveInMatrix = img_0_pixels.pixelGroup_matrix_representation_collect_matrix_coords_with_represented_names(
            pixelGroups_Glyphs[0].matrix_representation, {img_0_pixels.pixelsNameBackgroundInactive}
        )
        self.assertTrue(len(coordsInactiveInMatrix) == 4)
        # the relative/abs coords are different
        self.assertIn((2, 2), coordsInactiveInMatrix)

        # with absolute coords
        coordsInactiveInMatrix = img_0_pixels.pixelGroup_matrix_representation_collect_matrix_coords_with_represented_names(
            pixelGroups_Glyphs[0].matrix_representation, {img_0_pixels.pixelsNameBackgroundInactive},
            useAbsolutePixelCoordsInPage_insteadOf_relativeMatrixCoords=True
        )
        self.assertTrue(len(coordsInactiveInMatrix) == 4)

        # the relative/abs coords are different
        self.assertIn((3, 3), coordsInactiveInMatrix)



# python3 img_0_pixels_test.py  Test_active_pixel_group_detection.test_active_pixel_group_detection
class Test_active_pixel_group_detection(unittest.TestCase):


    def test_active_pixel_group_detection(self):
        testName = "test_active_pixel_group_detection"
        print(f"Test: {testName}")

        txt = """
          .*.
          ***
          .*.
        """

        pixels, errors, warnings = img_0_pixels.pixels_load_from_string(txt, callerPlaceName=testName)

        pixelGroups_Glyphs_id_group_dict = img_3_pixel_select.pixelGroups_active_select(pixels)
        pixelGroups_Glyphs = list(pixelGroups_Glyphs_id_group_dict.values())

        print("pixels in the group:", pixelGroups_Glyphs[0].pixels)

        pixelGroups_Glyphs[0].matrix_representation_display_in_terminal()
        self.assertTrue(len(pixelGroups_Glyphs[0].pixels) == 5)
        self.assertTrue(len(pixelGroups_Glyphs) == 1)





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

            pixelsInImg, errors, warnings = img_0_pixels.pixels_load_from_image(imgPath)
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

            _pixelsInImg, errors, warnings = img_0_pixels.pixels_load_from_image(imgPath)
            self.assertTrue(len(warnings) == 1)
            self.assertIn("probably Alpha channel is detected", str(warnings))




    def test_load_image_file_grayscale(self):
        imgPath = path_abs_to_testfile("../../samples/sample_abc_lower_ubuntu_light_300_grayscale.png")
        pixelsInImg, errors, warnings = img_0_pixels.pixels_load_from_image(imgPath)
        self.assertTrue(len(pixelsInImg[0][0]) == 3)
        self.assertTrue(warnings == list())
        # 3 values are in the pixel, rgb is created from one grayscale value


    def test_load_image_file_rgb(self):
        imgPath = path_abs_to_testfile("../../samples/sample_abc_lower_ubuntu_light_300.png")
        pixelsInImg, errors, warnings = img_0_pixels.pixels_load_from_image(imgPath)
        print(f"pixel 0, 0:")
        print(pixelsInImg[0][0])  # 3 values are in the pixel
        self.assertTrue(len(pixelsInImg[0][0]) == 3)  # 3 values are in the pixel
        self.assertTrue(warnings == list())


    def test_load_image_file__missing_file(self):
        imgPath = "unknown_file.png"
        pixelsInImg, errors, warnings = img_0_pixels.pixels_load_from_image(imgPath)
        self.assertTrue(len(errors) == 1)
        self.assertTrue(len(pixelsInImg) == 0)
        self.assertTrue(warnings == list())


# python3 img_0_pixels_test.py Test_matrix_representation_xAbsLeft_yAbsTop_xAbsRight_yAbsBottom
class Test_matrix_representation_xAbsLeft_yAbsTop_xAbsRight_yAbsBottom(unittest.TestCase):

    def test_matrix_representation_xAbsLeft_yAbsTop_xAbsRight_yAbsBottom(self):

        glyph = img_0_pixels.PixelGroup_Glyph()
        glyph.pixel_add(10, 11, (1,2,3))
        glyph.pixel_add(2, 22, (1,2,3))
        glyph.pixel_add(20, 21, (4,5,6))

        glyph.matrix_representation_refresh()
        coordsAbs, _errors = glyph.matrix_representation_xAbsLeft_yAbsTop_xAbsRight_yAbsBottom()
        self.assertEqual(coordsAbs, (2, 11, 20, 22))


    def test_missing_pixels_matrix_representation_xAbsLeft_yAbsTop_xAbsRight_yAbsBottom(self):

        glyph = img_0_pixels.PixelGroup_Glyph()
        coordsAbs, errors = glyph.matrix_representation_xAbsLeft_yAbsTop_xAbsRight_yAbsBottom()

        self.assertEqual(coordsAbs, (-1, -1, -1, -1))
        self.assertEqual(errors, ["noPixelInGlyph"])


# python3 img_0_pixels_test.py  Test_matrix_representation
class Test_matrix_representation(unittest.TestCase):

    txtInput = """
          .....**....... <- only STARs and DOTs are detected, any other chars are ignored
          ....*..*......
          ...******...**  <- extra active chars, don't belong to the first group
          ..*......*....
          .*........*...
        """

    # python3 img_0_pixels_test.py  Test_matrix_representation.test_matrix_representation_output
    def test_matrix_representation_output(self):
        testName = "test_matrix_representation_output"
        print(f"Test: {testName}")

        pixels, errors, warnings = img_0_pixels.pixels_load_from_string(
            self.txtInput, callerPlaceName=testName)

        pixelGroups_Glyphs_id_group_dict = img_3_pixel_select.pixelGroups_active_select(pixels)
        pixelGroups_Glyphs = list(pixelGroups_Glyphs_id_group_dict.values())

        matrixRepresentationOfPixelGroup = pixelGroups_Glyphs[0].matrix_representation_refresh()
        matrixReprStr = img_0_pixels.pixelGroup_matrix_representation_convert_to_str__forHumanReadingInTerminal(matrixRepresentationOfPixelGroup)
        print(matrixReprStr)

        """
        VERY IMPORTANT: in txtInput, the first column IS EMPTY.
        the matrix representation doesn't represent the totally empty
        columns/prefix lines, only where there is a real pixel value.
        Because of that, the first used Absolute X coord is 1, and not 0
        in the current example,
        in the representation's X axis.
        """
        wantedOut = "total * 14, . 36 (in matrix left/top output absolute coords are used, right/bottom: relative)\n" + \
                    "               1\n" + \
                    "      1234567890\n" + \
                    "   0: ....**....   0 (yRel)\n" + \
                    "   1: ...*..*...   1 (yRel)\n" + \
                    "   2: ..******..   2 (yRel)\n" + \
                    "   3: .*......*.   3 (yRel)\n" + \
                    "   4: *........*   4 (yRel)\n" + \
                    "      0123456789 (xRel)\n"

        self.assertEqual(wantedOut, matrixReprStr)


    # python3 img_0_pixels_test.py  Test_matrix_representation.test_matrix_representation_without_matrix_repr_data
    def test_matrix_representation_without_matrix_repr_data(self):
        matrixReprStr = img_0_pixels.pixelGroup_matrix_representation_convert_to_str__forHumanReadingInTerminal(
            list(), printStr=True)
        
        self.assertIn("The matrix representation is empty", matrixReprStr)

    def test_matrix_representation_empty_area(self):
        pixelGroupForBackgroundNonActivePixels = \
            img_0_pixels.PixelGroup_Glyph(representedPixelGroupName=img_0_pixels.pixelsNameBackgroundInactive)

        x_min = 2
        x_max = 6
        y_min = 3
        y_max = 8

        areaPixels = img_0_pixels.pixelGroup_matrix_representation_empty_area_create(
            pixelGroupForBackgroundNonActivePixels,
            x_min = x_min, x_max = x_max,
            y_min = y_min, y_max = y_max
        )

        ########### Test inactive empty area #############
        self.assertTrue(len(areaPixels) == (y_max-y_min+1))
        self.assertTrue(len(areaPixels[0]) == (x_max-x_min+1))




    # in src/p1_pixels dir: python3 img_0_pixels_test.py  Test_matrix_representation.test_matrix_representation_with_active_pixels__no_empty_border_around_representation
    def test_matrix_representation_with_active_pixels__no_empty_border_around_representation(self):

        testName = "test_matrix_representation_with_active_pixels"
        pixels, errors, warnings = img_0_pixels.pixels_load_from_string(
            self.txtInput, callerPlaceName=testName)

        pixelGroups_Glyphs_id_group_dict = img_3_pixel_select.pixelGroups_active_select(pixels)
        pixelGroups_Glyphs = list(pixelGroups_Glyphs_id_group_dict.values())

        matrixRepresentationOfPixelGroup = pixelGroups_Glyphs[0].matrix_representation_refresh()

        print(f"Test: {testName}")
        img_0_pixels.pixelGroup_matrix_representation_convert_to_str__forHumanReadingInTerminal(matrixRepresentationOfPixelGroup, printStr=True)

        y = 0 # matrixRepresentation is y,x based!!!!
        x = 0
        self.assertTrue(img_0_pixels.pixelsNameBackgroundInactive in matrixRepresentationOfPixelGroup[y][x][2].representedPixelGroupNames)

        y = 4 # matrixRepresentation is y,x based!!!!
        x = 0
        print(f"""
        This is tricky. Why x=0, y=4 is ACTIVE?
        
        By default the matrix representation starts with an active pixel:
      
        so the first column is TOTALLY EMPTY, it is not part of a representation. 
        v this first column is NOT in the representation of A !!!!
        .....**.......   ->  0: ....**....
        ....*..*......       1: ...*..*...
        ...******...**       2: ..******..
        ..*......*....       3: .*......*.
        .*........*...       4: *........*
 
        
        """)
        self.assertTrue(img_0_pixels.pixelsNameForegroundActive in matrixRepresentationOfPixelGroup[y][x][2].representedPixelGroupNames)


    # in src/p1_pixels dir: python3 img_0_pixels_test.py  Test_matrix_representation.test_matrix_representation_with_active_pixels__extra_empty_border_around_representation
    def test_matrix_representation_with_active_pixels__extra_empty_border_around_representation(self):

        testName = "test_matrix_representation_with_active_pixels_plus_extra_empty_border_around_representation"
        pixels, errors, warnings = img_0_pixels.pixels_load_from_string(
            self.txtInput, callerPlaceName=testName)

        pixelGroups_Glyphs_id_group_dict = img_3_pixel_select.pixelGroups_active_select(pixels)
        pixelGroups_Glyphs = list(pixelGroups_Glyphs_id_group_dict.values())

        # the extra border settings is the change, compared with the prev test case
        matrixRepresentationOfPixelGroup = pixelGroups_Glyphs[0].matrix_representation_refresh((3,4,5,6))
        
        
        # because of the border settings, the representation has a margin around the glyph:
        """
           0: ....................
           1: ....................
           2: ....................
           3: ..........**........
           4: .........*..*.......
           5: ........******......
           6: .......*......*.....
           7: ......*........*....
           8: ....................
           9: ....................
          10: ....................
          11: ....................
          12: ....................
        """

        print(f"Test: {testName}")
        img_0_pixels.pixelGroup_matrix_representation_convert_to_str__forHumanReadingInTerminal(matrixRepresentationOfPixelGroup, printStr=True)

        y = 4  # matrixRepresentation is y,x based!!!!
        x = 10
        self.assertTrue(img_0_pixels.pixelsNameBackgroundInactive in matrixRepresentationOfPixelGroup[y][x][2].representedPixelGroupNames)

        y = 7  # matrixRepresentation is y,x based!!!!
        x = 6
        self.assertTrue(img_0_pixels.pixelsNameForegroundActive in matrixRepresentationOfPixelGroup[y][x][2].representedPixelGroupNames)

# python3  img_0_pixels_test.py  Test_pixelGroup_matrix_representation_has_emptyborder_around_glyph
class Test_pixelGroup_matrix_representation_has_emptyborder_around_glyph(unittest.TestCase):

    def test_pixelGroup_matrix_representation_has_emptyborder_around_glyph(self):
        testName = "test_pixelGroup_matrix_representation_has_emptyborder_around_glyph"

        txt = """
          .*.
          ***
          .*.
        """

        pixels, errors, warnings = img_0_pixels.pixels_load_from_string(txt, callerPlaceName=testName)
        pixelGroups_Glyphs_id_group_dict = img_3_pixel_select.pixelGroups_active_select(pixels)
        pixelGroups_Glyphs = list(pixelGroups_Glyphs_id_group_dict.values())

        pixelGroups_Glyphs[0].matrix_representation_refresh()
        img_0_pixels.pixelGroup_matrix_representation_convert_to_str__forHumanReadingInTerminal(pixelGroups_Glyphs[0].matrix_representation, printStr=True)

        self.assertFalse(img_0_pixels.pixelGroup_matrix_representation_has_emptyborder_around_glyph(pixelGroups_Glyphs[0].matrix_representation, raiseExceptionIfNoBorder=False))

        # missing empty border around the pixelGroup, there are pixels
        self.assertRaises(ValueError,
                         img_0_pixels.pixelGroup_matrix_representation_has_emptyborder_around_glyph,
                         pixelGroups_Glyphs[0].matrix_representation,
                         raiseExceptionIfNoBorder=True
                         )

        # no pixel in representation, with exception
        self.assertRaises(ValueError,
                          img_0_pixels.pixelGroup_matrix_representation_has_emptyborder_around_glyph,
                          list(),
                          True
                          )

        # no pixel in representation, with False ret
        self.assertFalse( img_0_pixels.pixelGroup_matrix_representation_has_emptyborder_around_glyph(
                           list(), False) )

        #######################################################################################

        txt = """
          ....
          .**.
          ....
        """

        pixels, errors, warnings = img_0_pixels.pixels_load_from_string(txt, callerPlaceName=testName)
        pixelGroups_Glyphs_id_group_dict = img_3_pixel_select.pixelGroups_active_select(pixels)
        pixelGroups_Glyphs = list(pixelGroups_Glyphs_id_group_dict.values())

        pixelGroups_Glyphs[0].matrix_representation_refresh(addExtraEmptyBorderAroundArea=(1,1,1,1))

        self.assertTrue(img_0_pixels.pixelGroup_matrix_representation_has_emptyborder_around_glyph(pixelGroups_Glyphs[0].matrix_representation, raiseExceptionIfNoBorder=False))




if __name__ == '__main__':
    unittest.main()
