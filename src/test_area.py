import unittest, mark_util, area


class Area(unittest.TestCase):

    def test_area_coord_insert(self):
        Bg = mark_util.MarkBg
        Fg = mark_util.MarkFg
        Area = area.make_empty(5, 6, Bg)
        Mark = {(1,1):1, (2,2):2, (3,3):3, (1,3):4}
        area.coords_insert(Area, Mark, Fg, Xshift=1, Yshift=1)
        Wanted = (  ".....\n"
                    ".....\n"
                    "..O..\n"
                    "...O.\n"
                    "..O.O\n"
                    "....."  )
        self.assertEqual(Wanted, area.to_string(Area))

    def test_area_to_string(self):
        Bg = mark_util.MarkBg
        Fg = mark_util.MarkFg
        # there are two columns in the Area
        Area = [[Bg,
                 Bg,
                 Bg], [Bg,
                       Fg,
                       Bg]]
        Wanted = "..\n.O\n.."
        self.assertEqual(Wanted, area.to_string(Area))

    def test_mark_area_empty_making(self):
        Bg = mark_util.MarkBg
        Result = area.make_empty(2, 3, Bg)
        WantedColumn = [Bg, Bg, Bg]
        WantedRows = [WantedColumn, WantedColumn]
        self.assertEqual(WantedRows, Result)

def run_all_tests(P):
    print("run all tests")
    global Prg
    Prg = P
    unittest.main(module="test_area", verbosity=2, exit=False)
