# -*- coding: utf-8 -*-
import unittest, spiral, path, util_test, util, char

class PathTests(unittest.TestCase):
    def test_path_find_next_spirals(self):
        Spirals = util_test.spirals_letter_e()
        util.dict_with_lists_display_simple_data(Spirals, Title="Spirals:")
        Coord = list(Spirals.keys())[0]
        NeighboursDetected = spiral.neighbours_find_for_all_spirals(Spirals)
        PathAll, PathLongest = path.find_all_possible_path_from_one_Spiral([Coord], NeighboursDetected, Spirals)
        PathWanted = [{'PathTotalPointNumber': 24, 'Path': [(1, 5), (2, 1)]},
                      {'PathTotalPointNumber': 38, 'Path': [(1, 5), (2, 1), (6, 1)]}]
        self.assertEqual(PathAll[:2], PathWanted)
        self.assertEqual(PathLongest["PathTotalPointNumber"], 83)
        print("\nPathLongest, avoid is empty:", PathLongest)
        print("===============")
        Skipped = [(6, 1)]
        PathAll, PathLongest = path.find_all_possible_path_from_one_Spiral([Coord], NeighboursDetected, Spirals, SpiralsSkippedAvoidThem=Skipped)
        PathWanted = [{'PathTotalPointNumber': 24, 'Path': [(1, 5), (2, 1)]},
                      {'PathTotalPointNumber': 25, 'Path': [(1, 5), (5, 6)]}]
        self.assertEqual(PathAll[:2], PathWanted)
        self.assertEqual(PathLongest["PathTotalPointNumber"], 68)
        print("PathLongest Skip " + str(Skipped) + " spirals:", PathLongest)



    # TODO: now you know the connections. understand the vectors to identify the letters
    def test_find_spiral_with_longest_summarised_pathA_and_PathB(self):
        print("")
        Spirals = util_test.spirals_letter_e()
        SpiralWithMaxLen_AB_1, MaxLen1, PathTotal1 = path.find_spiral_with_longest_summarised_pathA_and_PathB(Spirals)
        self.assertEqual(MaxLen1, 132)
        self.assertEqual(SpiralWithMaxLen_AB_1, (1, 5))
        print("Spiral1 with longest Path B->Spiral1->A: ", SpiralWithMaxLen_AB_1, MaxLen1, PathTotal1)

        SpiralsUsed = list(PathTotal1["Path"])
        print("SpiralsUsed:", SpiralsUsed)
        # for Spiral in Spirals:
        #     if Spiral not in SpiralsUsed:
        #         # print("Spiral is not used: ", Spiral)
        #         pass

        SpiralWithMaxLen_AB_2, MaxLen2, PathTotal2 = path.find_spiral_with_longest_summarised_pathA_and_PathB(Spirals, SpiralsUsed=SpiralsUsed)
        print("Spiral2 with longest Path B->Spiral2->A: ", SpiralWithMaxLen_AB_2, MaxLen2, PathTotal2)

        char.path_in_char_to_svg(Prg, [PathTotal1["Path"], PathTotal2["Path"]], Spirals)



def run_all_tests(P):
    print("run all tests: Vector")
    global Prg
    Prg = P
    unittest.main(module="test_path", verbosity=2, exit=False)
