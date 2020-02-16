# -*- coding: utf-8 -*-
import copy, area, time, util, os

def spiral_generator(Direction="D"):
    pass


Up    = ( 0,-1)
Down  = ( 0, 1)
Left  = (-1, 0)
Right = ( 1, 0)
def spiral_operators(): return  {"CounterClockwise": {
                                      "Down" : [Down, Right, Up, Left],
                                      "Right": [Right, Up, Left, Down],
                                      "Up"   : [Up, Left, Down, Right],
                                      "Left" : [Left, Down, Right, Up] },
                                 "Clockwise": {
                                     "Down" : [Down, Left, Up, Right],
                                     "Left" : [Left, Up, Right, Down],
                                     "Up"   : [Up, Right, Down, Left],
                                     "Right": [Right, Down, Left, Up] }}


def _operator_next(DirectionOperators):
    Operator = DirectionOperators.pop(0)
    DirectionOperators.append(Operator)
    return Operator


_Ranges = dict() # cached ranges, I don't want to recreate it always
# Spiral search from point 1, Clockwise, Down start:
#                  5   56  567  567  567  567  567  567   567   567   567  g567
#    1  1   1  41  41  41  41   418  418  418  418  418   418   418  f418  f418
#       2  32  32  32  32  32   32   329  329  329  329   329  e329  e329  e329
#                                           a   ba  cba  dcba  dcba  dcba  dcba
def spiral_from_coord(MarkCoords, Coord, Direction="CounterClockwise", Start="Down"):
    DirectionOperators = spiral_operators()[Direction][Start]

    SpiralCoords = [(Coord)]
    X, Y = Coord
    Repetition = 1

    while True:
        if Repetition not in _Ranges:
            _Ranges[Repetition] = range(0, Repetition) # cached ranges to avoid nonstop range creation

        OperatorDeltaX, OperatorDeltaY = _operator_next(DirectionOperators)
        for _Rep in _Ranges[Repetition]: # to follow and understand
            X += OperatorDeltaX
            Y += OperatorDeltaY
            CoordNew = (X, Y)
            if CoordNew in MarkCoords:
                SpiralCoords.append(CoordNew)
            else:
                return SpiralCoords

        OperatorDeltaX, OperatorDeltaY = _operator_next(DirectionOperators)
        for _Rep in _Ranges[Repetition]:
            X += OperatorDeltaX
            Y += OperatorDeltaY
            CoordNew = (X, Y)
            if CoordNew in MarkCoords:
                SpiralCoords.append(CoordNew)
            else:
                return SpiralCoords

        Repetition += 1


def spiral_max_from_coord(MarkCoords, Coord):
    Spirals = dict()

    Spirals["ClockwiseUp"]    = spiral_from_coord(MarkCoords, Coord, "Clockwise", "Up")
    Spirals["ClockwiseDown"]  = spiral_from_coord(MarkCoords, Coord, "Clockwise", "Down")
    Spirals["ClockwiseLeft"]  = spiral_from_coord(MarkCoords, Coord, "Clockwise", "Left")
    Spirals["ClockwiseRight"] = spiral_from_coord(MarkCoords, Coord, "Clockwise", "Right")

    Spirals["CounterClockwiseUp"]    = spiral_from_coord(MarkCoords, Coord, "CounterClockwise", "Up")
    Spirals["CounterClockwiseDown"]  = spiral_from_coord(MarkCoords, Coord, "CounterClockwise", "Down")
    Spirals["CounterClockwiseLeft"]  = spiral_from_coord(MarkCoords, Coord, "CounterClockwise", "Left")
    Spirals["CounterClockwiseRight"] = spiral_from_coord(MarkCoords, Coord, "CounterClockwise", "Right")

    CoordsLongest = []
    for DirectionKey, CoordsSpiral in Spirals.items():
        if len(CoordsSpiral) > len(CoordsLongest):
            CoordsLongest = CoordsSpiral

    return CoordsLongest

def spiral_nonoverlap_search_in_mark(Mark):
    SpiralsInMark = {}
    CoordsTry = dict(Mark["Coords"])

    while CoordsTry:

        SpiralBiggestCoordStart = (-1, -1)
        SpiralBiggestCoords = [] # the order of coords are important to represent the spiral

        for Coord in CoordsTry:
            SpiralMaxNow = spiral_max_from_coord(CoordsTry, Coord)
            if len(SpiralMaxNow) > len(SpiralBiggestCoords):
                SpiralBiggestCoords = SpiralMaxNow
                SpiralBiggestCoordStart = Coord

        SpiralsInMark[SpiralBiggestCoordStart] = SpiralBiggestCoords
        coords_delete(CoordsTry, SpiralBiggestCoords)

    return SpiralsInMark

def coords_delete(CoordsDict, CoordsDeletedList):
    for CoordDel in CoordsDeletedList:
        # print("  del:", CoordDel)
        del CoordsDict[CoordDel]

# these chars have colors in Linux terminal, I hope in windows there are colored chars, too
# https://apps.timwhitlock.info/emoji/tables/unicode

def spirals_display(Prg, Spirals, Width, Height, SleepTime=0, Prefix="", PauseAtEnd=0, PauseAtStart=0, SaveAsFilename=None):
    SaveAsTxt = []

    CharBg = "🔸" #small orange diamond
    CharsetColorful = [
        "😎", # smiling face with sunglasses
        "🔘", #radio button,
        "🌼",
        "🍀",
        "🐙",
        "🎃", # jack-o-lantern
        "🐸",  # frog face
        "🎅", # father christmas
        "🐨",  # koala
        "🎁",  # Wrapped present,
        "🌷",  # tulip
        "🏀",  # basketball and hoop
        "😈", # smiling face with horns
        "🕐",  # clock face, one o'clock
        "🔴", #large red circle
        "🔵", #large blue circle,
        "🔆", # high brightness symbol
        "💜", #purple heart
        "🔅",  # low brightness symbol
        "🌑", # new moon symbol
        "💡",  # electric light bulb

    ]

    Area = area.make_empty(Width, Height, CharBg)
    print(area.to_string(Area, Prefix=Prefix, AfterString="\n\n", BeforeString="\n" * 33))
    time.sleep(PauseAtStart)

    for Coords in Spirals.values():
        CharColorful = CharsetColorful.pop(0)
        CharsetColorful.append(CharColorful)  # shifting elements in Colorful chars

        for X, Y in Coords:
            Area[X][Y] = CharColorful
            AreaTxt = area.to_string(Area, Prefix=Prefix, AfterString="\n\n", BeforeString="\n"*33)
            SaveAsTxt.append(AreaTxt)
            print(AreaTxt)
            if SleepTime:
                time.sleep(SleepTime)

    if PauseAtEnd:
        time.sleep(PauseAtEnd)

    if SaveAsFilename:
        util.file_write(Prg, os.path.join(Prg["DirTmpPath"], SaveAsFilename), "".join(SaveAsTxt))



