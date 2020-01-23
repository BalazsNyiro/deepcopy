#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest, util, os, mark_collect

import mark_util


class UtilFuncs(unittest.TestCase):
    def test_img_generate_id_for_loaded_list(self):
        PrgDict = {"ImagesLoaded": {1:"img_one", 2:"img_two"}}
        ImgId = util.img_generate_id_for_loaded_list(PrgDict, PreFix="Pre", PostFix="Post")
        self.assertEqual(ImgId, "Pre_3_Post")

    def test_coords_neighbours(self):
        #   neighbour coord order:
        #   CDE
        #   B F
        #   AHG
        PossibleNeighbours = [(0, 2), (0, 1), (0, 0), (1, 0), (2, 0), (2, 1), (2, 2), (1, 2)]
        self.assertEqual(util.coords_neighbours((1, 1)), PossibleNeighbours)

class OcrBusinessFuncs(unittest.TestCase):

    def test_mark_ids_collect_from_neighbourhood__mark_ids_set_for_pixel(self):
        # the second test uses the result of the first one.
        ######## test: mark_ids_collect_from_neighbourhood ###########
        Marks = {22: {(2, 2): 0},
                 42: {(4, 2): 0, (5, 2): 0},
                 44: {(4, 4): 0}}
        MarkIdIfNoNeighbour = 0
        InkPixelCoords_and_MarkId = {(2, 2): 22, (4, 2): 42, (4, 4): 44, (5, 2): 42}

        Coord = (3, 3)
        MarkIdsInNeighbourhood, _MarkIdIfNoNeighbour = \
            mark_collect.mark_ids_collect_from_neighbourhood(Coord, MarkIdIfNoNeighbour,
                                                             InkPixelCoords_and_MarkId)
        WantedMarkIdsInNeighbourhood = [22, 42, 44]

        self.assertEqual(MarkIdsInNeighbourhood, WantedMarkIdsInNeighbourhood)

        ######### test: mark_ids_set_for_pixel() ##########
        MarkIdCurrentPixel = MarkIdsInNeighbourhood.pop(0) # select first id from the possible list

        FilePathElems = ["test", "test_mark_ids_set_for_pixels_gray.png"]
        Img, _ImgId = util.img_load_into_prg_structure__get_imgid(Prg, FilePathElems)
        mark_collect.mark_ids_set_for_pixels(Marks, MarkIdCurrentPixel,
                                             InkPixelCoords_and_MarkId,
                                             MarkIdsInNeighbourhood, Img, Coord)
        # util.file_write(Prg, "log_mark.txt", str(Marks))
        WantedMarksPixelInserted_and_IdsMerged = {22: {(2, 2): 0, (3, 3): 128, (4, 2): 0, (4, 4): 0, (5, 2): 0}}
        WantedInkPixelCoords_and_MarkId = {(2, 2): 22, (3, 3): 22, (4, 2): 22, (4, 4): 22, (5, 2): 22}
        self.assertEqual(Marks, WantedMarksPixelInserted_and_IdsMerged)
        self.assertEqual(InkPixelCoords_and_MarkId, WantedInkPixelCoords_and_MarkId)


    def test_mark_pixels_select_from_img(self):

        ColorBlockBackgroundRgb = (128, 128, 128)
        ColorBlockBackgroundRgbDelta = (30, 30, 30)
        ColorBlockBackgroundGray = 225
        ColorBlockBackgroundGrayDelta = 128  # between 225+Delta - 225-Delta pixels are bg pixels

        FilePathElems = ["test", "test_color_scale_rgb.png"]
        Img, _ImgId = util.img_load_into_prg_structure__get_imgid(Prg, FilePathElems)

        InkPixelCoords_and_MarkId = mark_collect.mark_pixels_select_from_img(
            Prg, Img,
            ColorBlockBackgroundRgb, ColorBlockBackgroundRgbDelta,
            ColorBlockBackgroundGray, ColorBlockBackgroundGrayDelta)

        WantedPixels = {(0, 0): None, (1, 0): None, (2, 0): None, (3, 0): None, (7, 0): None, (8, 0): None, (9, 0): None, (10, 0): None}
        self.assertEqual(InkPixelCoords_and_MarkId, WantedPixels)

        # test with grayscale img
        FilePathElems = ["test", "test_color_scale_gray.png"]
        Img, _ImgId = util.img_load_into_prg_structure__get_imgid(Prg, FilePathElems)
        # util.file_write(Prg, "log.txt", str(Img))
        InkPixelCoords_and_MarkId = mark_collect.mark_pixels_select_from_img(
            Prg, Img,
            ColorBlockBackgroundRgb, ColorBlockBackgroundRgbDelta,
            ColorBlockBackgroundGray, ColorBlockBackgroundGrayDelta)

        # util.file_write(Prg, "log.txt", str(InkPixelCoords_and_MarkId))
        WantedPixels = {(7, 0): None, (8, 0): None, (9, 0): None, (10, 0): None}
        self.assertEqual(InkPixelCoords_and_MarkId, WantedPixels)

    def test_markid_of_coord_append_if_unknown(self):

        InkPixelCoords_and_MarkId = dict()
        InkPixelCoords_and_MarkId[(1, 1)] = 1
        InkPixelCoords_and_MarkId[(2, 2)] = 2
        MarkIdsPossible = [2] # this is a possible Id, as a theoretical start state

        mark_collect.markid_of_coord_append_if_unknown((1, 1), MarkIdsPossible, InkPixelCoords_and_MarkId)
        # 2 is in the Possible id's list, so the func doesn't insert it again
        mark_collect.markid_of_coord_append_if_unknown((2, 2), MarkIdsPossible, InkPixelCoords_and_MarkId)

        for MarkIdWanted in [1,2]:
            self.assertEqual(MarkIdWanted in MarkIdsPossible, True)


