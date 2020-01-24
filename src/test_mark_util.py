import unittest, mark_collect, mark_util, mark_parse


class MarkUtil(unittest.TestCase):


    # this is a developer tool to check the status
    # of marks, display informations about them
    def test_marks_info_table(self):
        FilePathImg = ["test", "test_mark_finding_word_the__font_ubuntu_24pt.png"]
        Marks = mark_collect.mark_collect_from_img_file(Prg, FilePathImg)

        MarkParserFuns = [mark_parse.mark_info_basic, mark_parse.mark_area_convex] # these functions analyses the Marks one by one
        print(mark_util.marks_info_table(Prg, Marks, MarkParserFuns=MarkParserFuns,
                                         WantedIdNums=[2, 3], OutputType="txt"))

        self.assertTrue(True)

    def test_mark_min_max_width_height(self):
        Mark = {(2,1):1, (4,3):1, (8,3):1,
                (4,4):1,
                (3,5):1, (4,6):1          }

        Result = mark_util.mark_min_max_width_height(Prg, Mark)
        Wanted = (2, 8, 1, 6, 7, 6)
        self.assertEqual(Result, Wanted)

    def test_mark_to_string(self):
        Mark = {(3,3):1, (4,3):1, (5,3):1,
                         (4,4):1,
                (3,5):1, (4,5):1          }

        Wanted = ( "OOO\n"
                   ".O.\n"
                   "OO."  )
        self.assertEqual(Wanted, mark_util.mark_to_string(Prg, Mark))

    def test_markstats_insert_id(self):
        MarkStats = dict()
        mark_util.markstats_insert_id(MarkStats, 1)
        self.assertTrue(1 in MarkStats)

    def test_mark_area_to_string(self):
        Bg = mark_util.MarkBg
        Fg = mark_util.MarkFg
        # there are two columns in the Area
        Area = [    [Bg,
                     Bg,
                     Bg], [Bg,
                           Fg,
                           Bg]]
        Wanted = "..\n.O\n.."
        self.assertEqual(Wanted, mark_util.mark_area_to_string(Area))

    def test_mark_area_empty_making(self):
        Result = mark_util.mark_area_empty_making(2, 3)
        Bg = mark_util.MarkBg
        WantedColumn = [Bg, Bg, Bg]
        WantedRows = [WantedColumn, WantedColumn]
        self.assertEqual(WantedRows, Result)

    def test_mark_area_convex(self):
        Mark = {(1,1):1, (2,2):2, (3,3):3, (1,3):4}
        AreaConvexGenerated = mark_util.mark_area_convex(Prg, Mark)
        AreaWanted = ("O..\n"
                      "OO.\n"
                      "OOO")
        self.assertEqual(AreaWanted, mark_util.mark_area_to_string(AreaConvexGenerated))

        ####################################
        Mark = {(1,1):11, (2,1):21, (3,1):31,
                (1,2):12,
                (1,3):13,
                (1,4):14,
                (1,5):15, (2,5):25, (3,5):35, (4,5):45, (5,5):55}

        AreaConvexGenerated = mark_util.mark_area_convex(Prg, Mark)
        AreaWanted = ("OOO..\n"
                      "OOO..\n"
                      "OOOO.\n"
                      "OOOO.\n"
                      "OOOOO" )
        self.assertEqual(AreaWanted, mark_util.mark_area_to_string(AreaConvexGenerated))

        ################## + sign convex area test ###################

        Mark = {                       (3,2): 32,
                                       (3,3): 33,
                                       (3,4): 34,
        (0,5):5, (1,5): 15, (2,5): 25, (3,5): 35, (4,5): 45, (5,5): 55, (6,5):65,
                                       (3,6): 36,
                                       (3,7): 37,
                                       (3,8): 38
        }
        AreaConvexGenerated = mark_util.mark_area_convex(Prg, Mark)
        AreaWanted = ("...O...\n"
                      "..OOO..\n"
                      ".OOOOO.\n"
                      "OOOOOOO\n"
                      ".OOOOO.\n"
                      "..OOO..\n"
                      "...O..."
                      )
        self.assertEqual(AreaWanted, mark_util.mark_area_to_string(AreaConvexGenerated))

def run_all_tests(P):
    print("run all tests")
    global Prg
    Prg = P
    # exec all test:
    unittest.main(module="test_mark_util", verbosity=2, exit=False)
    # unittest.main(TestMethodsAnalysed())
