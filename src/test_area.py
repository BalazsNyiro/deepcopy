import unittest, mark_util, area


class Area(unittest.TestCase):

    def test_fire(self):
        Bg = mark_util.MarkBg
        Fg = mark_util.MarkFg
        Width = 4
        Height = 5
        Area = area.make_empty(Width, Height, Bg)
        AreaDuplicated = area.duplicate(Area) # later we modify Area with burning
        Burning = [(1,1), (2,3)]
        area.fire(Area, Burning, ["Left"], [Fg])

        Wanted = ("...."
                  "FF.."
                  "...."
                  "FFF."
                  "....")

        self.assertEqual(Wanted, area.to_string(Area, OneLine=True))

        # The duplicated Area is independent from burning Area, made with deepcopy
        # the duplicated area has to be emtpy, like a new empty area.
        # area is a complex struct, and we made a real duplication, not a shallow copy
        self.assertEqual(area.to_string(area.make_empty(Width, Height, Bg)), area.to_string(AreaDuplicated))


        ##########################################
        Area2 = area.make_empty(Width, Height, Bg)
        Area2[2][1] = "X"
        Burning = [(1,1), (2,3)]
        area.fire(Area2, Burning, ["Up"], [Fg, "X"])
        Wanted = (".F.."
                  ".FX."
                  "..F."
                  "..F."
                  "....")

        self.assertEqual(Wanted, area.to_string(Area2, OneLine=True))

    def test_width_height_get(self):
        Bg = mark_util.MarkBg
        Area = area.make_empty(5, 6, Bg)
        WidthHeight = area.width_height_get(Area)
        self.assertEqual(WidthHeight, (5,6))

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
