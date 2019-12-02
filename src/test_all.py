#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest, util, os

class TestMethods(unittest.TestCase):

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
                   }
                }
              }
        # happy path:
        self.assertEqual("Mentés másként", util.ui_msg(Prg, "Menu.File.SaveAs"))

        # key is unknown:
        self.assertEqual("Ui message key is unknown: hun - Menu.File.UnknownKey",
                         util.ui_msg(Prg, "Menu.File.UnknownKey"))

        # key exists, language==hun, but only default eng element exists in transations
        self.assertEqual("Load", util.ui_msg(Prg, "Menu.File.Load"))

        # key hasn't got default eng value:
        self.assertEqual("Ui message, default eng translation is missing: Menu.File.Export",
                         util.ui_msg(Prg, "Menu.File.Export"))


    def test_file_read_all(self):
        TxtRaw = "  Test Line 1\n\n  Test Line 3"
        Path = os.path.join(Prg["PrgDirParent"], "test", "test_file_read_lines.txt")
        self.assertEqual(TxtRaw, util.file_read_all(Path))

    def test_file_funcs(self):
        self.assertFalse(util.file_test("unknown_file"))
        Path = os.path.join(Prg["PrgDirParent"], "test", "test_file_read_lines.txt")
        self.assertTrue(util.file_test(Path))

def run_all_tests(P):
    print("run all tests")
    global Prg
    Prg = P
    unittest.main(module="test_all", verbosity=2, exit=False)

if __name__ == '__main__':
    run_all_tests({})
