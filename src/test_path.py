# -*- coding: utf-8 -*-
import unittest, spiral, paths, util_test, util, char, mark_util

class PathTests(util_test.DeepCopyTest):
    def test_find_all_possible_path_from_one_Spiral_basic(self):
        Char, CharWidth, MarkChar = util_test.Data("char_minus_string")
        MarkGenerated = mark_util.mark_from_string(Char, CharWidth, MarkChar, Caller="test_find_all_possible_path_from_one_Spiral_basic")

        Spirals = spiral.spirals_nonoverlap_search_in_mark(MarkGenerated)
        # util.dict_with_lists_display_simple_data(Spirals, "find all path, basic, Spirals:")
        NeighboursDetected = spiral.neighbours_find_for_all_spirals(Spirals)
        util.dict_with_lists_display_simple_data(NeighboursDetected, "NeighboursDetected in Spirals")
        # FIXME: CONTINUE FROM HERE
        # i select one elem from Spirals, manually
        # Coord = list(Spirals.keys())[0]

    def test_path_find_next_spirals(self):
        Spirals = util_test.Data("char_e_spirals")
        util.dict_with_lists_display_simple_data(Spirals, Title="Spirals:")
        Coord = list(Spirals.keys())[0]
        NeighboursDetected = spiral.neighbours_find_for_all_spirals(Spirals)
        PathAll, PathLongest = paths.find_all_possible_path_from_one_Spiral([Coord], NeighboursDetected, Spirals)
        PathWanted = [{'PathTotalPointNumber': 24, 'Path': [(1, 5), (2, 1)]},
                      {'PathTotalPointNumber': 38, 'Path': [(1, 5), (2, 1), (6, 1)]}]
        self.assertEqual(PathAll[:2], PathWanted)
        self.assertEqual(PathLongest["PathTotalPointNumber"], 83)
        print("\nPathLongest, avoid is empty:", PathLongest)
        print("===============")
        Skipped = [(6, 1)]
        PathAll, PathLongest = paths.find_all_possible_path_from_one_Spiral([Coord], NeighboursDetected, Spirals, SpiralsSkippedAvoidThem=Skipped)
        PathWanted = [{'PathTotalPointNumber': 24, 'Path': [(1, 5), (2, 1)]},
                      {'PathTotalPointNumber': 25, 'Path': [(1, 5), (5, 6)]}]
        self.assertEqual(PathAll[:2], PathWanted)
        self.assertEqual(PathLongest["PathTotalPointNumber"], 68)
        print("PathLongest Skip " + str(Skipped) + " spirals:", PathLongest)



    # TODO: now you know the connections. understand the vectors to identify the letters
    def test_find_spiral_with_longest_summarised_pathA_and_PathB(self):
        print("")
        Spirals = util_test.Data("char_e_spirals")
        SpiralWithMaxLen_AB_1, MaxLen1, PathTotal1 = paths.find_spiral_with_longest_summarised_pathA_and_PathB(Spirals)
        self.assertEqual(MaxLen1, 132)
        self.assertEqual(SpiralWithMaxLen_AB_1, (1, 5))
        print("Spiral1 with longest Path B->Spiral1->A: ", SpiralWithMaxLen_AB_1, MaxLen1, PathTotal1)

        SpiralsUsed = list(PathTotal1["Path"])
        print("SpiralsUsed:", SpiralsUsed)
        for Spiral in Spirals:
            if Spiral not in SpiralsUsed:
                print("Spiral is not used: ", Spiral)
                # pass

        SpiralWithMaxLen_AB_2, MaxLen2, PathTotal2 = paths.find_spiral_with_longest_summarised_pathA_and_PathB(Spirals, SpiralsUsed=SpiralsUsed)
        print("Spiral2 with longest Path B->Spiral2->A: ", SpiralWithMaxLen_AB_2, MaxLen2, PathTotal2)

        char.path_in_char_to_svg(self.Prg, [PathTotal1["Path"], PathTotal2["Path"]], Spirals)

def run_all_tests(Prg):
    print("run all tests: Vector")
    PathTests.Prg = Prg
    unittest.main(module="test_path", verbosity=2, exit=False)
