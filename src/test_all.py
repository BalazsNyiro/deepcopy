#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest, util, os

class TestMethods(unittest.TestCase):

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
