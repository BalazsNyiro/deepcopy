# -*- coding: utf-8 -*-
import unittest, mark_util, area

class Area(unittest.TestCase):
    def test_count_separated_blocks(self):
        Bg = mark_util.MarkBg
        Fg = mark_util.MarkFg
        Width = 6
        Height = 9

        Area = area.make_empty(Width, Height, Bg)

        # this is a '8' char
        Area[2][1] = Fg;    Area[3][1] = Fg;   Area[4][1] = Fg
        Area[2][2] = Fg;                       Area[4][2] = Fg
        Area[2][3] = Fg;    Area[3][3] = Fg;   Area[4][3] = Fg
        Area[2][4] = Fg;                       Area[4][4] = Fg
        Area[2][5] = Fg;    Area[3][5] = Fg;   Area[4][5] = Fg

        # the correct result is 3 because the there are an outside block
        # with Bg and two inside block

        CharsBlocking =  [Fg]
        BlockVolume, BlockSizes = area.count_separated_blocks(Area, Bg, CharsBlocking)
        self.assertEqual(3, BlockVolume)
        self.assertEqual({(0, 0): 39, (3, 2): 1, (3, 4): 1}, BlockSizes)

        # we rease the outside block
        BurntAreaSize = area.fire(Area, [(0,0)], CharsBlocking)
        BlockVolume, BlockSizes = area.count_separated_blocks(Area, Bg, CharsBlocking)
        self.assertEqual(2, BlockVolume)
        self.assertEqual(39, BurntAreaSize)
        self.assertEqual({(3, 2): 1, (3, 4): 1}, BlockSizes)

        # then we erase one of the inside blocks
        area.fire(Area, [(3,2)], CharsBlocking)
        BlockVolume, BlockSizes = area.count_separated_blocks(Area, Bg, CharsBlocking)
        self.assertEqual(1, BlockVolume)
        self.assertEqual({(3, 4): 1}, BlockSizes)

    def test_pattern_position_find(self):
        Bg = mark_util.MarkBg
        Width = 6
        Height = 7
        Area = area.make_empty(Width, Height, Bg)
        Area[4][3] = "Y"
        Area[5][4] = "Y"

        Pos = area.pattern_position_find_first(Area, "Y")
        self.assertEqual(Pos, (4,3))

        Pos = area.pattern_position_find_first(Area, "U")
        self.assertEqual(Pos, None)


    def test_pattern_count(self):
        Bg = mark_util.MarkBg
        Width = 2
        Height = 3
        Area = area.make_empty(Width, Height, Bg)
        Area[1][2] = "X"

        CountedChars = area.pattern_count(Area, WantedPatterns=[Bg, "X"])
        WantedResult = {".": 5, "X":1, "Coords": {".": [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1)], "X":[(1,2)]}}
        self.assertEqual(CountedChars, WantedResult)

        CountedChars = area.pattern_count(Area, UnwantedPatterns=["Y"])
        self.assertEqual(CountedChars, WantedResult)

    def test_fire_from_side(self):
        Bg = mark_util.MarkBg
        Fg = mark_util.MarkFg
        Width = 6
        Height = 5

        ########### Test from Right #############################
        Area = area.make_empty(Width, Height, Bg)

        # this is a ⊃  math sign, more or less :-)
        Area[2][1] = Fg;    Area[3][1] = Fg;   Area[4][1] = Fg
        pass;                                  Area[4][2] = Fg
        Area[2][3] = Fg;    Area[3][3] = Fg;   Area[4][3] = Fg

        BurntAreaSize = area.fire_from_side(Area, "Right", [Fg])

        Wanted = ("FFFFFF"
                  "FFOOOF"
                  "FF..OF"
                  "FFOOOF"
                  "FFFFFF")

        self.assertEqual(Wanted, area.to_string(Area, OneLine=True))
        self.assertEqual(21, BurntAreaSize)

        ########### Test from Left#############################
        Area = area.make_empty(Width, Height, Bg)

        # stylized I sign
        Area[2][1] = Fg;    Area[3][1] = Fg;   Area[4][1] = Fg
        pass;               Area[3][2] = Fg
        Area[2][3] = Fg;    Area[3][3] = Fg;   Area[4][3] = Fg

        area.fire_from_side(Area, "Left", [Fg])

        Wanted = ("FFFFFF"
                  "FFOOOF"
                  "FFFO.F"
                  "FFOOOF"
                  "FFFFFF")

        self.assertEqual(Wanted, area.to_string(Area, OneLine=True))


        ########### Test from Top #############################
        Width = 5
        Height = 5

        Area = area.make_empty(Width, Height, Bg)
        Area[0][1] = Fg
        Area[1][1] = Fg
        Area[2][1] = Fg
        Area[3][1] = Fg
        Area[4][1] = Fg

        area.fire_from_side(Area, "Top", [Fg])

        Wanted = ("FFFFF"
                  "OOOOO"
                  "....."
                  "....."
                  ".....")

        self.assertEqual(Wanted, area.to_string(Area, OneLine=True))



        ########### Test from Bottom #############################
        Width = 5
        Height = 5

        Area = area.make_empty(Width, Height, Bg)
        Area[0][1] = Fg
        Area[1][1] = Fg
        Area[2][1] = Fg
        Area[3][1] = Fg
        Area[4][1] = Fg

        area.fire_from_side(Area, "Bottom", [Fg])

        Wanted = ("....."
                  "OOOOO"
                  "FFFFF"
                  "FFFFF"
                  "FFFFF")

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