class Ocr(unittest.TestCase):
    def test_is_mark_rgb(self):
        FilePathElems = ["test", "test_img_rgb_color_levels.png"]
        Img, ImgId = util.img_load_into_prg_structure__get_imgid(Prg, FilePathElems)

        self.assertEqual(util.is_rgb(Img), True)
        # Bg == Background

        ColorBgRMin = 0
        ColorBgGMin = 0
        ColorBgBMin = 0

        ColorBgGMax = 40
        ColorBgRMax = 40
        ColorBgBMax = 40

        IsMarkRgb_0_0 = mark_collect.is_mark_rgb(Img, 0, 0, ColorBgRMin, ColorBgGMin, ColorBgBMin,
                                                 ColorBgGMax, ColorBgRMax, ColorBgBMax, PrintRgb=True)
        IsMarkRgb_1_0 = mark_collect.is_mark_rgb(Img, 1, 0, ColorBgRMin, ColorBgGMin, ColorBgBMin,
                                                 ColorBgGMax, ColorBgRMax, ColorBgBMax, PrintRgb=True)
        IsMarkRgb_2_0 = mark_collect.is_mark_rgb(Img, 2, 0, ColorBgRMin, ColorBgGMin, ColorBgBMin,
                                                 ColorBgGMax, ColorBgRMax, ColorBgBMax, PrintRgb=True)
        self.assertEqual(IsMarkRgb_0_0, False)
        self.assertEqual(IsMarkRgb_1_0, True)
        self.assertEqual(IsMarkRgb_2_0, True)

        # The light colors have higher values in RGB. so it can be
        # the definition of white paper
        ColorBgRMin = 110
        ColorBgGMin = 110
        ColorBgBMin = 110

        ColorBgGMax = 255
        ColorBgRMax = 255
        ColorBgBMax = 255

        IsMarkRgb_0_0 = mark_collect.is_mark_rgb(Img, 0, 0, ColorBgRMin, ColorBgGMin, ColorBgBMin,
                                                 ColorBgGMax, ColorBgRMax, ColorBgBMax, PrintRgb=True, PrintRetVal=True)
        IsMarkRgb_1_0 = mark_collect.is_mark_rgb(Img, 1, 0, ColorBgRMin, ColorBgGMin, ColorBgBMin,
                                                 ColorBgGMax, ColorBgRMax, ColorBgBMax, PrintRgb=True, PrintRetVal=True)
        IsMarkRgb_2_0 = mark_collect.is_mark_rgb(Img, 2, 0, ColorBgRMin, ColorBgGMin, ColorBgBMin,
                                                 ColorBgGMax, ColorBgRMax, ColorBgBMax, PrintRgb=True, PrintRetVal=True)
        self.assertEqual(IsMarkRgb_0_0, True)
        self.assertEqual(IsMarkRgb_1_0, False)
        self.assertEqual(IsMarkRgb_2_0, False)


    def test_is_mark_grayscale(self):
        FilePathElems = ["test", "test_img_grayscale_color_levels.png"]
        Img, ImgId = util.img_load_into_prg_structure__get_imgid(Prg, FilePathElems)

        ColorBackgroundGrayMin = 10
        ColorBackgroundGrayMax = 240

        self.assertEqual(util.is_grayscale(Img), True)
        self.assertEqual(mark_collect.is_mark_grayscale(Img, 0, 0, ColorBackgroundGrayMin, ColorBackgroundGrayMax), True)
        self.assertEqual(mark_collect.is_mark_grayscale(Img, 1, 0, ColorBackgroundGrayMin, ColorBackgroundGrayMax), False)
        self.assertEqual(mark_collect.is_mark_grayscale(Img, 2, 0, ColorBackgroundGrayMin, ColorBackgroundGrayMax), True)

        ColorBackgroundGrayMin = 1
        ColorBackgroundGrayMax = 255

        self.assertEqual(mark_collect.is_mark_grayscale(Img, 0, 0, ColorBackgroundGrayMin, ColorBackgroundGrayMax), False)
        self.assertEqual(mark_collect.is_mark_grayscale(Img, 1, 0, ColorBackgroundGrayMin, ColorBackgroundGrayMax), False)
        self.assertEqual(mark_collect.is_mark_grayscale(Img, 2, 0, ColorBackgroundGrayMin, ColorBackgroundGrayMax), False)

    def test_is_rgb_pixel_datasize_field_missing(self):
        Img = dict()
        self.assertEqual(util.is_rgb(Img), False)

    def test_is_rgb_pixel_datasize_field_is_zero(self):
        Img = dict()
        Img["PixelDataSize"] = 0
        self.assertEqual(util.is_rgb(Img), False)

    def test_is_rgb_pixel_datasize_field_is_one(self):
        Img = dict()
        Img["PixelDataSize"] = 3
        self.assertEqual(util.is_rgb(Img), True)

    def test_is_grayscale_pixel_datasize_field_missing(self):
        Img = dict()
        self.assertEqual(util.is_grayscale(Img), False)

    def test_is_grayscale_pixel_datasize_field_is_zero(self):
        Img = dict()
        Img["PixelDataSize"] = 0
        self.assertEqual(util.is_grayscale(Img), False)

    def test_is_grayscale_pixel_datasize_field_is_one(self):
        Img = dict()
        Img["PixelDataSize"] = 1
        self.assertEqual(util.is_grayscale(Img), True)

