# -*- coding: utf-8 -*-
import unittest, mark_util, area

class Area(unittest.TestCase):
    def test_fire_from_side(self):
        Bg = mark_util.MarkBg
        Fg = mark_util.MarkFg
        Width = 6
        Height = 5
        Area = area.make_empty(Width, Height, Bg)

        # this is a ⊃  math sign, more or less :-)
        Area[2][1] = Fg;    Area[3][1] = Fg;   Area[4][1] = Fg
        pass;                                  Area[4][2] = Fg
        Area[2][3] = Fg;    Area[3][3] = Fg;   Area[4][3] = Fg

        area.fire_from_side(Area, "Right", [Fg])
        print("\n" + area.to_string(Area))

        Wanted = ("FFFFFF"
                  "FFOOOF"
                  "FF..OF"
                  "FFOOOF"
                  "FFFFFF")

        self.assertEqual(Wanted, area.to_string(Area, OneLine=True))

    def test_fire(self):
        Bg = mark_util.MarkBg
        Fg = mark_util.MarkFg
        Width = 4
        Height = 5
        Area = area.make_empty(Width, Height, Bg)
        AreaDuplicated = area.duplicate(Area) # later we modify Area with burning
        Burning = [(1,1), (2,3)]
        area.fire(Area, Burning, [Fg], ["Left"])

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
        area.fire(Area2, Burning, [Fg, "X"], ["Up"])
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
