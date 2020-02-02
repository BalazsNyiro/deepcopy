# -*- coding: utf-8 -*-
import unittest, vector, mark_util

class VectorTests(unittest.TestCase):
    def test_spiral_max_from_coord(self):
        Letter = ("OOOO"
                  "OOOO"
                  " OOO"
                  "OOOO")
        Mark = mark_util.mark_from_string(Letter, 4, "O")
        print("\n##############################")
        SpiralMax = vector.spiral_max_from_coord(Mark, (2,1))
        print("SpiralMax:", SpiralMax)

    def test_spiral_nonoverlap_search_in_mark__letter_e(self):
        Letter = ("    OOOOOOO   "
                  "  OOOOOOOOOO  "
                  " OOOOOOOOOOOO "
                  " OOOOO  OOOOO "
                  "OOOO      OOOO"
                  "OOOO      OOOO"
                  "OOOOOOOOOOOOOO"
                  "OOOOOOOOOOOOOO"
                  "OOO           "
                  "OOOO          "
                  "OOOO          "
                  " OOOOOO   OOO "
                  " OOOOOOOOOOOO "
                  "  OOOOOOOOOOO "
                  "    OOOOOOOO  ")
        MarkGenerated = mark_util.mark_from_string(Letter, 14, "O")
        #BlocksInMark = vector.block_nonoverlap_search_in_mark(MarkGenerated)
        #print("\n" + vector.block_to_string(MarkGenerated, BlocksInMark, Prefix=" ") + "\n")
        # TODO: display the blocks with colors and finish the test

def run_all_tests(P):
    print("run all tests: Vector")
    global Prg
    Prg = P
    unittest.main(module="test_vector", verbosity=2, exit=False)