class TestMethodsAnalysed(unittest.TestCase):
    def test_mark_collect___base_abc_ubuntu(self):

        FilePathImg      = ["test", "test_mark_finding_abc_basic__font_ubuntu_24pt.png"]
        FileWantedResult = ["test", "test_mark_finding_abc_basic__font_ubuntu_24pt_result.txt"]

        MarksNowDetected, TestWantedResults = marks_results_from_img_and_result_files(Prg, FilePathImg, FileWantedResult)
        #difference_display(Prg, self, MarksNowDetected, TestWantedResults, AppendToFileIfDifference=FileWantedResult)
        difference_display(Prg, self, MarksNowDetected, TestWantedResults)

class TestMethods(unittest.TestCase):

    def test_module_available(self):
        PrgEmpty = {}
        self.assertFalse(util.module_available(PrgEmpty, "unknown_module", "please install unknown module :-)"))
        self.assertTrue(util.module_available(PrgEmpty, "os", "Please install os module if you want to reach files"))

    def test_ui_msg(self):
        Prg = {"Os": "Linux",
               "UiLanguage": "hun",
               "UiMessages": {
                   "Menu" : {
                       "File": {
                           "SaveAs": {
                              "eng": "Save as",
                              "hun": "Mentés másként"
                           },
                           "Load": {
                               "eng": "Load"
                           },
                           "Export": {
                               "hun": "Exportálás"
                           }
                       }
                   },
                   "Text_formatted": {
                       "eng": "File: {:s}",
                       "hun": "Fájl: {:s}"
                   }
               }
        }
        # happy path:
        self.assertEqual("Mentés másként", util.ui_msg(Prg, "Menu.File.SaveAs", TestCase=True))

        # handle multiple value in one request:
        TxtSaveAs, Export = util.ui_msg(Prg, ["Menu.File.SaveAs", "Menu.File.Load"], TestCase=True)
        self.assertEqual("Mentés másként", TxtSaveAs)
        self.assertEqual("Load", Export)

        # key is unknown:
        self.assertEqual("Ui message key is unknown in container: hun - Menu.File.UnknownKey",
                         util.ui_msg(Prg, "Menu.File.UnknownKey", TestCase=True))

        # key exists, language==hun, but only default eng element exists in translations
        self.assertEqual("Load", util.ui_msg(Prg, "Menu.File.Load", TestCase=True))

        # key hasn't got default eng value:
        self.assertEqual("Ui message, default eng translation is missing: Menu.File.Export",
                         util.ui_msg(Prg, "Menu.File.Export", TestCase=True))

        # text with formatting:
        self.assertEqual("Fájl: /tmp/file.txt", util.ui_msg(Prg, "Text_formatted", TestCase=True).format("/tmp/file.txt"))

    def test_file_read_all(self):
        TxtRaw = "  Test Line 1\n\n  Test Line 3"
        Path = os.path.join(Prg["DirPrgParent"], "test", "test_file_read_lines.txt")
        self.assertEqual(TxtRaw, util.file_read_all(Prg, Path))

    def test_file_funcs(self):
        self.assertFalse(util.file_test(Prg, "unknown_file"))
        Path = os.path.join(Prg["DirPrgParent"], "test", "test_file_read_lines.txt")
        self.assertTrue(util.file_test(Prg, Path))

    def test_mark_collect___word_the(self):
        FilePathImg = ["test", "test_mark_finding_word_the__font_ubuntu_24pt.png"]
        FileWantedResult = ["test", "test_mark_finding_word_the__font_ubuntu_24pt_result.txt"]
        Marks, TestWantedResults = marks_results_from_img_and_result_files(Prg, FilePathImg, FileWantedResult)
        difference_display(Prg, self, Marks, TestWantedResults)


