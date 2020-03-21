# -*- coding: utf-8 -*-
import unittest, spiral, mark_util, char, util_test

class SpiralTests(unittest.TestCase):
    def test_spiral_from_coord(self):
        Letter = ("OOOO"
                  "OOOO"
                  " OOO"
                  "OOOO")
        Mark = mark_util.mark_from_string(Letter, 4, "O")
        # print(Mark)

        ######### DOWN: #################
        SpiralDetected = spiral._spiral_coords_list_from_coord(Mark["Coords"], (2, 1), "CounterClockwise", "Down")
        #print("Spiral CounterClockwise Down:", SpiralDetected)
        SpiralWanted = [(2, 1), (2, 2), (3, 2), (3, 1), (3, 0),
                        (2, 0), (1, 0), (1, 1), (1, 2), (1, 3), (2, 3), (3, 3)]
        self.assertEqual(SpiralDetected, SpiralWanted)

                    ######### opposite direction
        SpiralDetected = spiral._spiral_coords_list_from_coord(Mark["Coords"], (2, 1), "Clockwise", "Down")
        #print("Spiral Clockwise, Down:", SpiralDetected)
        SpiralWanted = [(2, 1), (2, 2), (1, 2), (1, 1), (1, 0), (2, 0),
                        (3, 0), (3, 1), (3, 2), (3, 3), (2, 3), (1, 3), (0, 3)]
        self.assertEqual(SpiralDetected, SpiralWanted)

        ##################### UP ###########################################
        SpiralDetected = spiral._spiral_coords_list_from_coord(Mark["Coords"], (2, 1), "CounterClockwise", "Up")
        #print("Spiral CounterClockwise Up:", SpiralDetected)
        SpiralWanted = [(2, 1), (2, 0), (1, 0), (1, 1), (1, 2), (2, 2), (3, 2), (3, 1), (3, 0)]
        self.assertEqual(SpiralDetected, SpiralWanted)

                    ######### opposite direction
        SpiralDetected = spiral._spiral_coords_list_from_coord(Mark["Coords"], (2, 1), "Clockwise", "Up")
        SpiralWanted = [(2, 1), (2, 0), (3, 0), (3, 1), (3, 2), (2, 2), (1, 2), (1, 1), (1, 0)]
        self.assertEqual(SpiralDetected, SpiralWanted)
        # print("Spiral clockwise, up:", SpiralDetected)

        ############# MAX tests ###################################
        SpiralMax = spiral._spiral_max_coords_list_from_coord(Mark["Coords"], (2, 1))
        SpiralWanted = [(2, 1), (2, 2), (1, 2), (1, 1), (1, 0), (2, 0), (3, 0),
                        (3, 1), (3, 2), (3, 3), (2, 3), (1, 3), (0, 3)]
        self.assertEqual(SpiralMax, SpiralWanted)
        # print("SpiralMax:", SpiralMax)

        SpiralMax = spiral._spiral_max_coords_list_from_coord(Mark["Coords"], (2, 2))
        SpiralWanted = [(2, 2), (2, 1), (1, 1), (1, 2), (1, 3), (2, 3), (3, 3), (3, 2), (3, 1), (3, 0),
                        (2, 0), (1, 0), (0, 0), (0, 1)]
        self.assertEqual(SpiralMax, SpiralWanted)
        # print("SpiralMax:", SpiralMax)

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

        SpiralsWanted = util_test.spirals_letter_e()
        self.assertEqual(SpiralsInMark, SpiralsWanted)

        # Beautiful spiral drawing in Linux terminal (unicode)
        # spiral.spirals_display(Prg, SpiralsInMark, MarkGenerated["Width"], MarkGenerated["Height"], SleepTime=0.01, Prefix="  ", PauseAtEnd=0, SaveAsFilename="Spiral_test_spiral_nonoverlap_search_in_mark__letter_e.txt")

    def test_spirals_find_neighbours(self):
        NeighboursDetected = spiral.find_neighbours(util_test.spirals_letter_e())
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
                            (11, 1): [(12, 5), (9, 1)],
                            (12, 5): [(11, 1), (9, 1), (8, 6)],
                            (12, 11): [(9, 13)],
                            (12, 13): [(9, 13), (12, 11)]
        }
        self.assertEqual(NeighboursDetected, NeighboursWanted)
        char.neighbours_to_svg(Prg, NeighboursDetected, util_test.spirals_letter_e(), Fname="test_spirals_find_neighbours.html")

    def test_spiral_sort_neighbours_by_len(self):
        Spirals = util_test.spirals_letter_e()
        NeighboursDetected = spiral.find_neighbours(Spirals)
        NeighboursSorted = spiral._sort_neighbours_by_len(Spirals, NeighboursDetected)
        # util.dict_display_simple_data(NeighboursSorted, "test_spiral_sort_neighbours_by_len")
        Wanted = [{'Len': 1, 'Spiral': (12, 13)}, {'Len': 1, 'Spiral': (7, 14)}, {'Len': 2, 'Spiral': (12, 11)}, {'Len': 2, 'Spiral': (7, 12)}, {'Len': 2, 'Spiral': (3, 9)}, {'Len': 3, 'Spiral': (11, 1)}, {'Len': 3, 'Spiral': (1, 12)}, {'Len': 5, 'Spiral': (2, 1)}, {'Len': 6, 'Spiral': (8, 6)}, {'Len': 6, 'Spiral': (5, 6)}, {'Len': 11, 'Spiral': (9, 1)}, {'Len': 11, 'Spiral': (1, 9)}, {'Len': 14, 'Spiral': (9, 13)}, {'Len': 14, 'Spiral': (6, 1)}, {'Len': 15, 'Spiral': (4, 12)}, {'Len': 19, 'Spiral': (12, 5)}, {'Len': 19, 'Spiral': (1, 5)}]
        self.assertEqual(NeighboursSorted, Wanted)

def run_all_tests(P):
    print("run all tests: Vector")
    global Prg
    Prg = P
    unittest.main(module="test_spiral", verbosity=2, exit=False)
