# -*- coding: utf-8 -*-
import copy

def spiral_generator(Direction="D"):
    pass


Up    = ( 0,-1)
Down  = ( 0, 1)
Left  = (-1, 0)
Right = ( 1, 0)
SpiralOperators = {"CounterClockwise": {
                        "Down" : [Down, Right, Up, Left],
                        "Right": [Right, Up, Left, Down],
                        "Up"   : [Up, Left, Down, Right],
                        "Left" : [Left, Down, Right, Up] },
                   "Clockwise": {
                       "Down" : [Down, Left, Up, Right],
                       "Left" : [Left, Up, Right, Down],
                       "Up"   : [Up, Right, Down, Left],
                       "Right": [Right, Down, Left, Up] }}

def spiral_from_coord(MarkCoords, Coord, Direction="CounterClockwise", Start="Down"):
    DirectionOperators = copy.deepcopy(SpiralOperators[Direction][Start])

    def op_shift():
        OperatorFirst = DirectionOperators.pop(0)
        OperatorSecond = DirectionOperators.pop(0)
        DirectionOperators.append(OperatorFirst)
        DirectionOperators.append(OperatorSecond)
        return OperatorFirst, OperatorSecond

    SpiralCoords = [(Coord)]
    X, Y = Coord
    Repetition = 1

    Continue = True
    while Continue:

        OperatorFirst, OperatorSecond = op_shift()
        print("operators", OperatorFirst, OperatorSecond)

        if True: # I don't want to refactor it into a function because it's difficult
            for Rep in range(0, Repetition): # to follow and understand
                X += OperatorFirst[0]
                Y += OperatorFirst[1]
                if (X, Y) in MarkCoords:
                    SpiralCoords.append((X, Y))
                else:
                    Continue = False

        if Continue:
            for Rep in range(0, Repetition):
                X += OperatorSecond[0]
                Y += OperatorSecond[1]
                if (X, Y) in MarkCoords:
                    SpiralCoords.append((X, Y))
                else:
                    Continue = False

        Repetition += 1

    return SpiralCoords

# Spiral search from point 1, Clockwise:
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

