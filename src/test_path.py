# -*- coding: utf-8 -*-
import unittest, spiral, path, util_test

class PathTests(unittest.TestCase):
    def test_path_find_next_spirals(self):
        Spirals = util_test.spirals_letter_e()
        Coord=list(Spirals.keys())[0]
        NeighboursDetected = spiral.find_neighbours(Spirals)
        PathAll, PathLongest = path.find_all_possible_path_from_one_Spiral([Coord], NeighboursDetected, Spirals)
        PathWanted = [{'PathTotalPointNumber': 24, 'Path': [(1, 5), (2, 1)]},
                      {'PathTotalPointNumber': 38, 'Path': [(1, 5), (2, 1), (6, 1)]}]
        self.assertEqual(PathAll[:2], PathWanted)
        self.assertEqual(PathLongest["PathTotalPointNumber"], 83)
        print("PathLongest, avoid is empty:", PathLongest)
        print("===============")
        PathAll, PathLongest = path.find_all_possible_path_from_one_Spiral([Coord], NeighboursDetected, Spirals, SpiralsSkippedAvoidThem=[(6, 1)])
        PathWanted = [{'PathTotalPointNumber': 24, 'Path': [(1, 5), (2, 1)]},
                      {'PathTotalPointNumber': 25, 'Path': [(1, 5), (5, 6)]}]
        self.assertEqual(PathAll[:2], PathWanted)
        self.assertEqual(PathLongest["PathTotalPointNumber"], 68)
        print("PathLongest Skip spirals:", PathLongest)



    # TODO: now you know the connections. understand the vectors to identify the letters
    def test_spiral_find_path_in_char(self):
        path.find_longest_path_with_unused_spirals(util_test.spirals_letter_e())
        # Path = spiral.find_path_in_char_with_spirals(util_test.spirals_letter_e(), ReturnObj="SimpleSpirals")
        # print("Path neighbours:", Path)
        # char.neighbours_to_svg(Prg, Path, util_test.spirals_letter_e(), Fname="test_spiral_find_path_in_char.html")

def run_all_tests(P):
    print("run all tests: Vector")
    global Prg
    Prg = P
    unittest.main(module="test_path", verbosity=2, exit=False)
