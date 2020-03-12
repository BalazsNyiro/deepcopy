# -*- coding: utf-8 -*-
import unittest, spiral, mark_util, char, path

class VectorTests(unittest.TestCase):
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

    def spirals_letter_e(self): return {
        (1, 5): [(1, 5), (1, 6), (2, 6), (2, 5), (2, 4), (1, 4), (0, 4), (0, 5), (0, 6), (0, 7), (1, 7), (2, 7), (3, 7), (3, 6), (3, 5), (3, 4), (3, 3), (2, 3), (1, 3)],
        (1, 9): [(1, 9), (1, 10), (0, 10), (0, 9), (0, 8), (1, 8), (2, 8), (2, 9), (2, 10), (2, 11), (1, 11)],
        (1, 12): [(1, 12), (2, 12), (2, 13)],
        (2, 1): [(2, 1), (3, 1), (3, 2), (2, 2), (1, 2)],
        (3, 9): [(3, 9), (3, 10)],
        (4, 12): [(4, 12), (5, 12), (5, 13), (4, 13), (3, 13), (3, 12), (3, 11), (4, 11), (5, 11), (6, 11), (6, 12), (6, 13), (6, 14), (5, 14), (4, 14)],
        (5, 6): [(5, 6), (6, 6), (6, 7), (5, 7), (4, 7), (4, 6)],
        (6, 1): [(6, 1), (5, 1), (5, 2), (6, 2), (7, 2), (7, 1), (7, 0), (6, 0), (5, 0), (4, 0), (4, 1), (4, 2), (4, 3), (5, 3)],
        (7, 12): [(7, 12), (7, 13)],
        (7, 14): [(7, 14)],
        (8, 6): [(8, 6), (9, 6), (9, 7), (8, 7), (7, 7), (7, 6)],
        (9, 1): [(9, 1), (9, 2), (10, 2), (10, 1), (10, 0), (9, 0), (8, 0), (8, 1), (8, 2), (8, 3), (9, 3)],
        (9, 13): [(9, 13), (10, 13), (10, 12), (9, 12), (8, 12), (8, 13), (8, 14), (9, 14), (10, 14), (11, 14), (11, 13), (11, 12), (11, 11), (10, 11)],
        (11, 1): [(11, 1), (11, 2), (12, 2)],
        (12, 5): [(12, 5), (12, 6), (11, 6), (11, 5), (11, 4), (12, 4), (13, 4), (13, 5), (13, 6), (13, 7), (12, 7), (11, 7), (10, 7), (10, 6), (10, 5), (10, 4), (10, 3), (11, 3), (12, 3)],
        (12, 11): [(12, 11), (12, 12)],
        (12, 13): [(12, 13)]
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

        # Beautiful spiral drawing in Linux terminal (unicode)
        # spiral.spirals_display(Prg, SpiralsInMark, MarkGenerated["Width"], MarkGenerated["Height"], SleepTime=0.01, Prefix="  ", PauseAtEnd=0, SaveAsFilename="Spiral_test_spiral_nonoverlap_search_in_mark__letter_e.txt")

    def test_spirals_find_neighbours(self):
        NeighboursDetected = spiral.find_neighbours(self.spirals_letter_e())
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
        char.neighbours_to_svg(Prg, NeighboursDetected, self.spirals_letter_e(), Fname="test_spirals_find_neighbours.html")

    def test_spiral_sort_neighbours_by_len(self):
        Spirals = self.spirals_letter_e()
        NeighboursDetected = spiral.find_neighbours(Spirals)
        NeighboursSorted = spiral._sort_neighbours_by_len(Spirals, NeighboursDetected)
        # util.dict_display_simple_data(NeighboursSorted, "test_spiral_sort_neighbours_by_len")
        Wanted = [{'Len': 1, 'Spiral': (12, 13)}, {'Len': 1, 'Spiral': (7, 14)}, {'Len': 2, 'Spiral': (12, 11)}, {'Len': 2, 'Spiral': (7, 12)}, {'Len': 2, 'Spiral': (3, 9)}, {'Len': 3, 'Spiral': (11, 1)}, {'Len': 3, 'Spiral': (1, 12)}, {'Len': 5, 'Spiral': (2, 1)}, {'Len': 6, 'Spiral': (8, 6)}, {'Len': 6, 'Spiral': (5, 6)}, {'Len': 11, 'Spiral': (9, 1)}, {'Len': 11, 'Spiral': (1, 9)}, {'Len': 14, 'Spiral': (9, 13)}, {'Len': 14, 'Spiral': (6, 1)}, {'Len': 15, 'Spiral': (4, 12)}, {'Len': 19, 'Spiral': (12, 5)}, {'Len': 19, 'Spiral': (1, 5)}]
        self.assertEqual(NeighboursSorted, Wanted)

    def test_path_find_next_spirals(self):
        Spirals = self.spirals_letter_e()
        Coord=list(Spirals.keys())[0]
        NeighboursDetected = spiral.find_neighbours(Spirals)
        PathAll, PathLongest = path.find_all_possible_path([Coord], NeighboursDetected, Spirals)
        PathWanted = [{'PathTotalPointNumber': 24, 'Path': [(1, 5), (2, 1)]},
                      {'PathTotalPointNumber': 38, 'Path': [(1, 5), (2, 1), (6, 1)]}]
        self.assertEqual(PathAll[:2], PathWanted)
        self.assertEqual(PathLongest["PathTotalPointNumber"], 83)
        print("PathLongest, avoid is empty:", PathLongest)
        print("===============")
        PathAll, PathLongest = path.find_all_possible_path([Coord], NeighboursDetected, Spirals, SpiralsSkippedAvoidThem=[(6, 1)])
        PathWanted = [{'PathTotalPointNumber': 24, 'Path': [(1, 5), (2, 1)]},
                      {'PathTotalPointNumber': 25, 'Path': [(1, 5), (5, 6)]}]
        self.assertEqual(PathAll[:2], PathWanted)
        self.assertEqual(PathLongest["PathTotalPointNumber"], 68)
        print("PathLongest Skip spirals:", PathLongest)

    # TODO: now you know the connections. understand the vectors to identify the letters
    def test_spiral_find_path_in_char(self):
        Path = spiral.find_path_in_char_with_spirals(self.spirals_letter_e(), ReturnObj="SimpleSpirals")
        print("Path neighbours:", Path)
        char.neighbours_to_svg(Prg, Path, self.spirals_letter_e(), Fname="test_spiral_find_path_in_char.html")

def run_all_tests(P):
    print("run all tests: Vector")
    global Prg
    Prg = P
    unittest.main(module="test_spiral", verbosity=2, exit=False)
