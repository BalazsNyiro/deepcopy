# -*- coding: utf-8 -*-
import unittest, spiral, mark_util

class VectorTests(unittest.TestCase):
    def test_spiral_from_coord(self):
        Letter = ("OOOO"
                  "OOOO"
                  " OOO"
                  "OOOO")
        Mark = mark_util.mark_from_string(Letter, 4, "O")
        # print(Mark)

        ######### DOWN: #################
        SpiralDetected = spiral.spiral_from_coord(Mark["Coords"], (2, 1), "CounterClockwise", "Down")
        #print("Spiral CounterClockwise Down:", SpiralDetected)
        SpiralWanted = [(2, 1), (2, 2), (3, 2), (3, 1), (3, 0),
                        (2, 0), (1, 0), (1, 1), (1, 2), (1, 3), (2, 3), (3, 3)]
        self.assertEqual(SpiralDetected, SpiralWanted)

                    ######### opposite direction
        SpiralDetected = spiral.spiral_from_coord(Mark["Coords"], (2, 1), "Clockwise", "Down")
        #print("Spiral Clockwise, Down:", SpiralDetected)
        SpiralWanted = [(2, 1), (2, 2), (1, 2), (1, 1), (1, 0), (2, 0),
                        (3, 0), (3, 1), (3, 2), (3, 3), (2, 3), (1, 3), (0, 3)]
        self.assertEqual(SpiralDetected, SpiralWanted)

        ##################### UP ###########################################
        SpiralDetected = spiral.spiral_from_coord(Mark["Coords"], (2, 1), "CounterClockwise", "Up")
        #print("Spiral CounterClockwise Up:", SpiralDetected)
        SpiralWanted = [(2, 1), (2, 0), (1, 0), (1, 1), (1, 2), (2, 2), (3, 2), (3, 1), (3, 0)]
        self.assertEqual(SpiralDetected, SpiralWanted)

                    ######### opposite direction
        SpiralDetected = spiral.spiral_from_coord(Mark["Coords"], (2, 1), "Clockwise", "Up")
        SpiralWanted = [(2, 1), (2, 0), (3, 0), (3, 1), (3, 2), (2, 2), (1, 2), (1, 1), (1, 0)]
        self.assertEqual(SpiralDetected, SpiralWanted)
        # print("Spiral clockwise, up:", SpiralDetected)

        ############# MAX tests ###################################
        SpiralMax = spiral.spiral_max_from_coord(Mark["Coords"], (2, 1))
        SpiralWanted = [(2, 1), (2, 2), (1, 2), (1, 1), (1, 0), (2, 0), (3, 0),
                        (3, 1), (3, 2), (3, 3), (2, 3), (1, 3), (0, 3)]
        self.assertEqual(SpiralMax, SpiralWanted)
        # print("SpiralMax:", SpiralMax)

        SpiralMax = spiral.spiral_max_from_coord(Mark["Coords"], (2, 2))
        SpiralWanted = [(2, 2), (2, 1), (1, 1), (1, 2), (1, 3), (2, 3), (3, 3), (3, 2), (3, 1), (3, 0),
                        (2, 0), (1, 0), (0, 0), (0, 1)]
        self.assertEqual(SpiralMax, SpiralWanted)
        # print("SpiralMax:", SpiralMax)

    def spirals_letter_e(self): return {
            (1, 5): [(1, 5), (1, 6), (2, 6), (2, 5), (2, 4), (1, 4), (0, 4), (0, 5), (0, 6), (0, 7), (1, 7), (2, 7), (3, 7), (3, 6), (3, 5), (3, 4), (3, 3), (2, 3), (1, 3)],
            (12, 5): [(12, 5), (12, 6), (11, 6), (11, 5), (11, 4), (12, 4), (13, 4), (13, 5), (13, 6), (13, 7), (12, 7), (11, 7), (10, 7), (10, 6), (10, 5), (10, 4), (10, 3), (11, 3), (12, 3)],
            (4, 12): [(4, 12), (5, 12), (5, 13), (4, 13), (3, 13), (3, 12), (3, 11), (4, 11), (5, 11), (6, 11), (6, 12), (6, 13), (6, 14), (5, 14), (4, 14)],
            (6, 1): [(6, 1), (5, 1), (5, 2), (6, 2), (7, 2), (7, 1), (7, 0), (6, 0), (5, 0), (4, 0), (4, 1), (4, 2), (4, 3), (5, 3)],
            (9, 13): [(9, 13), (10, 13), (10, 12), (9, 12), (8, 12), (8, 13), (8, 14), (9, 14), (10, 14), (11, 14), (11, 13), (11, 12), (11, 11), (10, 11)],
            (9, 1): [(9, 1), (9, 2), (10, 2), (10, 1), (10, 0), (9, 0), (8, 0), (8, 1), (8, 2), (8, 3), (9, 3)],
            (1, 9): [(1, 9), (1, 10), (0, 10), (0, 9), (0, 8), (1, 8), (2, 8), (2, 9), (2, 10), (2, 11), (1, 11)],
            (5, 6): [(5, 6), (6, 6), (6, 7), (5, 7), (4, 7), (4, 6)],
            (8, 6): [(8, 6), (9, 6), (9, 7), (8, 7), (7, 7), (7, 6)],
            (2, 1): [(2, 1), (3, 1), (3, 2), (2, 2), (1, 2)],
            (11, 1): [(11, 1), (11, 2), (12, 2)],
            (1, 12): [(1, 12), (2, 12), (2, 13)],
            (3, 9): [(3, 9), (3, 10)],
            (12, 11): [(12, 11), (12, 12)],
            (7, 12): [(7, 12), (7, 13)],
            (12, 13): [(12, 13)],
            (7, 14): [(7, 14)]
        }

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
        SpiralsInMark = spiral.spiral_nonoverlap_search_in_mark(MarkGenerated)
        # for CoordStart, CoordsSpiral in SpiralsInMark.items():
        #     print("SpiralStart ", CoordStart, " -> ", CoordsSpiral)

        SpiralsWanted = self.spirals_letter_e()
        self.assertEqual(SpiralsInMark, SpiralsWanted)
        spiral.spirals_display(Prg, SpiralsInMark, MarkGenerated["Width"], MarkGenerated["Height"], SleepTime=0.01, Prefix="  ", PauseAtEnd=0, SaveAsFilename="Spiral_test_spiral_nonoverlap_search_in_mark__letter_e.txt")
        #print("\n" + vector.block_to_string(MarkGenerated, BlocksInMark, Prefix=" ") + "\n")

    def test_spirals_find_neighbours(self):
        NeighboursDetected = spiral.spiral_find_neighbours(self.spirals_letter_e())
        print(NeighboursDetected)
        NeighboursWanted = {
                            (1, 5): [(2, 1), (6, 1), (5, 6), (1, 9)],
                            (1, 9): [(1, 12), (3, 9), (4, 12), (1, 5)],
                            (1, 12): [(4, 12), (1, 9)],
                            (2, 1): [(1, 5), (6, 1)],
                            (3, 9): [(1, 9), (4, 12)],
                            (4, 12): [(7, 12), (7, 14), (3, 9), (1, 9), (1, 12)],
                            (5, 6): [(1, 5), (8, 6)],
                            (6, 1): [(2, 1), (1, 5), (9, 1)],
                            (7, 12): [(4, 12), (9, 13)],
                            (7, 14): [(4, 12), (7, 12), (9, 13)],
                            (8, 6): [(5, 6), (12, 5)],
                            (9, 1): [(12, 5), (6, 1), (11, 1)],
                            (9, 13): [(12, 11), (12, 13), (7, 12), (7, 14)],
                            (11, 1): [(12, 5), (9, 1)], (12, 11): [(9, 13)],
                            (12, 13): [(9, 13), (12, 11)],
                            (12, 5): [(11, 1), (9, 1), (8, 6)]
        }
        self.assertEqual(NeighboursDetected, NeighboursWanted)

    # TODO: now you know the connections. understand the vectors to identify the letters


def run_all_tests(P):
    print("run all tests: Vector")
    global Prg
    Prg = P
    unittest.main(module="test_spiral", verbosity=2, exit=False)
