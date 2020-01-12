#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest, util, os, ocr

class TestMethods(unittest.TestCase):
    def PrgEmpty(self):
        return {}

    def test_module_available(self):
        self.assertFalse(util.module_available(self.PrgEmpty(), "unknown_module", "please install unknown module :-)"))
        self.assertTrue(util.module_available(self.PrgEmpty(), "os", "Please install os module if you want to reach files"))

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

    def test_ocr_mark_collect___word_the(self):
        FilePathImg = ["test", "test_mark_finding_word_the__font_ubuntu_24pt.png"]
        FileWantedResult = ["test", "test_mark_finding_word_the___font_ubuntu_24pt_result.txt"]
        Marks, TestWantedResults = marks_results_from_img_and_result_files(Prg, FilePathImg, FileWantedResult)
        difference_display(Prg, self, Marks, TestWantedResults)

    def test_ocr_mark_collect___base_abc_ubuntu(self):

        FilePathImg = ["test", "test_mark_finding_abc_basic__font_ubuntu_24pt.png"]
        FileWantedResult = ["test", "test_abc_basic.txt"]

        Marks, TestWantedResults = marks_results_from_img_and_result_files(Prg, FilePathImg, FileWantedResult)
        difference_display(Prg, self, Marks, TestWantedResults)

# if you want to execute only the tests:
# ./deepcopy.py testonly
def run_all_tests(P):
    print("run all tests")
    global Prg
    Prg = P
    unittest.main(module="test_all", verbosity=2, exit=False)

if __name__ == '__main__':
    run_all_tests({})

# TODO: a more general diff display in console without linux vimdiff
def difference_display(Prg, SelfObj, MarksNowDetected, TestWantedResults):
    print("Num of Marks now detected: ", len(MarksNowDetected.keys()))
    print("Num of wanted results: ", len( TestWantedResults))
    for Key in MarksNowDetected.keys():
        MarkDetected = ocr.mark_display_on_console(Prg, MarksNowDetected[Key])
        MarkWanted = TestWantedResults[Key]

        if MarkDetected != MarkWanted:
            PathDetected = os.path.join(Prg["PathTempDir"], "test_detected.txt")
            PathWanted = os.path.join(Prg["PathTempDir"], "test_wanted.txt")
            util.file_write(Prg, PathDetected, MarkDetected)
            util.file_write(Prg, PathWanted, MarkWanted)
            # theoretically all tests has been ok in released versions, this case happens only in dev time
            print("Dev message: test comparing with vimdiff:")
            os.system("vimdiff " + PathDetected + " " + PathWanted)
        SelfObj.assertEqual(MarkDetected, MarkWanted)


def marks_results_from_img_and_result_files(Prg, FilePathImg, FileWantedResult):
    Marks = ocr.mark_collect_from_img_file(Prg, FilePathImg)
    print("Test, Num of Marks:", len(Marks.keys()))
    TestWantedResults = test_results_load_from_mark_detection(Prg, FileWantedResult)
    return Marks, TestWantedResults

def test_results_load_from_mark_detection(Prg, FileResultPathElems):
    Marks = dict()
    MarkId = 0
    MarkLines = []
    FileResultPath =os.path.join(Prg["DirPrgParent"], *FileResultPathElems)
    [Prg["DirPrgParent"], "test", "test_mark_finding_word_the___font_ubuntu_24pt_result.txt"]
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

