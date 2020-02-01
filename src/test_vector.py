# -*- coding: utf-8 -*-
import unittest, vector, mark_util

class VectorTests(unittest.TestCase):
    def test_block_check_exist_in_mark(self):
        Txt = ("..XXX"
               "XXXXX"
               "XXXX."
               "XXX..")
        MarkGenerated = mark_util.mark_from_string(Txt, 5, "X")
        BlockCheck, PixelProblem, CoordsOfBlock = vector.block_exist_in_coords(MarkGenerated["Coords"], 0, 1, 2, 3)
        self.assertEqual(BlockCheck, True)

        BlockCheck, PixelProblem, CoordsOfBlock = vector.block_exist_in_coords(MarkGenerated["Coords"], 0, 1, 4, 3)
        self.assertEqual(BlockCheck, False)

    def test_block_nonoverlap_search_in_mark(self):
        Txt = ("..XXX"
               "XXXXX"
               "XXXX."
               "XXX..")
        MarkGenerated = mark_util.mark_from_string(Txt, 5, "X")
        BlocksInMark = vector.block_nonoverlap_search_in_mark(MarkGenerated)
        BlocksWanted = {3: [[(0, 1), (0, 2), (0, 3), (1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (2, 3)]],
                        2: [[(3, 0), (3, 1), (4, 0), (4, 1)]],
                        1: [[(2, 0)], [(3, 2)]]}
        self.assertEqual(BlocksInMark, BlocksWanted)

    def test_block_nonoverlap_search_in_mark__letter_e(self):
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
        BlocksInMark = vector.block_nonoverlap_search_in_mark(MarkGenerated)
        print("\n" + vector.block_to_string(MarkGenerated, BlocksInMark, Prefix=" ") + "\n")
        # TODO: display the blocks with colors and finish the test

def run_all_tests(P):
    print("run all tests: Vector")
    global Prg
    Prg = P
    unittest.main(module="test_vector", verbosity=2, exit=False)
