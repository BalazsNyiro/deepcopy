# -*- coding: utf-8 -*-
import unittest, vector, mark_util

class VectorTests(unittest.TestCase):
    def test_block_search_in_mark(self):
        Txt = ("..XXX"
               "XXXXX"
               "XXXX."
               "XXX..")
        MarkGenerated = mark_util.mark_from_string(Txt, 5, "X")
        vector.block_search_in_mark(MarkGenerated)
        self.assertEqual(1, 2)

def run_all_tests(P):
    print("run all tests: Vector")
    global Prg
    Prg = P
    unittest.main(module="test_vector", verbosity=2, exit=False)
