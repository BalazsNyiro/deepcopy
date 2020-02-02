# -*- coding: utf-8 -*-
import copy

# start_down: x modify, y modify,  step 2 xmodify, ymodify...
_Up = (0, -1)
_Down = (0, 1)
_Left = (-1, 0)
_Right = (1, 0)
_SpiralOperators = {
    "StartDown" : [_Down, _Right, _Up, _Left],
    "StartRight": [_Right, _Up, _Left, _Down],
    "StartUp"   : [_Up, _Left, _Down, _Right],
    "StartLeft" : [_Left, _Down, _Right, _Up]
}

def spiral_max_from_coord(Mark, Coord):
    DirectionOperators = copy.deepcopy(_SpiralOperators["StartDown"])
    SpiralCoords = []
    SpiralCoords.append(Coord)
    return SpiralCoords

# Spiral search from point 1:
#                  5   56  567  567  567  567  567  567   567   567   567  g567
#    1  1   1  41  41  41  41   418  418  418  418  418   418   418  f418  f418
#       2  32  32  32  32  32   32   329  329  329  329   329  e329  e329  e329
#                                           a   ba  cba  dcba  dcba  dcba  dcba

def spiral_nonoverlap_search_in_mark(Mark):
    SpiralsInMark = {}
    CoordsTry = dict(Mark["Coords"])

    while CoordsTry:

        SpiralBiggestCoordStart = (-1, -1)
        SpiralBiggestCoords = [] # the order of coords are important to represent the spiral

        for Coord in CoordsTry:
            SpiralMaxNow = sprial_max_from_coord(Coord)
            if len(SpiralMaxNow) > len(SpiralBiggestCoords):
                SpiralBiggestCoords = SpiralMaxNow
                SpiralBiggestCoordStart = Coord

        SpiralsInMark[SpiralBiggestCoordStart] = SpiralBiggestCoords
        coords_delete(CoordsTry, SpiralBiggestCoords)


    return SpiralsInMark

def coords_delete(CoordsDict, CoordsDeletedList):
    for CoordDel in CoordsDeletedList:
        print("  del:", CoordDel)
        del CoordsDict[CoordDel]

# these chars have colors in Linux terminal, I hope in windows there are colored chars, too
# https://apps.timwhitlock.info/emoji/tables/unicode

CharBg = "🔸" #small orange diamond
CharsetColorful = [
    "", # the [0] size isn't in blocks
    "🔅",  # low brightness symbol
    "🌑", # new moon symbol
    "💜", #purple heart
    "🔴", #large red circle
    "🔵", #large blue circle,
    "🔆", # high brightness symbol
    "🔘", #radio button,
]