# if you want to execute only the tests:
# ./deepcopy.py testonly
def run_all_tests(P):
    print("run all tests")
    global Prg
    Prg = P
    # exec all test:
    unittest.main(module="test_mark_collect", verbosity=2, exit=False)
    # unittest.main(TestMethodsAnalysed())


if __name__ == '__main__':
    run_all_tests({})

# TODO: a more general diff display in console without linux vimdiff
def difference_display(Prg, SelfObj, MarksNowDetected, TestWantedResults, AppendToFileIfDifference=None):
    print("Num of Marks now detected: ", len(MarksNowDetected.keys()))
    print("Num of wanted results: ", len( TestWantedResults))

    WantedKeys = sorted(list(TestWantedResults.keys()))

    for Key in sorted(list(MarksNowDetected.keys())):

        # in MarkDetected dict() can be index gaps.
        # example: D = {0:"A", 3:"B", 5, "C"}
        # so we loop over on detected keys and always take the next element from the test -
        # the two dict's keys can be different but the order of the keys are fixed
        MarkDetected = mark_util.mark_to_string(Prg, MarksNowDetected[Key])

        MarkWanted = TestWantedResults.get(WantedKeys.pop(0), "Key not in Wanted results: " + str(Key))

        if MarkDetected != MarkWanted:

            if AppendToFileIfDifference:
                util.file_append(Prg, os.path.join(*AppendToFileIfDifference), "\n\n" + MarkDetected)
            else:
                PathDetected = os.path.join(Prg["PathTempDir"], "test_detected_"+str(Key)+".txt")
                PathWanted   = os.path.join(Prg["PathTempDir"], "test_wanted_"+str(Key)+".txt")
                util.file_write(Prg, PathDetected, MarkDetected)
                util.file_write(Prg, PathWanted, MarkWanted)
                # theoretically all tests has been ok in released versions, this case happens only in dev time
                print("Dev message: test comparing with vimdiff:")
                os.system("vimdiff " + PathDetected + " " + PathWanted)

                SelfObj.assertEqual(MarkDetected, MarkWanted)

def marks_results_from_img_and_result_files(Prg, FilePathImg, FileWantedResult):
    Marks = mark_collect.mark_collect_from_img_file(Prg, FilePathImg)
    print("Test, Num of Marks:", len(Marks.keys()))
    TestWantedResults = test_results_load_from_mark_detection(Prg, FileWantedResult)
    return Marks, TestWantedResults

def test_results_load_from_mark_detection(Prg, FileResultPathElems):
    Marks = dict()
    MarkId = 0
    MarkLines = []
    FileResultPath =os.path.join(Prg["DirPrgParent"], *FileResultPathElems)

    print("File result path:", FileResultPath)
    for Line in util.file_read_lines(Prg, Fname=FileResultPath):
        Line = Line.strip()
        if mark_util.MarkBg not in Line and mark_util.MarkFg not in Line:
            if MarkLines:
                Marks[MarkId] = "\n".join(MarkLines)
                MarkLines = []
                MarkId += 1
        else:
            MarkLines.append(Line)
            # print("Line: ", Line)

    if MarkLines:
        Marks[MarkId] = "\n".join(MarkLines)

    # for Key in Marks:
    #     print(Marks[Key])
    return Marks

