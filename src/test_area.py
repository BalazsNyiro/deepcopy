# -*- coding: utf-8 -*-
import unittest, mark_util, area, util_test

class AreaProcessors(util_test.DeepCopyTest):
    def test_area_process_pixels(self):
        Bg = mark_util.MarkBg
        Fg = mark_util.MarkFg
        Width = 3
        Height = 2
        AreaA = area.make_empty(Width, Height, Bg)
        # P as point
        AreaA[0][0] = AreaA[0][1] = AreaA[1][0] = AreaA[1][1] = "P"

        AreaB = area.make_empty(Width, Height, Bg)
        AreaB[0][0] = AreaB[1][1] = Fg

        # the coordinate usage is important here, because process_pixels
        # loop over X,Y values and I want to test the fact of looping
        def processor_test(X, Y, _AreaA, _AreaB, AreaResult, _Fg, _Bg, Accumulator=None):
            AreaResult[X][Y] = X*10+Y

        AreaResult, _Acc = area.process_pixels(AreaA, AreaB, processor_test, Fg, Bg)
        Wanted = [ [0, 1], [10, 11], [20, 21] ]
        self.assertEqual(AreaResult, Wanted)

        # ========== TEST based on previous one's areas ===========
        AreaResult = area.mask_with_convex_shape(AreaA, AreaB, Fg, Bg)

        Wanted = [['P', '.'], ['.', 'P'], ['.', '.']]
        self.assertEqual(AreaResult, Wanted)

class Area(util_test.DeepCopyTest):
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

        CharsBlocking = [Fg]
        BlockVolume, FireInfo = area.count_separated_blocks(Area, Bg, CharsBlocking)
        self.assertEqual(3, BlockVolume)

        FireInfoWanted = {"total_size_of_closed_areas": 41,
                          (0, 0): {"AreaXmax": 5,
                                   "AreaXmin": 0,
                                   "AreaYmax": 8,
                                   "AreaYmin": 0,
                                   "BurntAreaSize": 39},
                          (3, 2): {"AreaXmax": 3,
                                   "AreaXmin": 3,
                                   "AreaYmax": 2,
                                   "AreaYmin": 2,
                                   "BurntAreaSize": 1},
                          (3, 4): {"AreaXmax": 3,
                                   "AreaXmin": 3,
                                   "AreaYmax": 4,
                                   "AreaYmin": 4,
                                   "BurntAreaSize": 1}}

        self.assertEqual( FireInfoWanted, FireInfo )

        # we erase the outside block
        FireInfo = area.fire(Area, [(0,0)], CharsBlocking)
        self.assertEqual(39, FireInfo["BurntAreaSize"])

        BlockVolume,  FireInfo = area.count_separated_blocks(Area, Bg, CharsBlocking)
        self.assertEqual(2, BlockVolume)

        FireInfoWanted = {"total_size_of_closed_areas": 2,
                          (3, 2): {"AreaXmax": 3,
                                   "AreaXmin": 3,
                                   "AreaYmax": 2,
                                   "AreaYmin": 2,
                                   "BurntAreaSize": 1},
                          (3, 4): {"AreaXmax": 3,
                                   "AreaXmin": 3,
                                   "AreaYmax": 4,
                                   "AreaYmin": 4,
                                   "BurntAreaSize": 1}}
        self.assertEqual(FireInfoWanted, FireInfo)

        # then we erase one of the inside blocks
        area.fire(Area, [(3,2)], CharsBlocking)
        BlockVolume, FireInfo = area.count_separated_blocks(Area, Bg, CharsBlocking)
        self.assertEqual(1, BlockVolume)

        FireInfoWanted = {"total_size_of_closed_areas": 1,
                          (3, 4): {"AreaXmax": 3,
                                   "AreaXmin": 3,
                                   "AreaYmax": 4,
                                   "AreaYmin": 4,
                                   "BurntAreaSize": 1}}
        self.assertEqual(FireInfoWanted, FireInfo)

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

        FireInfo = area.fire_from_side(Area, "Right", [Fg])

        Wanted = ("FFFFFF"
                  "FFOOOF"
                  "FF..OF"
                  "FFOOOF"
                  "FFFFFF")

        self.assertEqual(Wanted, area.to_string(Area, OneLine=True))
        self.assertEqual(21, FireInfo["BurntAreaSize"])

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
        Mark = {"Coords": {(1,1):1, (2,2):2, (3,3):3, (1,3):4}}
        area.coords_insert_from_mark(Area, Mark, Fg, Xshift=1, Yshift=1)
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

def run_all_tests(Prg):
    print("run all tests")
    Area.Prg = Prg
    AreaProcessors.Prg = Prg

    unittest.main(module="test_area", verbosity=2, exit=False)
