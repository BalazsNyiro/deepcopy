# -*- coding: utf-8 -*-
import unittest, vector, mark_util

class VectorTests(unittest.TestCase):
    def test_spiral_from_coord(self):
        Letter = ("OOOO"
                  "OOOO"
                  " OOO"
                  "OOOO")
        Mark = mark_util.mark_from_string(Letter, 4, "O")
        # print(Mark)

        ######### DOWN: #################
        SpiralDetected = vector.spiral_from_coord(Mark["Coords"], (2, 1),
                                                  "CounterClockwise", "Down")
        #print("Spiral CounterClockwise Down:", SpiralDetected)
        SpiralWanted = [(2, 1), (2, 2), (3, 2), (3, 1), (3, 0),
                        (2, 0), (1, 0), (1, 1), (1, 2), (1, 3), (2, 3), (3, 3)]
        self.assertEqual(SpiralDetected, SpiralWanted)

                    ######### opposite direction
        SpiralDetected = vector.spiral_from_coord(Mark["Coords"], (2, 1),
                                                  "Clockwise", "Down")
        #print("Spiral Clockwise, Down:", SpiralDetected)
        SpiralWanted = [(2, 1), (2, 2), (1, 2), (1, 1), (1, 0), (2, 0),
                        (3, 0), (3, 1), (3, 2), (3, 3), (2, 3), (1, 3), (0, 3)]
        self.assertEqual(SpiralDetected, SpiralWanted)

        ##################### UP ###########################################
        SpiralDetected = vector.spiral_from_coord(Mark["Coords"], (2, 1),
                                                  "CounterClockwise", "Up")
        #print("Spiral CounterClockwise Up:", SpiralDetected)
        SpiralWanted = [(2, 1), (2, 0), (1, 0), (1, 1), (1, 2), (2, 2), (3, 2), (3, 1), (3, 0)]
        self.assertEqual(SpiralDetected, SpiralWanted)

                    ######### opposite direction
        SpiralDetected = vector.spiral_from_coord(Mark["Coords"], (2, 1),
                                                  "Clockwise", "Up")
        SpiralWanted = [(2, 1), (2, 0), (3, 0), (3, 1), (3, 2), (2, 2), (1, 2), (1, 1), (1, 0)]
        self.assertEqual(SpiralDetected, SpiralWanted)
        # print("Spiral clockwise, up:", SpiralDetected)

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
