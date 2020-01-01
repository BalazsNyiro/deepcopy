#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest, util, os, ocr


class TestMethods(unittest.TestCase):
    def PrgEmpty(self):
        return {"Errors":[]}

    def test_module_available(self):
        self.assertFalse(util.module_available(self.PrgEmpty(), "unknown_module", "please install unknown module :-)"))
        self.assertTrue(util.module_available(self.PrgEmpty(), "os", "Please install os module if you want to reach files"))

    def test_ui_msg(self):
        Prg = {"Os": "Linux",
               "Errors": [],
               "Warnings": [],
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
        self.assertEqual("Mentés másként", util.ui_msg(Prg, "Menu.File.SaveAs"))

        # handle multiple value in one request:
        TxtSaveAs, Export = util.ui_msg(Prg, ["Menu.File.SaveAs", "Menu.File.Load"])
        self.assertEqual("Mentés másként", TxtSaveAs)
        self.assertEqual("Load", Export)

        # key is unknown:
        self.assertEqual("Ui message key is unknown: hun - Menu.File.UnknownKey",
                         util.ui_msg(Prg, "Menu.File.UnknownKey"))

        # key exists, language==hun, but only default eng element exists in transations
        self.assertEqual("Load", util.ui_msg(Prg, "Menu.File.Load"))

        # key hasn't got default eng value:
        self.assertEqual("Ui message, default eng translation is missing: Menu.File.Export",
                         util.ui_msg(Prg, "Menu.File.Export"))

        # text with formatting:
        self.assertEqual("Fájl: /tmp/file.txt", util.ui_msg(Prg, "Text_formatted").format("/tmp/file.txt"))

    def test_file_read_all(self):
        TxtRaw = "  Test Line 1\n\n  Test Line 3"
        Path = os.path.join(Prg["DirPrgParent"], "test", "test_file_read_lines.txt")
        self.assertEqual(TxtRaw, util.file_read_all(Path))

    def test_file_funcs(self):
        self.assertFalse(util.file_test("unknown_file"))
        Path = os.path.join(Prg["DirPrgParent"], "test", "test_file_read_lines.txt")
        self.assertTrue(util.file_test(Path))

    def test_ocr_mark_collect___word_the(self):
        FilePathImg = os.path.join(Prg["DirPrgParent"], "test", "test_mark_finding_word_the__font_ubuntu_24pt.png")
        ImgId = util.img_generate_id_for_loaded_list(Prg, PreFix="thumbnail", PostFix=FilePathImg)
        util.img_load_into_prg_structure(Prg, FilePathImg, ImgId)
        Img = Prg["ImagesLoaded"][ImgId]
        Marks = ocr.mark_collect(Prg, Img)
        print("Test, Num of Marks:", len(Marks.keys()))


        FilePathMarkDetect_the = os.path.join(Prg["DirPrgParent"], "test", "test_mark_finding_word_the___font_ubuntu_24pt_result.txt")
        TestWantedResults = load_test_result_mark_detection(Prg, FilePathMarkDetect_the)
        if Prg["Errors"]: return

        for ResultKey, ResultTxt in TestWantedResults.items():
            print("ResultKey:", ResultKey)
            print(ResultTxt)

        for Key in Marks.keys():
            MarkDetected = ocr.mark_display_on_console(Marks[Key])
            MarkWanted = TestWantedResults[Key]
            PathDetected = os.path.join(Prg["PathTempDir"], "test_detected.txt")
            PathWanted   = os.path.join(Prg["PathTempDir"], "test_wanted.txt")
            util.file_write(Prg, PathDetected, MarkDetected)
            util.file_write(Prg, PathWanted, MarkWanted)
            if Prg["Errors"]:
                print(Prg["Errors"])
            else:
                # theoretically all tests has been ok in released versions, this case happens only in dev time
                print("Dev message: test comparing with vimdiff:")
                os.system("vimdiff " + PathDetected + " " + PathWanted)
            self.assertEqual(MarkDetected, MarkWanted)

        # ocr.mark_display_on_console(Marks[1])

        util.error_display(Prg)

# if you want to execute only the tests:
# ./deepcopy.py testonly
def run_all_tests(P):
    print("run all tests")
    global Prg
    Prg = P
    unittest.main(module="test_all", verbosity=2, exit=False)

if __name__ == '__main__':
    run_all_tests({})

def load_test_result_mark_detection(Prg, FileResultPath):
    Marks = dict()
    MarkId = 0
    MarkLines = []

    print(FileResultPath)
    for Line in util.file_read_lines(Prg, Fname=FileResultPath):
        Line = Line.strip()
        if "." not in Line and "O" not in Line:
            if MarkLines:
                Marks[MarkId] = "\n".join(MarkLines)
                MarkLines = []
                MarkId += 1
        else:
            MarkLines.append(Line)
    return Marks


