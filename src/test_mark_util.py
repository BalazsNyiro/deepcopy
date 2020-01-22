import unittest, mark_collect, mark_util, mark_parse


class MarkUtil(unittest.TestCase):

    # this is a developer tool to check the status
    # of marks, display informations about them
    def test_marks_info_table(self):
        FilePathImg = ["test", "test_mark_finding_word_the__font_ubuntu_24pt.png"]
        Marks = mark_collect.mark_collect_from_img_file(Prg, FilePathImg)

        MarkParserFuns = [mark_parse.mark_width_height] # these functions analyses the Marks one by one
        print(mark_util.marks_info_table(Prg, Marks, MarkParserFuns=MarkParserFuns,
                                         WantedIdNums=[2, 3], OutputType="txt"))

        self.assertTrue(True, True)


def run_all_tests(P):
    print("run all tests")
    global Prg
    Prg = P
    # exec all test:
    unittest.main(module="test_mark_util", verbosity=2, exit=False)
    # unittest.main(TestMethodsAnalysed())
