import unittest, mark_collect, mark_util, mark_parse


class MarkUtil(unittest.TestCase):


    # this is a developer tool to check the status
    # of marks, display informations about them
    def test_marks_info_table(self):
        FilePathImg = ["test", "test_mark_finding_word_the__font_ubuntu_24pt.png"]
        Marks = mark_collect.mark_collect_from_img_file(Prg, FilePathImg)

        MarkParserFuns = [mark_parse.mark_info_basic, mark_parse.mark_convex_area] # these functions analyses the Marks one by one
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

        Wanted = "OOO\n" + \
                 ".O.\n" + \
                 "OO."
        self.assertEqual(Wanted, mark_util.mark_to_string(Prg, Mark))

    def test_markstats_insert_id(self):
        MarkStats = dict()
        mark_util.markstats_insert_id(MarkStats, 1)
        self.assertTrue(1 in MarkStats)

    def test_mark_area_to_string(self):
        Bg = mark_util.MarkBg
        # there are two columns in the Area
        Area = [    [Bg,
                     Bg,
                     Bg], [Bg,
                           Bg,
                           Bg]]
        Wanted = "..\n..\n.."
        self.assertEqual(Wanted, mark_util.mark_area_to_string(Area))

    def test_mark_area_empty_making(self):
        Result = mark_util.mark_area_empty_making(2, 3)
        Bg = mark_util.MarkBg
        WantedColumn = [Bg, Bg, Bg]
        WantedRows = [WantedColumn, WantedColumn]
        self.assertEqual(WantedRows, Result)


def run_all_tests(P):
    print("run all tests")
    global Prg
    Prg = P
    # exec all test:
    unittest.main(module="test_mark_util", verbosity=2, exit=False)
    # unittest.main(TestMethodsAnalysed())
