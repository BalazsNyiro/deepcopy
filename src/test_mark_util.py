import unittest, mark_collect, mark_util, mark_parse

import area


class MarkUtil(unittest.TestCase):


    # this is a developer tool to check the status
    # of marks, display informations about them
    def test_marks_info_table(self):
        FilePathImg = ["test", "test_mark_finding_word_the__font_ubuntu_24pt.png"]
        Marks = mark_collect.mark_collect_from_img_file(Prg, FilePathImg)

        MarkParserFuns = [mark_parse.mark_info_basic,
                          mark_parse.mark_area_convex,
                          mark_parse.mark_area_select_closed_empty_area
                          ] # these functions analyses the Marks one by one
        print(mark_util.marks_info_table(Prg, Marks, MarkParserFuns=MarkParserFuns,
                                         WantedIdNums=[0, 2, 3], OutputType="txt"))

        self.assertTrue(True)

    def test_mark_to_string(self):
        Mark = {"Coords":{(3,3):1, (4,3):1, (5,3):1,
                                   (4,4):1,
                          (3,5):1, (4,5):1          }, "Width":3, "Height":3, "Xmin":3, "Ymin":3, "Xmax":5, "Ymax":5}

        Wanted = ( "OOO\n"
                   ".O.\n"
                   "OO."  )
        self.assertEqual(Wanted, mark_util.mark_to_string(Prg, Mark))

    def test_markstats_insert_id(self):
        MarkStats = dict()
        mark_util.markstats_insert_id(MarkStats, 1)
        self.assertTrue(1 in MarkStats)


    def test_mark_area_convex(self):
        Mark = {"Coords":{(1,1):1, (2,2):2, (3,3):3, (1,3):4}, "Width":3, "Height":3, "Xmin":1, "Ymin":1, "Xmax":3, "Ymax":3}
        AreaConvexGenerated = mark_util.mark_area_convex(Prg, Mark)
        AreaWanted = ("O..\n"
                      "OO.\n"
                      "OOO")
        self.assertEqual(AreaWanted, area.to_string(AreaConvexGenerated))

        ####################################
        Mark = {"Coords":
                {(1,1):11, (2,1):21, (3,1):31,
                 (1,2):12,
                 (1,3):13,
                 (1,4):14,
                 (1,5):15, (2,5):25, (3,5):35, (4,5):45, (5,5):55},
                "Width": 5, "Height": 5, "Xmin": 1, "Ymin": 1, "Xmax": 5, "Ymax": 5
                }

        AreaConvexGenerated = mark_util.mark_area_convex(Prg, Mark)
        AreaWanted = ("OOO..\n"
                      "OOOO.\n"
                      "OOOO.\n"
                      "OOOO.\n"
                      "OOOOO" )
        self.assertEqual(AreaWanted, area.to_string(AreaConvexGenerated))

        ################## + sign convex area test ###################

        Mark = {"Coords":
                   {                       (3,2): 32,
                                           (3,3): 33,
                                           (3,4): 34,
            (0,5):5, (1,5): 15, (2,5): 25, (3,5): 35, (4,5): 45, (5,5): 55, (6,5):65,
                                           (3,6): 36,
                                           (3,7): 37,
                                           (3,8): 38
            },
            "Width": 7, "Height": 7, "Xmin": 0, "Ymin": 2, "Xmax": 6, "Ymax": 8
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
        self.assertEqual(AreaWanted, area.to_string(AreaConvexGenerated))

def run_all_tests(P):
    print("run all tests")
    global Prg
    Prg = P
    # exec all test:
    unittest.main(module="test_mark_util", verbosity=2, exit=False)
    # unittest.main(TestMethodsAnalysed())
